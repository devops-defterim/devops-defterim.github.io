---
title: Dosya işlemleri, PATH ve linkler
description: cp ve mv ile kopyalama, taşıma ve yeniden adlandırma, kök dizin, PATH değişkeni, which, export ile soft ve hard linkler.
module: linux
lessons: [2, 3]
order: 3
---

Örneklerde kullanılan `deneme` dosyasının içeriği şöyle:

```bash frame="terminal"
cat deneme
```

```text title="Çıktı"
1
2
3
4
4
```

## cp: kopyalama

`cp dosyaadi hedef` ile bir dosya başka bir konuma kopyalanır. Aşağıda `deneme` dosyası `ornek1` klasörünün altına `ikincidosya` adıyla kopyalanıyor:

```bash frame="terminal"
cp deneme ornek1/ikincidosya
cd ornek1
cat ikincidosya
```

```text title="Çıktı"
1
2
3
4
4
```

## mv: taşıma ve yeniden adlandırma

Bir dosyayı başka bir klasöre taşımak için `mv dosyaadi hedef` kullanılır. Aşağıda başlangıçta home klasöründe bulunan `deneme` dosyası `ornek1` klasörünün altına taşınıyor:

```bash frame="terminal"
ls
mv deneme ornek1/ikincidosya
ls
cd ornek1
ls
```

```text title="Çıktı"
deneme  ornek1
ornek1
deneme  ikincidosya
```

`mv` dosyanın adını değiştirmek için de kullanılır:

```bash frame="terminal"
mv deneme ilkdosya
ls
```

```text title="Çıktı"
ikincidosya  ilkdosya
```

`mv -i kaynak hedef` komutu işlemi etkileşimli (interactive) modda yapar. Aşağıdaki örnekte `deneme1` dosyası `deneme2` adıyla taşınıyor; `deneme2` zaten var olduğu için üzerine yazılsın mı diye sorulur. Onaylamak için `y` yazıp Enter'a basılır.

```bash frame="terminal"
ls
mv -i deneme1 deneme2
ls
```

```text title="Çıktı"
deneme1  deneme2  deneme3
mv: overwrite 'deneme2'? y
deneme2  deneme3
```

## Kök dizin

Linux'ta en üstte kök dizin (`/`, root) bulunur ve tüm klasörler onun altında şekillenir. Kök dizindeki klasörlerden bazıları:

```bash frame="terminal"
cd /
ls
```

