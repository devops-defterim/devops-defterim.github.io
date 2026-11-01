---
title: Bucket policy ve statik web sitesi
description: Block public access ayarını kapatma, herkese okuma izni veren bucket policy yazma ve S3 üzerinde statik web sitesi yayınlama.
module: aws
lessons: [23]
order: 12
---

## Block public access ayarını kapatma

Sıradaki **Permissions** başlığı altında neler yapabildiğimizi öğrenmeye başlayalım. Eğer oluşturduğumuz bir bucket public değilse ve bunu public olarak ayarlamak istiyorsak ilk olarak yapmamız gereken bu başlık altındaki block public access ayarını değiştirmek olmalıdır.

1. Bunun için **Block public access** yazan başlığın yanındaki **Edit** butonuna tıklıyoruz.

   ![Permissions sekmesinde Block public access başlığının yanındaki Edit butonu](../../../../assets/ekran/p185-1.webp)

2. Bu şekilde işaretlenmiş olarak açılan sayfada tik işaretlerini kaldırıyoruz ve **Save changes** diyoruz.

   ![Edit Block public access sayfasında işaretleri kaldırılmış kutucuklar](../../../../assets/ekran/p186-1.webp)

3. Ekrana gelen onayı da hallettikten sonra ilk aşamayı tamamlamış oluyoruz.

   ![Block public access değişikliği için confirm onay penceresi](../../../../assets/ekran/p186-2.webp)

Ardından bundan sonra bucket'a kimin erişip erişemeyeceğini, ne şekilde erişeceğini belirlemek adına Bucket policy yazmamız gerekiyor.

## Bucket policy nedir

Peki nedir bu Bucket Policy ve nasıl yazılır? Kısaca özetlemek gerekirse Bucket Policy, S3 bucket girişinde duran güvenlik görevlisidir. AWS'nin anlayacağı JSON formatında yazılan bu kurallar bütünü, kimin hangi dosyaya ne yapabileceğini veya ne yapamayacağını çok ince detaylarına kadar belirlememizi sağlar.

Bir policy yazarken AWS'ye temelde şu 4 ana sorunun cevabını veririz:

- **Principal (Kim?):** Bu kural kimin için geçerli? Belirli bir IAM kullanıcısı mı, farklı bir AWS hesabı mı, yoksa internetteki herkes mi?
- **Action (Ne yapacak?):** Hangi işleme izin veriyoruz? Dosya okuma, dosya yükleme veya dosya silme gibi spesifik yetkiler.
- **Resource (Nerede?):** Bu işlem hangi kaynakta yapılacak? (Hatırlarsanız önceki kısımlarda öğrendiğimiz [ARN](/aws/iam/roller-ve-arn/) değerini işte tam burada, hedefin tam açık adresini noktası noktasına göstermek için kullanıyoruz.)
- **Effect (Sonuç ne?):** Bu işleme izin mi veriyoruz, yoksa kesin olarak yasaklıyor muyuz?

## Örnek bir senaryo: dosyalarımızı dış dünyaya açmak

Madem bir önceki adımda "Block Public Access" ayarını kapattık ve dış erişimin önündeki kalkanı kaldırdık, şimdi de policy yazarak içerdeki dosyalarımızın herkes tarafından sadece "okunabilmesini" (görüntülenebilmesini) sağlayalım.

Bunun için Bucket Policy editörüne şu şekilde çok temel bir JSON kodu yazarız bunun için **Edit** butonuna tıklayarak yazmaya başlayabiliriz.

![Bucket policy bölümündeki Edit butonu ve policy editörü](../../../../assets/ekran/p187-1.webp)

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

Bu koda baktığımızda; Effect kısmındaki `"Allow"` ifadesi, tanımladığımız bu erişim işlemine izin verdiğimizi belirtir (eğer buraya `"Deny"` yazsaydık işlemi kesin bir şekilde yasaklamış olurduk). Principal kısmındaki `*` (yıldız) işareti "internetteki herkes" anlamına gelir. Action kısmındaki `s3:GetObject` ise bu kişilere sadece "dosyayı alıp görüntüleme/indirme" yetkisi verdiğimizi; kimsenin dışarıdan gelip bucket'ımıza dosya yükleyemeyeceğini veya silemeyeceğini garanti eder. Resource kısmının sonundaki `/*` ise bu okuma izninin bucket içindeki tüm dosyalar için geçerli olduğunu gösterir.

Yazdığımız kodu kaydetmek için **Save changes** butonuna tıklamamız yeterli olacaktır.

![Edit bucket policy sayfasında Save changes butonu](../../../../assets/ekran/p188-1.webp)

## Statik web sitesi yayınlama

Eğer tüm ayarlamaları yaptıysak artık Static website hosting için küçük bir çalışma yapabiliriz. Önceden bucket policy'miz olmadığı için dış dünyadan erişim yoktu.

### Static website hosting'i açma

1. Öncelikle **Properties** menüsü altından **Static website hosting** başlığında **Edit** butonuna tıklıyoruz.

   ![Properties sekmesinde Static website hosting bölümündeki Edit butonu](../../../../assets/ekran/p189-1.webp)

2. Açılan ekrandaki seçimi **Enable** olarak değiştiriyoruz ve istenilen yazıları boşluklara yazarak **Save changes** diyerek devam ediyoruz.

   ![Static website hosting Enable seçimi ve Index document alanı](../../../../assets/ekran/p189-2.webp)

   ![Static website hosting bölümünde oluşan Bucket website endpoint](../../../../assets/ekran/p189-3.webp)

   ```text
   http://ornek-bucket-123.s3-website-eu-west-1.amazonaws.com
   ```

Static website hosting altında oluşan bizim erişeceğimiz web sitemizin linkini oluşturuyor.

### Site dosyalarını yükleme

1. Ardından **Objects** menüsüne gelerek **Upload** butonuna tıklıyoruz ve https://github.com/aytitech/public/raw/main/sayfa.tgz linkte bulunan dosyaları buraya yüklüyoruz.

   ![Objects sekmesindeki Upload butonu](../../../../assets/ekran/p190-1.webp)

2. Gerekli dosyaları seçtikten sonra **Upload** butonuna tıklıyoruz.

   ![Upload sayfasında seçilen site dosyaları](../../../../assets/ekran/p190-2.webp)

   ![Upload sayfasında Destination ve Upload butonu](../../../../assets/ekran/p190-3.webp)

3. İşlememizin gerçekleşmesini bekliyoruz.

   ![Upload: status ekranında yüklemenin tamamlanması](../../../../assets/ekran/p191-1.webp)

Tebrikler! Web sitemiz artık erişime açık. Static website hosting başlığı altındaki linki tarayıcınıza yapıştırıp sonucu kendiniz görebilirsiniz.

![Tarayıcıda açılan statik web sitesi](../../../../assets/ekran/p191-2.webp)
