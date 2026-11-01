---
title: Launch template
description: Seçilen instance özelliklerini launch template olarak kaydedip bu şablondan hızlıca yeni EC2 makineleri başlatma.
module: aws
lessons: [25]
order: 21
---

Instance oluşturmayı seçtiğimiz özelliklerde otomatize etmek istersek **Launch Templates** menüsünden ayarlayabiliriz.

## Şablon oluşturma

1. `Create launch template` butonuna tıklayarak başlayalım.

   ![Launch Templates ekranında Create launch template butonu](../../../../assets/ekran/p220-1.webp)

2. Bir isim ve açıklama ekleyerek devam edelim.

   ![Launch template name and description alanları](../../../../assets/ekran/p220-2.webp)

3. Sanal makinelerimizi oluşturacağımız AMI ile devam ediyoruz.

   ![Launch template için Application and OS Images bölümü](../../../../assets/ekran/p220-3.webp)

   ![Launch template için seçilen Amazon Linux AMI](../../../../assets/ekran/p221-1.webp)

4. Sanal makine tipini seçiyoruz.

   ![Launch template için Instance type seçimi](../../../../assets/ekran/p221-2.webp)

5. Kullanmak istediğimiz key pair'i seçiyoruz.
6. Sanal makine oluştururken öğrendiğimiz tüm ayarları istediğimiz şekilde düzenleyerek `Create launch template` diyoruz.

## Şablondan instance başlatma

Ve oluşturduğumuz launch template'i seçerek **Actions** menüsü altından **Launch instance from template** seçeneğine tıklıyoruz.

![Launch Templates listesinde Actions menüsünden Launch instance from template](../../../../assets/ekran/p221-3.webp)

Artık belirlediğimiz özellikleri bir şablon olarak kullanıp daha hızlı sanal makineler oluşturabiliriz. Bunun için yalnızca `Launch instances` butonuna tıklamamız yeterli.

![Launch instance from template ekranında şablon ayarları ve Launch instance butonu](../../../../assets/ekran/p221-4.webp)
