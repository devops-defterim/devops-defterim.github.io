---
title: Bucket policy ve statik web sitesi
description: Block public access ayarını kapatma, herkese okuma izni veren bucket policy yazma ve S3 üzerinde statik web sitesi yayınlama.
module: aws
lessons: [23]
order: 12
---

Bu sayfada bucket'ın **Permissions** sekmesiyle bir bucket'ı dış dünyaya açıyor, ardından [Properties](/aws/s3/properties/) altında tanıdığımız **Static website hosting** özelliğiyle küçük bir web sitesi yayınlıyoruz.

## Block public access ayarını kapatma

Oluşturduğumuz bucket public değilse ve onu public olarak ayarlamak istiyorsak ilk yapılması gereken, **Permissions** sekmesindeki block public access ayarını değiştirmektir.

1. Bucket içinde **Permissions** sekmesine geçin.
2. **Block public access (bucket settings)** başlığının yanındaki `Edit` butonuna tıklayın. Varsayılan durumda **Block all public access** `On` olarak görünür.
3. Açılan **Edit Block public access (bucket settings)** sayfasında işaretli gelen kutucukların işaretini kaldırın (`Block all public access` ve altındaki dört ayar).
4. `Save changes` butonuna tıklayın.
5. Çıkan onay penceresinde alana `confirm` yazıp `Confirm` butonuna tıklayın.

İşlem başarılı olursa "Successfully edited Block Public Access settings for this bucket." mesajı görünür ve ayar `Off` durumuna geçer. Bu, ilk aşamadır; bucket'a kimin, nasıl erişeceğini belirlemek için ayrıca bir bucket policy yazmak gerekir.

## Bucket policy nedir

Bucket policy, kısaca S3 bucket'ının girişinde duran güvenlik görevlisidir. AWS'nin anlayacağı JSON formatında yazılan bu kurallar bütünü, kimin hangi dosyaya ne yapabileceğini veya ne yapamayacağını çok ince detaylarına kadar belirlememizi sağlar.

Bir policy yazarken AWS'ye temelde dört sorunun cevabını veririz:

| Alan | Soru | Açıklama |
| --- | --- | --- |
| Principal | Kim? | Kural kimin için geçerli? Belirli bir IAM kullanıcısı mı, farklı bir AWS hesabı mı, yoksa internetteki herkes mi? |
| Action | Ne yapacak? | Hangi işleme izin veriliyor? Dosya okuma, dosya yükleme veya dosya silme gibi spesifik yetkiler. |
| Resource | Nerede? | İşlem hangi kaynakta yapılacak? Hedefin tam adresini göstermek için daha önce öğrendiğimiz [ARN](/aws/iam/roller-ve-arn/) değeri burada kullanılır. |
| Effect | Sonuç ne? | Bu işleme izin mi veriliyor, yoksa kesin olarak yasaklanıyor mu? |

## Örnek: dosyaları herkese okunabilir yapmak

Block public access ayarını kapatıp dış erişimin önündeki kalkanı kaldırdıktan sonra, şimdi bucket içindeki dosyaların herkes tarafından yalnızca okunabilmesini (görüntülenebilmesini) sağlayan bir policy yazalım.

1. **Permissions** sekmesinde **Bucket policy** bölümündeki `Edit` butonuna tıklayın. (Henüz policy yoksa bölümde "No policy to display." yazar.)
2. **Edit bucket policy** sayfasında, üstte bucket'ın ARN'i (`arn:aws:s3:::ornek-bucket-123`) görünür. **Policy** editörüne aşağıdaki JSON'u yazın.
3. `Save changes` ile kaydedin.

```json title="Bucket policy"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::ornek-bucket-123/*"
        }
    ]
}
```

Bu kodda:

- **Effect** kısmındaki `"Allow"`, tanımlanan erişim işlemine izin verildiğini belirtir. Buraya `"Deny"` yazılsaydı işlem kesin olarak yasaklanmış olurdu.
- **Principal** kısmındaki `*` (yıldız) "internetteki herkes" anlamına gelir.
- **Action** kısmındaki `s3:GetObject`, bu kişilere yalnızca dosyayı alıp görüntüleme/indirme yetkisi verir. Kimse dışarıdan bucket'a dosya yükleyemez veya silemez.
- **Resource** kısmının sonundaki `/*`, okuma izninin bucket içindeki tüm dosyalar için geçerli olduğunu gösterir.

## Statik web sitesi yayınlama

Ayarlar tamamsa artık Static website hosting ile küçük bir çalışma yapabiliriz. Daha önce bucket policy olmadığı için dış dünyadan erişim yoktu; şimdi var.

### Static website hosting'i açma

1. **Properties** sekmesinde **Static website hosting** başlığındaki `Edit` butonuna tıklayın.
2. **Static website hosting** seçeneğini `Enable` yapın.
3. **Hosting type** olarak `Host a static website` seçili kalsın.
4. **Index document** alanına `index.html`, **Error document - optional** alanına `error.html` yazın.
5. `Save changes` ile kaydedin.

Kaydettikten sonra **Static website hosting** bölümünde **Bucket website endpoint** altında sitenin adresi oluşur:

```text
http://ornek-bucket-123.s3-website-eu-west-1.amazonaws.com
```

### Site dosyalarını yükleme

1. **Objects** sekmesine geçip `Upload` butonuna tıklayın.
2. https://github.com/aytitech/public/raw/main/sayfa.tgz adresindeki site dosyalarını `Add files` / `Add folder` ile ekleyin. Örnekte toplam 52 dosya (3,1 MB) seçildi; `assets/`, `js/` gibi klasörler de içinde.
3. **Destination** olarak bucket'ın (`s3://ornek-bucket-123`) göründüğünü kontrol edip `Upload` butonuna tıklayın.
4. **Upload: status** ekranında yüklemenin tamamlanmasını bekleyin; dosyaların durumu `Succeeded` olmalıdır.

Yükleme bitince site erişime açılır. **Static website hosting** altındaki endpoint linkini tarayıcıya yapıştırarak sonucu görebilirsiniz.
