---
title: "Management: lifecycle, replication, inventory"
description: S3 bucket Management sekmesindeki lifecycle kuralları, replication, inventory ve Metrics sekmesindeki bucket istatistikleri.
module: aws
lessons: [22, 23]
order: 11
---

Bucket ayarlarının bir sonraki durağı **Management** sekmesi. Burada üç ana başlık var: **Lifecycle rules**, **Replication rules** ve **Inventory configurations**. Sayfanın sonunda **Metrics** sekmesine de kısaca bakıyoruz.

## Lifecycle rules

Bir dosyayı yüklerken istediğimiz depolama sınıfını (storage class) seçebildiğimizi ve S3 Intelligent-Tiering sınıfını seçtiğimizde sistemin dosyayı kullanım sıklığına göre en uygun erişim katmanına yerleştirdiğini [depolama sınıfları](/aws/s3/depolama-siniflari/) sayfasında görmüştük. Lifecycle rule ise dosyaları bu farklı depolama sınıfları arasında taşıyan kurallar oluşturmamızı sağlar.

### Kural oluşturma

1. Bucket içinde **Management** sekmesine geçin ve **Lifecycle configuration** bölümünde `Create lifecycle rule` butonuna tıklayın.
2. **Lifecycle rule name** alanına bir isim verin (ör. `ornek`).
3. **Choose a rule scope** altında `Apply to all objects in the bucket` seçeneğini işaretleyin. Kural bucket altındaki tüm objelere uygulanacağı için çıkan uyarıdaki `I acknowledge that this rule will apply to all objects in the bucket.` kutucuğunu da işaretleyin.
4. **Lifecycle rule actions** bölümünden kuralın yapacağı aksiyonları seçin.
5. Ayarları tamamladıktan sonra `Create rule` ile kuralı oluşturun.

### Lifecycle aksiyonları

**Lifecycle rule actions** altında seçilebilecek aksiyonlar şunlar:

- `Transition current versions of objects between storage classes`
- `Transition noncurrent versions of objects between storage classes`
- `Expire current versions of objects`
- `Permanently delete noncurrent versions of objects`
- `Delete expired object delete markers or incomplete multipart uploads`

İlkini seçersek mevcut (current) versiyonlar, aşağıda belirlediğimiz kurallara göre sınıflar arasında taşınır. Örneğin "bir dosya oluşturulduktan 90 gün sonra Standard-IA katmanına gönder" kuralı için:

1. `Transition current versions of objects between storage classes` kutucuğunu işaretleyin. Geçişlerin istek başına ücretlendirildiğini belirten uyarıdaki onay kutucuğunu (`I acknowledge that this lifecycle rule will incur a transition cost per request.`) da işaretleyin.
2. **Transition current versions of objects between storage classes** bölümünde **Choose storage class transitions** alanından `Standard-IA` seçin.
3. **Days after object creation** alanına `90` yazın. Başka geçişler eklemek için `Add transition` kullanılabilir.

:::note
Ekrandaki bilgi kutusuna göre varsayılan olarak 128 KB'tan küçük objeler hiçbir depolama sınıfına taşınmaz.
:::

Sayfanın altındaki **Review transition and expiration actions** bölümü, current ve noncurrent versiyonlar için tanımlanan aksiyonları gün gün özetler.

## Replication rules

Management altındaki ikinci kavram **Replication rules**. Bu özellik, bucket'taki dosyaların otomatik olarak bir kopyasını başka bir bucket'a aktarır.

Örneğin Frankfurt bölgesinde çalışan ve sürekli yeni dosyalar yüklenen bir ana bucket'ımız olsun. Olası bir sistem arızası veya felaket senaryosuna karşı verileri yedekli tutmak için buraya yüklenen her dosyanın anında Amerika'daki farklı bir bucket'a kopyalanmasını isteyebiliriz. Replication rule oluşturduğumuzda, dosyayı ana bucket'a attığımız an AWS arka planda bu dosyanın birebir kopyasını hedef bucket'a da gönderir.

- Kopyalama tamamen farklı bir coğrafi bölgeye yapılabileceği gibi aynı bölgedeki başka bir bucket'a da yapılabilir.
- Kuralı oluştururken yapılması gereken iki şey var: hedef bucket'ı seçmek ve AWS'nin bu kopyalamayı bizim adımıza yapabilmesi için gerekli yetkiyi vermek.

Kural, **Management** sekmesindeki **Replication rules** bölümünden `Create replication rule` butonuyla oluşturulur.

### Yedekleme dışındaki kullanım: performans

Replikasyonun yedekleme dışında bir görevi daha var: kullanıcılara daha hızlı hizmet vermek. Küresel çapta hizmet veren bir projenin ana bucket'ı Avrupa'da olsun. Amerika'daki bir kullanıcı büyük bir dosya indirmek istediğinde verinin okyanusu aşması zaman alır ve dosya yavaş yüklenir.

Bu sorunu çözmek için Amerika bölgesinde de bir bucket oluşturulur ve replication kuralıyla dosyaların bir kopyası otomatik olarak oraya gönderilir. Böylece Amerika'daki kullanıcılar veriyi Avrupa'dan çekmek yerine kendilerine en yakın bucket'tan çok daha hızlı alır. Yani replikasyon, dünyanın farklı yerlerindeki kullanıcılara yüksek performanslı bir deneyim sunmakta da kritik rol oynar.

## Inventory configurations

Bucket'ta yalnızca birkaç yüz dosya varken nelerin yüklü olduğunu görmek veya liste üzerinden arama yapmak kolaydır. Ancak dosya sayısı milyonlara, hatta milyarlara ulaştığında içeride tam olarak neler olduğunu, boyutlarını, hangi storage class'ta tutulduklarını ya da şifrelenip şifrelenmediklerini tek tek sorgulamak hem çok yavaş hem de maliyetli hale gelir.

S3 Inventory burada devreye girer:

- Yapılandırma açıldığında AWS, belirlenen periyotlarda (günlük veya haftalık) bucket içindeki tüm objelerin ve bunlara ait detaylı verilerin bir dökümünü çıkarır.
- Bu raporu CSV veya Parquet gibi formatlarda, yine belirlediğimiz bir S3 bucket'ına dosya olarak bırakır.

Kısacası Inventory, çok büyük depolama alanlarında nelerin bulunduğunu raporlamak, denetlemek ve arka planda otomatik bir "depo sayımı" yapmak için kullanılan bir yönetim aracıdır. Management sekmesinde **Inventory configurations** bölümündeki `Create inventory configuration` butonuyla oluşturulur.

## Metrics

Bucket'ın **Metrics** sekmesinde bucket ile ilgili genel tabloyu görebiliriz. Burada günlük, haftalık veya aylık periyotlarla bucket'ın toplam ne kadar depolama alanı kapladığı veya içinde kaç obje barındırdığı gibi temel istatistiklere grafikler üzerinden erişilir.

**Bucket metrics** bölümünde iki grafik yer alır:

| Grafik | Gösterdiği |
| --- | --- |
| Total bucket size | Bucket'ın toplam boyutu |
| Total number of objects | Bucket'taki toplam obje sayısı |

Grafiklerin üstünden zaman aralığı (1h, 3h, 12h, 1d, 3d, 1w veya özel aralık) seçilebilir. Aynı sekmenin altında **Storage Class Analysis** bölümü de bulunur.
