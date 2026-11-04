---
title: EC2 Instance Connect ile bağlanma
description: Çalışan EC2 sanal makinesine tarayıcıdan EC2 Instance Connect ile bağlanma.
module: baslangic
lessons: [1]
order: 4
prev:
  link: /baslangic/makineyi-durdurma-ve-baslatma/
  label: Makineyi durdurma ve başlatma
next:
  link: /linux/isletim-sistemi-ve-shell/
  label: İşletim sistemi, terminal ve shell
---

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
