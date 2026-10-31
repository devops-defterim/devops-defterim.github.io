---
title: Görevler
description: Mini projenin amacı ve notlarda verilen sunucu, disk, GitHub ve otomasyon görevlerinin çözümsüz listesi.
module: mini-proje
lessons: ["talimat"]
order: 1
---

## Projenin amacı

Bu mini proje, o ana kadar öğrenilen Linux ve Git konularını pekiştirmek ve uygulama sırasında yeni yetkinlikler kazanmak için hazırlanmış uçtan uca küçük bir simülasyondur. Amaç, bir Cloud Engineer'ın günlük iş akışını deneyimlemektir:

- AWS üzerinde bir sunucu kurmak ve üzerinde gerekli ayarları yapmak,
- web sitesini ve onu barındıracak GitHub altyapısını oluşturmak,
- siteyi sunucuya yükleyip herkesin görebileceği hale getirmek ve tüm süreci bir script ile otomatik çalışır hale getirmek.

Görevlere başlamak için [AWS Console](https://aws.amazon.com/tr/console/) üzerinden oturum açılır.

:::note
Bu sayfada yalnızca görevler yer alır. Her görevin altındaki bağlantı, çözümün anlatıldığı sayfaya gider.
:::

## Sunucuyu kurma

### 1. EC2 instance oluşturma

1-) Amazon Linux 2023 AMI'dan bir adet t3.micro tipinde EC2 instance yaratın. Key pair login seçeneğiyle yeni bir keypair oluşturun. Dış dünyadan bu oluşturduğunuz instance'a SSH22 ve HTTP80 portlarından erişilebilir olsun.

Çözüm: [Sunucuyu açma ve SSH → Görev 1](/mini-proje/sunucu-ve-ssh/#görev-1-ec2-instance-oluşturma)

### 2. SSH ile bağlanma

2-) Oluşturduğunuz bu makineye kendi makinenizden ssh aracılığıyla bağlanın.

Çözüm: [Sunucuyu açma ve SSH → Görev 2](/mini-proje/sunucu-ve-ssh/#görev-2-ssh-ile-bağlanma)

### 3. Sistemi güncelleme

3-) Sistemi ve sistemde yüklü paketleri güncelleyin.

Çözüm: [Sunucu kurulumu → Görev 3](/mini-proje/sunucu-kurulumu/#görev-3-sistemi-güncelleme)

### 4. Git kurulumu

4-) Git uygulamasını yükleyin.

Çözüm: [Sunucu kurulumu → Görev 4](/mini-proje/sunucu-kurulumu/#görev-4-git-kurulumu)

### 5. Yeni kullanıcı

5-) Yeni bir kullanıcı ekleyin. Bu kullanıcının şifre sormadan sudo yapabilmesini sağlayın.

Çözüm: [Sunucu kurulumu → Görev 5](/mini-proje/sunucu-kurulumu/#görev-5-yeni-kullanıcı-ve-sudo-yetkisi)

### 6. /evim klasörü ve home directory

6-) Root'da /evim diye bir klasör oluşturun. Bu klasörün owner ve grup değerlerini bu yeni oluşturduğunuz kullanıcı ve bu kullanıcının ana grubu olarak değiştirin. Ardından bu kullanıcının home directory'sinin /evim klasörü olmasını sağlayacak işlemi yapın.

Çözüm: [Sunucu kurulumu → Görev 6](/mini-proje/sunucu-kurulumu/#görev-6-evim-klasörü-ve-home-directory)

### 7. Network interface

7-) AWS üstünden yeni bir network interface ekleyin ve bunu makinenize attach edin. Sonra bu interface'e 10.10.10.10/255.255.255.0 ip adresini ekleyin.

Çözüm: [Sunucu kurulumu → Görev 7](/mini-proje/sunucu-kurulumu/#görev-7-network-interface-ekleme)

### 8. Route tanımı

8-) 199.199.199.0/24 adreslerine giderken bu yeni interface üstünden gitmesini sağlayacak route tanımı yapın.

Çözüm: [Sunucu kurulumu → Görev 8](/mini-proje/sunucu-kurulumu/#görev-8-route-tanımı)

### 9. Apache Web Server

9-) Apache Web Server (httpd) servisini sisteme yükleyin. Bilgisayar yeniden başlatıldığında bu servisin de otomatik olarak çalışmasını sağlayacak ayarı da yapın.

Çözüm: [Sunucu kurulumu → Görev 9](/mini-proje/sunucu-kurulumu/#görev-9-apache-web-server-httpd)

### 10. EBS volume

10-) 4gb boyutunda bir EBS Volume yaratın ve bunu oluşturduğunuz instance'a bağlayın. Bunun üzerinde tüm disk boyutunu kullanan tek bir partition yaratın ve xfs dosya sistemiyle formatlayın.

Çözüm: [Ek disk → Görev 10](/mini-proje/ek-disk/#görev-10-ebs-volume-oluşturma-ve-formatlama)

## Web sitesi ve GitHub

### 11. Site dosyalarını indirme

11-) https://github.com/aytitech/public/raw/main/sayfa.tgz dosyasını indirin ve açın.

Çözüm: [Web sitesi ve GitHub → Görev 11](/mini-proje/web-sitesi-ve-github/#görev-11-site-dosyalarını-indirme)

### Git initialization

onepage klasörüne girin ve git initialization gerçekleştirin.

Çözüm: [Web sitesi ve GitHub → Git initialization](/mini-proje/web-sitesi-ve-github/#git-initialization)

### GitHub reposu oluşturma

Ardından GitHub üzerinde onepage adında public bir GitHub reposu oluşturun. README.md dosyası olmasın içinde.

Çözüm: [Web sitesi ve GitHub → GitHub reposu oluşturma](/mini-proje/web-sitesi-ve-github/#github-reposu-oluşturma)

### Projeyi repoya gönderme

Bu git initialization yaptığınız projeyi yeni oluşturduğunuz repo'ya gönderin.

Çözüm: [Web sitesi ve GitHub → Projeyi repoya gönderme](/mini-proje/web-sitesi-ve-github/#projeyi-repoya-gönderme)

### main branch koruması

GitHub repo'nuzun main branch'ını koruma altına alın ve 1 kişi review etmeden main branch'a merge işlemi gerçekleşemesin.

Çözüm: [Web sitesi ve GitHub → main branch koruması](/mini-proje/web-sitesi-ve-github/#main-branch-koruması)

## Siteyi yayına alma ve otomasyon

### Script yazma

Bir script yazın. Bu script sunucunuzda çalıştırıldığı zaman:

1. İlk olarak `git clone` ile onepage GitHub reposunu `/tmp` folder'ına clonelasın. Bu işlem sadece ilk defa indireceğiniz zaman ya da makine kapatılıp açıldığında işe yarayacaktır, çünkü makine kapanıp açıldığında tmp folder'ı temizlenir. Bu nedenle script önce bu folder var mı diye baksın. Folder yoksa `git clone` çalışsın, varsa çalışmasın.
2. Scripte devam edin ve bu onepage folder'ına girerek remote repository'deki değişiklikleri locale çekin.
3. Ardından `index.html` dosyasının içindeki `ISIM` kelimesini kendi isminizle, `EPOSTA` değerini de kendi e-posta adresinizle değiştirin.
4. Son olarak onepage folder'ının içindeki tüm dosyaları `/var/www/html` folder'ına kopyalayın. Eğer bu folder'da aynı isimli dosyalar varsa bunların üzerine yazsın.

Çözüm: [Web sitesi ve GitHub → Yayına alma scripti](/mini-proje/web-sitesi-ve-github/#yayına-alma-scripti)
