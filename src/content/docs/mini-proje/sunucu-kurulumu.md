---
title: Sunucu kurulumu
description: Mini projede sistemi güncelleme, Git ve httpd kurulumu, kullanıcı ekleme, network interface ve route tanımlama adımları.
module: mini-proje
lessons: [14]
order: 3
---

SSH ile bağlanılan sunucu üzerinde 3-9 numaralı görevlerin çözümleri. Görevlerin tam listesi için [Görevler](/mini-proje/gorevler/) sayfasına bakın.

## Görev 3: Sistemi güncelleme

> 3-) Sistemi ve sistemde yüklü paketleri güncelleyin.

```bash frame="terminal"
sudo dnf update -y
```

```text title="Çıktı"
Amazon Linux 2023 Kernel Livepatch repository                  242 kB/s |  31 kB     00:00
=============================================================================================
WARNING:
  A newer release of "Amazon Linux" is available.

  Available Versions:

  Version 2023.10.20260202:
    Run the following command to upgrade to 2023.10.20260202:

      dnf upgrade --releasever=2023.10.20260202

    Release notes:
     https://docs.aws.amazon.com/linux/al2023/release-notes/relnotes-2023.10.20260202.html

=============================================================================================
Dependencies resolved.
Nothing to do.
Complete!
```

`dnf` ile ilgili ayrıntılar için [Paket yönetimi](/linux/paket-yonetimi/) sayfasına bakabilirsiniz.

## Görev 4: Git kurulumu

> 4-) Git uygulamasını yükleyin.

```bash frame="terminal"
sudo dnf install git -y
```

```text title="Çıktı"
Last metadata expiration check: 0:03:36 ago on Fri Feb  6 12:11:35 2026.
Dependencies resolved.
=============================================================================================
 Package               Architecture     Version                       Repository        Size
=============================================================================================
Installing:
 git                   x86_64           2.50.1-1.amzn2023.0.1         amazonlinux       53 k
Installing dependencies:
 git-core              x86_64           2.50.1-1.amzn2023.0.1         amazonlinux      4.9 M
 git-core-doc          noarch           2.50.1-1.amzn2023.0.1         amazonlinux      2.8 M
 perl-Error            noarch           1:0.17029-5.amzn2023.0.2      amazonlinux       41 k
 perl-File-Find        noarch           1.37-477.amzn2023.0.7         amazonlinux       25 k
 perl-Git              noarch           2.50.1-1.amzn2023.0.1         amazonlinux       41 k
 perl-TermReadKey      x86_64           2.38-9.amzn2023.0.2           amazonlinux       36 k
 perl-lib              x86_64           0.65-477.amzn2023.0.7         amazonlinux       15 k

Transaction Summary
=============================================================================================
Install  8 Packages

Total download size: 7.9 M
Installed size: 41 M
Downloading Packages:
...
```

Kurulumun ardından `git --version` ile sürüm kontrol edilir. Ekran görüntüsünde aynı kontrol `git version` olarak çalıştırılmıştır:

```bash frame="terminal"
git version
```

```text title="Çıktı"
git version 2.50.1
```

## Görev 5: Yeni kullanıcı ve sudo yetkisi

> 5-) Yeni bir kullanıcı ekleyin. Bu kullanıcının şifre sormadan sudo yapabilmesini sağlayın.

Adımlar:

1. `sudo useradd kullanıcı_adı` ile kullanıcı oluşturulur.
2. `sudo passwd kullanıcı_adı` ile şifre belirlenir. Şifre girilir ve onay için tekrar girilir.
3. `sudo usermod -a -G wheel kullanıcı_adı` ile kullanıcı, sistemdeki en yetkili gruplardan biri olan ve yönetici (root) yetkilerine erişim sağlayan `wheel` grubuna ikincil grup olarak eklenir.

Örnekte kullanıcı adı `proje`:

```bash frame="terminal"
sudo useradd proje
sudo passwd proje
```

```text title="Çıktı"
Changing password for user proje.
New password:
Retype new password:
passwd: all authentication tokens updated successfully.
```

```bash frame="terminal"
sudo usermod -a -G wheel proje
su proje
groups proje
```

```text title="Çıktı"
Password:
proje : proje wheel
```

Kullanıcı ve grup komutlarının ayrıntısı için [Kullanıcı ve grup yönetimi](/linux/kullanici-ve-grup/) sayfasına bakabilirsiniz.

