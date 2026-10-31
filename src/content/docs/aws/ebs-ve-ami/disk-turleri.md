---
title: EBS disk türleri
description: Instance Store ile EBS farkı, SSD ve HDD tabanlı diskler ile io1, gp2, st1 ve sc1 EBS disk tiplerinin özellikleri.
module: aws
lessons: [26]
order: 22
---

Sanal makine oluştururken sadece CPU ve RAM gibi özellikleri seçmek yeterli değildir. İşletim sistemini ve verileri barındırabilmesi için makineye bir de disk bağlamamız gerekir. EC2 makinelerine bağlanabilecek iki temel disk altyapısı vardır.

## Instance Store (Ephemeral, geçici)

AWS veri merkezlerindeki fiziksel sunucuların üzerinde donanımsal diskler bulunur. Instance Store tipi diskler, sanal makinenin o an üzerinde çalıştığı fiziksel makineye doğrudan bağlıdır.

- Sanal makineyi durdurup (stop) tekrar başlattığınızda (start) makine arka planda farklı bir fiziksel sunucuya taşınabilir. Makine yer değiştirdiği için eski diskte kalan veriler de silinir.
- Bu sebeple Instance Store kalıcı olmayan bir veri deposudur; içindekilere sadece makine çalışırken erişilebilir.
- Bu disklerde **Snapshot** desteği yoktur.
- Kalıcılık dezavantajlarına rağmen disk fiziksel olarak makinenin içinde olduğu için okuma/yazma hızı çok yüksektir.

:::note
**Snapshot (anlık görüntü):** Diskin o anki tam halinin fotoğrafını çekerek yedeğini almayı sağlayan sistemdir. Bu yedek sayesinde veriler korunabilir veya aynı disk daha sonra başka makinelere kopyalanabilir. Ayrıntılar: [Volume ve snapshot](/aws/ebs-ve-ami/volume-ve-snapshot/).
:::

## Elastic Block Store (EBS)

Kalıcı veri ihtiyacı nedeniyle AWS'de yaygın olarak kullanılan asıl disk modeli **Elastic Block Store (EBS)**'dir.

- EBS, AWS altında kendi başına bağımsız bir servistir.
- Disk, sanal makinenin fiziksel kasasında değil, ağ üzerinden dışarıdan bağlı şekilde çalışır.
- Tamamen kalıcı bir veri deposudur. %99.999 erişilebilirlik garantisi sunar.
- Veri kaybını önlemek için aynı Availability Zone içindeki birden fazla fiziksel cihaza arka planda otomatik olarak kopyalanır.

## SSD ve HDD tabanlı diskler

S3'teki [depolama sınıflarına](/aws/s3/depolama-siniflari/) benzer şekilde EBS'de de ihtiyaca, performans beklentisine ve bütçeye göre seçilecek disk modelleri vardır. Bu diskler iki ana başlıkta incelenir.

### SSD (Solid State Drive)

İçinde hareketli parça bulunmayan, verileri bellek yongalarında tutan yeni nesil ve çok hızlı disklerdir. Verilere rastgele ulaşıp küçük ama çok sayıda işlemi aynı anda yapması gereken durumlar için tasarlanmıştır.

**Avantajları:**

- Saniyedeki işlem kapasitesi (IOPS) çok yüksektir.
- EC2 makinesine işletim sistemi kurmak (boot volume) için en uygun ve varsayılan seçenektir.
- Sürekli ve hızlı veri yazılıp okunan işlemler (ör. veritabanları) için idealdir.

**Dezavantajları:**

- HDD'ye kıyasla GB başına maliyeti daha yüksektir.
- Sadece depolama veya arşivleme yapılacaksa gereksiz ve pahalı bir çözümdür.

### HDD (Hard Disk Drive)

İçinde fiziksel olarak dönen manyetik plakalar bulunan geleneksel disk teknolojisidir. Disk döndüğü için verilere rastgele değil, sırayla okuma-yazma yaparken çok daha başarılıdır.

**Avantajları:**

- Maliyeti SSD'lere göre çok daha düşüktür.
- Saniyedeki işlem sayısından çok büyük veri paketlerinin aktarımında başarılıdır.
- Büyük veri analizi (Big Data), log dosyalarının tutulması veya nadir erişilen büyük dosyaların depolanması için idealdir.

**Dezavantajları:**

- Hareketli parçaları olduğu için SSD'ler kadar hızlı tepki veremez (IOPS değerleri düşüktür).
- AWS'de bu diskler işletim sistemi kurmak (boot volume) için kullanılamaz; sadece ek veri diski olarak makineye bağlanabilir.

## EBS disk tipleri

| Disk | API adı | Teknoloji | Boyut | Maks. IOPS (disk başına) | Kullanım |
|---|---|---|---|---|---|
| Provisioned IOPS SSD | `io1` | SSD | 4 GB - 16 TB | 32,000 | Gecikmeye duyarlı (latency-sensitive) işlemler için en yüksek performanslı SSD. Yüksek I/O gerektiren NoSQL ve ilişkisel veritabanları. |
| General Purpose SSD | `gp2` | SSD | 1 GB - 16 TB | 10,000 | Fiyat ve performans dengesini en iyi sağlayan genel amaçlı SSD. Boot volume'ler, düşük gecikmeli interaktif uygulamalar, geliştirme/test ortamları. |
| Throughput Optimized HDD | `st1` | HDD | 500 GB - 16 TB | 500 | Sık erişilen, yüksek veri aktarımı (throughput) gerektiren yoğun iş yükleri için düşük maliyetli HDD. Big data, veri ambarları, log işleme. |
| Cold HDD | `sc1` | HDD | 500 GB - 16 TB | 250 | Çok nadir erişilen iş yükleri için en düşük maliyetli HDD. Günlük olarak daha az tarama gerektiren "soğuk" verilerin depolanması ve arşivlenmesi. |
