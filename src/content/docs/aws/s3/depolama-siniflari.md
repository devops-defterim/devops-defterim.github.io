---
title: Depolama sınıfları ve fiyatlandırma
description: S3 depolama sınıflarının dayanıklılık, erişilebilirlik ve maliyet farkları ile S3 fiyatlandırmasının nasıl hesaplandığı.
module: aws
lessons: [21]
order: 8
---

## Depolama sınıfları (Storage Classes)

S3 tek bir servis olmasına rağmen, objeleri kullanım senaryomuza göre tutabileceğimiz farklı depolama sınıfları vardır.

S3'ü kullandığımızda arka tarafta şu olur: AWS'nin veri merkezlerinde çok büyük disklerden oluşan depolama altyapıları vardır ve bunların tamamını AWS yönetir. Bir objeyi S3'e yüklediğimizde, bu verinin arka planda makinelere nasıl dağıtılacağını ve nasıl saklanacağını depolama sınıfını seçerek biz belirleriz.

## S3 Standard

Değiştirilmediği sürece yüklediğimiz her dosya varsayılan olarak bu sınıfa yüklenir. Bunun anlamı şudur:

- Yüklediğimiz dosya, makinelerden biri bozulursa veri kaybolmasın diye veri merkezindeki birden fazla makineye yedeklenir.
- Aynı zamanda o bölgedeki diğer veri merkezlerine de kopyalanır. Bu sayede bir veri merkezine tamamen erişilemese bile verimize her zaman ulaşabiliriz.

AWS, S3 Standard'da %99.999999999 dayanıklılık (durability) sunarak zaman içinde bir milyar dosyadan en fazla bir tanesini kaybedebileceğinin garantisini verir.

Garanti edilen diğer özellik %99.99 oranındaki Availability SLA'dir. Bu, bir ay içinde en fazla 4 dakika 21 saniye erişim kesintisi yaşanabileceği, diğer tüm zamanlarda dosyalara kesintisiz erişileceği anlamına gelir.

En sık ve sürekli erişmemiz gereken objeleri bu sınıfta tutarız. Depolama maliyeti en yüksek olan sınıf da budur.

## Diğer sınıflar

**S3 Standard-IA (Infrequent Access):** En çok kullanılan ikinci sınıftır. Teknik özellikler hemen hemen aynıdır, ancak depolama için Standard sınıfın yarı fiyatı ücretlendirilir; buna karşılık yüklediğiniz dosyaya her eriştiğinizde ekstra bir veri çekme ücreti alınır. Amaç, nadiren eriştiğimiz ama gerektiğinde anında ulaşmak istediğimiz dosyaları maliyet avantajıyla saklamaktır.

**S3 One Zone-IA:** En büyük farkı, dosyaların üç farklı veri merkezinde değil tek bir veri merkezinde tutulmasıdır. Dolayısıyla o veri merkezinde yaşanan bir felakette dosyalarınıza erişemeyebilir veya onları kaybedebilirsiniz. Bu risk karşılığında diğer iki sınıfa göre daha ucuz depolama sunar.

**S3 Intelligent-Tiering (Akıllı Katmanlandırma):** Sınıflardan hiçbirini seçmekle uğraşmak istemiyorsanız bu sınıfı seçersiniz; AWS kullanım alışkanlıklarınızı izleyerek dosyayı en uygun maliyetli yere otomatik taşır.

**S3 Glacier Deep Archive:** Erişim süresinin önemsiz olduğu, istediğinizde gelmesinin birkaç saat sürmesinin sorun yaratmayacağı, ama yasal zorunluluk gibi sebeplerle yıllarca saklanması gereken dosyalar için kullanılır. S3'ün depolama maliyeti açık ara en ucuz olan sınıfıdır.

**S3 Glacier Instant Retrieval:** Arşivlemeniz gereken ancak istediğinizde anında erişmek istediğiniz dosyalar için kullanılır.

:::caution
Glacier sınıflarında aylık *depolama* ücretleri çok ucuz olsa da, dosyayı okumak veya indirmek istediğinizde kesilen *veri çekme* ücretleri yüksektir. Bu sınıftaki bir dosyaya sürekli erişmeye çalışırsanız faturanız S3 Standard sınıfından bile çok daha pahalıya gelebilir.
:::

## Sınıfların karşılaştırması

| | S3 Standard | S3 Intelligent-Tiering* | S3 Standard-IA | S3 One Zone-IA† | S3 Glacier | S3 Glacier Deep Archive** |
| --- | --- | --- | --- | --- | --- | --- |
| Designed for durability | 99.999999999% (11 9's) | 99.999999999% (11 9's) | 99.999999999% (11 9's) | 99.999999999% (11 9's) | 99.999999999% (11 9's) | 99.999999999% (11 9's) |
| Designed for availability | 99.99% | 99.9% | 99.9% | 99.5% | N/A | N/A |
| Availability SLA | 99.9% | 99% | 99% | 99% | N/A | N/A |
| Availability Zones | ≥3 | ≥3 | ≥3 | 1 | ≥3 | ≥3 |
| Minimum capacity charge per object | N/A | N/A | 128KB | 128KB | 40KB | 40KB |
| Minimum storage duration charge | N/A | 30 days | 30 days | 30 days | 90 days | 180 days |
| Retrieval fee | N/A | N/A | per GB retrieved | per GB retrieved | per GB retrieved | per GB retrieved |
| First byte latency | milliseconds | milliseconds | milliseconds | milliseconds | select minutes or hours | select hours |
| Storage type | Object | Object | Object | Object | Object | Object |
| Lifecycle transitions | Yes | Yes | Yes | Yes | Yes | Yes |

Sınıfları sıcak (sık erişilen) veriden soğuk (arşiv) veriye doğru şöyle sıralayabiliriz:

| Sınıf | Kullanım | Dikkat edilecekler |
| --- | --- | --- |
| Standard | Active, frequently accessed data | |
| Intelligent Tiering | Data with changing access patterns | Minimum storage duration; per-object monitoring fee |
| Infrequent Access | Infrequently accessed data | Minimum storage duration and object size |
| One Zone | Re-creatable, less accessed data | Minimum storage duration and object size; retrieval fee GB |
| Glacier | Archival data | Minimum storage duration and object size; retrieval fee GB; retrieval in minutes or hours |
| Deep Archive | Long-term archive data | Minimum storage duration and object size; retrieval fee GB; retrieval in hours |

Soldan sağa: Frequent Access (Hot) → Infrequent Access → Archive (Cold).

## Sınıf seçmenin yolları

Depolama sınıfını üç şekilde belirleyebiliriz:

1. Dosyaları yüklerken seçmek.
2. Yükledikten sonra değiştirmek.
3. Lifecycle Rule kuralları koyarak dosyaların belirli bir süre sonra otomatik olarak diğer sınıflara taşınmasını sağlamak (bkz. [Management: lifecycle, replication, inventory](/aws/s3/management/)).

## S3 fiyatlandırması

S3 servislerindeki fiyat hesaplaması şunlara göre yapılır:

- Toplam depolanan veri boyutu (GB cinsinden)
- S3'ten dış dünyaya transfer edilen veri boyutu
- Toplam obje erişim isteği sayısı

Ayrıca fiyatlandırma her region için değişebilir ve AWS kullanımınız arttıkça birim fiyat düşer.

Kullanımınız sonucunda ne kadar ücret çıkacağını hesaplamak isterseniz [https://calculator.aws/#/](https://calculator.aws/#/) adresini kullanabilirsiniz.
