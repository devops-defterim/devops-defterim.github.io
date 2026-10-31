---
title: Shell ve temel komutlar
description: Bash prompt satırının anlamı, home klasörü ve pwd, cd, ls, echo, touch, cat, rm, mkdir, rmdir, --help ve man komutları.
module: linux
lessons: [2]
order: 2
---

## Prompt satırı

Sanal makineye bağlanınca terminalde şuna benzer bir satır görünür:

```text
[ec2-user@ip-172-31-0-10 ~]$
```

Bu, bash'in varsayılan görünümüdür ve istenirse değiştirilebilir. Satır, hangi kullanıcıyla nereye bağlı olunduğunu gösterir:

- `ec2-user`: bağlı olunan kullanıcının adı.
- `@ip-172-31-0-10`: bağlı olunan bilgisayarın adı. Burada makine adı IP adresi biçiminde verilmiş.
- `~`: o an bulunulan klasör.

## Home klasörü ve pwd

Linux'ta her şey bir dosyadır. Her kullanıcının bir home klasörü vardır; bunu Windows'taki masaüstü gibi düşünebilirsin. Değiştirilmediği sürece kök dizinin altındaki `home` klasörünün içindeki kullanıcı adı klasörüdür ve kısaca `~` sembolüyle gösterilir.

O an hangi klasörde olduğunu görmek için `pwd` kullanılır:

```bash frame="terminal"
pwd
```

```text title="Çıktı"
/home/ec2-user
```

Çıktı, kök dizin altındaki `home` klasöründe, kullanıcı adının klasöründe olunduğunu gösterir.

## whoami ve clear

`whoami`, bu oturuma hangi kullanıcıyla bağlanıldığını, yani kim olduğunu gösterir:

```bash frame="terminal"
whoami
```

```text title="Çıktı"
ec2-user
```

`clear` ile ekrana yazılmış komut satırları temizlenir.

## cd: klasör değiştirme

`cd` (change directory) komutunun ardından gidilecek klasör yazılınca mevcut klasör o klasörle değişir. Aşağıda önce bulunulan klasöre bakılıyor, sonra `/etc` klasörüne geçiliyor:

```bash frame="terminal"
pwd
cd /etc
pwd
```

```text title="Çıktı"
/home/ec2-user
/etc
```

- Bir üst klasöre geçmek için `cd ..`
- İki üst klasöre geçmek için `cd ../..`

Bir komutun sonuna `.` konursa bu "bu klasör" anlamına gelir; işlemin bulunulan klasörde yapılacağını belirtir.

## ls: listeleme

`ls` mevcut klasördeki gizli olmayan dosyaları listeler. Gizli dosyaları da görmek için `ls -a` kullanılır:

```bash frame="terminal"
ls -a
```

```text title="Çıktı"
.  ..  .bash_history  .bash_logout  .bash_profile  .bashrc  .ssh
```

Çıktıyı alt alta, ayrıntılı listelemek için `ls -al` yazılır. Bazı dosyaların adı `.` ile başlar; Linux'ta bu, dosyanın gizli olduğu anlamına gelir.

```bash frame="terminal"
ls -al
```

```text title="Çıktı"
total 16
drwx------. 3 ec2-user ec2-user  95 Nov  8 14:48 .
drwxr-xr-x. 3 root     root      22 Nov  7 14:49 ..
-rw-------. 1 ec2-user ec2-user   5 Nov  8 14:48 .bash_history
-rw-r--r--. 1 ec2-user ec2-user  18 Jan 28  2023 .bash_logout
-rw-r--r--. 1 ec2-user ec2-user 141 Jan 28  2023 .bash_profile
-rw-r--r--. 1 ec2-user ec2-user 492 Jan 28  2023 .bashrc
drwx------. 2 ec2-user ec2-user  29 Nov  7 14:49 .ssh
```

Listelenen öğelerin tipini görmek için `ls -alF` kullanılır. Klasörlerin sonuna `/` eklenir:

```bash frame="terminal"
ls -alF
```

```text title="Çıktı"
total 16
drwx------. 3 ec2-user ec2-user  95 Nov  8 14:48 ./
drwxr-xr-x. 3 root     root      22 Nov  7 14:49 ../
-rw-------. 1 ec2-user ec2-user   5 Nov  8 14:48 .bash_history
-rw-r--r--. 1 ec2-user ec2-user  18 Jan 28  2023 .bash_logout
-rw-r--r--. 1 ec2-user ec2-user 141 Jan 28  2023 .bash_profile
-rw-r--r--. 1 ec2-user ec2-user 492 Jan 28  2023 .bashrc
drwx------. 2 ec2-user ec2-user  29 Nov  7 14:49 .ssh/
```

