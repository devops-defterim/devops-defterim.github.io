---
title: cherry-pick, .gitignore, tag ve log biçimleri
description: git cherry-pick ile tek commit taşıma, .gitignore dosyası, git tag ile etiketleme, git log --pretty=oneline ve git fetch origin.
module: git
lessons: [12, 13]
order: 5
---

## git cherry-pick

Bazen bir branch'te onlarca commit yapılır ama yalnızca biri o kadar kritiktir ki diğer değişiklikleri almadan yalnızca o commit'i ana dala veya başka bir dala taşımak istenir. `cherry-pick`, başka bir daldaki tüm commit'leri değil, yalnızca istenen commit'i alıp bulunulan dala uygular:

```bash frame="terminal"
git cherry-pick commit_id
```

## .gitignore

Proje klasöründeki her şeyin GitHub'a gitmesi gerekmez; bazı dosyalar hem yer kaplar hem de güvenlik riski oluşturur. GitHub'a gitmesi istenmeyen her şey `.gitignore` dosyasına yazılır. Git bu dosyayı okur ve içindeki dosyaları hiç yokmuş gibi görmezden gelir. Böylece proje daha güvenli olur ve yalnızca gerekli dosyalar paylaşılır.

Bunun için projenin kök (root) klasöründe `.gitignore` adlı bir dosya oluşturulur. Diğer dosyalarda olduğu gibi bu dosya için de sırasıyla `git add` ve `git commit` çalıştırılır.

## git tag

Commit ID'ler karmaşıktır ve akılda tutulamaz. Tag ile bu ID'lere istenen isimler verilebilir. İki yöntem vardır:

| Komut | Sonuç |
| --- | --- |
| `git tag etiket_ismi commit_id` | Basit bir etiket koyar |
| `git tag -a etiket_ismi commit_id -m "mesaj"` | Açıklamalı etiket oluşturur; tag'in ne zaman, kim tarafından ve niçin eklendiği bilgisini de verir |
| `git tag etiket_ismi` | Etiketi son commit'e koyar |
| `git tag -d etiket_ismi` | Tag'i siler |

Oluşturulan tag'ler standart `git push` ile GitHub'a gönderilmez. Tek bir tag'i göndermek için:

```bash frame="terminal"
git push origin etiket_ismi
```

Tüm tag'leri tek seferde göndermek için:

```bash frame="terminal"
git push origin --tags
```

## git log --pretty=oneline

Normalde `git log` her kayıt için yazar, tarih, commit ID ve mesaj gibi 4-5 satırlık yer kaplar. Projede 50 commit varsa aranan kaydı bulmak için sayfalarca aşağı inmek gerekir. Her commit'i (ID ve mesajı) tek satırda listelemek için:

```bash frame="terminal"
git log --pretty=oneline
```

```text title="Çıktı"
125696f4aef808140e654d8aae15377da041e90e (HEAD -> main) çakışmalar düzeltildi
9584415128c469d600d0b7bdcc6998f40dd684dc (origin/main) main üzerindeki degisiklik
d42b7e8ab22a6584d81eacca5c828a3ef94fdfd7 (origin/titledegis, titledegis) branch için dosya eklendi
97c5029a7445693644aa83dea9dd4835f952c0a4 silind
aaa45a57c312b9207b3edb7668f79e886da961f0 branch için dosya ekledim
e5a64c00d4e0766e749656c40d94948b2be649aa ornek dosyasında son değişiklik
320860ec2ce4d6d5a132876d718a678a098db687 ornek dosyasına yeni ekleme yapıldı.
8dbdaaa2342ea1be3c458369c65dcfb9fce5fadd yeni dosyalar olusturuldu
```

- İlk satırdaki `HEAD -> main`, bilgisayardaki çalışma alanının en son yapılan commit ile eşleştiğini, yani yerel sistemin güncel olduğunu gösterir.
- İkinci satırdaki `origin/main`, GitHub'daki `origin` sunucusunda `main` dalının bilgisayardaki son commit ile eşleşmediğini gösterir. İkisini eşlemek için yerel değişiklik `git push` ile GitHub'a gönderilir.

Push sonrasında aynı komut `origin/main`'in de son commit'te olduğunu gösterir:

```text title="Çıktı"
125696f4aef808140e654d8aae15377da041e90e (HEAD -> main, origin/main) çakışmalar düzeltildi
9584415128c469d600d0b7bdcc6998f40dd684dc main üzerindeki degisiklik
...
```

## git fetch origin

GitHub'da yapılan bir değişikliği yerelde görmek için `git pull` kullanılır. Ancak gelen değişiklikleri her zaman hemen kodlara dahil etmek istemeyebiliriz. Yalnızca "neler değişmiş" bilgisini görmek için:

```bash frame="terminal"
git fetch origin
```

`git fetch origin` gelen değişiklikleri bilgisayara indirir ama mevcut kodlarla birleştirmez, yani merge işlemini otomatik yapmaz. Amaç, değişiklikleri önce güvenli şekilde görmek, ardından emin olunca kontrollü biçimde dahil etmektir.
