---
title: Instance oluşturma
description: EC2 konsolunda isim ve tag, AMI, instance type, key pair, disk, ağ, Advanced details ve user data ile sanal makine oluşturma.
module: aws
lessons: [25]
order: 18
---

Sol menüdeki **Instances** başlığına gidip açılan ekrandaki `Launch instances` butonuna tıklayarak sanal makine oluşturmaya başlıyoruz. Ekranın sağındaki **Summary** paneli seçilen özelliklerin özetini gösterir.

## 1. Name and tags

EC2 oluşturmanın ilk adımı makineye bir isim vermektir. Burada S3'teki isimlendirmeden farklı olarak özel bir isim vermiyoruz; aslında `Name` anahtarlı bir **tag** oluşturmuş oluyoruz. Bunun sebebi, buraya yazdığımız isim üzerinden makineyle herhangi bir etkileşim kuramamamızdır.

- İsteğe bağlı olarak ilave tag eklenebilir. İsim kutucuğunun yanındaki `Add additional tags` yazısına tıklayıp açılan ekranda istenen **Key** ve **Value** girilir (ör. Key: `ortam`, Value: `test`).
- Bu tag'in makineye bağlanan diğer nesnelere de eklenmesi isteniyorsa **Resource types** listesinden seçilir (ör. `Instances`, `Volumes`, `Spot instance requests`, `Network interfaces`).
- Sağdaki **Number of instances** alanına bu özelliklerde kaç sanal makine oluşturulacağı yazılır.

## 2. Application and OS Images (AMI)

Bulut soyut bir kavram gibi görünse de EC2'de oluşturduğumuz her sanal makine aslında AWS veri merkezlerindeki fiziksel bir sunucu üzerinde çalışır. Oluştur butonuna bastığınız anda AWS makine parkını tarar, boş kapasitesi olan uygun bir donanımı bulur ve sanal makinenizi bu fiziksel sunucunun üzerinde ayağa kaldırır.

Bu donanımda hangi işletim sisteminin kurulacağını ve başlangıçta hangi programların yer alacağını **Application and OS Images**, yani **AMI (Amazon Machine Image)** belirler. AMI'yi sanal makinenin altyapısını oluşturan bir **ana şablon** olarak düşünebilirsiniz.

- AWS başlangıç için içinde sadece işletim sistemi (Linux, Windows vb.) bulunan hazır şablonlar sunar.
- Asıl avantaj kendi özel imajımızı yaratabilmemizdir. Standart bir sanal makine açıp projeniz için gereken yazılımları kurduğunuzu, güncellemeleri tamamladığınızı ve sistemi istediğiniz yapılandırmaya getirdiğinizi düşünün. Ardından makineyi durdurup o anki halinin bir kopyasını alırsınız; artık size özel bir AMI'niz olur.
- İleride yeni bir makineye ihtiyaç olduğunda kurulum adımlarını sıfırdan yapmazsınız. Kendi imajınızı seçersiniz ve AWS bir fotokopi makinesi gibi tüm özelliklerle donatılmış yeni sanal makineyi saniyeler içinde klonlar.
- `Browse more AMIs` butonuyla hazır AMI'lere veya kendi oluşturduğumuz AMI'lere (**My AMIs** sekmesi) ulaşılır.

Biz şimdilik **Amazon Linux** (Amazon Linux 2023) işletim sistemini seçerek devam ediyoruz. Kendi AMI'mizi oluşturma adımları [AMI ve Image Builder](/aws/ebs-ve-ami/ami-ve-image-builder/) sayfasında.

## 3. Instance type

**Instance type** kısmından ihtiyacımıza göre sanal makine tipini seçiyoruz (örnekte `t3.micro`). Tiplerin anlamı için [Makine aileleri ve isimlendirme](/aws/ec2/makine-aileleri/) sayfasına bakabilirsiniz.

## 4. Key pair (login)

Sanal makinelere klasik kullanıcı adı ve parolayla bağlanmak yerine, parola çalınma riskini ortadan kaldıran daha güvenli bir yöntem olan **Key Pair** yapısını kullanırız.

1. **Key pair (login)** bölümünde `Create new key pair` yazan yere tıklayın.
2. Açılan **Create key pair** penceresinde key pair için bir isim girin (ör. `ornek-key`).
3. **Key pair type** olarak `RSA`, **Private key file format** olarak `.pem` (OpenSSH ile kullanım için) seçin.
4. `Create key pair` butonuna tıklayın. Private key dosyası bilgisayarınıza iner.

:::caution
Konsolun uyarısında da belirtildiği gibi, indirilen private key dosyasını güvenli ve erişilebilir bir yerde saklayın; makineye bağlanmak için daha sonra bu dosyaya ihtiyacınız olacak.
:::

