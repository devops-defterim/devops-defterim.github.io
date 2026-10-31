---
title: Giriş ve ilk bucket
description: S3'ün ne olduğu, blok ve obje tabanlı depolama farkı, ilk bucket'ın oluşturulması ve obje URL'sine erişim denemesi.
module: aws
lessons: [21]
order: 7
---

## S3 nedir?

S3 kısaltması, adını İngilizce **S**imple **S**torage **S**ervice (Basit Depolama Servisi) kelimelerinin baş harflerindeki üç adet "S" harfinden alır.

S3'ü en basit haliyle OneDrive ya da Google Drive gibi düşünebiliriz. Google Drive'a nasıl kendimiz dosya gönderip orada saklayabiliyorsak, AWS dünyasında bunu S3 hizmeti sağlar. S3 kişisel dosyalarımızı tutmak için oluşturulmuş bir servis değildir, ancak temelde yaptığı iş aynıdır. Resim, PDF, log dosyaları gibi dosya olarak tutabildiğimiz tüm verileri saklayabildiğimiz obje tabanlı bir servistir.

## Blok ve obje tabanlı depolama

Depolama olarak kullanabileceğimiz temelde iki çeşit sistem vardır: blok tabanlı ve obje tabanlı veri depolama sistemleri.

| | Blok tabanlı | Obje tabanlı |
| --- | --- | --- |
| Yapı | Esasında birer disk imajı şeklindedir | Dosyalar obje olarak tutulur |
| Makineye bağlanma | Bir bilgisayara bağlanır; üzerine işletim sistemi, uygulama, veritabanı vb. kurulabilir | Makineye bağlanamaz |
| Erişim | Bağlı olduğu makine üzerinden | Web, API veya uygulamalar üzerinden |
| İçerik | | Aklınıza gelebilecek her türlü dosya ve bu objelerle ilgili metadata |

## S3 obje özellikleri

- 0 KB'tan 5 TB'a kadar büyüklükte dosyaları depolayabilirsiniz. 5 TB, tek bir dosyanın maksimum büyüklüğüdür.
- S3 limitsizdir; istediğiniz kadar dosya koyabilirsiniz.
- S3 depolama birimlerine **bucket** (kova) denir.
- **Metadata**, veri hakkındaki veri demektir. Örneğin objenin yaratılma tarihi (`Date`) ve boyutu (`Content-Length`) o obje ile birlikte tutulan metadatalardır.

## İlk bucket'ı oluşturma

1. Console ana sayfasındaki arama kutusuna `s3` yazıp ilk seçenek olan **S3** servisine tıklayın.
2. Açılan **Amazon S3 → Buckets** ekranında sağ üstteki `Create bucket` butonuna tıklayın.
3. **General configuration** altında AWS Region (örnekte `Europe (Ireland) eu-west-1`) ve Bucket type olarak `General purpose` seçili gelir.
4. **Bucket name** alanına benzersiz bir isim girin (örnekte `ornek-bucket-123`).
5. Diğer ayarları şimdilik geçip en alttaki `Create bucket` butonuna tıklayın.

:::note
Bucket isimleri temel olarak benzersiz (unique) olmak zorundadır. Buradaki isim yalnızca kendi hesabınızda değil, tüm AWS hesaplarında benzersiz olmalıdır. Nedeni aşağıda, obje URL'si kısmında açıklanıyor.
:::

## Bucket'a dosya yükleme

1. Oluşturduğunuz bucket'ın adına tıklayarak içine girin. **Objects** sekmesinde henüz obje yoktur (`No objects`).
2. `Upload` butonuna tıklayın.
3. Açılan **Upload** ekranında `Add files` diyerek yüklemek istediğiniz görselleri seçin. Seçilen dosyalar **Files and folders** tablosunda listelenir; **Destination** olarak `s3://ornek-bucket-123` görünür.
4. En alttaki `Upload` butonuna tıklayarak dosyaları yükleyin.

Yükleme bitince **Objects** sekmesinde dört görsel `png` tipiyle ve `Standard` storage class ile listelenir.

## Obje bilgileri ve obje URL'si

Yüklediğimiz görsellerin bilgilerine **Name** sütunu altındaki mavi yazılara (obje adlarına) tıklayarak erişebiliriz. Açılan **Properties** sekmesindeki **Object overview** bölümünde şu bilgiler yer alır:

| Alan | Örnek değer |
| --- | --- |
| AWS Region | `Europe (Ireland) eu-west-1` |
| Size | `694.5 KB` |
| Type | `png` |
| Key | `Ekran Resmi 2026-07-30 13.26.33.png` |
| S3 URI | `s3://ornek-bucket-123/Ekran Resmi 2026-07-30 13.26.33.png` |
| Amazon Resource Name (ARN) | `arn:aws:s3:::ornek-bucket-123/Ekran Resmi 2026-07-30 13.26.33.png` |
| Object URL | `https://ornek-bucket-123.s3.eu-west-1.amazonaws.com/Ekran+Resmi+2026-07-30+13.26.33.png` |

Ekranın alt kısmındaki **Object management overview** bölümünde Bucket Versioning'in `Disabled` olduğu ve bucket için versiyonlamanın açılmasının önerildiği bir uyarı da görünür.

**Object URL** adresine tarayıcıdan gitmeye çalıştığımızda aşağıdaki gibi bir hata alırız:

```text title="Tarayıcı çıktısı"
AccessDenied
Access Denied
...
```

Bu URL'ye dikkat edersek, linkin içinde bucket oluştururken verdiğimiz ismi görürüz. Bucket isimlerinin benzersiz olma zorunluluğu tam olarak buradan kaynaklanır: S3 üzerinde oluşturduğunuz her bucket aslında internette bir web adresi üretir. İnternet dünyasında aynı URL'den iki tane olamayacağı için başka hiçbir AWS kullanıcısıyla aynı bucket ismini paylaşamazsınız.

Aldığımız hatanın sebebi ise şudur: Bu URL yapısı teorik olarak dünyanın her yerinden dosyamıza erişim imkanı sunsa da, güvenlik gereği bucket'ı dışarıya açık (Public Access) hale getirmedik. AWS bu erişimi varsayılan olarak kapalı tutar.
