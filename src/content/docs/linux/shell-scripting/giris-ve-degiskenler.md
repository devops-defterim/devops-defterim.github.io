---
title: Giriş, read ve değişkenler
description: Bash script yapısı, ekrana yazdırma, read ile input alma, pozisyonel parametreler, özel değişkenler, komut çıktısı ve jq.
module: linux
lessons: [6]
order: 12
---

## Neden bash script

Bir DevOps mühendisi veya sistem yöneticisi için bir işi iki kez elle yapmak vakit kaybıdır. Bash scripting, her gün terminal başında aynı komutları yazmaktan kurtarır ve süreçleri otomasyona dökmemizi sağlar. Böylece hem zamandan tasarruf edilir hem de insan hatası ortadan kalkar. Karar verme yeteneği eklenen ve zamanlanmış görevlerle biz bilgisayar başında değilken bile çalışan scriptler, sunucu kurulumundan yedeklemeye kadar pek çok işi tek komutla yapılabilir hale getirir.

## Shebang: `#!/bin/bash`

Her script dosyası `#!/bin/bash` satırıyla başlar. Bu satır dosyanın bir script olduğunu ve bash ile yazıldığını belirtir. Linux çekirdeğinden bir dosyayı çalıştırması istendiğinde dosyanın ilk satırına bakar; `#!` işaretini görünce bunun bir script olduğunu anlar. `/bin/bash` ise "bu dosyadaki kodlar bash ile yazıldı, bash yorumlayıcısını çağır ve dosyayı ona teslim et" anlamına gelir.

## Ekrana yazdırma: echo, heredoc ve printf

```bash title="scr.sh"
#!/bin/bash

echo "ornek"
echo -e "selam\n" alt satırdan devam edecek

cat << EOL
bu yazı EOL komutunu görene dek devam edecek
EOL

printf 1234
```

```bash frame="terminal"
/bin/bash "/Users/ornekkullanici/Desktop/ilk_scriptim.sh/scr.sh"
```

```text title="Çıktı"
ornek
selam
 alt satırdan devam edecek
bu yazı EOL komutunu görene dek devam edecek
1234
```

- **echo:** Ekrana yazdırmanın ilk yolu. `\n` ile alt satıra geçilmesi isteniyorsa `echo -e` kullanılır.
- **`cat << EOL`:** `cat` dosya okuma/yazma için kullanılır. `<< EOL` ise cat'e, verilen girdiyi `EOL` kelimesini görene kadar almasını söyler. Buradaki girdi "bu yazı EOL komutunu görene dek devam edecek" cümlesidir; 8. satırdaki `EOL` görülünce sona erer.
- **printf:** C dilinden de bilinen `printf` ile de ekrana çıktı yazdırılabilir.

## Kullanıcıdan input alma: read

Kullanıcıdan input almak için `read` komutu kullanılır. Kullanımı `read -p 'soru' degisken_adi` biçimindedir. `-p` parametresi soruyu yazar ve cevabı bekler; girilen değer `degisken_adi` değişkenine atanır. Bu değer `$degisken_adi` ile kullanılır.

```bash title="scr.sh"
#!/bin/bash

read -p "isminiz nedir?" isim

echo "memnun oldum $isim"
```

```text title="Çıktı"
isminiz nedir?ornek
memnun oldum ornek
```

### Girilen değeri gizleme: `read -s`

Kullanıcının yazdığı karakterlerin ekranda görünmemesi için `read -s` kullanılır:

```bash title="scr.sh"
#!/bin/bash

read -p "username:"  name

echo "username: $name"

read -s -p "password:"  pwd

echo $pwd
```

```text title="Çıktı"
username:ornek
username: ornek
password:1234
```

## Çok satırlı yorum

Birden fazla satırı yorum olarak işaretlemek için bloğun başına `: '`, sonuna `'` konur. Aşağıdaki script çalıştırıldığında ekrana hiçbir şey yazmaz:

```bash title="scr.sh"
#!/bin/bash

: '
echo -e "selam\n" echo test

cat << EOL
asd
EOL

printf 1234

'
```

## Pozisyonel parametreler

Kullanıcıdan birden çok parametre almak gerektiğinde `read` yerine pozisyonel parametreler (`$1`, `$2`, `$3` ...) kullanılır. Değerler script çalıştırılırken komutun sonuna yazılır.

```bash title="scr.sh"
#!/bin/bash

echo "Arabanın Markası: $1"
echo "Arabanın Modeli : $2"
echo "Arabanın Rengi  : $3"

echo "Kayıt başarıyla oluşturuldu: $3 renkli bir $1 $2 sisteme eklendi."
```

