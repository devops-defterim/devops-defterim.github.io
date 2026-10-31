---
title: Branch, merge ve conflict
description: git branch ve git checkout ile dal oluşturma ve geçiş, git merge ile birleştirme, merge conflict çözümü ve git branch -r.
module: git
lessons: [12]
order: 4
---

## Branch nedir

Bir tez yazdığımızı düşünelim. Yazıyı bitirip son halini kaydettik, sonra eklenmesi gereken yeni bir kısım çıktı. En mantıklı yol, tezin son halinin bir kopyasını çıkarıp değişikliği onun üzerinde denemektir. Branch'ler tam olarak bu işe yarar.

Projenin çalışan ve kararlı haline yeni bir özellik eklemek istendiğinde, bunu doğrudan `main` branch (ana dal) üzerinde yapıp olası hatalarla projeyi çalışmaz hale getirmek yerine yeni bir dal oluşturulur. Değişiklikler bu güvenli alanda tamamlanır, her şeyin sorunsuz çalıştığından emin olunduktan sonra dal ana dalla birleştirilir.

## Branch oluşturma ve listeleme

| Komut | İşlev |
| --- | --- |
| `git branch <branch_adi>` | Yeni branch oluşturur |
| `git branch --list` | Branch'leri listeler |
| `git checkout <branch_adi>` | Belirtilen branch'e geçer |
| `git checkout -b <branch_adi>` | Branch oluşturur ve aynı anda o branch'e geçer |
| `git branch -d <branch_adi>` | Branch'i siler |

```bash frame="terminal"
git branch titledegis
git branch --list
```

```text title="Çıktı"
* main
  titledegis
```

## Branch'ler arasında geçiş

Aşağıdaki örnekte `titledegis` branch'inde yeni bir dosya oluşturulup commit ediliyor. `main` branch'e dönüldüğünde bu dosyanın orada görünmediği görülüyor:

```bash frame="terminal"
git checkout main
ls
```

```text title="Çıktı"
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
ornek.txt       index.html      README.md
```

```bash frame="terminal"
git checkout titledegis
touch branchdosyam
git add .
git commit -m "branch için dosya eklendi"
ls
```

```text title="Çıktı"
Switched to branch 'titledegis'
[titledegis d42b7e8] branch için dosya eklendi
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 branchdosyam
branchdosyam    ornek.txt       index.html      README.md
```

```bash frame="terminal"
git checkout main
ls
```

```text title="Çıktı"
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
ornek.txt       index.html      README.md
```

## Merge

Branch üzerinde yapılan değişiklikleri ana projeye dahil etme işlemine **merge** denir. Böylece yan yolda geliştirilen özellikler ana yola (`main`) bağlanır. `main` branch'teyken:

```bash frame="terminal"
git merge branchadi
```

## Branch'i GitHub'a gönderme

Yerelde oluşturulan bir branch'i GitHub'a göndermek için önce o branch'e geçilir, ardından push yapılır:

```bash frame="terminal"
git checkout branchadı
git push -u origin branchadı
```

## Merge conflict

Kendi dalımızda çalışırken `main` branch'e de yeni commit'ler eklenir. Bu değişiklikler dosyanın farklı satırlarındaysa Git bunları kendisi birleştirir. Ancak iki dalda aynı dosyanın aynı satırında farklı değişiklikler yapılmışsa Git hangisinin doğru olduğuna karar veremez. Bu duruma **merge conflict** (birleştirme çakışması) denir.

```bash frame="terminal"
git merge titledegis
```

```text title="Çıktı"
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
```

:::note
Merge conflict bir hata değil, Git'in veri kaybını önlemek için aldığı bir güvenlik önlemidir.
:::

Böyle bir durumda Git, aynı satırda yapılan iki değişikliği de dosyaya yazar ve hangisinin doğru olduğunu sorar. Dosya açılır (`code index.html`) ve istenmeyen satırlar elle silinerek çakışma çözülür. Örnekteki `index.html` dosyası:

```html title="index.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
<<<<<<< HEAD
    <title>main branch üzerinde yapılan değişiklik</title>
=======
    <title>bulut bilisim ve devops egitim kampı</title>
>>>>>>> titledegis
</head>
<body>

</body>
</html>
```

`<<<<<<< HEAD` ile `=======` arası bulunulan daldaki (Current Change), `=======` ile `>>>>>>> titledegis` arası birleştirilmek istenen daldaki (Incoming Change) satırdır. VS Code bu bölümün üstünde `Accept Current Change | Accept Incoming Change | Accept Both Changes | Compare Changes` seçeneklerini gösterir.

## Uzak branch'leri listeleme

`git branch` normalde yalnızca yerelde oluşturulan dalları gösterir. GitHub (uzak sunucu) tarafındaki dalları görmek için:

```bash frame="terminal"
git branch -r
```

```text title="Çıktı"
  origin/main
  origin/titledegis
```

Rebase, [Detached HEAD, diff, reset ve stash](/git/detached-head-conflict-stash/) sayfasında anlatılıyor.
