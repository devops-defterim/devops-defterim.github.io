---
title: Web sitesi ve GitHub
description: Mini projede site dosyalarını Git ile GitHub'a gönderme, main branch'i koruma ve siteyi script ile yayına alma.
module: mini-proje
lessons: [15]
order: 5
---

Sunucu hazır olduktan sonra web sitesi ve onu barındıracak GitHub altyapısı oluşturulur, ardından site sunucuya yüklenip süreç bir script ile otomatikleştirilir. Görevlerin tam listesi için [Görevler](/mini-proje/gorevler/) sayfasına bakın.

## Görev 11: Site dosyalarını indirme

> 11-) https://github.com/aytitech/public/raw/main/sayfa.tgz dosyasını indirin ve açın.

Dosya indirilip açıldığında içinden `onepage` klasörü çıkar. Sonraki adımlar bu klasörde yapılır.

## Git initialization

> onepage klasörüne girin ve git initialization gerçekleştirin.

Önce Git'e kullanıcı bilgileri tanıtılır (`git config --global user.email` ve `git config --global user.name`), ardından sırasıyla `git init`, `git add .` ve `git commit -m "commit_mesajı"` çalıştırılır:

```bash frame="terminal"
git config --global user.email "kullanici@example.com"
git config --global user.name "Ad Soyad"
git init
git add .
git commit -m "ilk kurulum tamamlandi"
```

```text title="Çıktı"
[master (root-commit) a06d105] ilk kurulum tamamlandi
 52 files changed, 23144 insertions(+)
 create mode 100644 _first-steps.url
 create mode 100644 _open-generator.url
 create mode 100644 ajax-email.php
 create mode 100644 assets/img/background/img-10.jpg
 create mode 100644 assets/img/background/img-56.jpg
 create mode 100644 assets/img/background/img-74.jpg
 create mode 100644 assets/img/background/img-75.jpg
 create mode 100644 assets/img/background/img-90.jpg
...
```

