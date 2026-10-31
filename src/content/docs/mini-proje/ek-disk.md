---
title: Ek disk
description: Mini projede 4 GiB EBS volume oluşturup instance'a bağlama, fdisk ile partition açma ve xfs ile formatlama.
module: mini-proje
lessons: [14, 15]
order: 4
---

Görevlerin tam listesi için [Görevler](/mini-proje/gorevler/) sayfasına bakın.

## Görev 10: EBS volume oluşturma ve formatlama

> 10-) 4gb boyutunda bir EBS Volume yaratın ve bunu oluşturduğunuz instance'a bağlayın. Bunun üzerinde tüm disk boyutunu kullanan tek bir partition yaratın ve xfs dosya sistemiyle formatlayın.

### Volume oluşturma

1. EC2 konsolunda soldaki menüden **Elastic Block Store → Volumes** seçeneğine tıklayın.
2. Açılan ekranda `Create volume` butonuna tıklayın.
3. **Create volume** ekranında volume boyutunu ve özelliklerini belirleyin:
   - **Volume type**: `General Purpose SSD (gp3)`
   - **Size (GiB)**: `4`
   - **IOPS**: `3000`
   - **Throughput (MiB/s)**: `125`
   - **Availability Zone**: instance ile aynı zone (örnekte `use1-az4 (us-east-1c)`)
   - **Snapshot ID**: `Don't create volume from a snapshot`
   - **Encryption**: `Encrypt this volume` işaretsiz
4. Sağ alttaki `Create volume` butonuyla volume'ü oluşturun. Listede 4 GiB'lık yeni volume görünür.

### Volume'ü instance'a bağlama

1. Oluşturulan volume'ü seçip **Attach volume** ekranını açın.
2. **Instance** alanında proje instance'ını seçin (örnekte `miniprojem (running)`). Yalnızca volume ile aynı Availability Zone'daki instance'lar listelenir.
3. **Device name** alanında `/dev/sdf` seçili kalsın.
4. `Attach volume` butonuna tıklayın.

:::note
Konsol bu ekranda, yeni Linux kernel'lerinin cihazları içeride `/dev/xvdf` ile `/dev/xvdp` arasında yeniden adlandırabileceğini belirtir; ekranda girilen ad `/dev/sdf` olsa bile. Örnekteki sunucuda disk `/dev/nvme1n1` olarak görünmüştür.
:::

### Partition oluşturma

Tüm disk boyutunu kullanan tek bir partition için `sudo fdisk cihaz_yolu` komutu kullanılır:

```bash frame="terminal"
sudo fdisk /dev/nvme1n1
```

fdisk içinde verilen yanıtlarla oturum şöyle ilerler (`d` mevcut partition'ı siler, `n` yeni partition oluşturur, `p` primary seçer, `1` partition numarasıdır, sektör sorularında Enter ile varsayılanlar kabul edilir, `w` değişiklikleri yazar):

```text title="fdisk oturumu"
Welcome to fdisk (util-linux 2.37.4).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Command (m for help): d
Selected partition 1
Partition 1 has been deleted.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-8388607, default 2048):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-8388607, default 8388607):

Created a new partition 1 of type 'Linux' and of size 4 GiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

### xfs ile formatlama

```bash frame="terminal"
sudo mkfs.xfs -f /dev/nvme1n1p1
```

```text title="Çıktı"
meta-data=/dev/nvme1n1p1         isize=512    agcount=8, agsize=131040 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=1    bigtime=1 inobtcount=1 nrext64=0
         =                       exchange=0
data     =                       bsize=4096   blocks=1048320, imaxpct=25
         =                       sunit=1      swidth=1 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1, parent=0
log      =internal log           bsize=4096   blocks=16384, version=2
         =                       sectsz=512   sunit=1 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
```

Disk, partition ve dosya sistemi kavramları için [Disk yönetimi](/linux/disk-yonetimi/) sayfasına bakabilirsiniz.
