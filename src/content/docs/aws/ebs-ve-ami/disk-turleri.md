---
title: EBS disk türleri
description: Instance Store ile EBS farkı, SSD ve HDD tabanlı diskler ile io1, gp2, st1 ve sc1 EBS disk tiplerinin özellikleri.
module: aws
lessons: [26]
order: 22
---

EC2 hakkında öğrenmemiz gereken diğer konularla devam edelim.

Sanal makine oluştururken sadece CPU ve RAM gibi özellikleri seçmek, tahmin edebileceğiniz gibi tek başına yeterli olmuyor. İşletim sistemimizi ve verilerimizi barındırabilmesi için bu sanal makineye bir de disk bağlamamız gerekiyor. Şimdi gelin birlikte bu disk çeşitlerini öğrenelim.

## Instance Store (Ephemeral - Geçici)

EC2 makinelerine bağlayabileceğimiz iki temel disk altyapısı mevcuttur. Bunlardan ilki **Instance Store** (Ephemeral - Geçici) disklerdir. AWS'nin veri merkezlerinde bulunan fiziksel sunucuların kendi üzerlerinde donanımsal diskler bulunur. Instance Store tipi diskler, sanal makinenizin o an üzerinde çalıştığı fiziksel makineye doğrudan bağlıdır. Ancak sanal makinenizi durdurup (stop) tekrar başlattığınızda (start), makineniz arka planda farklı bir fiziksel sunucuya taşınabilir. Makine yer değiştirdiği için eski diskte kalan verileriniz de silinir.

Bu sebeple Instance Store, kalıcı olmayan bir veri deposudur ve diskin içindekilere sadece makine çalışırken erişilebilir. Ayrıca bu disklerde Snapshot desteği yoktur.

:::note
(Kısa Bilgi: [Snapshot](/aws/ebs-ve-ami/volume-ve-snapshot/) (Anlık Görüntü), diskinizin o anki tam halinin fotoğrafını çekerek yedeğini almanızı sağlayan sistemdir. Bu yedek sayesinde verilerinizi koruyabilir veya aynı diski daha sonra başka makinelere de kopyalayabilirsiniz.)
:::

Tüm bu kalıcılık dezavantajlarına rağmen, disk fiziksel olarak makinenin tam içinde yer aldığı için verilere erişim hızı (okuma/yazma) inanılmaz derecede yüksektir.

## Elastic Block Store (EBS)

Kalıcı veri ihtiyacımız olduğu için AWS üzerinde yaygın olarak kullandığımız asıl disk modeli ise **Elastic Block Store (EBS)**'dir. EBS, AWS altında kendi başına bağımsız bir servistir. Bu diski seçtiğimizde, sanal makinemizin fiziksel kasasında değil, ağ üzerinden dışarıdan bağlı bir şekilde çalışır. Tamamen kalıcı bir veri deposudur. %99.999 oranında erişilebilirlik garantisi sunar ve verilerinizi kaybetmemeniz için aynı Availability Zone içindeki birden fazla fiziksel cihaza arka planda otomatik olarak kopyalanır.

## SSD ve HDD tabanlı diskler

Şimdi de EBS üzerinde oluşturabileceğimiz disk tiplerine göz atalım. Tıpkı S3 servisindeki [depolama katmanlarında](/aws/s3/depolama-siniflari/) olduğu gibi, EBS'de de ihtiyacımıza, performans beklentimize ve bütçemize göre seçeceğimiz çeşitli disk modelleri bulunur. Bu diskler temel olarak iki ana başlıkta incelenir: SSD tabanlı diskler ve HDD tabanlı diskler.

Şimdi bu iki teknolojinin farklarına, avantajlarına ve dezavantajlarına kısaca değinelim:

### 1. SSD (Solid State Drive) tabanlı diskler

İçerisinde hiçbir hareketli parça bulunmayan, verileri bellek yongalarında tutan yeni nesil ve çok hızlı disklerdir. Sistemin verilere rastgele ulaşıp küçük ama çok sayıda işlemi aynı anda yapması gereken durumlar için tasarlanmıştır.

**Avantajları:**

