---
title: Çalışma makinesini açma
description: AWS Console üzerinden EC2 sanal makinesi oluşturma, durdurup başlatma ve EC2 Instance Connect ile bağlanma adımları.
module: baslangic
lessons: [1]
order: 2
---

Derslerde komutları denemek için AWS üzerinde bir sanal makine (EC2 instance) kullanılıyor. Bu sayfa makinenin konsoldan nasıl açılacağını, nasıl durdurulup başlatılacağını ve tarayıcı üzerinden nasıl bağlanılacağını anlatır.

## EC2 ekranına ulaşma

1. https://aws.amazon.com/tr/console/ adresinden AWS hesabına giriş yap. **Console Home** ekranı açılır.
2. Üstteki arama kutusuna `EC2` yaz ve çıkan ilk seçeneği (**EC2 – Virtual Servers in the Cloud**) seç.
3. Açılan EC2 Dashboard'unda **Resources** bölümündeki **Instances** bağlantısına tıkla.

**Instances** ekranında oluşturulan sanal makineler listelenir. Yeni makine oluşturma ve silme işlemleri de buradan yapılır.

## Yeni sanal makine oluşturma

1. **Instances** ekranında sağ üstteki `Launch instances` butonuna tıkla. **Launch an instance** sayfası açılır.
2. Sanal makinenin özelliklerini belirle (ad, AMI, instance tipi vb.). Örnekte sağdaki **Summary** panelinde şu değerler görünüyor:
   - Software Image (AMI): Amazon Linux 2023 AMI
   - Virtual server type (instance type): `t3.micro`
   - Firewall (security group): New security group
   - Storage (volumes): 1 volume(s) - 8 GiB
3. Sağ alttaki `Launch instance` butonuyla makineyi oluştur.

## Makineyi durdurma ve başlatma

1. **EC2 → Instances** ekranına gel.
2. İşlem yapmak istediğin makineyi yanındaki onay kutusuyla seç.
3. `Instance state` menüsüne tıkla ve açılan listeden istediğin işlemi seç: `Stop instance`, `Start instance`, `Reboot instance`, `Hibernate instance` veya `Terminate (delete) instance`.

## EC2 Instance Connect ile bağlanma

Makineye hızlıca tarayıcıdan bağlanmak için:

1. Makine çalışır durumdayken (**Instance state**: Running) **Instances** listesinde makinenin **Instance ID** değerine tıkla.
2. Açılan **Instance summary** sayfasında `Connect` butonuna bas.
3. **Connect** sayfasında **EC2 Instance Connect** sekmesi seçili gelir. Hiçbir ayarı değiştirmeden sağ alttaki `Connect` butonuna tıkla. Varsayılan ayarlar:
   - Connection type: Connect using a Public IP
   - Username: `ec2-user`

Bağlantı kurulunca tarayıcıda Amazon Linux 2023 karşılama ekranıyla bir terminal açılır:

```text title="Çıktı"
Last login: Sat Nov  8 14:46:47 2025 from 203.0.113.11
```

Oturumdan çıkmak için `exit` yazıp Enter'a basman yeterli:

```bash frame="terminal"
exit
```

Terminalde görünen satırın anlamı ve ilk komutlar için [Shell ve temel komutlar](/linux/temel-komutlar/) sayfasına bak.
