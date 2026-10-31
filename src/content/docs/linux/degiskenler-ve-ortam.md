---
title: Sıkıştırma, değişkenler ve geçmiş
description: du, gzip ve tar ile sıkıştırma, alias, environment variable, history kullanımı ve bash başlangıç dosyaları.
module: linux
lessons: [5]
order: 8
---

## Dosya boyutu: du

Dosyaların boyutunu görmek için `du` komutu kullanılır. `-h` eklendiğinde boyutlar okunabilir biçimde (K, M, G) gösterilir.

```bash frame="terminal"
du -h gonder.tar
```

```text title="Çıktı"
12K     gonder.tar
```

## Sıkıştırma: gzip, gunzip ve tar

Dosyaları sıkıştırmak için birçok araç vardır. Bunlardan ilki `gzip dosyaadı` şeklinde kullanılır. Sıkıştırılmış dosyayı açmak için `gunzip dosyaadı` yeterlidir.

```bash frame="terminal"
gzip gonder.tar
du -h gonder.tar.gz
```

```text title="Çıktı"
4.0K    gonder.tar.gz
```

Sıkıştırılmış bir tar arşivi doğrudan oluşturmak için `tar zcf dosyaadı` biçimi kullanılır.

## alias

Alias ile sık kullandığımız bir komut için kısayol oluştururuz. Kısayolu yazdığımızda asıl komut çalışır.

```bash frame="terminal"
alias eo="echo 'ornek bir değişkendir.'"
eo
```

```text title="Çıktı"
ornek bir değişkendir.
```

## Değişkenler

Bir değişken tanımlayıp ona değer atayabilir, sonra değer yerine değişkeni çağırabiliriz. Tanımlama `isim=deger` biçimindedir, çağırmak için `$isim` yazılır.

```bash frame="terminal"
isim=osman
echo $isim
isim=ozgur
echo $isim
```

```text title="Çıktı"
osman
ozgur
```

### export ile environment variable

Normal bir değişken sadece tanımlandığı oturumda geçerlidir. Diğer oturumlarda (ör. açılan yeni bir `bash` içinde) da geçerli olması için onu environment variable'a dönüştürmemiz gerekir. Bunun için tanımın başına `export` yazılır:

```bash frame="terminal"
export osman=bir
bash
echo $osman
```

```text title="Çıktı"
bir
```

### printenv ve unset

Sistemdeki environment variable'ları görmek için `printenv` komutu kullanılır. Sonuna değişkenin adı yazılırsa sadece o değişkenin değeri basılır.

```bash frame="terminal"
printenv
```

```text title="Çıktı"
SHELL=/bin/bash
osman=bir
HISTCONTROL=ignoredups
SYSTEMD_COLORS=false
HOSTNAME=ip-172-31-0-10.eu-west-1.compute.internal
HISTSIZE=1000
PWD=/home/ec2-user
LOGNAME=ec2-user
XDG_SESSION_TYPE=tty
MOTD_SHOWN=pam
HOME=/home/ec2-user
LANG=C.UTF-8
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:...
```

Bir environment variable'ı silmek için:

```bash frame="terminal"
unset degiskenadı
```

## Komut geçmişi: history

`history` komutu bash shell geçmişini listeler:

```bash frame="terminal"
history
```

```text title="Çıktı"
    1  hostname
    2  exit
    3  clear
    4  sh
    5  echo $SHELL
    6  clear
    7  pwd
    8  whoami
    9  pwd
   10  whoami
...
```

Geçmişteki komutları tekrar çalıştırmak için `!` kullanılır:

| Kullanım | Anlamı |
|---|---|
| `!!` | En son komutu tekrarlar |
| `!10` | Geçmiş listesindeki 10 numaralı komutu çalıştırır |
| `!echo` | `echo` ile başlayan en son komutu bulup çalıştırır |

```bash frame="terminal"
!10
```

```text title="Çıktı"
whoami
ec2-user
```

```bash frame="terminal"
!echo
```

```text title="Çıktı"
echo $OSTYPE
linux-gnu
```

Geçmişi temizlemek için `history -c` kullanılır:

```bash frame="terminal"
history -c
history
```

```text title="Çıktı"
    1  history
```

## Yorum ve çok satırlı komut

`#` karakterinden sonra yazılanlar yorum kabul edilir ve işlenmez:

```bash frame="terminal"
echo "osman" #bundan sonra yazdigim islenmeyecek
```

```text title="Çıktı"
osman
```

Uzun bir komutu daha kolay okunması için birden fazla satıra bölmek istersek satır sonuna `\` koyarız:

```bash frame="terminal"
echo osman \
neredesin osman \
bla bla bala
```

```text title="Çıktı"
osman neredesin osman bla bla bala
```

## Bash başlangıç dosyaları

Bir Linux sisteme ya interactive olarak (terminal ile) bağlanırız ya da non-interactive olarak (script çalıştırarak). Interactive bağlantının iki çeşidi vardır:

- **Login:** Kendi terminal uygulamamızla bash shell'e bağlanmak.
- **Non-login:** Mevcut bir bash oturumu altında yeni bir bash açarak bağlanmak.

| Bağlantı türü | İşlenen dosya |
|---|---|
| Interactive login | Home dizinindeki `.bash_profile`. Bu dosyada sadece `.bashrc`'yi yükleyen komutlar bulunur. |
| Interactive non-login | Home dizinindeki `.bashrc` |

İki durumda da ilk olarak `/etc/profile` işlenir.

Her login olduğumuzda çalışmasını istediğimiz şeyleri `.bash_profile` dosyasına yazmamız gerekir. Ancak `.bash_profile` artık `.bashrc`'ye bağlı olduğu için alias ve environment variable tanımları gibi her şeyi `.bashrc` dosyasına yazıyoruz.
