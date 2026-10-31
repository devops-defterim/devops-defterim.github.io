---
title: Bucket ayarları
description: Bucket oluştururken karşılaşılan Object Ownership, Block Public Access, versiyonlama, şifreleme ve Object Lock ayarları.
module: aws
lessons: [22]
order: 9
---

Bucket konusunu biraz daha detaylandırmak için **Amazon S3 → Buckets** ekranında `Create bucket` diyerek yeni bir bucket oluşturmaya başlıyoruz ve bu ekrandaki ayarları sırayla inceliyoruz.

## General configuration

- **Bucket name:** Daha önce bahsettiğimiz gibi benzersiz bir isim giriyoruz (örnekte `ornek-bucket`). Kuralın nedeni için bkz. [Giriş ve ilk bucket](/aws/s3/giris-ve-ilk-bucket/).
- **Copy settings from existing bucket - optional:** Daha önce oluşturduğumuz başka bir bucket'ın ayarlarını yeni bucket'a aktarmak istersek `Choose bucket` butonundan seçim yapabiliriz.

## Erişim yönetiminin geçmişi: IAM Policies ve ACL

AWS, S3 servisi ilk çıktığında bucket'lara erişimi yönetmek için iki temel yol sunuyordu: **IAM Policies** ve **ACL (Access Control List)**.

