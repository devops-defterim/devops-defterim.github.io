---
title: Diziler
description: Bash dizilerinde eleman okuma, değiştirme, ekleme, yer değiştirme, silme ve eleman sayısını alma.
module: linux
lessons: [6, 7]
order: 13
---

## Dizi tanımlama, okuma ve ekleme

Dizi elemanları parantez içinde tanımlanır, `${dizi[indeks]}` ile okunur. `${dizi[@]}` dizinin tüm elemanlarını verir.

Bir diziye yeni eleman eklemenin en basit yollarından biri `int+=("4" "5")` kullanmaktır. Son satırdaki `echo` ile dizinin yeni elemanlar eklenmiş hali yazdırılır.

```bash title="scr.sh"
#!/bin/bash

int=("1" "2" "3")

echo ${int[0]}
echo ${int[1]}

int[1]="0"
echo ${int[1]}

int+=("4" "5")
echo ${int[@]}
```

```text title="Çıktı"
1
2
0
1 0 3 4 5
```

## Elemanların yerini değiştirme

Yeni elemanları dizinin sonuna değil araya yerleştirmek istersek indeksler arasında yer değiştirme yapabiliriz. Önceki scriptin sonuna şu satırlar eklenir:

```bash title="scr.sh"
a=${int[0]}
int[0]=${int[1]}
int[1]=$a
echo ${int[@]}
```

```text title="Çıktı"
1
2
0
1 0 3 4 5
0 1 3 4 5
```

Bu kod çalışmadan önce dizi `(1 0 3 4 5)` durumundadır:

1. `a=${int[0]}`: 0. indeksteki değer (1) `a` değişkenine konur. Artık `a=1`.
2. `int[0]=${int[1]}`: 1. indeksteki değer (0) 0. indeksin üzerine yazılır. Dizi: `(0 0 3 4 5)`.
3. `int[1]=$a`: Yedeklenen `a` değeri (1) 1. indekse konur. Dizinin son hali: `(0 1 3 4 5)`.

## Eleman silme

Belirli bir elemanı diziden silmek için `unset` kullanılır:

```bash title="scr.sh"
#!/bin/bash

int=("1" "2" "3")

unset int[3]
echo ${int[@]}
```

```text title="Çıktı"
1 2 3
```

## Eleman sayısı

Dizideki toplam eleman sayısı `${#int[@]}` ile alınır:

```bash title="scr.sh"
#!/bin/bash

int=("1" "2" "3")

echo ${#int[@]}
```

```text title="Çıktı"
3
```
