---
title: Launch template
description: Seçilen instance özelliklerini launch template olarak kaydedip bu şablondan hızlıca yeni EC2 makineleri başlatma.
module: aws
lessons: [25]
order: 21
---

Instance oluşturmayı seçtiğimiz özelliklerle otomatikleştirmek istersek **Launch Templates** menüsünü kullanırız. Şablon bir kez hazırlandıktan sonra aynı özelliklerde makineleri her seferinde tüm adımları tekrarlamadan oluşturabiliriz.

## Şablon oluşturma

1. **EC2 → Launch Templates** yolunu izleyin ve `Create launch template` butonuna tıklayın.
2. **Launch template name and description** bölümünde bir isim (**Launch template name**, ör. `ornek-template`) ve açıklama (**Template version description**) girin.
3. **Application and OS Images (Amazon Machine Image)** bölümünde sanal makinelerin oluşturulacağı AMI'yi seçin (örnekte Amazon Linux 2023).
4. **Instance type** bölümünde sanal makine tipini seçin (örnekte `t3.micro`).
5. **Key pair (login)** bölümünde kullanmak istediğiniz key pair'i seçin.
6. Network settings, Storage (volumes), Resource tags ve Advanced details bölümlerini [Instance oluşturma](/aws/ec2/instance-olusturma/) sayfasında anlatılan ayarlara göre istediğiniz şekilde düzenleyin.
7. `Create launch template` butonuna tıklayın.

## Şablondan instance başlatma

1. **Launch Templates** listesinde oluşturduğunuz şablonu seçin.
2. **Actions → Launch instance from template** seçeneğine tıklayın.
3. Açılan **Launch instance from template** ekranında **Source template** ve sürüm (`1 (Default)`) seçili gelir; şablondaki ayarlar doldurulmuş olarak görünür.
4. `Launch instance` butonuna tıklamanız yeterlidir.

Böylece belirlediğimiz özellikleri bir şablon olarak kullanıp daha hızlı sanal makineler oluşturabiliriz.
