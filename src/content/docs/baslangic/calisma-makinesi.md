---
title: Çalışma makinesini açma
description: AWS Console üzerinden EC2 sanal makinesi oluşturma, durdurup başlatma ve EC2 Instance Connect ile bağlanma adımları.
module: baslangic
lessons: [1]
order: 2
---

## EC2 ekranına ulaşma

1. Sanal bir makine oluşturmak için öncelikle https://aws.amazon.com/tr/console/ sitesi üzerinden amazon hesabımıza giriş yaparak aşağıdaki ekrana ulaşıyoruz.

   ![AWS Console Home ekranı](../../../assets/ekran/p001-1.webp)

2. Arama kısmına `EC2` yazarak çıkan ilk seçeneği seçerek devam ediyoruz.

   ![Konsol arama kutusunda EC2 araması ve çıkan ilk sonuç](../../../assets/ekran/p001-2.webp)

3. Açılan sayfada okla gösterilen **Instances** bölümüne tıklıyoruz.

   ![EC2 Dashboard'unda okla gösterilen Instances bağlantısı](../../../assets/ekran/p002-1.webp)

Burada oluşturduğumuz sanal makineleri görebileceğimiz, yeni sanal makineler oluşturup silebileceğimiz ekranla karşılaşıyoruz.

![EC2 Instances ekranı](../../../assets/ekran/p002-2.webp)

## Yeni sanal makine oluşturma

1. Yeni bir sanal makine oluşturmak için sağ üstte görünen **Launch instance** butonuna tıklayarak aşağıdaki ekranın açılmasını sağlıyoruz.

   ![Launch an instance sayfası ve sağdaki Summary paneli](../../../assets/ekran/p003-1.webp)

2. Burada oluşturacağımız sanal makinenin özelliklerini belirterek ilerliyoruz.
3. Ve sağ alttaki **Launch instance** butonuyla sanal makinemizi oluşturuyoruz.

## Makineyi durdurma ve başlatma

1. Oluşturduğumuz sanal makineyi durdurmak veya tekrar başlatmak için **Instances** kısmına gelerek istediğimiz sanal makineleri yanındaki buton yardımıyla seçiyoruz.

   ![Instances listesinde onay kutusuyla seçilmiş sanal makine](../../../assets/ekran/p003-2.webp)

2. Burada okla gösterilen **Instance state** menüsüne tıklayarak açılan pencereden gerçekleştirmek istediğimiz işlemi seçiyoruz.

   ![Instance state menüsünde Stop, Start, Reboot, Hibernate ve Terminate seçenekleri](../../../assets/ekran/p004-1.webp)

## EC2 Instance Connect ile bağlanma

1. Oluşturduğumuz sanal makineye hızlı ve kolay şekilde bağlanıp işlemlerimizi gerçekleştirmek için sanal makinemiz çalışır durumdayken **Instance ID** tıklıyoruz.

   ![Running durumdaki makinenin Instance ID bağlantısı](../../../assets/ekran/p004-2.webp)

2. Açılan sayfada **Connect** butonuna basarak devam ediyoruz.

   ![Instance summary sayfasında Connect butonu](../../../assets/ekran/p005-1.webp)

3. Daha sonra hiçbir ayarı değiştirmeden sağ alttaki **Connect** yazan butona tıklıyoruz.

   ![EC2 Instance Connect sekmesi ve sağ alttaki Connect butonu](../../../assets/ekran/p005-2.webp)

Böylece sanal makinemize erişmiş olduk. Çıkmak için `exit` komutunu yazıp enter'a tıklamamız yeterlidir.

![Tarayıcıda açılan Amazon Linux 2023 terminali](../../../assets/ekran/p006-1.webp)

```text title="Çıktı"
Last login: Sat Nov  8 14:46:47 2025 from 203.0.113.11
```

```bash frame="terminal"
exit
```