Bu komutlar için [Git'e giriş ve ilk ayarlar](/git/giris-ve-ayarlar/) ve [status, log, diff ve commit](/git/temel-akis/) sayfalarına bakabilirsiniz.

## GitHub reposu oluşturma

> Ardından GitHub üzerinde onepage adında public bir GitHub reposu oluşturun. README.md dosyası olmasın içinde.

1. GitHub hesabınıza giriş yapın ve sol üstteki **Top repositories** bölümünde `New` butonuna tıklayın.
2. **Create a new repository** ekranında **Repository name** alanına repo adını (`onepage`) yazın.
3. **Choose visibility** değerini `Public` bırakın.
4. **Add README** seçeneğini `Off` olarak bırakın. `.gitignore` ve lisans eklemeyin (`No .gitignore`, `No license`).
5. `Create repository` butonuna tıklayın.

## Projeyi repoya gönderme

> Bu git initialization yaptığınız projeyi yeni oluşturduğunuz repo'ya gönderin.

```bash frame="terminal"
git push -u origin main
```

```text title="Çıktı"
Enumerating objects: 62, done.
Counting objects: 100% (62/62), done.
Delta compression using up to 2 threads
Compressing objects: 100% (60/60), done.
Writing objects: 100% (62/62), 2.25 MiB | 11.79 MiB/s, done.
Total 62 (delta 3), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (3/3), done.
```

Remote, token ve push konuları için [GitHub: clone, token ve push](/git/github/) sayfasına bakabilirsiniz.

## main branch koruması

> GitHub repo'nuzun main branch'ını koruma altına alın ve 1 kişi review etmeden main branch'a merge işlemi gerçekleşemesin.

1. Oluşturulan repoya girin ve **Settings** menüsünü açın.
2. Soldaki menüden **Code and automation → Branches** seçeneğine tıklayın.
3. **Branch protection rules** bölümünde `Add classic branch protection rule` seçeneğine tıklayın.
4. **Branch name pattern** alanına `main` yazın.
5. **Protect matching branches** altında ilk iki seçeneği işaretleyin:
   - `Require a pull request before merging`
   - `Require approvals` (**Required number of approvals before merging**: `1`)
6. Kuralı kaydederek işlemi tamamlayın.

Branch ve merge kavramları için [Branch, merge ve rebase](/git/branch-merge-rebase/) sayfasına bakabilirsiniz.

## Yayına alma scripti

> Bir script yazın. Bu script sunucunuzda çalıştırıldığı zaman önce onepage reposunu `/tmp` folder'ına clonelasın (folder varsa clone çalışmasın), remote repository'deki değişiklikleri locale çeksin, `index.html` içindeki `ISIM` ve `EPOSTA` değerlerini kendi bilgilerinizle değiştirsin ve tüm dosyaları `/var/www/html` folder'ına üzerine yazarak kopyalasın.

Görevin tam metni [Görevler](/mini-proje/gorevler/#script-yazma) sayfasındadır. Notlardaki çözüm scripti aşağıdadır. Script içindeki isim ve e-posta kısımları kendi bilgilerinizle değiştirilmelidir.

:::note
Notlardaki çözüm, görev metninden farklı olarak repoyu `/tmp` yerine kullanıcının ana dizinine (`~/onepage`) clone'lar. Klasörün varlığını kontrol edip `git pull` yapmak yerine, her çalıştırmada eski klasörü silip repoyu baştan indirir.
:::

### Script dosyasını oluşturma

```bash frame="terminal"
cat > ~/script.sh << 'EOF'
#!/usr/bin/bash

# 1. Temiz bir başlangıç için eski klasörleri kontrol et
cd ~
sudo rm -rf ~/onepage

# 2. Projeyi GitHub'dan çek
echo "Proje indiriliyor..."
git clone https://github.com/ozgurozturknet/onepage.git ~/onepage
cd ~/onepage

# 3. Kişisel bilgilerini index.html dosyasına işle
echo "Bilgiler güncelleniyor..."
# Not: Orijinal dosyada ISIM ve EPOSTA anahtar kelimeleri aranıyor
sed -i 's/ISIM/Ad Soyad/g' index.html
sed -i 's/EPOSTA/kullanici@example.com/g' index.html

# 4. Dosyaları web klasörüne kopyala
echo "Web sitesi yayına alınıyor..."
sudo cp -rf ./* /var/www/html/

echo "--- Site güncel haliyle yayında ---"
EOF
```

- `cat > ~/script.sh << 'EOF'`: `EOF` satırı görülene kadar yazılan her şeyi `script.sh` adlı dosyaya kaydeder.
- `#!/usr/bin/bash`: Shebang satırıdır; sisteme bu dosyanın bir Bash scripti olduğunu ve Bash ile çalıştırılması gerektiğini söyler.

Yönlendirme ve here-document kullanımı için [Yönlendirme, pipe ve komut zincirleri](/linux/yonlendirme-ve-pipe/), script yazımı için [Giriş, read ve değişkenler](/linux/shell-scripting/giris-ve-degiskenler/) sayfalarına bakabilirsiniz.

### Script içindeki adımlar

| Komut | Açıklama |
| --- | --- |
| `cd ~` | Kullanıcının ana dizinine gider. |
| `sudo rm -rf ~/onepage` | Varsa eski proje klasörünü zorla siler; her seferinde temiz bir başlangıç sağlar. |
| `echo "..."` | Terminale bilgi mesajı yazdırır; script çalışırken hangi aşamada olduğunu anlamaya yardımcı olur. |
| `git clone https://...` | Belirtilen GitHub reposunu sunucuya indirir. |
| `cd ~/onepage` | İndirilen proje klasörüne girer. |
| `sed -i 's/ISIM/Ad Soyad/g' index.html` | `index.html` içindeki `ISIM` kelimesini bulur ve yazılan isimle değiştirir. |
| `sed -i 's/EPOSTA/.../g' index.html` | Aynı işlemi e-posta adresi için yapar. |
| `sudo cp -rf ./* /var/www/html/` | Hazırlanan tüm dosyaları web sunucusunun yayın yaptığı klasöre kopyalar. `-f` parametresi mevcut dosyaların üzerine sormadan yazılmasını sağlar. |

### Scripti çalıştırma

```bash frame="terminal"
chmod +x ~/script.sh
./script.sh
```

```text title="Çıktı"
Proje indiriliyor...
Cloning into '/home/ec2-user/onepage'...
remote: Enumerating objects: 70, done.
remote: Counting objects: 100% (70/70), done.
remote: Compressing objects: 100% (61/61), done.
remote: Total 70 (delta 8), reused 68 (delta 7), pack-reused 0 (from 0)
Receiving objects: 100% (70/70), 2.44 MiB | 37.24 MiB/s, done.
Resolving deltas: 100% (8/8), done.
Bilgiler güncelleniyor...
Web sitesi yayına alınıyor...
--- Site güncel haliyle yayında ---
```

- `chmod +x ~/script.sh`: Dosyaya çalıştırma yetkisi verir. Bu adım olmadan script yalnızca bir metin dosyası olarak kalır.
- `./script.sh`: Scripti tek seferde başlatır. Çıktıdaki "Cloning into...", "Bilgiler güncelleniyor..." gibi satırlar bu komutun sonucudur.

## Sonuç

Son adımla birlikte sanal makinenin public IP adresi tarayıcıya girildiğinde web sayfası yayında görünür. Böylece bulut ve DevOps'a giriş için bir temel atılmış olur. Sıradaki konu AWS'dir; ancak AWS'nin teknik detaylarına girmeden önce bulut bilişimin tarihine ve temel kavramlara [Sunucudan buluta](/bulut-temelleri/sunucudan-buluta/) sayfasından başlanır.
