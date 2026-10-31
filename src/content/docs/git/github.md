---
title: "GitHub: clone, token ve push"
description: git clone ile repository indirme, GitHub personal access token oluşturma, git pull, HEAD, git remote add ve git push -u ile yükleme.
module: git
lessons: [10, 11]
order: 3
---

## git clone

Mevcut bir repository'yi kendi bilgisayarımıza kopyalamak için:

```bash frame="terminal"
git clone repository_url
```

Örnekte eğitimin repository'si klonlandı:

```bash frame="terminal"
git clone https://github.com/ozgurozturknet/bb_devops_bootcamp.git
```

```text title="Çıktı"
Cloning into 'bb_devops_bootcamp'...
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 16 (delta 4), reused 11 (delta 1), pack-reused 0 (from 0)
Receiving objects: 100% (16/16), 449.15 KiB | 1.66 MiB/s, done.
Resolving deltas: 100% (4/4), done.
```

Repository private ise erişim yetkisini doğrulamak için kullanıcı adı ve erişim anahtarı (token) girmek gerekir.

## git push

İndirilen repository üzerinde değişiklik yapıldıktan sonra sırasıyla `git add` ve `git commit` ile değişiklikler yerelde kaydedilir. Yeni değişiklikleri projenin ana sunucusuna, yani GitHub'a geri göndermek için `git push` kullanılır. Bunun için yetki gerekir: kullanıcı adı ve erişim anahtarı istenir.

:::note[HTTPS ve SSH]
Güvenlik nedeniyle GitHub artık terminalde şifre yerine erişim anahtarı (token) kullanıyor. GitHub ile iletişim kurmanın iki yolu vardır: HTTP ve SSH.

- **HTTP** yönteminde her işlemde bir doğrulama (token) istenir. Şu an projeler bu yöntemle yönetiliyor.
- **SSH** (Secure Shell) yöntemi, bilgisayar ile GitHub arasında dijital bir "el sıkışma" gerçekleştirir. Bir kez SSH anahtarı oluşturup GitHub'a tanıtıldığında artık şifre veya token girmeden güvenli ve hızlı veri alışverişi yapılabilir. Kurulumu biraz vakit alsa da uzun vadede çok konforludur; profesyonel iş hayatında sürekli şifre/token girmemek için bu yöntem kullanılır.
:::

## Personal access token oluşturma

1. GitHub hesabına giriş yapıldıktan sonra profil resmine tıklanır ve açılan menüden **Settings** seçilir.
2. Açılan sayfanın sol menüsünün en altındaki **Developer settings** seçilir.
3. **Personal access tokens → Tokens (classic)** seçilir.
4. **Generate new token** menüsünden **Generate new token (classic)** seçilir.
5. Açılan pencerede token'ın özellikleri belirlenir:
   - `Note`: token'ın adı (örnekte "eğitimde kullandığım token")
   - `Expiration`: kaç gün geçerli olacağı (örnekte 7 gün)
   - `Select scopes`: ne için kullanılacağı (örnekte `repo` seçili)
6. `Generate token` ile token oluşturulur.

Oluşan token listede görünür. Ekrandaki uyarı: *Make sure to copy your personal access token now. You won't be able to see it again!*

```text title="Tokens (classic)"
<GITHUB_TOKEN>
```

:::caution
Token yalnızca oluşturulduğu anda gösterilir; o anda kopyalanmalıdır.
:::

Artık şifre yerine bu token kopyalanıp terminalde kullanıcı adından sonra yapıştırılarak repository'deki değişiklikler GitHub'a gönderilebilir.

## git pull

İndirilen repository üzerinde başka bir kullanıcının yaptığı değişiklikler, bizim bilgisayarımızdaki kopyada görünmez. Karşı taraftaki değişiklikleri kendi bilgisayarımıza çekmek için:

```bash frame="terminal"
git pull
```

## HEAD kavramı

Git'te **HEAD** (repository HEAD), projenin o anki güncel versiyonunu ifade eder. Bir dosya üzerinde çalışırken aslında deponun o andaki en uç noktasındaki verilerle çalışılır. HEAD, projenin "canlı" ve "son onaylanmış" halini temsil eden bir etiket gibidir.

## Yerel projeyi GitHub'a yükleme

GitHub'da oluşturulan bir projeyi bilgisayara çekmek yukarıda anlatıldı. Tersi için, yani yerelde `git init` ile başlatılmış bir repository'yi uzaktaki (remote) sunucuya yüklemek için şu adımlar izlenir.

Önce `origin` adıyla kayıtlı uzak depo adresleri sorgulanır:

```bash frame="terminal"
git remote get-url --all origin
```

```text title="Çıktı"
error: No such remote 'origin'
```

Ardından projeye "nereye gideceği" söylenir:

```bash frame="terminal"
git remote add origin url_adresi
```

Burada `origin`, repository'ye verilen bir takma isimdir. Yerine başka bir isim yazılabilir ama `origin` bir standart haline gelmiştir. Bu sayede her seferinde uzun URL'yi yazmak gerekmez.

```bash frame="terminal"
git remote add origin https://github.com/ornekkullanici/proje.git
git remote get-url --all origin
```

```text title="Çıktı"
https://github.com/ornekkullanici/proje.git
```

Proje artık `push` ile GitHub'a yüklenmeye hazırdır:

```bash frame="terminal"
git push -u origin main
```

```text title="Çıktı"
Username for 'https://github.com': ornekkullanici
Password for 'https://ornekkullanici@github.com':
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 8 threads
Compressing objects: 100% (9/9), done.
Writing objects: 100% (11/11), 1.17 KiB | 1.17 MiB/s, done.
Total 11 (delta 1), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), done.
To https://github.com/ornekkullanici/proje.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

`Password` istendiğinde şifre yerine token yapıştırılır.

`git push -u origin main` yereldeki tüm commit geçmişini GitHub'daki ana dala (`main`) yüklemekle kalmaz, `-u` parametresiyle iki uç arasında kalıcı bir takip bağı (upstream) kurar. Git hangi dalın nereye gideceğini hatırlar; projenin ilerleyen aşamalarında yalnızca `git push` yazmak yeterli olur. `-u` kullanılmazsa her push'ta Git'e hangi adrese ve hangi dala (`origin main`) gönderileceğini tekrar belirtmek gerekir. `-u` bir kez kullanılır ve "bu iki dalı birbirine eşle" talimatı verir.

:::note
`git clone` ile çekilen projede yerel proje ile GitHub'daki ana depo (remote) arasındaki bağ otomatik kurulur. Klonlanan bir projede ayrıca `git remote add origin` yazmaya gerek yoktur; Git o adresi zaten `origin` olarak kaydeder.
:::
