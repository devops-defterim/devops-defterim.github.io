---
title: Disk yönetimi
description: EC2'ye yeni EBS volume ekleme, lsblk ve fdisk ile disk ve partition işlemleri, mkfs ile formatlama, mount ve df -hT ile kontrol.
module: linux
lessons: [8]
order: 17
---

Bir EC2 makinesine yeni bir disk takıp Linux tarafında kullanılabilir hale getirmenin akışı şöyledir: diski oluştur ve makineye bağla, sistemin diski gördüğünü kontrol et, partition oluştur, formatla, bir klasöre mount et.

EBS volume ve snapshot konusu AWS tarafında [Volume ve snapshot](/aws/ebs-ve-ami/volume-ve-snapshot/) sayfasında ayrıca anlatılıyor.

## Yeni disk oluşturma (AWS Console)

1. **EC2** menüsünde **Elastic Block Store → Volumes** seçeneğine tıklanır.
2. Açılan ekranda sağ üstteki `Create volume` butonuna tıklanır.
3. Diskin özellikleri belirlenir. Ekranda görülen alanlar: `Size (GiB)`, `IOPS` (3000), `Throughput (MiB/s)` (125), `Availability Zone` (örnekte `us-east-1a`), `Snapshot ID - optional` (`Don't create volume from a snapshot`), `Encryption` ve `Tags - optional`.
4. Sağ alttaki `Create volume` butonuna tıklanarak disk oluşturulur. Örnekte 10 GiB'lık bir `gp3` volume oluştu.

## Diski makineye bağlama

1. Volumes listesinde oluşturulan disk seçilir.
2. **Actions → Attach volume** seçeneğine tıklanır.
3. Açılan ekranda `Instance` alanından diskin bağlanacağı makine seçilir.
4. `Attach volume` butonuna tıklanır.

:::note
Attach volume ekranındaki `Instance` listesinde yalnızca volume ile aynı Availability Zone'daki instance'lar görünür (ekrandaki açıklama: *Only instances in the same Availability Zone as the selected volume are displayed*).
:::

Disk artık sanal makineye bağlıdır, ancak üzerine henüz veri yazılamaz; çünkü üzerinde bir partition (bölümlendirme) yapısı yoktur. Partition, disk üzerinde verilerin yazılacağı alanın sınırlarını çizer: veriyi yazmaya hangi byte'tan başlanacağı, nerede bitirileceği ve bu alanın ne kadarının kullanılabileceği tanımlanır.

## Diskin görüldüğünü kontrol etme

### lsblk

Diski bölümlere ayırmadan önce sistemin yeni donanımı tanıyıp tanımadığı kontrol edilir. `lsblk` (List Block Devices) komutu HDD, SSD ve NVMe sürücüler gibi veriyi bloklar halinde işleyen tüm blok cihazlarını hiyerarşik bir yapıda listeler. Böylece sistemde kaç disk takılı olduğu, adları (sdb, sdc gibi) ve kapasiteleri görülür.

```bash frame="terminal"
lsblk
```

```text title="Çıktı"
NAME      MAJ:MIN RM SIZE RO TYPE MOUNTPOINTS
xvda      202:0    0   8G  0 disk
├─xvda1   202:1    0   8G  0 part /
├─xvda127 259:0    0   1M  0 part
└─xvda128 259:1    0  10M  0 part
xvdf      202:80   0  10G  0 disk
```

Yeni takılan 10 GB'lık disk `xvdf` olarak görünüyor ve üzerinde henüz partition yok.

### df -h

`df -h` yalnızca işletim sistemine bağlanmış (mount edilmiş) ve veri yazmaya hazır alanların doluluk oranlarını raporlar. Bu yüzden diski bölümlendirip bağladıktan sonra, son aşamada kullanılır. Henüz mount edilmemiş `xvdf` bu listede yer almaz:

```bash frame="terminal"
df -h
```

```text title="Çıktı"
Filesystem      Size  Used Avail Use% Mounted on
devtmpfs        4.0M     0  4.0M   0% /dev
tmpfs           475M     0  475M   0% /dev/shm
tmpfs           190M  2.8M  188M   2% /run
/dev/xvda1      8.0G  3.1G  4.9G  40% /
tmpfs           475M     0  475M   0% /tmp
tmpfs            95M     0   95M   0% /run/user/1000
```

### fdisk -l

Makinedeki disklerin ve oluşturulmuş partition'ların listesi:

```bash frame="terminal"
sudo fdisk -l
```

