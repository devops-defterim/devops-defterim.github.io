---
title: Konsol turu
description: EC2 konsolunda Dashboard, bölge seçimi, AWS Global View, Instances, Instance Types ve Launch Templates ekranlarının tanıtımı.
module: aws
lessons: [24]
order: 17
---

Teori kısmından sonra AWS konsolunda EC2 ekranlarını tanıyalım. Üstteki arama kutusuna `EC2` yazıp ilk sıradaki **EC2 (Virtual Servers in the Cloud)** seçeneğine tıklıyoruz.

## Dashboard

İlk açılan sayfa **Dashboard**'dur.

- **Resources:** Tüm sanal makineler, çalışmakta olan sanal makineler (`Instances (running)`), oluşturulan volume'ler, security group'lar, key pair'ler, snapshot'lar gibi EC2 kaynaklarıyla ilgili temel bilgilere buradan ulaşılır.
- **Service health:** Hemen altındaki bu bölümden, bölgelerle ilgili bir servis sorunu varsa görülebilir.
- **Launch instance:** Service health bölümünün solundaki `Launch instance` butonuyla yeni bir sanal makine oluşturulabilir.

## Bölge seçimi ve AWS Global View

- Farklı bölgelerde oluşturduğumuz sanal makineleri görmek için sağ üstteki bölge menüsünden ilgili bölgeyi (ör. Europe (Frankfurt) `eu-central-1`, Europe (Ireland) `eu-west-1`) seçeriz. Dashboard'daki bilgiler seçilen bölgeye göre değişir.
- Farklı bölgelerdeki tüm makineleri tek ekranda görmek için soldaki menüden **AWS Global View** seçeneğine tıklarız. Buradaki **Region explorer** tablosu, her bölgedeki instance, VPC, subnet, security group, volume gibi kaynak sayılarını listeler.

## Instances

En çok kullanacağımız menü **Instances** başlığıdır.

- **Instances** ekranında sanal makineler listelenir. Bir makineyi yanındaki kutucuktan seçince alt panelde (Details, Status and alarms, Monitoring, Security, Networking, Storage, Tags sekmeleri) makine hakkındaki tüm bilgilere ulaşılır: Instance ID, public/private IPv4 adresleri, public DNS, instance type, VPC ID, subnet ID, AMI ID vb.
- AWS üzerindeki her EC2 makinesinin benzersiz bir **Instance ID**'si vardır (ör. `i-0123456789abcdef0`).
- **Instance state** butonundan makineyi başlatma, durdurma gibi işlemler yapılır: `Stop instance`, `Start instance`, `Reboot instance`, `Hibernate instance`, `Terminate (delete) instance`.
- Hemen yanındaki **Actions** butonundan makinenin değiştirilmesi gereken özellikleri ayarlanır. Menü altında `Instance diagnostics`, `Instance settings`, `Networking`, `Security`, `Image and templates`, `Storage`, `Monitor and troubleshoot` grupları bulunur. Örneğin `Instance settings` altında `Change stop protection`, `Change termination protection`, `Change shutdown behavior`, `Change instance type`, `Edit user data`, `Manage tags` gibi seçenekler yer alır.

## Instance Types

**Instance Types** başlığında sanal makine tipleri listelenir. Tabloda her tipin vCPU, mimari, bellek, depolama, ağ performansı ve On-Demand saatlik fiyatları görülür. Bir tipi seçince alt panelde detaylarına (Details, Compute, Networking, Storage, Accelerators, Pricing) ulaşılır. Tip adlarının nasıl okunduğu [Makine aileleri ve isimlendirme](/aws/ec2/makine-aileleri/) sayfasında anlatılıyor.

## Launch Templates

Sürekli aynı özelliklere sahip sanal makineler oluşturmanız gerekiyorsa ve bu süreci hızlandıracak bir kısayol arıyorsanız, **Launch Templates** başlığı altındaki `Create launch template` butonuyla kendi şablonlarınızı hazırlayabilirsiniz. Adımlar [Launch template](/aws/ec2/launch-template/) sayfasında.
