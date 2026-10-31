---
title: Kullanıcı ve grup yönetimi
description: root ve normal kullanıcılar, sudo, useradd, passwd ve su ile kullanıcı işlemleri; groups, groupadd, usermod, chgrp ve chown.
module: linux
lessons: [4]
order: 6
---

## root, normal kullanıcılar ve sudo

Linux'ta birden fazla kullanıcı aynı anda bağlanıp sistemi kullanabilir.

Bir Linux sistemi kurulduğunda başlangıçta her zaman iki tür kullanıcı bulunur:

- **root user**: en yetkili kullanıcı.
- **Normal kullanıcılar**.

Normal bir kullanıcıyla girilen komutları root yetkisiyle çalıştırmak için `sudo` kullanılır. Bir kullanıcının `sudo` kullanabilmesi için root kullanıcının onu `sudoers` adlı dosyaya eklemiş olması gerekir; yani `sudo` kullanacak kullanıcıları root belirler.

## Kullanıcıları listeleme

Sistemdeki kullanıcıları listelemek için `/etc/passwd` dosyasına bakılır:

```bash frame="terminal"
cat /etc/passwd
```

```text title="Çıktı"
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
...
ec2-instance-connect:x:993:993::/home/ec2-instance-connect:/sbin/nologin
stapunpriv:x:159:159:systemtap unprivileged user:/var/lib/stapunpriv:/sbin/nologin
rpcuser:x:29:29:RPC Service User:/var/lib/nfs:/sbin/nologin
tcpdump:x:72:72::/:/sbin/nologin
```

## useradd ile kullanıcı oluşturma

Yeni bir kullanıcı `useradd kullaniciadi` ile oluşturulur. Bu komutun çalışması için root olmak ya da başına `sudo` yazmak gerekir:

```bash frame="terminal"
sudo useradd ornekkullanici
cat /etc/passwd
```

```text title="Çıktı"
...
tcpdump:x:72:72::/:/sbin/nologin
ec2-user:x:1000:1000:EC2 Default User:/home/ec2-user:/bin/bash
ornekkullanici:x:1001:1001::/home/ornekkullanici:/bin/bash
```

Yeni kullanıcı listenin sonuna eklenir.

## passwd ile parola atama

Yeni kullanıcıyla giriş yapabilmek için ona parola atamak gerekir. Bunun için `sudo passwd kullaniciadi` kullanılır:

```bash frame="terminal"
sudo passwd ornekkullanici
```

```text title="Çıktı"
Changing password for user ornekkullanici.
New password:
BAD PASSWORD: The password is shorter than 8 characters
Retype new password:
passwd: all authentication tokens updated successfully.
```

Örnekte parola 8 karakterden kısa olduğu için uyarı veriliyor, ancak parola tekrar girildiğinde yine de güncelleniyor.

## su ile kullanıcı değiştirme

Kullanıcılar arasında geçiş yapmak için `su kullaniciadi` kullanılır ve o kullanıcının parolası girilir:

```bash frame="terminal"
su ornekkullanici
cd ~
pwd
```

```text title="Çıktı"
Password:
/home/ornekkullanici
```

Bu durumdayken `exit` yazınca önceki kullanıcıya dönülür; tekrar `exit` yazınca oturum kapanır (logout):

```bash frame="terminal"
exit
exit
```

```text title="Çıktı"
exit
logout
```

## Gruplar

Oluşturulan her kullanıcının adıyla bir grup vardır ve kullanıcı varsayılan olarak bu gruba dahildir. Bunun dışında Linux'ta başka gruplar da bulunur. Hangi gruplara üye olduğunu görmek için `groups` kullanılır:

```bash frame="terminal"
groups
```

```text title="Çıktı"
ec2-user adm wheel systemd-journal
```

Bir kullanıcının hangi gruplara dahil olduğunu görmek için `groups kullaniciadi` yazılır. Kullanıcı yoksa hata verir:

```bash frame="terminal"
groups ornek1
```

```text title="Çıktı"
groups: 'ornek1': no such user
```

:::note
Bir kullanıcı `wheel` grubuna eklenirse otomatik olarak parolasız `sudo` yetkisine sahip olur.
:::

### Grupları listeleme

Sistemde oluşturulmuş grupları listelemek için `/etc/group` dosyasına bakılır:

```bash frame="terminal"
cat /etc/group
```

```text title="Çıktı"
root:x:0:
bin:x:1:
daemon:x:2:
sys:x:3:
adm:x:4:ec2-user
tty:x:5:
disk:x:6:
lp:x:7:
mem:x:8:
kmem:x:9:
wheel:x:10:ec2-user
cdrom:x:11:
mail:x:12:
man:x:15:
dialout:x:18:
floppy:x:19:
games:x:20:
tape:x:33:
video:x:39:
ftp:x:50:
lock:x:54:
audio:x:63:
users:x:100:
...
```

### groupadd ile grup oluşturma

Yeni bir grup `sudo groupadd grupadi` ile eklenir:

```bash frame="terminal"
sudo groupadd selam
cat /etc/group
```

```text title="Çıktı"
root:x:0:
bin:x:1:
...
ornekkullanici:x:1001:
selam:x:1002:
```

### usermod ile kullanıcıyı gruba ekleme

Bir kullanıcıyı gruba eklemek için `sudo usermod -a -G grupadi kullaniciadi` kullanılır:

```bash frame="terminal"
sudo usermod -a -G selam ec2-user
groups ec2-user
```

```text title="Çıktı"
ec2-user : ec2-user adm wheel systemd-journal selam
```

## chgrp ve chown

Bir dosyanın veya klasörün grubunu değiştirmek için `sudo chgrp grupadi dosyaadi` kullanılır:

```bash frame="terminal"
ls -l
sudo chgrp selam deneme2.txt
ls -l
```

```text title="Çıktı"
total 4
drwxr-xr-x. 2 ec2-user ec2-user    6 Jan  5 15:25 denem2.txt
-rw-r--r--. 1 ec2-user ec2-user    0 Jan  5 15:26 deneme2.txt
dr-xr-xr-x. 3 ec2-user ec2-user   36 Nov 10 19:43 ornek1
-rwxrwxrwx. 1 ec2-user ec2-user 1713 Nov 13 14:15 linuxsample.txt
total 4
drwxr-xr-x. 2 ec2-user ec2-user    6 Jan  5 15:25 denem2.txt
-rw-r--r--. 1 ec2-user selam       0 Jan  5 15:26 deneme2.txt
dr-xr-xr-x. 3 ec2-user ec2-user   36 Nov 10 19:43 ornek1
-rwxrwxrwx. 1 ec2-user ec2-user 1713 Nov 13 14:15 linuxsample.txt
```

Bir dosyanın sahibini değiştirmek için `chown` kullanılır. Örneğin dosyanın sahibini root yapmak için:

```bash frame="terminal"
sudo chown root deneme2.txt
ls -l
```

```text title="Çıktı"
total 4
drwxr-xr-x. 2 ec2-user ec2-user    6 Jan  5 15:25 denem2.txt
-rw-r--r--. 1 root     selam       0 Jan  5 15:26 deneme2.txt
dr-xr-xr-x. 3 ec2-user ec2-user   36 Nov 10 19:43 ornek1
-rwxrwxrwx. 1 ec2-user ec2-user 1713 Nov 13 14:15 linuxsample.txt
```

Dosya izinleri için [Dosya izinleri](/linux/izinler/) sayfasına bak.
