---
title: Arama, görüntüleme ve editörler
description: find ile dosya arama, less, head ve tail ile dosya okuma, vim ve nano editörleri, diff, vimdiff, sdiff ve grep komutları.
module: linux
lessons: [3]
order: 4
---

## find: dosya ve klasör arama

Bir dosyanın nerede olduğunu bilmiyorsan ya da sistemde bir dosyayı bulmak istiyorsan `find` kullanılır. Yalnızca `find` yazıp Enter'a basarsan bulunduğun klasördeki bütün klasör ve dosyalar listelenir:

```bash frame="terminal"
find
```

```text title="Çıktı"
.
./.bash_logout
./.bash_profile
./.bashrc
./.ssh
./.ssh/authorized_keys
./.bash_history
./.lesshst
./ornek1
./ornek1/hedef.txt
./ornek1/ornek1
./linkimiz.txt
./.viminfo
./linkimiz1.txt
```

### -name ve -iname

`find` komutundan sonra aramanın yapılacağı yer yazılır. Örneğin `/etc` altında adı `conf` ile başlayıp devamı herhangi bir şey olan dosyaları listelemek için:

```bash frame="terminal"
find /etc -name conf*
```

```text title="Çıktı"
/etc/pm/config.d
/etc/selinux/config
find: '/etc/grub.d': Permission denied
/etc/crypto-policies/config
/etc/pam.d/config-util
find: '/etc/ssh/sshd_config.d': Permission denied
find: '/etc/sssd': Permission denied
find: '/etc/sudoers.d': Permission denied
find: '/etc/audit': Permission denied
```

Linux büyük-küçük harf duyarlıdır. `conf` ile başlayan dosyalar aranırken harflerden biri büyük olan dosyalar gösterilmez. Büyük-küçük harf ayrımı yapmadan aramak için `-iname` kullanılır:

```bash frame="terminal"
find . -iname conf*
```

```text title="Çıktı"
./ConFig
./confİG
```

Bulunan dosyaların ayrıntılarını listelemek için sona `-ls` eklenir:

```bash frame="terminal"
find . -iname conf* -ls
```

```text title="Çıktı"
  8561844      4 -rw-r--r--   1 ec2-user ec2-user        6 Nov 10 20:21 ./ConFig
  8566151      4 -rw-r--r--   1 ec2-user ec2-user        8 Nov 10 20:21 ./conf\304\260G
```

### Zamana, boyuta ve tipe göre arama

10 günden eski dosyaları bulmak için `-mtime +10` kullanılır:

```bash frame="terminal"
find . -mtime +10
```

```text title="Çıktı"
./.bash_logout
./.bash_profile
./.bashrc
```

`-size` ile boyuta göre arama yapılır. Aşağıdaki komut `/etc` altında boyutu 20 bloktan büyük dosya ve klasörleri listeler. Birim yazılmadığında `find` 512 baytlık blok kullanır; megabayt cinsinden aramak için birim eklenir, örneğin `-size +20M`.

```bash frame="terminal"
find /etc -size +20
```

```text title="Çıktı"
/etc
/etc/sysconfig
/etc/cloud/templates
/etc/pki/ca-trust/extracted/edk2/cacerts.bin
/etc/pki/ca-trust/extracted/java/cacerts
/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
/etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem
/etc/pki/ca-trust/extracted/pem/objsign-ca-bundle.pem
/etc/pki/ca-trust/extracted/pem/directory-hash
/etc/pki/tls/openssl.cnf
```

`-type` ile belirli tipteki öğeler aranır: `d` dizin, `l` link gibi.

```bash frame="terminal"
find . -type d
```

```text title="Çıktı"
.
./.ssh
./ornek1
./ornek1/ornek1
```

`find -newer dosyaadi`, verilen dosyadan daha yeni bir değiştirme zamanına (modification time) sahip tüm dosya ve dizinleri bulur. Yani o dosya oluşturulduktan ya da son değiştirildikten sonra değiştirilmiş her şeyi listeler:

```bash frame="terminal"
find -newer confİG
```

```text title="Çıktı"
.
./.lesshst
./linuxsample.txt
./.wget-hsts
```

### -exec

`find` ile bulunan dosyalar üzerinde başka bir komut çalıştırmak için `-exec` seçeneği eklenir. Notlardaki kullanım:

```bash frame="terminal"
find . -iname config -exec {} \;
```

```text title="Çıktı"
find: './ConFig': Permission denied
find: './confİG': Permission denied
```

## less, head ve tail

