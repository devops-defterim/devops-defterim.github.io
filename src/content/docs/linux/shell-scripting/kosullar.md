---
title: Koşullar
description: Bash'te if, elif, else yapısı, sayısal karşılaştırma operatörleri ve dosya test operatörleri.
module: linux
lessons: [7]
order: 14
---

## if yapısı

`if` ifadesinin iskeleti şöyledir; `fi` bloğu sonlandırır:

```bash
if [ koşul ]
then
    # koşul doğruysa
else
    # koşul hatalıysa
fi
```

## Karşılaştırma operatörleri

Köşeli parantez içinde sayısal karşılaştırma için sembollerin yerine şu ifadeler kullanılır:

| Sembol | Bash ifadesi |
|---|---|
| `<` | `-lt` |
| `>` | `-gt` |
| `==` | `-eq` |
| `>=` | `-ge` |
| `<=` | `-le` |
| `!=` | `-ne` |

```bash title="scr.sh"
#!/bin/bash

var="5"
var2="10"

if [ "$var" -gt "$var2" ]
then
echo "var, var2'den buyuktur"
elif [ "$var" -eq "5" ]
then
echo "variable degeri: $var"
else
echo "var, var2'den kucuktur"
fi
```

:::caution
`[` ile `]` karakterlerinin iç tarafında boşluk bırakılmalıdır. Notlardaki ilk denemede `["$var" -gt "$var2"]` boşluksuz yazıldığı için script `[5: command not found` hatası verdi ve `else` dalına düştü:

```text title="Çıktı"
/Users/ornekkullanici/Desktop/ilk_scriptim.sh/scr.sh: line 6: [5: command not found
/Users/ornekkullanici/Desktop/ilk_scriptim.sh/scr.sh: line 9: [5: command not found
var, var2'den kucuktur
```
:::

## Dosya test operatörleri

| Operatör | Kontrol ettiği |
|---|---|
| `-e` | Dosya mevcut mu |
| `-r` | Dosya okunabilir mi |
| `-w` | Dosya yazılabilir mi |
| `-x` | Dosya çalıştırılabilir mi |
| `-f` | Bu bir dosya mı |
| `-d` | Bu bir dizin mi |

`!` operatörü koşulu tersine çevirir. Aşağıdaki script `devops.txt` dosyasının varlığını ve yazılabilirliğini kontrol eder:

```bash title="scr.sh"
#!/bin/bash

file="devops.txt"

if [ ! -e $file ]
then
echo "dosya bulunamadi"
elif [ -w $file ]
then
echo "yazilabilir dosya"
else
echo "dosya mevcut ancak yazılamaz"
fi
```

```text title="Çıktı"
dosya bulunamadi
```