## 5. Network settings

**Network settings** başlığında sanal makinemize dış dünyadan herkesin erişebilmesi için şu seçimleri yapıyoruz:

- **Auto-assign public IP:** `Enable`
- **Firewall (security groups):** `Create security group`
- `Allow SSH traffic from` işaretli, kaynak `Anywhere 0.0.0.0/0`
- `Allow HTTPS traffic from the internet` işaretli
- `Allow HTTP traffic from the internet` işaretli

Buradaki ayarların ne anlama geldiği network konusunda ayrıntılı olarak işleniyor.

## 6. Configure storage

Hangi tipte ve kaç GB disk oluşturmak istediğimizi **Configure storage** başlığında belirliyoruz (örnekte `8 GiB`, `gp3`). Sanal makinenin işletim sistemi bu diske kurulur. Disk tipleri [EBS disk türleri](/aws/ebs-ve-ami/disk-turleri/) sayfasında anlatılıyor.

## 7. Advanced details

Son olarak **Advanced details** başlığındaki ayarları varsayılan bırakıyoruz (Metadata ve User data hariç, aşağıya bakın). Alanların anlamları:

| Ayar | Açıklama |
|---|---|
| **Domain join directory** | Kurumsal ağlarda kullanılan Microsoft Active Directory yapısına sanal makineyi otomatik dahil eder. Böylece şirketin mevcut kullanıcı hesapları ve yetkilendirme kurallarıyla sunucuya giriş yapılabilir. |
| **IAM instance profile** | Sanal makineye AWS ekosistemi içinde bir "kimlik kartı" atanan kısımdır. Bu profil sayesinde sunucu, diğer AWS servislerine (ör. S3'ten dosya okumak veya veritabanına yazmak) manuel parola girmeden güvenli şekilde erişim izni kazanır. |
| **Hostname type & DNS Hostname** | Makinenin iç ağdaki adını ve bu adın IP adresleriyle nasıl eşleşeceğini belirler. Sunucuyla karmaşık IP numaraları yerine anlaşılır isimlerle iletişim kurmayı sağlar. |
| **Instance auto-recovery** | Donanımsal bir arızada AWS'nin sanal makineyi otomatik olarak başka bir sağlıklı fiziksel donanıma taşıyıp yeniden başlatmasını sağlar. |
| **Shutdown behavior** | Makinenin içinden kapatma komutu verildiğinde makinenin sadece durdurulmasını (Stop) veya tamamen silinmesini seçtiğiniz ayardır. Yanlışlıkla veri kaybetmemek için genellikle varsayılan `Stop` bırakılır. |
| **Stop - Hibernate behavior** | Makine durdurulduğunda RAM'deki anlık verilerin diske kaydedilmesini sağlar. Makine tekrar açıldığında uygulamalar sıfırdan başlamak yerine kaldığı yerden daha hızlı devam eder. |
| **Termination protection** | Sunucunun dalgınlıkla veya yanlış bir tıklamayla kazara silinmesini engeller. Kritik iş yükü barındıran makinelerde mutlaka açılmalıdır. |
| **Stop protection** | Sunucunun kazara `Stop` konumuna getirilmesini engeller. Sürekli çalışması gereken canlı ortam makineleri için tercih edilir. |
| **Detailed CloudWatch monitoring** | Standart 5 dakikalık metrik ölçümlerini 1 dakikalık aralıklara indirir. Ek ücret karşılığında açılabilir. |
| **Credit specification** | T serisi makinelerin işlemci kapasitesi dolduğunda ekstra performans sergilemeye devam edip etmeyeceğini belirler. `Unlimited` seçilirse makine darboğaza girmez ama aşılan limit kadar faturaya ek ücret yansır. |
| **Placement group** | Birden fazla makine kuruluyorsa bunların veri merkezinde fiziksel olarak nasıl konumlanacağını belirler. Ağ hızı için birbirine çok yakın, donanım arızası riskini dağıtmak için farklı donanımlara yerleştirilebilir. |
| **EBS-optimized instance** | Makine ile bağlı disk arasında özel ve ayrılmış bir veri yolu tahsis eder; yoğun disk işlemlerinde performansı garanti altına alır. |
| **Instance bandwidth configuration** | Makinenin ağ trafiği için özel bir bant genişliği limiti veya garantisi belirler; yüksek veri transferi gereken uygulamalarda ağ darboğazlarını önler. |
| **Purchasing option** | Makinenin hangi fiyatlandırma modeliyle alınacağı seçilir. Borsa mantığındaki `Spot instances` buradan talep edilebilir; hiçbiri seçilmezse (`None`) standart kullandığın kadar öde modeliyle devam edilir. |
| **Capacity reservation** | Belirli bir bölge için önceden donanım kapasitesi ayırttıysanız makineyi o kapasitenin içine dahil eder. Böylece "uygun donanım kalmadı" hatası alma riski ortadan kalkar. |
| **Tenancy** | Makinenin diğer müşterilerle aynı fiziksel donanımı paylaşıp paylaşmayacağını belirler. Güvenlik veya lisans nedenleriyle donanımın size özel olması isteniyorsa `Dedicated` seçilir. |
| **RAM disk ID & Kernel ID** | İşletim sistemi çekirdeğini veya başlangıç RAM diskini manuel değiştirmeye olanak tanır. Güncel AMI'lerde bu ayarlar imajın içinde olduğundan, çok eski sistemlerle uyumluluk gereken özel senaryolar dışında boş bırakılır. |
| **Nitro Enclave** | Sunucunun içinde dış dünyadan ve hatta sunucu yöneticilerinden bile izole edilmiş ekstra güvenli bir "kasa" oluşturur. Sağlık verileri veya finansal şifreleme anahtarları gibi hassas bilgileri işleyen uygulamalar içindir. |
| **License configurations** | Şirkete ait mevcut Windows veya SQL Server gibi lisansları (BYOL, Bring Your Own License) bu makineyle ilişkilendirir. Böylece bulutta ek lisans ücretiyle karşılaşmadan mevcut haklar kullanılmaya devam edilir. |
| **CPU options** | Çekirdek sayısını veya işlemci iş parçacığı özelliklerini manuel olarak kısmaya (kapatmaya) olanak tanır. İşlemci çekirdeği sayısına göre ücretlendirilen pahalı yazılım lisanslarından tasarruf etmek için kullanılır. |
| **Nested virtualization** | Sanal makinenin içinde başka sanal makineler (ör. Hyper-V veya KVM) çalıştırmaya olanak tanır. Sanal laboratuvarlar için kullanışlıdır ama her makine tipinde desteklenmez. |
| **Metadata accessible & Metadata version** | Makinenin içinden IP adresi veya ID gibi bilgilere ulaşmasını sağlar; bunun için `Enabled` seçilmelidir. **Metadata version** alanını `V2 only (token required)` seçmek ekstra bir oturum anahtarı zorunluluğu getirerek sunucuyu olası güvenlik açıklarına karşı korur. |
| **Metadata response hop limit** | Makine içindeki metadata isteklerinin ağda en fazla kaç duraktan (router/hop) geçebileceğini belirler. Sunucuda Docker gibi konteyner yapıları çalışacaksa iletişimin kesilmemesi için bu sayı yükseltilmelidir (örnekte `2`). |
| **Allow tags in metadata** | Makineye atanan "Additional tags" verilerinin doğrudan makinenin içinden komut satırıyla okunabilmesini sağlar. |
| **User data** | Sanal makine ilk kez ayağa kalkarken arka planda otomatik çalıştırılmasını istediğiniz komutların yazıldığı alandır. Sunucu açılır açılmaz bir web servisi kurmak veya sistem güncellemelerini başlatmak için bash komutları buraya yapıştırılır; aynı işlemleri tekrar tekrar elle yapma zahmetinden kurtarır. |

Metadata servisinin kullanımı [Metadata servisi](/aws/ec2/metadata/) sayfasında.

### User data script'i

**User data - optional** başlığı altındaki alana aşağıdaki script'i yazıyoruz. Her komutun ne yaptığı yorum satırlarında yazıyor.

```bash title="user-data.sh"
#!/bin/bash
# Tüm sistem paketlerini güncelleyelim
dnf update -y
# Apache web sunucusunu kuralım
dnf install -y httpd
# Web sunucusunu başlatalım
systemctl start httpd
# Makine her yeniden başlatıldığında web sunucusu da otomatik başlasın
systemctl enable httpd
# Test edebilmemiz için basit bir web sayfası oluşturalım
echo "<h1>Merhaba! Ornek EC2 Sanal Makinesine Hos Geldiniz! Projeler hazirlaniyor...</h1>" > /var/www/html/index.html
```

`dnf` ve `systemctl` komutları Linux bölümündeki [Paket yönetimi](/linux/paket-yonetimi/) ve [systemd ve boot](/linux/systemd-ve-boot/) sayfalarında anlatılıyor.

## 8. Launch instance

Bu son ayarla birlikte `Launch instance` butonuna tıklayarak ilk sanal makinemizi oluşturuyoruz. Instances listesinde makine önce `Running` durumuna geçer, **Status check** sütunu bir süre `Initializing` görünür.
