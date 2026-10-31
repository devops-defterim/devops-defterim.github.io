---
title: Döngüler
description: Bash'te for ve while döngüleri, break ile çıkış ve IFS ile dosyayı satır satır okuma örnekleri.
module: linux
lessons: [7]
order: 15
---

## for döngüsü

1'den 10'a kadar sayıları ekrana yazdıran basit bir for döngüsü:

```bash title="scr.sh"
#!/bin/bash

for i in {1..10}
do
echo "sayi: $i"
done
```

```text title="Çıktı"
sayi: 1
sayi: 2
sayi: 3
...
sayi: 10
```

Bulunulan dizindeki `.asd` uzantılı tüm dosyaları kontrol eden for döngüsü:

```bash title="scr.sh"
#!/bin/bash

for file in *.asd
do
if [ -f "$file" ]
then
echo "file: $file"
fi
done
```

```text title="Çıktı"
file: 1.asd
file: 2.asd
```

## while döngüsü

while ile 1'den 10'a kadar sayıları yazdırma:

```bash title="scr.sh"
#!/bin/bash

x=1

while [ $x -le 10 ]

do
echo $x

((x++))
done
```

```text title="Çıktı"
1
2
3
...
10
```

### break ile döngüden çıkma

Kullanıcının girdiği değer 7 olduğunda sonlanan bir while döngüsü. `while :` sonsuz bir döngü başlatır, `break` döngüden çıkar:

```bash title="scr.sh"
#!/bin/bash

while :
do

read -r -p "bir sayi giriniz:" sayi
[ "$sayi" == "7" ] && break
echo girdiginiz sayi: "$sayi"
done
```

```text title="Çıktı"
bir sayi giriniz:5
girdiginiz sayi: 5
bir sayi giriniz:7
```

## IFS ile dosyayı satır satır okuma

`while IFS= read -r line` kalıbıyla bir dosya, satırlar bitene kadar satır satır okunur. Her satır `line` değişkenine atanır ve `echo` ile yazdırılır. Dosya döngüye `done < "$t1"` ile verilir:

```bash title="scr.sh"
#!/bin/bash
t1="devops.t1"

if [ ! -f "$t1" ]
then
echo "gecersiz dosya"
fi

while IFS= read -r line
do
echo $line
done < "$t1"
```

```text title="Çıktı"
devops.t1
kdmddmd error
mdkwjcnec error 23
1234
234324

64393029

48792042

error
```

Aynı örneğin genişletilmiş hali, çalıştığı klasördeki tüm `.t1` uzantılı dosyaları döngüye alır. Her birinin dosya olup olmadığını kontrol eder, IFS ile satır satır okur ve `error` olan satır varsa "hata bulundu" yazar:

```bash title="scr.sh"
#!/bin/bash

for file in *.t1
do
if [[ -f $file ]]
then
while IFS= read -r line
do
if [[ $line == "error" ]]
then
echo "hata bulundu $line"
fi
done < "$file"
fi
done
```

```bash frame="terminal"
cat devops.t1
```

```text title="Çıktı"
ıdcwkmwkclwk error mdckemckdwmc
```

```text title="Script çıktısı"
hata bulundu error
```
