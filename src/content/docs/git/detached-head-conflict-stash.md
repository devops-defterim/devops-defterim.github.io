---
title: Detached HEAD, diff, reset ve stash
description: Detached HEAD, git diff ile farkları görme, git rm, merge ile rebase farkı, git reset seçenekleri ve git stash ile yarım işi saklama.
module: git
lessons: [13]
order: 6
---

## Detached HEAD

Bilgisayarda checkout olunan yer `main` dalı değil de farklı bir commit ise buna **Detached HEAD** denir.

Belirli bir commit'i sisteme çekmek için:

1. `git log --pretty=oneline` ile commit'ler listelenir.
2. İstenen commit ID kopyalanır ve o commit'e checkout olunur (`git checkout commit_id`).
3. Burada yeni bir branch oluşturulur.
4. `main` branch'e geçilir ve `git merge branch_adı` ile istenen commit sisteme alınır.

## git diff

`git diff` ile dosyalar ve commit'ler arasındaki farklara bakılır:

| Komut | Gösterdiği fark |
| --- | --- |
| `git diff` | Son commit'ten bu yana yapılan değişiklikler |
| `git diff branch_adi1 branch_adi2` | İki branch arasındaki fark |
| `git diff commit_id1 commit_id2` | İki commit arasındaki fark |

```bash frame="terminal"
git diff main titledegis
```

```text title="Çıktı"
diff --git a/index.html b/index.html
index 4b4f039..103b178 100644
--- a/index.html
+++ b/index.html
@@ -3,7 +3,6 @@
 <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
-
     <title>bulut bilisim ve devops egitim kampı</title>
 </head>
 <body>
```

## git rm

Bir dosya oluşturulup `git add` ile takibe alındıktan sonra vazgeçilirse `git rm dosya_adi` ile dosya hem bilgisayardan hem projeden tamamen silinir. Dosya yalnızca Git'in takibinden çıkarılıp bilgisayarda tutulmak isteniyorsa komutun sonuna `--cached` eklenir:

```bash frame="terminal"
git rm dosya_adi
git rm dosya_adi --cached
```

:::note
Her iki durumda da işlemin kalıcı olması için ardından commit yapmak gerekir.
:::

```bash frame="terminal"
ls
git rm branchdosyam
ls
git status
```

```text title="Çıktı"
branchdosyam    ornek.txt       index.html      README.md
rm 'branchdosyam'
ornek.txt       index.html      README.md
On branch titledegis
Your branch is up to date with 'origin/titledegis'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        deleted:    branchdosyam
```

```bash frame="terminal"
git commit -m "Gereksiz olan branchdosyam silindi"
git status
```

```text title="Çıktı"
[titledegis c626c39] Gereksiz olan branchdosyam silindi
 1 file changed, 0 insertions(+), 0 deletions(-)
 delete mode 100644 branchdosyam
On branch titledegis
Your branch is ahead of 'origin/titledegis' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

## Merge ve rebase

Farklı dallarda çalışmak özgürce kod yazmayı sağlar. İş bitip dallar ana dalla birleştirilmek istendiğinde iki yol vardır:

- **Merge:** Klasik merge yöntemiyle birleştirildiğinde dalların ayrılıp tekrar birleştiği karmaşık "örümcek ağı" görüntüsü ana geçmişte (history) kalır. Proje büyüdükçe geçmişin okunması zorlaşabilir.
- **Rebase:** Proje geçmişini tek bir düz çizgide, sanki her şey sırayla yapılmış gibi görmek için kullanılır. Rebase, farklı bir dalda yapılan tüm işlemleri alır ve ana dalın en ucuna ekleyerek tüm geçmişi tek bir satıra (single line) dizer. Karmaşık dallanma görüntüleri ortadan kalkar; projenin gelişimi bir kitap gibi düz bir çizgide okunur.

Merge'ün kullanımı [Branch, merge ve conflict](/git/branch-merge-rebase/) sayfasında.

## git reset

Çalışırken hatalı bir commit yapılabilir, yanlış dosyalar hazırlık alanına (staging area) eklenebilir ya da proje birkaç adım geriye döndürülmek istenebilir. `git reset`, Git'in en güçlü "geri alma" aracıdır.

En temel haliyle `git reset`, projenin o anki durumunu geçmişteki belirli bir commit'e geri döndürür. Geri dönüşün "sertliği" kullanılan parametreye göre değişir:

| Komut | Etkisi |
| --- | --- |
| `git reset --soft commit_id` | Yalnızca commit'i iptal eder. Kodlara dokunmaz, onları hazırlık alanında (staged) tutar. "Commit mesajını yanlış yazdım ama kodlarım kalsın" durumunda kullanılır. |
| `git reset --mixed commit_id` | Varsayılandır. Commit'i iptal eder ve dosyaları hazırlık alanından çıkarır. Kodlar bilgisayarda durur ama Git onları henüz takip etmiyor gibidir. |
| `git reset --hard commit_id` | Belirlenen commit'ten sonra yapılan tüm değişiklikleri fiziksel olarak siler ve projeyi tamamen o ana döndürür. |

:::danger
`git reset --hard` en tehlikeli ve kesin olan seçenektir; belirtilen commit'ten sonraki değişiklikler silinir.
:::

Yanlışlıkla `git add .` ile tüm klasör hazırlık alanına eklendiyse, yalnızca o dosyaları çıkarmak için `git reset` yeterlidir:

```bash frame="terminal"
git reset
```

## git stash

Bir iş üzerinde çalışırken, değişiklikler commit'e hazır olmadan başka bir branch'e geçmek gerekebilir. Bu durumda `git stash` kullanılır: mevcut klasördeki tamamlanmamış değişiklikler bir kenara kaydedilir.

| Komut | İşlev |
| --- | --- |
| `git stash` | Tamamlanmamış değişiklikleri saklar |
| `git stash list` | Saklanan kayıtları listeler |
| `git stash pop` | En son saklanan kaydı geri getirir ve işe kalınan yerden devam edilir |
| `git stash drop` | Saklanan kaydı siler |

Birden fazla stash kaydı varsa `git stash pop` yalnızca en sonuncuyu geri getirir. Belirli bir kaydı geri getirmek için `git stash list` çıktısındaki ID'si (örneğin `stash@{0}`) kullanılır.

## Yerelden GitHub'a

Buraya kadarki işlemlerin hepsi yerelde, kendi bilgisayarımızda yapıldı. Gerçek hayatta projeler kişisel bilgisayarlarda kalmaz; başkalarıyla paylaşılması, yedeklenmesi ve ekipçe yönetilmesi gerekir.

Git bir versiyon kontrol sistemiyken GitHub bu sistemin üzerine kurulmuş bir bulut platformudur. Terminalden GitHub'ın görsel arayüzüne geçmenin temel sebebi, projeleri internete taşıyarak her yerden erişilebilir hale getirmek ve diğer yazılımcılarla iş birliği yapabilmektir.