- Saniyedeki işlem yapma kapasitesi (IOPS) çok yüksektir.
- EC2 makinemize işletim sistemi kurmak (Boot volume) için en uygun ve varsayılan seçenektir.
- Sürekli ve hızlı veri yazılıp okunan işlemler (örneğin Veritabanları - Databases) için kusursuzdur.

**Dezavantajları:**

- HDD'ye kıyasla GB başına düşen maliyeti daha yüksektir.
- Sadece depolama veya arşivleme yapılacaksa gereksiz lüks ve pahalı bir çözümdür.

### 2. HDD (Hard Disk Drive) tabanlı diskler

İçerisinde fiziksel olarak dönen manyetik plakaların bulunduğu geleneksel disk teknolojisidir. Disk döndüğü için verilere rastgele değil, sırayla okuma-yazma yaparken çok daha başarılıdır.

**Avantajları:**

- Maliyeti SSD'lere göre çok daha düşüktür.
- Saniyedeki işlem sayısından ziyade, büyük veri paketlerinin aktarımı konusunda harikadır.
- Büyük veri analizi (Big Data), log dosyalarının tutulması veya nadir erişilen büyük dosyaların depolanması için en ideal çözümdür.

**Dezavantajları:**

- Hareketli parçaları olduğu için SSD'ler kadar hızlı tepki veremez (IOPS değerleri düşüktür).
- AWS üzerinde bu diskleri işletim sistemi kurmak (Boot volume) için kullanamayız; sadece ek depo (veri diski) olarak makineye bağlayabiliriz.

## EBS disk tipleri

### 1. Provisioned IOPS SSD (io1)

- Gecikmeye duyarlı işlemler (latency-sensitive) için tasarlanmış en yüksek performanslı SSD disk türüdür.
- Özellikle yüksek giriş/çıkış (I/O) işlemi gerektiren NoSQL ve ilişkisel veritabanlarında (relational databases) kullanılır.
- Sistemdeki API adı `io1`'dir.
- Oluşturulabilecek disk boyutu 4 GB ile 16 TB arasında değişir.
- Disk başına ulaşabildiği maksimum IOPS (saniyelik işlem) kapasitesi 32,000'dir.

### 2. General Purpose SSD (gp2)

- Çok çeşitli işlemler için fiyat ve performans dengesini en iyi şekilde sağlayan genel amaçlı SSD disk türüdür.
- İşletim sistemi kurulan ana disklerde (boot volumes), düşük gecikmeli interaktif uygulamalarda ve geliştirme/test (dev & test) ortamlarında sıklıkla kullanılır.
- Sistemdeki API adı `gp2`'dir.
- Oluşturulabilecek disk boyutu 1 GB ile 16 TB arasında değişir.
- Disk başına ulaşabildiği maksimum IOPS kapasitesi 10,000'dir.

### 3. Throughput Optimized HDD (st1)

- Sık erişilen ve yüksek veri aktarımı (throughput) gerektiren yoğun iş yükleri için tasarlanmış düşük maliyetli HDD disk türüdür.
- Büyük veri (big data) projelerinde, veri ambarlarında (data warehouses) ve log işleme görevlerinde kullanım için idealdir.
- Sistemdeki API adı `st1`'dir.
- Oluşturulabilecek disk boyutu 500 GB ile 16 TB arasında değişir.
- Disk başına ulaşabildiği maksimum IOPS kapasitesi 500'dür.

### 4. Cold HDD (sc1)

- Çok nadir erişilen iş yükleri için tasarlanmış en düşük maliyetli HDD disk seçeneğidir.
- Günlük olarak daha az tarama işlemi gerektiren "soğuk (colder)" verilerin depolanması ve arşivlenmesi için kullanılır.
- Sistemdeki API adı `sc1`'dir.
- Oluşturulabilecek disk boyutu 500 GB ile 16 TB arasında değişir.
- Disk başına ulaşabildiği maksimum IOPS kapasitesi 250'dir.

:::caution[Düzeltme]
Bu değerler eski AWS dokümantasyonundan. Güncel sınırlar: `io1` için disk başına en fazla 64,000 IOPS, `gp2` için en fazla 16,000 IOPS; `st1` ve `sc1` için en küçük boyut 125 GiB. Bugün genel amaçlı varsayılan disk tipi `gp3`'tür (en fazla 16,000 IOPS).
:::
