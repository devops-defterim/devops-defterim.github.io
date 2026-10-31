---
title: AMI ve Image Builder
description: AMI çeşitleri, snapshot'tan manuel AMI oluşturma ve EC2 Image Builder pipeline'ı ile imaj üretimini otomatikleştirme.
module: aws
lessons: [26]
order: 24
---

## AMI nedir?

Daha önce [Instance oluşturma](/aws/ec2/instance-olusturma/) sırasında bahsettiğimiz AMI'yi, sanal sunucuları kurmak için kullandığımız **hazır bir kurulum kalıbı** olarak düşünebiliriz. Bulutta bir sanal makineyi ayağa kaldırmak için işletim sistemi ve temel ayarlar gibi gereken tüm başlangıç bilgileri bu paketin içinde hazır gelir.

AWS'de yeni bir sanal makine başlatırken sistem mutlaka bir kaynak AMI seçmemizi ister. Tamamen aynı ayarlara ve altyapıya sahip birden fazla sunucuya ihtiyacınız varsa her birini sıfırdan kurmazsınız; **tek bir AMI kalıbından saniyeler içinde yüzlerce birebir aynı kopya başlatabilirsiniz.** Farklı özelliklerde sunucular gerektiğinde her biri için uygun farklı bir AMI seçilir.

## AMI çeşitleri

Erişim haklarına ve lisans durumlarına göre üç çeşit AMI vardır:

| Çeşit | Açıklama |
|---|---|
| **Public** (herkese açık) | AWS'nin kendisi veya topluluk tarafından hazırlanan, herkesin varsayılan olarak erişip kullanabileceği standart kalıplar. |
| **Private** (özel) | Sadece kendi hesabımızda oluşturduğumuz, dışarıya kapalı ve yalnızca bizim kullanabildiğimiz kalıplar. |
| **Paid** (ücrete tabi) | AWS Marketplace üzerinde satılan, içinde özel lisanslı programlar veya kurumsal yazılımlar kurulu gelen kalıplar. |

## 1. Yöntem: Manuel AMI oluşturma

1. **Volumes** sekmesinden ilgili diski seçip bir snapshot oluşturun (bkz. [Volume ve snapshot](/aws/ebs-ve-ami/volume-ve-snapshot/)).
2. **Snapshots** menüsünde snapshot'ı seçip **Actions → Create image from snapshot** seçeneğine tıklayın.
3. İşlem tamamlanınca soldaki menüden **AMIs** kısmına geldiğinizde oluşturduğunuz kalıbın burada olduğunu görürsünüz.
4. **Instances** menüsünden sanal makine oluşturma adımlarına geçin. İmaj seçim ekranında kendi oluşturduğunuz AMI'yi (**My AMIs**) seçerek yeni sanal makineyi başlatın.

:::note
Oluşturulan AMI'ler varsayılan olarak **Private** durumdadır. Bunu değiştirmek için **AMIs → Actions → Edit AMI permissions** ekranından imajı **Public** yapabilir veya Private kalıpları farklı AWS hesaplarıyla paylaşabilirsiniz.
:::

## 2. Yöntem: EC2 Image Builder ile otomatikleştirme

Her seferinde manuel olarak makine açmak, güncellemeleri yapmak ve imaj almak bir süre sonra yorucu ve hataya açık hale gelir. AMI oluşturma adımlarını otomatikleştirmek için **EC2 Image Builder** kullanılır. Servis bir **pipeline** kurmaya dayanır.

1. EC2 servisinde **AMIs** başlığına tıklayın; açılan ekranda `EC2 Image Builder` butonuna tıklayın.
2. `Create image pipeline` butonuyla pipeline oluşturmaya başlayın. Sihirbaz şu adımlardan oluşur: Specify pipeline details, Choose recipe, Define image creation process, Define infrastructure configuration (isteğe bağlı), Define distribution settings (isteğe bağlı), Review.

### Adım 1: Pipeline detayları

| Alan | Açıklama |
|---|---|
| **Pipeline name** | Otomatik imaj alma hattının adı. Gelecekte kaynaklar arasında kaybolmamak için projeyi anlatan net bir isim girilir (ör. `aylik-ubuntu-guncel-imaj`). |
| **Description** | İsteğe bağlı. Pipeline'ın hangi amaca hizmet ettiği veya hangi ekibin kullanacağı not edilir. |
| **Enhanced metadata collection** | İşaretliyken AWS (Systems Manager Inventory aracılığıyla) imajın içindeki bileşenler hakkında daha detaylı bilgi toplar. Kurulan programların imajla uyumlu çalışıp çalışmadığını doğrulamak için varsayılan olarak işaretli bırakmak iyi bir pratiktir. |
| **Save a snapshot of vulnerability findings** | Amazon Inspector ile imajda işletim sistemi veya yazılım güvenlik açığı olup olmadığı denetlenir. Kutucuklar ekranda pasif görünse de güvenlik standartları yüksek kurumsal projelerde bu taramalar aktif edilebilir. |

**Build schedule** bölümü:

- **Schedule options:** İmaj alma işleminin nasıl tetikleneceği seçilir. Üç seçenek vardır:
  - **Schedule builder:** Ekranda seçili olan, en pratik yöntem. İşlem gün ve saat belirterek otomatikleştirilir. Örnekteki ayara göre sistem her hafta (`Week`), cumartesi (`Saturday`) UTC 14:00'te çalışıp yeni bir imaj üretir.
  - **cron expression:** Çalışma takvimi cron formatında kodla, daha detaylı kurallarla belirlenir.
  - **Manual:** Otomasyonu takvime bağlamak yerine sadece biz çalıştırdığımızda imaj alınır.