Parametresiz çalıştırıldığında değerler boş kalır:

```bash frame="terminal"
/bin/bash "/Users/ornekkullanici/Desktop/ilk_scriptim.sh/scr.sh"
```

```text title="Çıktı"
Arabanın Markası:
Arabanın Modeli :
Arabanın Rengi  :
Kayıt başarıyla oluşturuldu:  renkli bir   sisteme eklendi.
```

Parametrelerle çalıştırıldığında:

```bash frame="terminal"
/bin/bash "/Users/ornekkullanici/Desktop/ilk_scriptim.sh/scr.sh" Toyota Corolla Beyaz
```

```text title="Çıktı"
Arabanın Markası: Toyota
Arabanın Modeli : Corolla
Arabanın Rengi  : Beyaz
Kayıt başarıyla oluşturuldu: Beyaz renkli bir Toyota Corolla sisteme eklendi.
```

## Özel değişkenler

| Değişken | Verdiği değer |
|---|---|
| `$0` | Çalıştırılan dosyanın adı |
| `$#` | Verilen pozisyonel parametre sayısı |
| `$?` | Son komutun exit kodu |

```bash title="scr.sh"
#!/bin/bash

echo $0

echo $#

mdckdmc

echo $?
```

```text title="Çıktı"
/Users/ornekkullanici/Desktop/ilk_scriptim.sh/scr.sh
0
/Users/ornekkullanici/Desktop/ilk_scriptim.sh/scr.sh: line 7: mdckdmc: command not found
127
```

Ortamdan gelen bazı hazır değişkenler de vardır:

```bash title="scr.sh"
#!/bin/bash

echo "kullanıcı dizini: $HOME"

echo "user: $USER"

echo "shell: $SHELL"
```

```text title="Çıktı"
kullanıcı dizini: /Users/ornekkullanici
user: ornekkullanici
shell: /bin/zsh
```

## Değişken tanımlama

Değişken, eşittir işaretinin iki yanında boşluk olmadan `isim=ornek` biçiminde tanımlanır. Değerde birden fazla kelime ve boşluk olacaksa tırnak kullanılması gerekir: `isimler="ornek selin"`.

```bash title="scr.sh"
#!/bin/bash

isim=ornek

isimler="ornek,selin"

echo $isim
echo $isimler
```

```text title="Çıktı"
ornek
ornek,selin
```

## Komut çıktısını değişkene atama

Bir komutun çıktısını değişkene atamak için `$( )` kullanılır. Aşağıda `date` çıktısı `time` değişkenine atanıp yazdırılıyor:

```bash title="scr.sh"
#!/bin/bash

time=$(date +"%d-%m-%Y")

echo $time

date
```

```text title="Çıktı"
11-01-2026
Sun Jan 11 18:03:12 +03 2026
```

O anda terminali kullanan kullanıcının adını yazdırmak için `whoami` kullanılır:

```bash title="scr.sh"
#!/bin/bash

whoami
```

```text title="Çıktı"
ornekkullanici
```

### who çıktısını filtreleme

`who` komutu kullanıcı, tarih, saat gibi pek çok bilgi verir. Aşağıda önce ham çıktı `whoami` değişkenine atanıyor, ardından çıktı pipe ile filtrelerden geçirilerek sadece kullanıcı adları alınıyor:

```bash title="scr.sh"
#!/bin/bash

whoami=$(who)
echo $whoami

who2=$(who | cut -d ' ' -f1 | sort | uniq)
echo $who2
```

```text title="Çıktı"
ornekkullanici console Dec 7 18:29
ornekkullanici
```

`|` (pipe) soldaki komutun sonucunu sağdaki komuta aktarır. Adımlar:

1. `who`: Ham listeyi getirir.
2. `cut -d ' ' -f1`: Boşluğu ayraç kabul eder ve sadece ilk sütunu, yani kullanıcı adlarını alır (tarih ve saat kısmı atılır).
3. `sort`: İsimleri alfabetik sıraya dizer.
4. `uniq`: Listede aynı isimden birden fazla varsa (aynı kişi iki terminal açmışsa) teke indirir.

## JSON'dan değer alma: jq

Binlerce satırlık bir JSON dosyasından tek bir değeri almak için `jq` ile nokta (`.`) operatörü kullanılır. Örneğin bir hava durumu verisinden sadece dereceyi almak için:

```bash frame="terminal"
cat hava.json | jq '.derece'
```

Normalde jq sonucu JSON formatına uygun olarak çift tırnak içinde verir. Bu değer bir değişkene atanıp kullanılacaksa tırnaklar sorun çıkarabilir. `jq -r` parametresi tırnakları kaldırıp metni olduğu gibi verir.
