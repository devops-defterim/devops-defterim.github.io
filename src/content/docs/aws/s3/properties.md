---
title: Objects ve Properties sekmeleri
description: Bucket konsolunda Objects sekmesindeki obje işlemleri ve Properties sekmesindeki loglama, bildirim, hızlandırma ve requester pays ayarları.
module: aws
lessons: [22]
order: 10
---

Bucket oluştururken nelere dikkat etmemiz gerektiğini gördükten sonra S3 konsolunu tanımaya başlıyoruz.

## Objects sekmesi

Bucket'a girdiğimizde açılan **Objects** sekmesi, dosyalarımızı yüklediğimiz, her yüklenen dosyanın birer obje olarak tutulduğu ve bu objeler üzerinde işlem yapabildiğimiz yerdir. Bir objeyi seçtiğinizde üst kısımdaki butonlar aktif olur:

| Buton | İşlev |
| --- | --- |
| `Copy S3 URI` | Daha önce gördüğümüz public URL'den farklı olarak, CLI üzerindeki işlemlerde kullanabileceğimiz `s3://...` biçimindeki adresi kopyalar (bkz. [S3 CLI](/aws/s3/s3-cli/)). |
| `Download` | Objeyi bilgisayara indirir. |
| `Open` | Objeyi açar. |
| `Delete` | Objeyi siler. |
| `Actions` | Diğer işlemler; bunları objelerin kendi ayarlarında göreceğiz. |
| `Create folder` | Bir klasör oluşturur; objeyi bu klasöre taşıyabiliriz. |

:::caution
Bir objeyi klasöre taşıdıktan sonra objenin URL'si değişir.
:::

## Properties sekmesi

Bucket oluştururken yaptığımız tüm ayarlara **Properties** sekmesinden erişebiliriz. Ayrıca burada yapabileceğimiz birkaç ekstra ayar daha vardır.

### Intelligent-Tiering Archive configurations

Intelligent-Tiering'in dosyayı kullanımımıza göre en uygun maliyetli katmana otomatik taşıdığından bahsetmiştik (bkz. [Depolama sınıfları ve fiyatlandırma](/aws/s3/depolama-siniflari/)). Ancak bu otomatik taşıma varsayılan olarak Standard ve Standard-IA katmanları arasında gerçekleşir. Dosyanın belirli bir süre hiç kullanılmadığında en ucuz seçenekler olan Glacier katmanlarına da otomatik inmesini istiyorsak, bu izni **Intelligent-Tiering Archive configurations** başlığı altında `Create configuration` ile ayrıca yapılandırmamız gerekir.

### Server access logging

Kim hangi dosyayı yazmış, kim erişmiş gibi S3 API'si üzerinden gelen tüm işlemlerin loglarına **Server access logging** başlığı altından ulaşabiliriz (varsayılan `Disabled`). Bunun için ikinci bir bucket oluşturup tüm logların oraya yazılmasını sağlarız:

1. **Server access logging** bölümündeki `Edit` butonuna tıklayın.
2. **Edit server access logging** ekranında `Enable` seçeneğini işaretleyin.
3. Hedef bucket seçimi için açılan **Choose destination** penceresinde logların yazılacağı bucket'ı seçip `Choose destination` deyin.
4. `Save changes` ile kaydedin.

:::note
Choose destination penceresindeki bilgi notuna göre kaynak bucket ile aynı region'da (örnekte `Europe (Ireland) eu-west-1`) olmayan bucket'lar hedef olarak seçilemez.
:::

### AWS CloudTrail data events

S3 servisindeki tüm olayları; kimin, ne şekilde, hangi tarihte eriştiğini ve hangi değişiklikleri yaptığını logladığımız başlık **AWS CloudTrail data events**'tir. Bu loglar `AWS CloudTrail` butonuyla açılan CloudTrail konsolundan görüntülenir ve yapılandırılır.

### Event notifications

Hemen altındaki **Event notifications** başlığından, örneğin "bu bucket'a yeni bir `.jpg` uzantılı dosya atılırsa şu işlemi gerçekleştir" diyebiliriz. Bu işlem örneğin Lambda'daki bir kodun tetiklenmesi olabilir. Yeni bildirim `Create event notification` ile oluşturulur.

### Transfer acceleration

**Transfer acceleration**, uzak mesafelerden yapılan dosya transferlerini büyük ölçüde hızlandırır (varsayılan `Disabled`). Örneğin bucket'ımızı Amerika'da oluşturduğumuzu düşünelim. Türkiye'den veya dünyanın öbür ucundan bu bucket'a gigabaytlarca büyüklükte bir video dosyası yüklemeye çalışırsak standart internet üzerinden bu işlem epey yavaş olabilir. Bu özellik aktifken AWS dosyayı bize en yakın merkezinden teslim alır ve kendi yüksek hızlı özel ağı üzerinden bucket'a ulaştırır. Böylece dünyanın neresinde olursak olalım büyük dosyaları yükleme ve indirme hızımız ciddi şekilde artar.

:::caution
AWS bu ekstra hızlandırma hizmeti için veri transferi başına faturaya ek ücret yansıtır.
:::

### Requester pays

AWS'nin verimizi saklamak için ücret aldığından, veriyi dış dünyaya çıkarırken de ayrıca ücret talep ettiğinden bahsetmiştik. **Requester pays** özelliği aktifken (varsayılan `Disabled`) veriyi dış dünyaya açtığımızda, veriyi çeken taraf bu ücrete tabi tutulur. Bunun için veriyi çekmek isteyen kişinin bir AWS hesabı olması gerekir, çünkü ücret onun hesabına yansıtılır.

### Static website hosting

Properties sekmesindeki son başlık, S3'ün en sevilen özelliklerinden **Static website hosting**'dir (varsayılan `Disabled`). Bu özellik sayesinde HTML, CSS ve JavaScript dosyalarından oluşan statik bir web sitesini hiçbir sunucuya (örneğin bir EC2 sanal sunucusuna) ihtiyaç duymadan doğrudan S3 üzerinden yayınlayabiliriz.

Örneğin kendiniz için sadece tanıtım amaçlı bir portfolyo sitesi tasarladınız ve arka planda çalışan karmaşık bir veritabanı veya üyelik sistemi yok. Site dosyalarını doğrudan bucket'a yükleyip Static website hosting özelliğini aktif ettiğinizde AWS size anında sitenize ait bir web adresi verir. Böylece siteyi yayınlamak için işletim sistemi kurma, sunucu yönetme veya bakım yapma gibi işlerle uğraşmazsınız. Bu yöntem, geleneksel bir sunucu kiralamaya kıyasla çok daha pratik ve maliyet açısından oldukça avantajlıdır.

Uygulamalı kurulum için bkz. [Bucket policy ve statik web sitesi](/aws/s3/bucket-policy-ve-statik-site/).
