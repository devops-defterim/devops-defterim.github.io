---
title: Gruplar, parola politikası ve STS
description: IAM user group oluşturma, policy listesi, hesap parola politikası, STS ve Identity Providers servislerinin amacı.
module: aws
lessons: [19]
order: 4
---

## User group oluşturma

1. IAM servisinde sol menüdeki **IAM user groups** seçeneğine tıklayın.
2. Sağ üstteki **Create group** butonuna basın.
3. **Name the group** bölümünde **User group name** alanına grubun adını yazın (örnekte `adminler`).
4. **Add users to the group - Optional** bölümünde gruba eklenecek kullanıcıları işaretleyin.
5. **Attach permissions policies - Optional** bölümünde grubun yetkilerini seçin (örnekte **AdministratorAccess**). Bir gruba en fazla 10 policy bağlanabilir; gruptaki tüm kullanıcılar seçilen policy'lerdeki yetkilere sahip olur.
6. Sağ alttaki **Create user group** ile grubu oluşturun. Grup, **IAM user groups** listesinde kullanıcı sayısı ve tanımlı yetkileriyle görünür.

:::note
Bir kullanıcıya doğrudan verilen yetkiler eklendiği gruptaki yetkilerden farklıysa, kullanıcının sonuçta sahip olduğu yetkiler hem kendisine verilmiş olanların hem de grubundakilerin birleşimidir.
:::

## Policy listesi

İstediğimiz yetkilere uygun policy'leri sol menüdeki **Policies** sayfasında bulabiliriz. Liste, AWS'nin hazır sunduğu **AWS managed** policy'leri (ör. `AdministratorAccess`) içerir ve her policy'nin nerede kullanıldığını (**Used as**) gösterir. Hazır policy'ler ihtiyacı karşılamıyorsa sağ üstteki **Create policy** ile kendi policy'mizi oluşturabiliriz.

## Parola politikası

IAM altında yönetilen hesap ayarlarından biri, **Account settings** menüsündeki **Password policy**'dir. Varsayılan politika şöyledir:

- Minimum şifre uzunluğu 8 karakter.
- Büyük harf, küçük harf, rakam ve alfanümerik olmayan karakterlerden en az üç türün kullanılması.
- Şifrenin süresi hiç dolmaz.
- Şifre, AWS hesap adı veya e-posta adresiyle aynı olmamalıdır.

Kuralları değiştirmek için **Password policy** kutusunda **Edit**'e tıklayıp özelleştirilmiş politikayı seçiyoruz. Burada şunları belirleyebiliriz:

| Ayar | Örnekteki değer |
| --- | --- |
| Minimum şifre uzunluğu (6-128) | 8 karakter |
| En az bir büyük harf | İşaretli |
| En az bir küçük harf | İşaretli |
| En az bir rakam | İşaretli |
| En az bir alfanümerik olmayan karakter | İşaretli |
| Şifre süresinin dolması (1-1095 gün) | 36 gün |
| Süresi dolan şifre için yönetici sıfırlaması gerekmesi | İşaretli |
| Kullanıcıların kendi şifrelerini değiştirebilmesi | İşaretli |
| Eski şifrelerin tekrar kullanılmasını engelleme (1-24) | Son 3 şifre |

Ayarları **Save changes** ile kaydediyoruz.

## Security Token Service (STS)

Account settings sayfasında **Security Token Service (STS)** bölümü de bulunur. STS esasında bir API hizmetidir: API'ye bir çağrı göndeririz ve çağrıya göre bir cevap alırız.

Örneğin bir kullanıcıya varsayılan olarak çok az hakkı olan bir policy atayalım, ama bu kullanıcı atadığımız policy dışında başka policy'leri de assume edebilsin. Yani başlangıçta en az yetkiyi verip, talebe göre kullanıcılara farklı izinleri geçici olarak, örneğin 30 dakikalığına verebiliriz. Bu konu ileride daha detaylı ele alınacak.

## Identity Providers

IAM altındaki bir diğer hizmet **Identity Providers**'dır. Amacı, AWS içinde tek tek kullanıcı oluşturmak yerine şirketinizde mevcut olan kullanıcıları AWS'ye entegre etmektir.

1. Kullanıcılar AWS için yeni bir şifre ezberlemek yerine kendi şirket veya dış hesaplarıyla giriş yapar.
2. Girişin ardından Identity Provider, AWS'ye "Bu kişi onaylıdır" der.
3. AWS bu dış kullanıcıya arka planda geçici bir Role giydirir.

Böylece yüzlerce çalışana ayrı ayrı AWS hesabı açmak yerine, mevcut sisteminiz üzerinden onlara güvenli ve geçici erişim yetkisi vermiş olursunuz. Konsolda bu servis sol menüdeki **Identity providers** sayfasından yönetilir; yeni sağlayıcı **Add provider** ile eklenir. Rol tarafındaki karşılığı için [IAM rolleri ve ARN](/aws/iam/roller-ve-arn/#web-identity-ve-saml-20-federation) sayfasına bakın.