Satırların başındaki karakter öğenin tipini gösterir:

| İlk karakter | Anlamı |
| --- | --- |
| `d` | Klasör |
| `-` | Dosya |
| `l` | Link |

## echo

`echo`, yazılan metni çıktı olarak geri döndürür. Metin tek veya çift tırnak içinde yazılabilir. Metinleri dosyalara yazmak gibi işlerde de kullanılır.

```bash frame="terminal"
echo "selamlar"
```

```text title="Çıktı"
selamlar
```

`echo` değişkenlerle de çalışır. Aşağıda `SHELL` değişkeninin değeri öğreniliyor:

```bash frame="terminal"
echo $SHELL
```

```text title="Çıktı"
/bin/bash
```

## touch

`touch dosyaadi` biçiminde kullanılır. Adı verilen dosyanın değiştirilme (modification) tarihini günceller. O adda bir dosya yoksa o adla boş bir dosya oluşturur.

```bash frame="terminal"
touch ilkdosya
ls -al
```

```text title="Çıktı"
total 16
drwx------. 3 ec2-user ec2-user 111 Nov  9 12:18 .
drwxr-xr-x. 3 root     root      22 Nov  7 14:49 ..
-rw-------. 1 ec2-user ec2-user 285 Nov  8 21:08 .bash_history
-rw-r--r--. 1 ec2-user ec2-user  18 Jan 28  2023 .bash_logout
-rw-r--r--. 1 ec2-user ec2-user 141 Jan 28  2023 .bash_profile
-rw-r--r--. 1 ec2-user ec2-user 492 Jan 28  2023 .bashrc
drwx------. 2 ec2-user ec2-user  29 Nov  7 14:49 .ssh
-rw-r--r--. 1 ec2-user ec2-user   0 Nov  9 12:18 ilkdosya
```

## cat

Bir metin dosyasının içeriğini hızlıca görmek için `cat dosyaadi` kullanılır:

```bash frame="terminal"
cat ilkdosya
```

```text title="Çıktı"
selamlar
```

## rm: dosya silme

Bir dosyayı silmek için `rm dosyaadi` kullanılır:

```bash frame="terminal"
ls
rm denemedosyası
ls
```

```text title="Çıktı"
denemedosyası  ilk  ilkdosya
ilk  ilkdosya
```

## mkdir ve rmdir: klasör oluşturma ve silme

Klasör oluşturmak için `mkdir klasoradi` kullanılır:

```bash frame="terminal"
mkdir ilkfolder
ls
```

```text title="Çıktı"
ilkdosya  ilkfolder
```

İçi boş bir klasörü silmek için `rmdir klasoradi` kullanılır:

```bash frame="terminal"
rmdir ilkfolder
ls
```

```text title="Çıktı"
ilkdosya
```

Bir klasörün altında başka bir klasörü tek seferde oluşturmak için `-p` seçeneği kullanılır:

```bash frame="terminal"
mkdir -p ilkklasör/ikinciklasör
ls
```

```text title="Çıktı"
ilkdosya  ilkklasör
```

İçinde başka bir klasör bulunan bir klasörü silmek için `rm -rf klasoradi` yazılır:

```bash frame="terminal"
rm -rf ilkklasör
ls
```

```text title="Çıktı"
ilkdosya
```

## --help ve man

Bir komutun seçeneklerini, nasıl ve ne için kullanıldığını öğrenmek için `komutadi --help` ya da `man komutadi` kullanılır. `man` sayfasından çıkmak için `q` tuşuna basman yeterli.

```bash frame="terminal"
ls --help
```

```text title="Çıktı"
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

Mandatory arguments to long options are mandatory for short options too.
  -a, --all                  do not ignore entries starting with .
  -A, --almost-all           do not list implied . and ..
      --author               with -l, print the author of each file
  -b, --escape               print C-style escapes for nongraphic characters
...
  -F, --classify             append indicator (one of */=>@|) to entries
...
```

```bash frame="terminal"
man ls
```

```text title="Çıktı"
LS(1)                        User Commands                        LS(1)

NAME
       ls - list directory contents

SYNOPSIS
       ls [OPTION]... [FILE]...

DESCRIPTION
       List information about the FILEs (the current directory by default).
       Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
...
 Manual page ls(1) line 1 (press h for help or q to quit)
```