```text title="Çıktı"
bin  boot  dev  etc  home  lib  lib64  local  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

## PATH değişkeni

Linux'ta bir komut girildiğinde sistem önce `PATH` ortam değişkenine (environment variable) bakar. `PATH`, girilen komutların nerede ve hangi sırayla aranacağını söyler. `cat`, `touch` gibi komutların bir kısmı aslında birer uygulamadır.

```bash frame="terminal"
echo $PATH
```

```text title="Çıktı"
/home/ec2-user/.local/bin:/home/ec2-user/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
```

Bir komut çalıştırılmak istendiğinde önce `/home/ec2-user/.local/bin` klasörüne bakılır; uygulama orada varsa oradaki çalıştırılır. Orada bulunamazsa `/home/ec2-user/bin` klasörüne bakılır. Orada da yoksa çıktıdaki sıra takip edilir.

## which

`which uygulamaadi`, çalıştırılan komutun dosyasının sistemde nerede durduğunu (dosya yolunu) gösterir:

```bash frame="terminal"
which cat
```

```text title="Çıktı"
/usr/bin/cat
```

## export: ortam değişkeni oluşturma ve değiştirme

Yeni bir ortam değişkeni oluşturmak ya da var olanı değiştirmek için `export` kullanılır. Değişkenin değerini görmek için `echo $degiskenadi` yazılır:

```bash frame="terminal"
export TANISMA="merhaba, isminiz nedir"
echo $TANISMA
```

```text title="Çıktı"
merhaba, isminiz nedir
```

Var olan bir değişkeni değiştirmek için de aynı komut kullanılır. Aşağıdaki komut mevcut `PATH` değişkenine `ornek1` klasörünü ekler:

```bash frame="terminal"
export PATH=$PATH:/home/ec2-user/ornek1
echo $PATH
```

```text title="Çıktı"
...:/home/ec2-user/ornek1
```

## Linkler

Bir dosya başka bir kaynağa linklenebilir. Böylece link üzerinde yapılan işlemler, linkin hedefi olan kaynak üzerinde yapılmış olur. Linkler sayesinde bir dosyaya veya klasöre aynı anda birden fazla yerden erişilebilir. Soft ve hard olmak üzere iki çeşit link vardır.

### Soft link

Soft link oluşturmak için `ln -s hedefdosyayolu linkadi` kullanılır. Ana dosya silinirse link silinmez.

```bash frame="terminal"
ln -s /home/ec2-user/ornek1/hedef.txt linkimiz.txt
ls -a
ls -l
```

```text title="Çıktı"
.  ..  .bash_history  .bash_logout  .bash_profile  .bashrc  .lesshst  .ssh  .viminfo  ornek1  linkimiz.txt
total 0
drwxr-xr-x. 2 ec2-user ec2-user 23 Nov 10 19:02 ornek1
lrwxrwxrwx. 1 ec2-user ec2-user 30 Nov 10 19:04 linkimiz.txt -> /home/ec2-user/ornek1/hedef.txt
```

Link dosyası `vi` ile açılıp içine bir şey yazıldığında hedef dosyanın içeriği de değişir (`vi` için bkz. [Arama, görüntüleme ve editörler](/linux/arama-ve-goruntuleme/)):

```bash frame="terminal"
vi linkimiz.txt
cat linkimiz.txt
cd ornek1
cat hedef.txt
```

```text title="Çıktı"
bu yazacağım yazı link üzerinden olacak ama ana dosyada da değişiklik yapmış olacağım.
bu yazacağım yazı link üzerinden olacak ama ana dosyada da değişiklik yapmış olacağım.
```

Sonradan aynı dosyaya yeni bir link oluşturulursa onun içeriği de aynı olur:

```bash frame="terminal"
ln -s /home/ec2-user/ornek1/hedef.txt linkimiz1.txt
cat linkimiz1.txt
```

```text title="Çıktı"
bu yazacağım yazı link üzerinden olacak ama ana dosyada da değişiklik yapmış olacağım.
```

### Hard link

Hard link oluşturmak için `-s` olmadan `ln hedefdosyayolu linkadi` kullanılır. Soft linkten farkı şudur: ana dosya silindiğinde soft link kırık kalır, hard link ise aynı veriye bağlı ikinci bir dosya adı olduğu için içeriği korumaya devam eder. Hard link bir dosya oluşturur ve `ls -l` çıktısındaki görünümü soft linkten farklıdır:

```bash frame="terminal"
ln /home/ec2-user/ornek1/hedef.txt linkimiz3.txt
ls -l
```

```text title="Çıktı"
total 8
-rw-r--r--. 2 ec2-user ec2-user 97 Nov 10 19:08 hedef.txt
lrwxrwxrwx. 1 ec2-user ec2-user 30 Nov 10 19:18 linkimiz.txt2 -> /home/ec2-user/ornek1/hedef.txt
-rw-r--r--. 2 ec2-user ec2-user 97 Nov 10 19:08 linkimiz3.txt
```

Çıktıda soft link `l` ile başlar ve `->` ile hedefini gösterir; hard link ise sıradan bir dosya (`-`) gibi görünür.

### Linkleri kaldırma

Soft link `unlink linkadi` ile kaldırılır. Hedef dosya (`hedef.txt`) silinmez:

```bash frame="terminal"
ls -l
unlink linkimiz.txt2
ls -l
```

```text title="Çıktı"
total 8
-rw-r--r--. 2 ec2-user ec2-user 97 Nov 10 19:08 hedef.txt
lrwxrwxrwx. 1 ec2-user ec2-user 30 Nov 10 19:18 linkimiz.txt2 -> /home/ec2-user/ornek1/hedef.txt
-rw-r--r--. 2 ec2-user ec2-user 97 Nov 10 19:08 linkimiz3.txt
total 8
-rw-r--r--. 2 ec2-user ec2-user 97 Nov 10 19:08 hedef.txt
-rw-r--r--. 2 ec2-user ec2-user 97 Nov 10 19:08 linkimiz3.txt
```

Hard link bir dosya olduğu için normal bir dosya gibi `rm linkadi` ile silinir. Hedef dosya yine silinmez:

```bash frame="terminal"
ls
rm linkimiz3.txt
ls
```

```text title="Çıktı"
ornek1  hedef.txt  linkimiz3.txt
ornek1  hedef.txt
```
