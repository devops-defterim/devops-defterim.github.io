---
title: Yönlendirme, pipe ve komut zincirleri
description: stdin, stdout ve stderr kanalları, çıktı yönlendirme, pipe, komut zincirleme operatörleri ve tar ile arşivleme.
module: linux
lessons: [4, 5]
order: 7
---

## Standart kanallar

Linux'ta bir uygulama çalıştığında buna process denir. Her process'e üç stream (kanal) bağlanır:

| Kanal | Numara | Görevi |
|---|---|---|
| stdin | 0 | Giriş kanalı, doğrudan klavyeye bağlıdır. Process'e input vermek istediğimizde bu girişe göndeririz, process de bu inputu alıp işler. |
| stdout | 1 | Process bir bilgi üreteceği zaman bu kanala gönderir. Ekrana bağlıdır. |
| stderr | 2 | Process bir hata üretecekse bu kanala gönderir. Bu da ekrana bağlıdır. |

## Çıktıyı dosyaya yönlendirme: `>` ve `>>`

Ekrana yazılan bir çıktıyı bir dosyanın içine yazmak için `>` karakteri kullanılır:

```bash frame="terminal"
echo "bu bir deneme" >deneme1.txt
cat deneme1.txt
```

```text title="Çıktı"
bu bir deneme
```

`>>` karakteri, solundaki process'in çıktısını sağdaki dosyaya gönderir. Dosyada veri varsa yeni mesaj dosyanın en sonuna eklenir:

```bash frame="terminal"
echo "bu ikinci denemedir." >> deneme1.txt
cat deneme1.txt
```

```text title="Çıktı"
bu bir deneme
bu ikinci denemedir.
```

## Çıktıyı yok etmek: `/dev/null`

Bir script çalışırken çıktılarının terminale gelmesini istemiyorsak bu çıktıları başka bir yere yönlendirmemiz gerekir. `/dev/null` cihazı bir kara delik gibi düşünülebilir: gönderilen verileri yok eder, göstermez.

```bash frame="terminal"
ls -al > /dev/null
```

Komutun çıktısını `/dev/null`'a göndermek ve hata alırsa hatayı da aynı yere göndermek için:

```bash frame="terminal"
komut > /dev/null 2>&1
```

## Girişi dosyadan almak: `<`

`<` karakteri `>`'nin tersi yönde çalışır: sağdaki dosyanın içeriğini soldaki komutun standart inputuna verir. `sort` komutu kendisine verilen inputu sıralar.

```bash frame="terminal"
sort < linuxsample.txt
```

```text title="Çıktı"
A small river named Duden flows by their place and supplies it with the necessary regelialia.
Altı
At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
Beş
Bir
Bu birinci satır.
Bu ikinci satır.
Bu son satır.
Bu sondan bir önceki satır.
Config
Dokuz
Dört
...
```

Bu komut `cat linuxsample.txt | sort` ile aynı işi yapar.

## Pipe: `|`

`|` karakteri soldaki process'i çalıştırır ve standart outputunu sağdakine standart input olarak verir. Zincir uzadıkça her komutun çıktısı bir sonrakinin girdisi olur:

```bash frame="terminal"
cat linuxsample.txt | sort | head -2
```

```text title="Çıktı"

A small river named Duden flows by their place and supplies it with the necessary regelialia.
```

## Komut zincirleme

### `;` ile sıralı çalıştırma

Birden fazla komutu `;` ile ayırarak yan yana yazıp çalıştırabiliriz. Komutlar birbiriyle ilişkili değildir, sadece sırayla çalışırlar. Birinin hata vermesi diğerlerinin çalışmasına engel olmaz.

```bash frame="terminal"
echo "ornek" ; echo "ornek1" ; echo "ornek2"
```

```text title="Çıktı"
ornek
ornek1
ornek2
```

### `&&`: ilki başarılıysa çalıştır

İkinci komutun çalışmasını birincinin başarıyla çalışması şartına bağlamak için `&&` kullanılır. İlk komut hata verirse ikincisi çalışmaz:

```bash frame="terminal"
ls dkmkd && echo "ornek6"
```

```text title="Çıktı"
ls: cannot access 'dkmkd': No such file or directory
```

### `||`: ilki başarısızsa çalıştır

Soldaki komut çalışmazsa sağdakinin çalışmasını istiyorsak `||` kullanılır:

```bash frame="terminal"
echo "ornek" || echo "ornek3"
```

```text title="Çıktı"
ornek
```

```bash frame="terminal"
ls mdkc || echo "ornek3"
```

```text title="Çıktı"
ls: cannot access 'mdkc': No such file or directory
ornek3
```

## tar ile arşivleme

Birden fazla dosyayı arşivleyerek tek bir arşiv dosyası oluşturmak için `tar` komutu kullanılır:

| Parametre | Görevi |
|---|---|
| `-c` | Yeni bir tar arşivi oluşturur |
| `-x` | Tar dosyasındaki içerikleri çıkarır |
| `-t` | Arşivin içeriğini listeler |
| `-f` | Üzerinde çalışılacak dosyayı belirtir |

Arşiv oluşturma:

```bash frame="terminal"
tar -cf gonder.tar dosyalar/
ls -l
```

```text title="Çıktı"
total 20
-rw-r--r--. 1 ec2-user ec2-user    35 Jan  6 12:41 deneme1.txt
drwxr-xr-x. 3 ec2-user ec2-user    37 Jan  6 14:45 dosyalar
drwxr-xr-x. 2 ec2-user ec2-user     6 Jan  6 13:01 ornek1
-rw-r--r--. 1 ec2-user ec2-user 10240 Jan  6 14:49 gonder.tar
-rw-r--r--. 1 ec2-user ec2-user  1683 Jan  6 13:00 linuxsample.txt
```

Arşivin içeriğini görüntüleme:

```bash frame="terminal"
tar -tf gonder.tar
```

```text title="Çıktı"
dosyalar/
dosyalar/loglar/
dosyalar/loglar/rapor.txt
dosyalar/resim.jpg
```

Arşivi başka bir dizine (burada `tmp`) çıkarma:

```bash frame="terminal"
tar -xf ../gonder.tar
ls
ls -l dosyalar/
```

```text title="Çıktı"
dosyalar
total 0
drwxr-xr-x. 2 ec2-user ec2-user 23 Jan  6 14:45 loglar
-rw-r--r--. 1 ec2-user ec2-user  0 Jan  6 14:45 resim.jpg
```

Arşivi sıkıştırma ve boyut kontrolü [Sıkıştırma, değişkenler ve geçmiş](/linux/degiskenler-ve-ortam/) sayfasında devam ediyor.