Uzun bir dosyayı aşağı kaydırmak yerine sayfa sayfa okumak için `less dosyaadi` kullanılır:

```bash frame="terminal"
less linuxsample.txt
```

```text title="Çıktı"
Bu birinci satır.
Bu ikinci satır.
Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.
...
Sekiz
linuxsample.txt
```

- Sonraki sayfaya geçmek için `Space`.
- Satır satır ilerlemek için aşağı yön tuşu veya `Enter`.
- Çıkmak için `q`.

Dosyanın sonuna gelindiğinde altta `(END)` görünür.

Uzun bir dosyanın başını görmek için `head dosyaadi` kullanılır. Kaç satır görmek istediğin `head -2 dosyaadi` biçiminde belirtilir:

```bash frame="terminal"
head -2 linuxsample.txt
```

```text title="Çıktı"
Bu birinci satır.
Bu ikinci satır.
```

Tersine, sondan belirli sayıda satır okumak için `tail -3 dosyaadi` kullanılır.

`tail -f dosyaadi`, dosyaya yeni eklenen satırları anlık olarak ekranda takip etmeyi sağlar. Genellikle sistem günlük dosyalarını (log files) canlı izlemek ve çalışan bir uygulamanın ürettiği hataları veya durum güncellemelerini anında görmek için kullanılır. Takibi durdurmak için `Ctrl + C` ile komut sonlandırılır.

## vim

Linux'ta dosya içeriğini düzenlemek için çeşitli araçlar vardır. Bunlardan ilki **vim**'dir. Okuma ve yazma (edit) olmak üzere iki modu vardır.

Dosya ilk açıldığında okuma modunda açılır. Bu moddayken dosyadan çıkmak için `:x` + Enter veya `:q` + Enter kullanılır.

Okuma (navigasyon) modunda hareket tuşları:

| Tuş | Yön |
| --- | --- |
| `h` | Sola |
| `l` | Sağa |
| `j` | Aşağı |
| `k` | Yukarı |

Yön tuşları da kullanılabilir.

- Yazma moduna geçmek için `i` tuşuna basılır; `Esc` ile okuma moduna dönülür.
- Dosyayı kaydedip çıkmak için `Esc` ardından `:wq` + Enter.
- `:set nu` satır numaralarını açar, `:set nonu` kapatır.

## nano

Diğer bir metin editörü **nano**'dur. `nano dosyaadi` biçiminde kullanılır. `Ctrl + X` ile dosya kaydedilip çıkılır.

## diff, vimdiff ve sdiff

Dosyalar arasındaki farkları bulmak için `diff dosyaadi1 dosyaadi2` kullanılır. Çıktıda birinci dosyadaki satırlar (`<`), değişim bilgisi ve ikinci dosyadaki satırlar (`>`) gösterilir:

```bash frame="terminal"
diff ConFig confİG
```

```text title="Çıktı"
1,3c1
< selam
< bugün hava güzel
< iyi hissediyorum
---
> merhaba
```

`vimdiff dosyaadi1 dosyaadi2` iki dosyayı vim içinde yan yana açar ve farklı satırları renklendirir. Çıkmak için `Esc` ardından `:wq` kullanılır.

```bash frame="terminal"
vimdiff ConFig confİG
```

İki dosyayı komut satırında yan yana görmek için `sdiff dosyaadi1 dosyaadi2` kullanılır:

```bash frame="terminal"
sdiff ConFig confİG
```

```text title="Çıktı"
selam                                                 | merhaba
bugün hava güzel                                      <
iyi hissediyorum                                      <
```

## grep: dosya içinde arama

`grep` metin dosyalarının içinde arama yapar. `find` sistemde dosya ve klasör bulurken `grep` dosyanın içinde arar.

```bash frame="terminal"
grep Osman linuxsample.txt
```

```text title="Çıktı"
Osman
```

Sık kullanılan seçenekler:

| Seçenek | İşlevi |
| --- | --- |
| `-i` | Büyük-küçük harf ayrımı yapmadan arar: `grep -i kelime dosyaadi` |
| `-c` | Kelimenin kaç satırda bulunduğunu verir |
| `-n` | Kelimenin bulunduğu satır numarasını verir |
| `-v` | Kelimenin bulunmadığı satırları gösterir |

```bash frame="terminal"
grep -c Osman linuxsample.txt
```

```text title="Çıktı"
1
```

```bash frame="terminal"
grep -n Osman linuxsample.txt
```

```text title="Çıktı"
31:Osman
```
