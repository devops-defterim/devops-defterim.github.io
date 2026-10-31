---
title: Paket yönetimi
description: rpm ve deb paketleri, repository kavramı, yum ile paket arama, kurma, güncelleme ve sık kullanılan dnf komutları.
module: linux
lessons: [5]
order: 11
---

## rpm ve deb paketleri

Linux distro'larının iki temel çeşidi vardır ve bunları birbirinden ayıran şey uygulamalar için kullandıkları paketleme yöntemidir:

- **rpm:** Red Hat tabanlı sistemlerin paket formatı. İçinde bilgisayara yüklenecek uygulama dosyaları ve uygulamayla ilgili metadata bilgileri bulunur.
- **deb:** Debian tabanlı sistemlerin paket formatı.

## Repository ve package manager

Debian, Red Hat veya başka firmaların oluşturduğu uygulama repository'leri vardır. Bunları, sistemlerimizde kullandığımız uygulamaları indirebileceğimiz kataloglar gibi düşünebiliriz. Bu işlemi elle yapmayız; package manager'lar repository'lerle konuşarak uygulamaları sistemimize indirir.

| Sistem | Package manager |
|---|---|
| Fedora, Red Hat (rpm tabanlı) | `yum`, `dnf` |
| Ubuntu (deb tabanlı) | `apt`, `apt-get` |

Makinede konfigüre edilmiş repository'lerin bilgileri `/etc/yum.repos.d` dizinindeki dosyalarda bulunur.

## yum ile paket arama

`yum search uygulamaadı`, bağlı olunan repository'lerde istenen uygulamayı arar:

```bash frame="terminal"
yum search mysql
```

```text title="Çıktı"
Amazon Linux 2023 repository                        41 MB/s |  17 MB     00:00
Amazon Linux 2023 Kernel Livepatch repository      851 kB/s | 159 kB     00:00
===================== Name & Summary Matched: mysql =====================
apr-util-mysql.x86_64 : APR utility library MySQL DBD driver
bind-dlz-mysql.x86_64 : BIND server mysql and mysqldyn DLZ modules
collectd-mysql.x86_64 : MySQL plugin for collectd
dovecot-mysql.x86_64 : MySQL back end for dovecot
mysql-selinux.noarch : SELinux policy modules for MySQL and MariaDB packages
perl-DBD-MySQL.x86_64 : A MySQL interface for Perl
perl-DateTime-Format-MySQL.noarch : Parse and format MySQL dates and times
php8.1-mysqlnd.x86_64 : A module for PHP 8.1 applications that use MySQL databases
php8.2-mysqlnd.x86_64 : A module for PHP 8.2 applications that use MySQL databases
postfix-mysql.x86_64 : Postfix MySQL map support
========================= Summary Matched: mysql =========================
mariadb105-devel.x86_64 : Files for development of MariaDB/MySQL applications
mariadb105-server-utils.x86_64 : Non-essential server utilities for MariaDB/MySQL applications
perl-DBD-MariaDB.x86_64 : MariaDB and MySQL driver for the Perl5 Database Interface (DBI)
```

## yum ile paket kurma

`sudo yum install paketismi` ile bir paket sisteme kurulur. Komut önce onay ister, `y` ile onaylanınca indirme başlar:

```bash frame="terminal"
sudo yum install mariadb105.x86_64
```

```text title="Çıktı"
Last metadata expiration check: 1 day, 2:40:46 ago on Thu Sep  7 16:05:33 2023.
Dependencies resolved.
================================================================================
 Package                   Architecture  Version                  Repository   Size
================================================================================
Installing:
 mariadb105                x86_64        3:10.5.18-1.amzn2023.0.1 amazonlinux  1.6 M
Installing dependencies:
 mariadb-connector-c       x86_64        3.1.13-1.amzn2023.0.3    amazonlinux  196 k
 mariadb-connector-c-config noarch       3.1.13-1.amzn2023.0.3    amazonlinux  9.2 k
 mariadb105-common         x86_64        3:10.5.18-1.amzn2023.0.1 amazonlinux   31 k
 perl-Sys-Hostname         x86_64        1.23-477.amzn2023.0.5    amazonlinux   18 k

Transaction Summary
================================================================================
Install  5 Packages

Total download size: 1.8 M
Installed size: 19 M
Is this ok [y/N]:
```

Onay sormadan doğrudan kurulum için `-y` eklenir:

```bash frame="terminal"
sudo yum install -y paketadı
```

## Sistemi güncelleme

`yum` paket kurmanın yanında sistemi güncellemek için de kullanılır:

```bash frame="terminal"
yum upgrade
```

Sistemde güncellenecek bir şey olup olmadığına bakmak için:

```bash frame="terminal"
sudo yum update
```

## Sık kullanılan dnf komutları

| Açıklama | Komut |
|---|---|
| Kurulu DNF sürümünü görme | `dnf --version` |
| DNF yardımı | `dnf help`<br/>`dnf help search` |
| Kurulu ve kurulabilir paketleri listeleme | `dnf list`<br/>`dnf list available`<br/>`dnf list installed` |
| Repository listesi | `dnf repolist`<br/>`dnf repolist all` |
| Bir paket hakkında bilgi | `dnf info package_name` |
| Paket arama ve detayları | `dnf search package_name` |
| Bir dosya/değeri hangi paketin içerdiğini bulma | `dnf provides package_name` |
| DNF ile paket kurma | `dnf install package_name` |
| Elle indirilmiş paketi kurma | `dnf localinstall your_package_name.rpm` |
| Paketi yeniden kurma | `dnf reinstall package_name` |
| Güncelleme kontrolü ve sistemi güncelleme | `dnf check-update`<br/>`dnf list updates`<br/>`dnf update`<br/>`dnf update package_name` |
| Paketi eski sürüme düşürme | `dnf downgrade package_name` |
| Tüm paketleri eşitleme (downgrade/upgrade) | `dnf distro-sync` |
| Paket kaldırma | `dnf remove application_name` |
| Grup işlemleri | `dnf grouplist`<br/>`dnf groupinstall group_name`<br/>`dnf groupremove group_name` |
| Sistemi temizleme | `dnf clean all`<br/>`dnf autoremove` |
| DNF komut geçmişi | `dnf history`<br/>`dnf history info id_number` |