```text title="Çıktı"
Disk /dev/xvda: 8 GiB, 8589934592 bytes, 16777216 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: EA7CC522-38EA-41D1-AC32-5AB64479781E

Device          Start      End  Sectors Size Type
/dev/xvda1      24576 16777182 16752607   8G Linux filesystem
/dev/xvda127    22528    24575     2048   1M BIOS boot
/dev/xvda128     2048    22527    20480  10M EFI System

Partition table entries are not in disk order.


Disk /dev/xvdf: 10 GiB, 10737418240 bytes, 20971520 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

## Partition oluşturma (fdisk)

Bir disk üzerinde işlem yapmak için `fdisk` diskin yoluyla açılır, ardından gelen istemde yapılacak işlem yazılır:

```bash frame="terminal"
sudo fdisk /dev/xvdf
```

```text title="Çıktı"
Welcome to fdisk (util-linux 2.37.4).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0xaca3cf77.

Command (m for help):
```

Adımlar:

1. `n` yazılarak yeni bir partition oluşturulmak istendiği belirtilir.
2. Partition'ın `p` (primary) mi `e` (extended) mi olacağı seçilir.
3. Partition numarası verilir.
4. Partition'ın diskte hangi sektörde başlayıp nerede biteceği yazılır. Örnekte ilk sektör varsayılan bırakıldı, son sektör için `+2GB` girildi.
5. `w` ile değişiklikler kaydedilir, `q` (quit) ile çıkılır.

Örnek oturum:

```text title="fdisk oturumu"
Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1):
First sector (2048-20971519, default 2048):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-20971519, default 20971519): +2GB

Created a new partition 1 of type 'Linux' and of size 1.9 GiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

## Formatlama: dosya sistemi oluşturma

Oluşturulan partition'ı, kaba inşaatı bitmiş bir evin odalara bölünmesi gibi düşünebiliriz. Bu haliyle odalar henüz kullanıma hazır değildir; hangisinin mutfak, hangisinin yatak odası olacağını belirlemek ve içine eşyaları yerleştirmek gerekir. Aynı şekilde bir partition'a veri yazabilmek için ona hangi dosya sistemini kullanacağını söylemek, yani onu formatlamak gerekir.

Dosya sistemi, verilerin disk üzerinde hangi koordinatlarda duracağına, nasıl isimlendirileceğine ve nereye yazılacağına dair hiyerarşik tabloyu oluşturan yapıdır. Bu tablo sayesinde işletim sistemi aranan bir veriyi diskteki milyonlarca byte arasından saniyeler içinde bulup getirebilir.

Komut iskeleti:

```bash frame="terminal"
sudo mkfs -t <dosya_sistemi_adi> <partition_yolu>
```

Örnekte partition `ext4` ile formatlandı:

```bash frame="terminal"
sudo mkfs -t ext4 /dev/xvdf1
```

```text title="Çıktı"
mke2fs 1.46.5 (30-Dec-2021)
Creating filesystem with 488192 4k blocks and 122160 inodes
Filesystem UUID: c638c958-be7b-423b-9aca-01c45939dc31
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912

Allocating group tables: done
Writing inode tables: done
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done
```

Bu işlemle disk veri kabul etmeye hazır hale gelir.

## Mount

Diski kullanabilmek için Linux'ta **mount** işlemi yapılır. Mount ile formatlanan disk bölümü sistemdeki boş bir klasöre bağlanır ve disk kullanılabilir hale gelir.

Komut iskeleti:

```bash frame="terminal"
sudo mount -t auto <kullanilacak_cihaz> <baglanacak_klasor>
```

Örnek:

```bash frame="terminal"
sudo mount -t auto /dev/xvdf1 /ornek/x1
```

Bu komut `/dev/xvdf1` cihazını `/ornek` altındaki `x1` klasörüne bağlar. Bundan sonra `x1` klasörüne ne yazılırsa `/dev/xvdf1` partition'ına yazılmış olur.

## df -hT ile kontrol

`df -hT` sistemdeki disk bölümlerinin doluluk oranlarını dosya sistemi tipiyle birlikte listeler:

```bash frame="terminal"
df -hT
```

```text title="Çıktı"
Filesystem     Type      Size  Used Avail Use% Mounted on
devtmpfs       devtmpfs  4.0M     0  4.0M   0% /dev
tmpfs          tmpfs     475M     0  475M   0% /dev/shm
tmpfs          tmpfs     190M  2.8M  188M   2% /run
/dev/xvda1     xfs       8.0G  3.1G  4.9G  40% /
tmpfs          tmpfs     475M     0  475M   0% /tmp
tmpfs          tmpfs      95M     0   95M   0% /run/user/1000
/dev/xvdf1     ext4      1.8G   24K  1.7G   1% /ornek/x1
```

- `-h`: değerleri GB/MB gibi okunabilir biçimde gösterir.
- `-T`: her bölümün dosya sistemi tipini gösterir.

Yeni partition `/dev/xvdf1`, `ext4` dosya sistemiyle `/ornek/x1` klasörüne bağlanmış görünüyor.
