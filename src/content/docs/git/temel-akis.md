---
title: status, log ve temel akış
description: git status ve git log ile durum ve geçmişi izleme, code komutu, init-add-commit akışının özeti ve repository kavramı.
module: git
lessons: [10]
order: 2
---

## git status

Yapılan işlemlerin durumunu bir rapor halinde görmek için `git status` kullanılır. Aşağıdaki örnekte bir dosya VS Code ile açılıp değiştiriliyor, ardından adım adım hazırlık alanına alınıp commit ediliyor:

```bash frame="terminal"
code ornek.txt
git status
```

```text title="Çıktı"
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   ornek.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

```bash frame="terminal"
git add ornek.txt
git status
```

```text title="Çıktı"
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   ornek.txt
```

```bash frame="terminal"
git commit -m "ornek dosyasında son değişiklik"
git status
```

```text title="Çıktı"
[main e5a64c0] ornek dosyasında son değişiklik
 1 file changed, 2 insertions(+), 1 deletion(-)
On branch main
nothing to commit, working tree clean
```

## git log

`git log`, projenin başlangıcından bugüne atılan tüm adımların dökümüdür. Kimin, ne zaman, hangi amaçla değişiklik yaptığını takip etmeyi sağlar. Bir hata oluştuğunda geçmişe dönmek veya bir özelliğin ne zaman eklendiğini bulmak için kullanılır.

```bash frame="terminal"
git log
```

```text title="Çıktı"
commit e5a64c00d4e0766e749656c40d94948b2be649aa (HEAD -> main)
Author: Ad Soyad <kullanici@example.com>
Date:   Sun Jan 25 16:12:24 2026 +0300

    ornek dosyasında son değişiklik

commit 320860ec2ce4d6d5a132876d718a678a098db687
Author: Ad Soyad <kullanici@example.com>
Date:   Sun Jan 25 16:10:32 2026 +0300

    ornek dosyasına yeni ekleme yapıldı.

commit 8dbdaaa2342ea1be3c458369c65dcfb9fce5fadd
Author: Ad Soyad <kullanici@example.com>
Date:   Sun Jan 25 15:52:32 2026 +0300

    yeni dosyalar olusturuldu
```

Daha ayrıntılı çıktı için:

```bash frame="terminal"
git log -p
```

Bir dosya üzerinde çalışıp commit ettikten sonra tekrar değişiklik yapıp bir kez daha commit edildiğinde, iki kayıt arasındaki tüm değişiklikler ve projenin o anki hali saklanır. Bu geçmişe istendiği zaman `git log` ile ulaşılır.

Tek satırlık log biçimi için [cherry-pick, tag ve log biçimleri](/git/cherry-pick-tag-log/) sayfasına bakılabilir.

## Dosyayı VS Code ile açma

Bir dosya oluşturup Visual Studio Code editörüyle açmak için `code dosyaadı` kullanılır:

```bash frame="terminal"
code README.md
ls
```

```text title="Çıktı"
README.md
```

## Akışın özeti

1. **`git init`**: Bir klasörde Git kullanmaya karar verildiğinde ilk iş budur. Klasörü Git'in denetimine sokar ve arka planda bir takip sistemi kurar. Artık klasörde yapılan her işlem Git tarafından fark edilir.
2. **`git add`**: Git, yapılan değişiklikleri habersiz kaydetmez. Bir dosyada değişiklik yapıldıktan sonra bu değişiklik onay sırasına alınır, yani dosya **hazırlık alanına (staging area)** eklenir. Bu alan, hangi dosyaların kalıcı olarak kaydedileceğinin seçildiği bir bekleme odasıdır.
3. **`git commit`**: Hazırlık alanındaki tüm dosyalar Git'in kendi veritabanına kalıcı kayıt olarak işlenir. Böylece yapılan işler versiyonlanır ve projenin o anki hali kaybolmamak üzere kaydedilir.

## Sunucu tarafı ve repository

Git dağıtık yapıdadır: proje yalnızca merkezi bir sunucuda değil, projeye dahil olan herkesin bilgisayarında bulunur. Süreç şöyle işler:

1. Geliştirici projenin son halini kendi makinesine indirir (clone).
2. İstediği değişiklikleri yapar ve önce kendi yerel veritabanına kaydeder (commit). Bu kayıt henüz sunucuya gitmemiştir.
3. Yereldeki kayıtlar sunucuya aktarılır. Geliştiricinin yetkisi varsa gönderdiği değişiklikler merkezi projeye eklenir.

Projelerin ve kayıt geçmişinin bulunduğu dijital depolara **repository (depo)** denir. Bu depolar kendi bilgisayarımızda tutulabildiği gibi, dünya çapında erişilebilir hale getirmek ve diğer geliştiricilerle ortak çalışmak için GitHub gibi bulut tabanlı platformlar merkezi depo sunucusu olarak kullanılır. GitHub'da repository oluşturmak, yerelde yeni bir proje açıp `git init` ile başlatmanın GitHub'daki karşılığıdır.

GitHub ile çalışma adımları [GitHub: clone, token ve push](/git/github/) sayfasında.
