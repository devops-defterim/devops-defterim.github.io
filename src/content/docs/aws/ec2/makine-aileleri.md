---
title: Makine aileleri ve isimlendirme
description: EC2 makine aileleri (General Purpose, Compute, Memory, Storage, Accelerated) ve m5.large gibi tip adlarının okunuşu.
module: aws
lessons: [24]
order: 16
---

Fiyatlandırma modellerinden sonra hangi EC2 makine çeşitlerini oluşturabileceğimize bakalım.

## Makine aileleri özet tablosu

| | General Purpose | Compute Optimized | Memory Optimized | Storage Optimized | Accelerated Computing |
|---|---|---|---|---|---|
| **Aileler** | T, M, A | C | R, X, Z, U | D, I, H | F, P, G |
| **Kullanım alanları** | Web sunucuları, kaplanmış mikro servisler, önbellek filoları ve dağıtılmış veri depoları ile geliştirme ortamları gibi ölçeklendirilmiş iş yükleri | Yüksek performanslı web sunucuları, bilimsel modelleme, toplu işlem, dağıtık analitik, yüksek performanslı bilgi işlem (HPC), makine / derin öğrenme çıkarımı, reklam sunumu, yüksek ölçeklendirilebilir çok oyunculu oyun ve video kodlama | Yüksek performanslı veritabanları, dağıtılmış web ölçeğinde bellek içi önbellekleri, orta boyutlu bellek içi veritabanları, gerçek zamanlı büyük veri analitiği ve diğer kurumsal uygulamalar gibi yoğun bellek kullanan uygulamalar | MapReduce tabanlı iş yükleri, HDFS ve MapR-FS gibi dağıtılmış dosya sistemleri, ağ dosya sistemleri, Apache Kafka gibi günlük veya veri işleme uygulamaları ve büyük veri iş yükü kümesi | Makine / derin öğrenme, yüksek performanslı bilgi işlem, hesaplamalı akışkanlar dinamiği, hesaplamalı finans, sismik analiz, konuşma tanıma, özerk araçlar, ilaç keşfi |

## Aileler

### 1. General Purpose (Genel Amaçlı: T, M, A)

İşlemci, bellek ve ağ kaynaklarını dengeli bir şekilde sunarak çok yönlü ve stabil bir temel oluşturur. Projenin ne kadar kaynak tüketeceğinden emin değilseniz veya trafikte anlık büyük dalgalanmalar beklemiyorsanız en güvenli başlangıç noktasıdır. Kurumsal uygulamaların arka plan süreçlerinde, küçük ve orta ölçekli veritabanlarında veya test ortamlarında sıklıkla tercih edilir. Kaynakların eşit dağılımı sayesinde maliyet ve performans açısından iyi bir orta yol sunar.

### 2. Compute Optimized (İşlemci Optimize: C)

Odak noktası yüksek işlemci gücü olan bu makineler, standart sunucuların zorlanacağı karmaşık matematiksel hesaplamaları hızlıca çözmek için tasarlanmıştır. Uygulama bellekten çok doğrudan işlem gücüne ihtiyaç duyuyorsa darboğaz yaşamadan çalışmayı sağlar. Sürekli CPU sınırlarını zorlayan algoritmalar için idealdir; özellikle büyük verileri şifreleme veya medya dönüştürme gibi yoğun işlem gerektiren durumlarda kullanılır.

### 3. Memory Optimized (Bellek Optimize: R, X, Z, U)

Bazı sistemler veriyi diske yazmak yerine anlık olarak çok büyük RAM kapasitelerinde tutarak hızlı işlem yapmak ister; bu makineler bunun için üretilmiştir. Büyük boyutlu verileri doğrudan belleğe yükleyerek milisaniyelik tepki süreleri elde etmeyi sağlar. İşlemciden çok geniş bir çalışma alanına ihtiyaç duyan uygulamalarda, özellikle milyonlarca satırlık verinin anında işlenmesi ve filtrelenmesi gereken durumlarda kullanılır.

### 4. Storage Optimized (Depolama Optimize: D, I, H)

Yerel disklerde saniyede on binlerce okuma ve yazma işlemi gerçekleştirmeniz gerektiğinde kullanılır. Verileri uzak bir ağ üzerinde değil, doğrudan makinenin içine gömülü çok hızlı disklerde tutarak veri erişim gecikmesini en aza indirir. Sürekli diske büyük boyutlarda veri yazıp okuyan kayıt sistemleri veya büyük veri ambarları için uygundur. Uygulamanın performansı disk hızına takılıyorsa bu aile sorunu çözer.

### 5. Accelerated Computing (Hızlandırılmış İşlem: F, P, G)

Standart işlemcilerin yetersiz kaldığı, spesifik ve paralel hesaplama gerektiren görevler için özel donanımlarla güçlendirilmiş makinelerdir. Sanal makinenin doğrudan GPU'ya ya da özel donanım hızlandırıcılarına erişmesini istiyorsak bu aileyi kullanırız. Yapay zeka eğitimleri, 3D render işlemleri veya ağır simülasyonlar gibi yükler için tercih edilir.

## İsimlendirme mantığı (T-Shirt Sizing)

Makine ailesine karar verdikten sonra sıra ihtiyacımız olan donanım kapasitesini seçmeye gelir. AWS sanal makineleri isimlendirirken kıyafet bedenlerine benzeyen bir **T-Shirt Sizing** mantığı kullanır. **m5.large** örneğini parçalara ayıralım:

| Parça | Anlamı |
|---|---|
| **m** (aile / sınıf) | Makinenin hangi aileye ait olduğunu gösterir. `M` harfi makinenin General Purpose olduğunu ifade eder. Bellek odaklı olsaydı `R`, işlemci odaklı olsaydı `C` görecektik. |
| **5** (nesil) | Donanımın kaçıncı nesil olduğunu belirtir. Sayı ne kadar yüksekse arka plandaki fiziksel işlemci ve teknoloji o kadar yenidir (1'den başlayıp 6'ya ve ötesine gidebilir). |
| **large** (boyut / kapasite) | Noktadan sonraki kısım, makinedeki CPU ve RAM miktarını belirleyen asıl beden kısmıdır. |

### Boyutlar nasıl okunur?

Kaynaklar çok küçük donanımlardan çok büyük sunuculara kadar uzanır. Boyut büyüdükçe işlemci ve bellek miktarı genellikle ikiye katlanarak artar:

- **Nano / Micro / Small:** Ailenin en küçük üyeleridir. Düşük trafikli kişisel bloglar, ufak test ortamları veya geliştirme aşamasındaki basit projeler için yeterlidir. Maliyeti en düşük gruptur (örneğin `t2.micro`, AWS'nin ücretsiz deneme katmanında sıkça kullanılır).
- **Medium / Large:** Standart ve kararlı iş yükleri için orta segment donanımlardır. Kurumsal web siteleri, orta ölçekli veritabanları ve standart arka plan uygulamaları için en çok tercih edilen boyutlardır (örneğin `m5.large` 2 vCPU ve 8 GB RAM sunar).
- **XLarge ve katları (2XLarge, 4XLarge ... 24XLarge):** Kurumsal seviyedeki ağır iş yükleri için tasarlanmış büyük sistemlerdir. Milyonlarca kullanıcısı olan uygulamalar, saniyede binlerce işlem yapan büyük veritabanları veya ağır analiz motorları için kullanılır. Sayı arttıkça çekirdek sayısı ve bellek kapasitesi de büyür.
