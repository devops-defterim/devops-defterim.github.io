---
title: Konsol turu
description: EC2 konsolunda Dashboard, bölge seçimi, AWS Global View, Instances, Instance Types ve Launch Templates ekranlarının tanıtımı.
module: aws
lessons: [24]
order: 17
---

Teori kısmını geride bırakıp AWS ekranlarımızdan EC2 öğrenmeye geçebiliriz. Arama kısmına `EC2` yazarak ilk sıradaki seçeneğe tıklayalım.

![Konsol arama kutusunda EC2 araması ve ilk sıradaki EC2 servisi](../../../../assets/ekran/p201-1.webp)

## Dashboard

İlk öğreneceğimiz **Dashboard** sayfası. **Resources** kısmında tüm sanal makineleri ve ayrıca çalışmakta olan sanal makineleri, oluşturmuş olduğumuz volume'leri, kısaca oluşturduğumuz EC2 kaynaklarıyla ilgili temel bilgilere erişebiliriz. Hemen altında **Service health** menüsünden regionlar ile ilgili bir servis sıkıntısı varsa onlara ulaşabiliriz. Service health menüsünün solundan da yeni bir sanal makine oluşturmak için `Launch instances` butonuna tıklayabiliriz.

![EC2 Dashboard ekranında Resources, Service health ve Launch instance bölümleri](../../../../assets/ekran/p201-2.webp)

## Bölge seçimi ve AWS Global View

Farklı bölgelerde oluşturduğumuz sanal makineleri görmek için sağ üstten seçerek görebiliriz.

![Sağ üstteki bölge seçim menüsü](../../../../assets/ekran/p202-1.webp)

![Farklı bir bölge seçildiğinde EC2 Dashboard ekranı](../../../../assets/ekran/p202-2.webp)

Farklı bölgelerdeki tüm makineleri tek bir ekranda görmek için ise soldaki menüden **AWS Global View** seçeneğine tıklıyoruz.

![AWS Global View ekranında bölgelere göre kaynak sayıları](../../../../assets/ekran/p203-1.webp)

## Instances

Şimdi en çok kullanacağımız menü olan **Instances** başlığı altındakileri inceleyelim. Öncelikle Instances başlığına bakalım. Burada sanal makinelerimizi listelediğimiz ekran bulunur. Yanındaki kutucuktan seçerek aşağıdaki gibi sanal makinemiz hakkındaki tüm bilgilere erişebiliriz. AWS üzerindeki her EC2 makinenin unique bir **Instance ID**'si vardır.

![Instances listesinde seçili makinenin alt paneldeki detayları](../../../../assets/ekran/p203-2.webp)

Sanal makinemizin başlatma, durdurma gibi özelliklerini **Instance state** butonundan kontrol edebiliriz.

![Instance state menüsündeki Stop, Start, Reboot, Hibernate ve Terminate seçenekleri](../../../../assets/ekran/p204-1.webp)

Hemen yanında bulunan **Actions** butonundan ise sanal makinemizin değiştirilmesi gereken özellikler varsa onları ayarlayabiliriz.

![Actions menüsü ve Instance settings alt seçenekleri](../../../../assets/ekran/p204-2.webp)

## Instance Types

**Instance Types** başlığından da anlaşılacağı üzere sanal makinelerimizin tiplerini listeleyebileceğimiz kısım vardır. İstediğimizi seçerek detaylarına aşağıdaki gibi ulaşabiliriz.

![Instance Types listesi ve seçilen tipin detay paneli](../../../../assets/ekran/p205-1.webp)

## Launch Templates

Sürekli aynı özelliklere sahip sanal makineler oluşturmanız gerekiyorsa ve bu süreci hızlandıracak bir kısayol arıyorsanız, [Launch Templates](/aws/ec2/launch-template/) başlığı altındaki `Create launch template` butonuna tıklayarak kendi şablonlarınızı hazırlayabilirsiniz.

![Launch Templates ekranında Create launch template butonu](../../../../assets/ekran/p205-2.webp)