## Görev 6: /evim klasörü ve home directory

> 6-) Root'da /evim diye bir klasör oluşturun. Bu klasörün owner ve grup değerlerini bu yeni oluşturduğunuz kullanıcı ve bu kullanıcının ana grubu olarak değiştirin. Ardından bu kullanıcının home directory'sinin /evim klasörü olmasını sağlayacak işlemi yapın.

1. `sudo mkdir /evim` ile root dizininde klasör oluşturulur.
2. `sudo chown proje /evim` ile klasörün sahibi (owner) yeni kullanıcı yapılır.
3. `sudo chgrp proje /evim` ile grup değeri kullanıcının ana grubuna atanır. Böylece klasör üzerindeki mülkiyet hakları root kullanıcısından alınıp yeni kullanıcıya ve grubuna aktarılır.
4. `sudo usermod -d /evim proje` ile kullanıcının home directory değeri bu klasörle eşleştirilir.

```bash frame="terminal"
sudo mkdir /evim
sudo chown proje /evim
sudo chgrp proje /evim
cat /etc/passwd
```

```text title="Çıktı"
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
...
ec2-user:x:1000:1000:EC2 Default User:/home/ec2-user:/bin/bash
proje:x:1001:1001::/home/proje:/bin/bash
```

```bash frame="terminal"
sudo usermod -d /evim proje
cat /etc/passwd
```

```text title="Çıktı"
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
...
ec2-user:x:1000:1000:EC2 Default User:/home/ec2-user:/bin/bash
proje:x:1001:1001::/evim:/bin/bash
```

`/etc/passwd` dosyasında `proje` kullanıcısının home directory değeri `/home/proje` yerine `/evim` olmuştur. Kullanıcıya geçip kontrol edilir:

```bash frame="terminal"
su proje
cd ~
pwd
```

```text title="Çıktı"
Password:
/evim
```

Sahiplik ve izinler için [Dosya izinleri](/linux/izinler/) sayfasına bakabilirsiniz.

## Görev 7: Network interface ekleme

> 7-) AWS üstünden yeni bir network interface ekleyin ve bunu makinenize attach edin. Sonra bu interface'e 10.10.10.10/255.255.255.0 ip adresini ekleyin.

### Interface oluşturma

1. EC2 konsolunda soldaki menüden **Network & Security → Network Interfaces** seçeneğine tıklayın.
2. Sağ üstteki `Create network interface` butonuna tıklayın.
3. **Create network interface** ekranında gerekli alanları doldurun:
   - **Description**: açıklayıcı bir isim (örnekte `miniprojem`)
   - **Subnet**: instance ile aynı subnet (örnekte instance'ın bulunduğu `us-east-1c` subnet'i)
   - **Interface type**: `ENA`
   - **Private IPv4 address**: `Auto-assign`
   - **Security groups**: instance oluşturulurken açılan security group (örnekte `launch-wizard-3`)
4. Sayfanın altındaki `Create network interface` butonuyla işlemi tamamlayın.

### Instance'a bağlama

1. Oluşturulan network interface'i listede seçin.
2. **Actions → Attach** diyerek instance'a bağlayın.

### IP adresini ekleme

AWS arayüzündeki işlemlerden sonra terminale dönülerek IP adresi eklenir:

```bash frame="terminal"
sudo ip address add 10.10.10.10/255.255.255.0 dev ens5
```

`ip` komutları için [Network](/linux/network/) sayfasına bakabilirsiniz.

## Görev 8: Route tanımı

> 8-) 199.199.199.0/24 adreslerine giderken bu yeni interface üstünden gitmesini sağlayacak route tanımı yapın.

```bash frame="terminal"
sudo ip route add 199.199.199.0/24 dev ens5
```

## Görev 9: Apache Web Server (httpd)

> 9-) Apache Web Server (httpd) servisini sisteme yükleyin. Bilgisayar yeniden başlatıldığında bu servisin de otomatik olarak çalışmasını sağlayacak ayarı da yapın.

### Kurulum

```bash frame="terminal"
sudo dnf install -y httpd
```