- **Dependency update settings:** Takvim geldiğinde sistemin nasıl davranacağı seçilir. Seçili olan `Run pipeline based on schedule` ile sistem, temel işletim sisteminde veya kurulu programlarda güncelleme olup olmadığına bakmadan takvime uyar ve her hafta o saatte yeni imaj üretir.
- **Auto-disable policy** (Advanced settings): Maliyetleri ve kaynakları koruyan bir güvenlik ayarıdır. Hatta bir şey ters giderse (ör. hatalı kod nedeniyle imaj oluşturulamıyorsa) sistemin sürekli boşuna çalışıp hata vermesini engeller. Örnekte sınır `5`; sistem üst üste 5 kez başarısız olursa, biri hatayı çözene kadar pipeline kendini otomatik olarak devre dışı bırakır.

### Adım 2: Recipe (tarif)

| Alan | Açıklama |
|---|---|
| **Recipe configuration** | `Create new recipe` seçilerek önceden kaydedilmiş bir şablon yerine sıfırdan yeni tarif oluşturulacağı belirtilir. |
| **Image type** | Üretilecek imaj türü. Standart sanal makine kalıbı için `Amazon Machine Image (AMI)` seçili. Diğer seçenek olan Docker, konteyner altyapıları içindir. |
| **Recipe details** | Tarife bir isim ve **Version** (ör. `1.0.0`) verilir. Tarifler sonradan değiştirilemediği için her yapılandırma değişikliğinde sürüm numarası artırılır. |
| **Select image** | Kalıbın hangi temel üzerine inşa edileceği. `Select managed images` ile AWS'nin yönettiği güvenli imajlar kullanılır. |
| **Image Operating System (OS)** | Temel işletim sistemi olarak Amazon Linux seçili. İhtiyaca göre Ubuntu, Windows veya CentOS da seçilebilir. |
| **Image origin** | `Quick start` ile AWS'nin kullanıma hazır sunduğu optimize edilmiş standart başlangıç kalıplarından biri seçilir. |
| **SSM agent** | AWS'nin imajı hazırlarken açtığı geçici makineye güvenle bağlanıp komutları (kurulumları) çalıştırabilmesi için gereken araçtır. İmaj bittikten sonra yeni kalıpta yer almasın isteniyorsa `Remove SSM agent after pipeline execution` işaretlenir. |
| **User data** | Makine ilk ayağa kalkarken otomatik çalışması istenen özel başlangıç script'leri varsa buraya yazılır. |
| **Working directory** | AWS'nin kurulum sırasında indireceği dosyaları geçici olarak tutup çalıştıracağı klasör. Varsayılan `/tmp`. |
| **Build components** | İmajın içine nelerin kurulacağı adım adım belirlenir. Örneğin "işletim sistemini güncelle", "şu yazılımı indir", "güvenlik ayarlarını yap" gibi komut paketleri buradan eklenir. |
| **Test components** | Kurulumlar bittikten sonra "kurduğum programlar düzgün çalışıyor mu?" diye makineyi kontrol eden doğrulama testleri eklenir. |
| **Storage (volumes)** | Üretilecek AMI'nin diskinin kaç GB ve hangi tipte (ör. gp3) olacağı ayarlanır. Temel imajın disk ayarları otomatik yansır; istenirse `Add new EBS volume` ile ek disk eklenir. |
| **AMI watermarks** | İsteğe bağlı güvenlik ve takip adımı. Üretilen imaja gizli bir filigran eklenir; kalıp kopyalanıp başka yerde kullanılsa bile kaynağının bu otomasyon hattı olduğu takip edilebilir. |

### Adım 3: Image creation process

**Type:** AWS'nin imajı üretirken işlemleri hangi sırayla (workflow) yapacağı belirlenir.

- Ekranda `Default workflows` seçili; yani AWS'ye "standart derleme (build) ve test adımlarını kendi varsayılan sıranla yap" talimatı verilir.
- Adımların sırasına tamamen kendimiz karar vermek isteseydik (ör. önce şu testi yap, sonra bunu kur) `Custom workflows` seçeneğini kullanırdık.

### Adım 4: Infrastructure configuration

- **Configuration options:** AWS'nin imajı hazırlamak için arka planda açacağı geçici sanal makinenin özellikleri belirlenir. `Create infrastructure configuration using service defaults` seçili olduğu için sistem AWS'nin otomatik ayarlarına bırakılır.
- **IAM instance profile:** Geçici makinenin program kurabilmesi ve AWS servisleriyle konuşabilmesi için bir kimliğe ihtiyacı vardır. AWS bu seçenekte gereken IAM rollerini bizim yerimize otomatik oluşturur ve tanımlar.
- İsteğe bağlı olarak alt kısımdaki ayarlardan geçici makinenin boyutu (Instance type), çalışacağı ağ (VPC) veya tabi olacağı ağ güvenlik kuralları (Security groups) manuel belirlenebilir.

### Adım 5: Distribution settings

Testler başarılı olup imaj üretildikten sonra yeni kalıbın nereye gideceği, yani dağıtım kuralları bu ekranda belirlenir.

- **Region settings:** Varsayılan (service defaults) ayarlar kullanıldığı için üretilen AMI sadece o an işlem yapılan bölgeye (ekranda `us-east-1`) kaydedilir.
- İsteğe bağlı olarak kapsamlı bir projede gelişmiş ayarlarla AWS'ye "Ürettiğin imajı otomatik olarak Avrupa (Frankfurt) bölgesine de kopyala ve diğer ekiplerin kullandığı şu AWS hesaplarıyla da paylaş" denebilir.