IAM tarafındaki S3 ile ilgili hazır policy'leri **IAM → Policies** ekranında arama kutusuna `s3` yazarak görebiliriz (örnekte 25 sonuç; `AmazonS3FullAccess`, `AmazonS3ExpressFullAccess` gibi AWS managed policy'ler). Örneğin `AmazonS3ExpressFullAccess` policy'sinin içeriği şöyledir:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3ExpressFullAccess",
            "Effect": "Allow",
            "Action": "s3express:*",
            "Resource": "*"
        }
    ]
}
```

ACL sayesinde ister farklı AWS hesaplarındaki kullanıcılara, ister doğrudan dış dünyaya manuel olarak dosya bazında erişim yetkisi verebiliyorduk.

## Object Ownership

Günümüzde de **Object Ownership** bölümünde `ACLs enabled` seçeneğini seçerek bu şekilde manuel izinler tanımlamak hâlâ mümkündür. Varsayılan seçenek `ACLs disabled (recommended)` olup bu durumda Object Ownership `Bucket owner enforced` olur.

`ACLs enabled` seçildiğinde AWS, nesne bazında erişim kontrolü gerekmiyorsa ACL'lerin kapalı tutulmasını ve hesap dışındaki kullanıcılarla paylaşım için ACL yerine bucket policy kullanılmasını öneren bir uyarı gösterir. Ayrıca iki seçenek açılır:

| Seçenek | Anlamı |
| --- | --- |
| `Bucket owner preferred` | Bucket'a dışarıdan kim dosya yüklerse yüklesin, yüklenen dosyaların sahipliği ve üzerindeki hakları belirleme yetkisi doğrudan bucket'ın asıl sahibinde (yani bizde) kalır. |
| `Object writer` | Bucket'a yüklenen dosyaların sahipliği ve yetki hakları, o dosyayı yükleyen kişiye (hesaba) ait olur. |

## Block Public Access ve Bucket Policies

Zamanla S3 kullanımı o kadar yoğunlaştı ki, ufak konfigürasyon hataları yüzünden gizli kalması gereken bucket'ların yanlışlıkla tüm internete açılması büyük güvenlik sorunlarına yol açtı. AWS bunun önüne geçmek için iki önemli adım attı.

**1. Ekstra güvenlik uyarıları:** Bir bucket'ı public yapmak istediğinizde olası tehlikeleri açıkça kabul ettiğinizi onaylamanız istenir. **Block Public Access settings for this bucket** bölümünde varsayılan olarak `Block all public access` işaretlidir ve altındaki dört ayarın hepsini kapsar:

- Block public access to buckets and objects granted through *new* access control lists (ACLs)
- Block public access to buckets and objects granted through *any* access control lists (ACLs)
- Block public access to buckets and objects granted through *new* public bucket or access point policies
- Block public and cross-account access to buckets and objects through *any* public bucket or access point policies

`Block all public access` işaretini kaldırdığınızda "Turning off block all public access might result in this bucket and the objects within becoming public" uyarısı çıkar ve devam etmek için `I acknowledge that the current settings might result in this bucket and the objects within becoming public.` kutucuğunu işaretlemeniz gerekir.

**2. Bucket Policies:** Erişimi yönetmek için çok daha güvenli üçüncü bir yol geliştirildi. ACL'lerdeki gibi her dosya veya kullanıcı için tek tek izin ayarlamak yerine, tüm bucket'ı veya içindeki belirli klasörleri tek bir JSON dosyası üzerinden yönetmemizi sağlar. Böylece "Sadece şirketimizin IP adresinden girilebilsin" veya "Sadece şu hesaptaki kullanıcılar okuma yapabilsin" gibi çok daha detaylı kuralları tek bir merkezden yazabiliriz. Günümüzde AWS'nin erişim yönetimi için en çok tavsiye ettiği yöntem budur. Uygulaması için bkz. [Bucket policy ve statik web sitesi](/aws/s3/bucket-policy-ve-statik-site/).

## Bucket Versioning

Sıradaki ayar **Bucket Versioning**'dir (varsayılan `Disable`). Bu ayar aktifken aynı isimli bir dosyayı yüklemeye devam ettikçe S3 her seferinde en son gönderilen dosyayı gösterir, ancak önceki aynı isimli dosyaları silmez, versiyonlar. Böylece dosyamızdaki değişikliklere de S3 üzerinden ulaşabiliriz.

### Örnek

1. İçinde `ilk version` yazan `deneme.txt` dosyasını bucket'a yükleyin (**Upload → Add files → Upload**).
2. Dosyayı tarayıcıda açtığınızda içindeki metni görürsünüz:

   ```text title="deneme.txt"
   ilk version
   ```

3. Bilgisayarınızdaki dosyada değişiklik yapıp aynı isimle S3'e tekrar yükleyin.
4. **Objects** sekmesinde `Show versions` düğmesini aktif edin. `deneme.txt` dosyasının hem ilk hali hem de değiştirilmiş güncel versiyonu, farklı **Version ID** değerleriyle alt alta listelenir.

### Delete Marker

:::caution
Versiyonlama açıkken dosyayı arayüzden normal şekilde sildiğinizde dosyanın geçmiş versiyonları aslında silinmez. AWS bunun yerine dosyanın en üstüne **Delete Marker** adında, 0 byte yer kaplayan özel bir etiket yerleştirir.
:::

`Show versions` açıkken dosyanın altındaki tüm gerçek versiyonları silerseniz dosyanın içeriği gitse bile bu Delete Marker bucket'ta kalmaya devam eder. AWS buna **süresi dolmuş silme işaretçisi** (expired object delete marker) der. Bucket'ta kalan bu içi boş Delete Marker'ları Lifecycle Rule ile otomatik olarak temizleyebiliriz:

1. Bucket'ın **Management** sekmesinde **Lifecycle rules** altındaki `Create lifecycle rule` butonuna tıklayın.
2. **Lifecycle rule actions** bölümünde `Delete expired object delete markers or incomplete multipart uploads` kutucuğunu işaretleyin.
3. Hemen altında açılan **Delete expired object delete markers or incomplete multipart uploads** bölümünde `Delete expired object delete markers` kutucuğunu da işaretleyin.
4. En alttaki `Create rule` butonuyla kuralı kaydedin.

Böylece bucket bu içi boş kalıntılardan otomatik olarak arındırılır. Lifecycle Rule'ların ayrıntısı için bkz. [Management: lifecycle, replication, inventory](/aws/s3/management/).

## Default encryption

Verilerimizi dış dünyaya karşı nasıl koruduğumuzu gördük. Peki verilerimiz AWS'nin fiziksel makinelerinde, disklerinde dururken saf verinin güvenliğini nasıl sağlarız? Bunun cevabı **Default encryption** ayarıdır. **Encryption type** üç seçenekle sunulur:

| Seçenek | Açıklama |
| --- | --- |
| `Server-side encryption with Amazon S3 managed keys (SSE-S3)` | Varsayılan seçenek. Oluşturulan key dahil her şeyin yönetimi tamamen AWS'ye bırakılır. |
| `Server-side encryption with AWS Key Management Service keys (SSE-KMS)` | Key'i kendimiz belirlemek istediğimizde seçilir. |
| `Dual-layer server-side encryption with AWS Key Management Service keys (DSSE-KMS)` | AWS'nin sağladığı bir key ile kendi oluşturduğumuz bir key'i birlikte kullanarak güvenliği artırmak için seçilir. |

SSE-KMS seçildiğinde **AWS KMS key** altında `Choose from your AWS KMS keys` veya `Enter AWS KMS key ARN` seçenekleri gelir. Key'i dilersek AWS KMS üzerinden oluşturabilir (`Create a KMS key`), dilersek kendi key management sistemimizde oluşturduğumuz key'i kullanabiliriz. KMS key ARN formatı şöyledir:

```text
arn:aws:kms:<region>:<account-ID>:key/<key-id>
```

İkisi arasındaki temel fark, oluşturduğumuz key için belli aralıklarla yapılması gereken bakımları (90 gün içinde değiştirilmesi, saklanması vb.) AWS KMS kullanıldığında AWS'nin yönetiyor olmasıdır.

Aynı bölümde **Bucket Key** ayarı da bulunur (varsayılan `Enable`).

## Object Lock

Bucket oluştururken yapabileceğimiz son ayar, **Advanced settings** altındaki **Object Lock** ayarıdır (varsayılan `Disable`). Bu seçeneği aktif ederek hiçbir şekilde silinmemesi ve değiştirilmemesi gereken dosyalarınızı muhafaza edebilirsiniz.

:::note
Konsoldaki bilgi notuna göre Object Lock yalnızca versiyonlamanın açık olduğu bucket'larda çalışır; Object Lock'u etkinleştirmek Versioning'i de otomatik olarak açar.
:::