```text title="Çıktı"
Last metadata expiration check: 0:52:01 ago on Fri Feb  6 12:11:35 2026.
Dependencies resolved.
=============================================================================================
 Package                 Architecture   Version                     Repository        Size
=============================================================================================
Installing:
 httpd                   x86_64         2.4.66-1.amzn2023.0.1       amazonlinux       47 k
Installing dependencies:
 apr                     x86_64         1.7.5-1.amzn2023.0.4        amazonlinux      129 k
 apr-util                x86_64         1.6.3-1.amzn2023.0.2        amazonlinux       97 k
 apr-util-lmdb           x86_64         1.6.3-1.amzn2023.0.2        amazonlinux       13 k
 generic-logos-httpd     noarch         18.0.0-12.amzn2023.0.3      amazonlinux       19 k
 httpd-core              x86_64         2.4.66-1.amzn2023.0.1       amazonlinux      1.4 M
 httpd-filesystem        noarch         2.4.66-1.amzn2023.0.1       amazonlinux       13 k
 httpd-tools             x86_64         2.4.66-1.amzn2023.0.1       amazonlinux       81 k
 libbrotli               x86_64         1.0.9-4.amzn2023.0.2        amazonlinux      315 k
 mailcap                 noarch         2.1.49-3.amzn2023.0.3       amazonlinux       33 k
Installing weak dependencies:
 apr-util-openssl        x86_64         1.6.3-1.amzn2023.0.2        amazonlinux       15 k
 mod_http2               x86_64         2.0.27-1.amzn2023.0.3       amazonlinux      166 k
 mod_lua                 x86_64         2.4.66-1.amzn2023.0.1       amazonlinux       60 k

Transaction Summary
=============================================================================================
Install  13 Packages
```

### Servisi etkinleştirme ve başlatma

- `sudo systemctl status httpd.service`: servisin o anki durumunu gösterir.
- `sudo systemctl enable httpd.service`: bilgisayar yeniden açıldığında servisin otomatik çalışmasını sağlar.
- `sudo systemctl start httpd.service`: web sunucusunu çalıştırır.
- Son olarak tekrar `sudo systemctl status httpd.service` ile servisin çalıştığı kontrol edilir.

```bash frame="terminal"
sudo systemctl status httpd.service
```

```text title="Çıktı"
○ httpd.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; preset: disabled)
     Active: inactive (dead)
       Docs: man:httpd.service(8)
```

```bash frame="terminal"
sudo systemctl enable httpd.service
```

```text title="Çıktı"
Created symlink /etc/systemd/system/multi-user.target.wants/httpd.service → /usr/lib/systemd/system/httpd.service.
```

```bash frame="terminal"
sudo systemctl start httpd.service
sudo systemctl status httpd.service
```

```text title="Çıktı"
● httpd.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; preset: disabled)
     Active: active (running) since Fri 2026-02-06 13:05:13 UTC; 6s ago
       Docs: man:httpd.service(8)
   Main PID: 3820 (httpd)
     Status: "Started, listening on: port 80"
      Tasks: 177 (limit: 1067)
     Memory: 13.3M
        CPU: 63ms
     CGroup: /system.slice/httpd.service
             ├─3820 /usr/sbin/httpd -DFOREGROUND
             ├─3821 /usr/sbin/httpd -DFOREGROUND
             ├─3822 /usr/sbin/httpd -DFOREGROUND
             ├─3823 /usr/sbin/httpd -DFOREGROUND
             └─3824 /usr/sbin/httpd -DFOREGROUND

Feb 06 13:05:13 ip-172-31-0-10.ec2.internal systemd[1]: Starting httpd.service - The Apache HTTP Server...
Feb 06 13:05:13 ip-172-31-0-10.ec2.internal systemd[1]: Started httpd.service - The Apache HTTP Server.
Feb 06 13:05:13 ip-172-31-0-10.ec2.internal httpd[3820]: Server configured, listening on: port 80
```

`systemctl` ile servis yönetimi için [systemd ve boot](/linux/systemd-ve-boot/) sayfasına bakabilirsiniz.

### Yerel test

```bash frame="terminal"
curl 127.0.0.1
```

```text title="Çıktı"
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>It works! Apache httpd</title>
</head>
<body>
<p>It works!</p>
</body>
</html>
```

`curl 127.0.0.1`, sunucu dış dünyaya açılmadan önce kendi üzerindeki web servisine bir istek gönderir ve sistemin doğru çalışıp çalışmadığını kontrol etmeyi sağlar. `127.0.0.1`, her bilgisayarın kendisini ifade eden özel localhost adresidir; `curl` ise bu adresteki web içeriğini terminale metin olarak döker.
