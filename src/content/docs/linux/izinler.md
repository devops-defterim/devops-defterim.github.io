---
title: Dosya izinleri
description: Linux dosya ve klasör izinlerinin sembolik ve sayısal gösterimi, chmod ile izin değiştirme ve umask ile varsayılan izinler.
module: linux
lessons: [3]
order: 5
---

## Sembolik gösterim

`ls -l` çıktısındaki her satırın başı, dosyanın tipini ve izinlerini gösterir. Örnek bir çıktı:

```text
total 20
drwx------ 2 shum staff 4096 Jan 16 22:04 Mail
drwx------ 3 shum staff 4096 Jan 16 14:15 csc128
drwxr-xr-x 2 shum staff 4096 Jan 13 16:42 public
drwxr-xr-x 2 shum staff 4096 Jan 16 14:07 public_html
-rw-r--r-- 1 shum staff  628 Jan 15 20:04 verse
```

Sütunların anlamı (soldan sağa):

| Sütun | Örnek | Anlamı |
| --- | --- | --- |
| 1. karakter | `d`, `-` | Dosya tipi (klasör, dosya vb.) |
| 2-4. karakterler | `rwx` | Dosya sahibinin (user) izinleri |
| 5-7. karakterler | `r-x` | Grup üyelerinin (örnekte `staff` grubu) izinleri |
| 8-10. karakterler | `r-x` | Sistemdeki diğer tüm kullanıcıların (other) izinleri |
| Sayı | `2` | Hard link sayısı |
| Kullanıcı | `shum` | Dosyanın sahibi (owner) |
| Grup | `staff` | Grup adı |
| Boyut | `4096` | Dosya boyutu |
| Tarih | `Jan 16 22:04` | Son değiştirilme tarihi |
| Ad | `Mail` | Dosya adı |

İzin harfleri:

- `r` (read): okuma
- `w` (write): yazma
- `x` (execute): çalıştırılabilir dosyaları çalıştırma

## Sayısal (numerik) gösterim

İzinler harf yerine sayıyla da gösterilebilir. Her izin grubu üç bitlik bir sayıdır: `r` = 4, `w` = 2, `x` = 1.

| Binary | Octal | Sembolik | İzinler |
| --- | --- | --- | --- |
| 000 | 0 (0+0+0) | `---` | No Permission |
| 001 | 1 (0+0+1) | `--x` | Execute |
| 010 | 2 (0+2+0) | `-w-` | Write |
| 011 | 3 (0+2+1) | `-wx` | Write + Execute |
| 100 | 4 (4+0+0) | `r--` | Read |
| 101 | 5 (4+0+1) | `r-x` | Read + Execute |
| 110 | 6 (4+2+0) | `rw-` | Read + Write |
| 111 | 7 (4+2+1) | `rwx` | Read + Write + Execute |

Örneğin `rwxrw-r-x` izni şöyle hesaplanır:

| | Owner | Group | Other |
| --- | --- | --- | --- |
| Sembolik | `rwx` | `rw-` | `r-x` |
| Hesap | 4+2+1 | 4+2+0 | 4+0+1 |
| Sayısal | 7 | 6 | 5 |

Bir örnek daha (`U` user, `G` group, `O` other):

| | U | G | O |
| --- | --- | --- | --- |
| Symbolic | `rwx` | `r-x` | `r--` |
| Binary | 111 | 101 | 100 |
| Decimal | 7 | 5 | 4 |

## İzinleri görüntüleme

Dosya ve klasörlerin izinlerini görmek için `ls -l` kullanılır:

```bash frame="terminal"
ls -l
```

```text title="Çıktı"
total 4
drwxr-xr-x. 3 ec2-user ec2-user   36 Nov 10 19:43 ornek1
-rw-r--r--. 1 ec2-user ec2-user 1713 Nov 13 14:15 linuxsample.txt
```

## chmod ile izin değiştirme

İzinleri sayısal olarak değiştirmek için `chmod 777 dosyaadi` biçimi kullanılır:

```bash frame="terminal"
chmod 777 linuxsample.txt
ls -l
chmod 777 ornek1
ls -l
```

```text title="Çıktı"
total 4
drwxr-xr-x. 3 ec2-user ec2-user   36 Nov 10 19:43 ornek1
-rwxrwxrwx. 1 ec2-user ec2-user 1713 Nov 13 14:15 linuxsample.txt
total 4
drwxrwxrwx. 3 ec2-user ec2-user   36 Nov 10 19:43 ornek1
-rwxrwxrwx. 1 ec2-user ec2-user 1713 Nov 13 14:15 linuxsample.txt
```

İzinleri değiştirmenin diğer yolu harflerle belirtmektir:

| Harf | Kime |
| --- | --- |
| `u` | user (sahip) |
| `g` | group (grup) |
| `o` | others (diğerleri) |
| `a` | all (hepsi) |

`+` izin ekler, `-` izin kaldırır. Örneğin gruptan yazma iznini almak için `chmod g-w dosyaadi` kullanılır. Aşağıda herkesten yazma izni kaldırılıyor:

```bash frame="terminal"
chmod a-w ornek1
ls -l
```

```text title="Çıktı"
total 4
dr-xr-xr-x. 3 ec2-user ec2-user   36 Nov 10 19:43 ornek1
-rwxrwxrwx. 1 ec2-user ec2-user 1713 Nov 13 14:15 linuxsample.txt
```

## umask ile varsayılan izinler

Normalde bir klasör ilk oluşturulduğunda 777, bir dosya ilk oluşturulduğunda 666 izinleriyle oluşturulur. **umask**, yeni oluşturulan dosya ve klasörlere varsayılan olarak verilecek izinleri belirlemeyi sağlar. Belirtilen değer varsayılan izinlerden (777, 666) düşülür. Örneğin `umask 022` yazılırsa klasörler için 777 - 022 işleminden kalan değer izin olarak atanır.

```bash frame="terminal"
umask 022
```
