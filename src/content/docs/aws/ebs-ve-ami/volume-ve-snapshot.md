---
title: Volume ve snapshot
description: EC2 konsolunda EBS volume oluşturma, değiştirme, makineye bağlama ve snapshot alıp ondan imaj üretme adımları.
module: aws
lessons: [26]
order: 23
---

## Volume oluşturma

Elastic Block Store servisine EC2 altından ulaşılır: **EC2 → Elastic Block Store → Volumes → Create volume**. **Volume settings** bölümündeki alanlar:

| Alan | Açıklama |
|---|---|
| **Volume type** | İhtiyaca ve bütçeye en uygun disk teknolojisi, yani performans katmanı seçilir. Örnekte genel amaçlı işlemler için iyi bir fiyat/performans dengesi sunan `General Purpose SSD (gp3)` kullanılıyor. Tipler için bkz. [EBS disk türleri](/aws/ebs-ve-ami/disk-turleri/). |
| **Size (GiB)** | Diskin toplam kapasitesi gigabayt cinsinden belirlenir (örnekte `100`). Kurulacak işletim sisteminin veya barındırılacak verilerin büyüklüğüne göre girilir. |
| **IOPS** | Diskin saniyede yapabileceği maksimum okuma/yazma işlemi sayısıdır (örnekte `3000`). Yüksek trafikli uygulamalar veya veritabanları gibi yoğun işlemlerde artırılabilir. |
| **Throughput (MiB/s)** | Saniyede disk üzerinden aktarılabilecek veri miktarıdır (örnekte `125`). Büyük dosyalarla veya hacimli veri analizleriyle çalışırken aktarım hızını doğrudan etkiler. |
| **Availability Zone** | Diskin hangi fiziksel veri merkezinde oluşturulacağı seçilir. Mimari açıdan en kritik adımdır. |
| **Snapshot ID** | Daha önce alınmış bir yedekten başlatmak için kullanılır. Sıfırdan boş bir disk isteniyorsa `Don't create volume from a snapshot` seçili bırakılır. |
| **Encryption** | Disk içindeki verilerin AWS tarafından otomatik şifrelenip şifrelenmeyeceği seçilir (`Encrypt this volume`). Hassas veriler tutulacaksa yetkisiz erişim ve veri sızıntılarına karşı güçlü bir önlemdir. |

:::caution
Diski EC2 makinesine bağlayabilmek için diskin makineyle **aynı Availability Zone** içinde olması gerekir.
:::

## Volume'ü değiştirme ve makineye bağlama

- Oluşturulan volume'ün özellikleri **Actions → Modify volume** ile değiştirilebilir.
- Actions menüsündeki en önemli işlem **Attach volume**'dür. Açılan ekranda **Instance** listesinden diskin kullanılacağı makine ve **Device name** seçilip `Attach volume` butonuna tıklanır.

## Snapshot

**Snapshot**, diskin mevcut halinin anlık görüntüsünü çekerek yedeğini alma işlemidir. Snapshot'tan daha sonra yeni bir **Volume** veya **AMI** oluşturabiliriz; yani bu yedekten sıfır bir sanal makine veya disk türetebiliriz.

1. **Volumes** listesinde ilgili diski seçin, **Actions → Create snapshot** deyin.
2. Sol taraftaki **Elastic Block Store** menüsünden **Snapshots** başlığına gelin ve oluşturduğunuz yedeği seçin.
3. **Actions → Create image from snapshot** seçeneğine tıklayın (aynı menüde `Create volume from snapshot` da bulunur).

:::danger
Snapshot alırken en kritik nokta, o esnada diske yeni veri yazılmıyor olmasıdır. Veri kaybı veya dosya bozulması yaşamamak için işlem öncesinde ya sanal makineyi kapatın ya da diski **Detach** ederek makineden güvenle ayırın.
:::

Snapshot'tan AMI oluşturup bununla makine başlatma adımları [AMI ve Image Builder](/aws/ebs-ve-ami/ami-ve-image-builder/) sayfasında.
