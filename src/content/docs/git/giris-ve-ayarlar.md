---
title: Git'e giriş ve ilk ayarlar
description: Versiyon kontrol sistemleri, Git'in dağıtık yapısı, git config ile ilk ayarlar ve git init, git add, git commit ile ilk kayıt.
module: git
lessons: [9, 10]
order: 1
---

## Versiyon kontrol sistemleri

Yazılım geliştirmede en büyük zorluklardan biri, birden fazla kişinin aynı dosyalar üzerinde birbirinin emeğini ezmeden çalışabilmesidir. Birden fazla kişi aynı anda birden fazla dosyada değişiklik yapıyorsa, bu değişikliklerin bir araya getirilip tek bir proje haline getirilmesi için araçlar kullanılır.

Tek başına çalışırken bile her gün eklenen veya çıkarılan kod satırlarını takip etmek gerekir; yanlışlıkla yapılan bir işlem, farkında olmadan programı çalışmaz hale getirebilir. Tüm değişikliklerin kaydı tutulsaydı, ne zaman nasıl bir değişiklik yapıldığı görülür ve hata daha kolay bulunurdu. Bu sorunları çözmek için versiyon kontrol sistemleri geliştirilmiştir.

**Versiyon kontrol sistemleri**, yönetim altına alınan dosyaların birden fazla kişi tarafından aynı anda değiştirilebilmesini, bu sırada çıkabilecek sorunların çözülmesini ve dosyalarda kimin, ne zaman, neyi değiştirdiğinin kayıt altına alınmasını sağlayan araçlardır. Bunların en bilineni Git'tir.

## Git

Git, projelerdeki her satır değişikliğinin kim tarafından ve ne zaman yapıldığını kaydeden, dağıtık yapısı sayesinde projenin tam bir kopyasını her geliştiricide saklayan modern bir versiyon kontrol sistemidir. Hem ekip içi çakışmaları önler hem de projenin geçmişinde güvenle gezinmeyi sağlar.

Git'in diğer versiyon kontrol sistemlerinden farkı **decentralized** (dağıtık) olmasıdır: projenin yalnızca merkezi bir sunucuda değil, projeye dahil olan herkesin bilgisayarında tam bir kopyası bulunur. Bu sayede internet olmadan da çalışılabilir ve ana sunucu çökse bile proje kaybolmaz.

Git terminalden kullanılır.

## İlk ayarlar

Git'i kullanmaya başlamadan önce bazı temel ayarlar yapılır. Git'te kaydedilen her değişikliğin bir sahibi olmalıdır; bu yüzden önce işlemlerin kime ait olduğu belirtilir.

Kullanıcı adını tüm projelerde geçerli olacak şekilde tanıtmak için:

```bash frame="terminal"
git config --global user.name "Kullanıcı Adınız"
```

Ardından e-posta adresi tanıtılır. Buradaki adres, GitHub hesabına kayıt olunan e-posta adresiyle aynı olmalıdır:

```bash frame="terminal"
git config --global user.email "mail adresiniz"
```

Son olarak, yeni oluşturulan her Git projesinde varsayılan ana dal adının otomatik olarak `main` olması için:

```bash frame="terminal"
git config --global init.defaultBranch main
```

Böylece projeler GitHub gibi platformlarla birleştirilirken isim farklılıklarından doğabilecek karışıklıkların önüne geçilir.

### Komut yapısı

Git komutları üç parçadan oluşur: ana komut (`git`), yapılacak eylem ve bu eylemin nasıl yapılacağını belirleyen seçenekler.

### git config --list

Git'te tanımlı tüm yapılandırma ayarlarını (kullanıcı adı, e-posta, varsayılan branch adı, editör ayarları vb.) tek ekranda listeler. O ana kadar yapılan ayarların özetini görmek için kullanılır:

```bash frame="terminal"
git config --list
```

```text title="Çıktı"
credential.helper=osxkeychain
init.defaultbranch=main
user.name=Ad Soyad
user.email=kullanici@example.com
filter.lfs.clean=git-lfs clean -- %f
filter.lfs.smudge=git-lfs smudge -- %f
filter.lfs.process=git-lfs filter-process
filter.lfs.required=true
http.version=HTTP/1.1
init.defaultbranch=main
```

## Çalışma klasörü ve git init

Komutları, gerekli verileri ve alıştırmaları tutmak için bir çalışma klasörü oluşturmak işi kolaylaştırır:

```bash frame="terminal"
mkdir git
```

Bir klasördeki işlemlerin Git tarafından izlenmesi ve kaydedilmesi için Git'in üç aşamalı takip mekanizması başlatılmalıdır. Bir projede Git kullanmak için ilk iş, o klasörde Git'i başlatmaktır (initialize). Bundan sonra Git klasör içinde olup bitenleri takip edebilir:

```bash frame="terminal"
git init
```

```text title="Çıktı"
Initialized empty Git repository in /Users/ornekkullanici/git/proje/.git/
```

## Staging: git add

Git, yapılan değişiklikleri otomatik olarak kalıcı kayda dönüştürmez. Değişiklikler yapılır, ardından Git'e bu dosyaların bir sonraki kayda dahil edilmeye hazır olduğu söylenir (staging):

```bash frame="terminal"
git add dosyaadı
```

`git add .` kullanılırsa bulunulan klasördeki tüm değişmiş dosyalar hazırlık alanına alınır.

## Kayıt: git commit

Git'in her şeyi otomatik kaydetmemesinin sebebi, hangi değişikliğin önemli olup hangisinin olmadığını seçme şansı vermesidir. Sürecin sonunda hazırlanan değişiklikler Git'e kaydedilir (commit) ve projenin o anki hali kalıcı hale gelir:

```bash frame="terminal"
git commit -m "yorum satırı"
```

Örnek:

```bash frame="terminal"
git commit -m "yeni dosyalar olusturuldu"
```

```text title="Çıktı"
[main (root-commit) 8dbdaaa] yeni dosyalar olusturuldu
 3 files changed, 13 insertions(+)
 create mode 100644 README.md
 create mode 100644 ornek.txt
 create mode 100644 index.html
```

Durumu izleme ve geçmişi görme komutları [status, log ve temel akış](/git/temel-akis/) sayfasında.
