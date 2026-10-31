---
title: IAM kavramları
description: IAM'in dört temel objesi olan user, group, policy ve role ile root account'un rolü ve güvenli kullanımı.
module: aws
lessons: [19]
order: 2
---

## Dört temel obje

IAM servisi altında dört temel obje bulunur: **user**, **group**, **policy** ve **role**.

| Obje | Görevi |
| --- | --- |
| User | AWS hesabını kullanacak insanların veya uygulamaların kendilerini tanıtmak için kullandığı obje |
| Group | Birden fazla kullanıcı hesabını daha kolay yönetmek için kullanılan obje |
| Policy | Bir kimliğin neler yapabileceğini satır satır listeleyen yetki tanımı |
| Role | Kalıcı şifresi olmayan, ihtiyaç anında geçici olarak üstlenilen yetki kimliği |

## Policy

AWS'nin bütün authorization altyapısı policy objeleri üzerine kuruludur. AWS'de bir user oluşturup bu kullanıcıyla ilk kez giriş yaptığımızda hesapta hiçbir hak yoktur. Kullanıcının neler yapabilmesini istiyorsak bunları bir dosyaya satır satır yazmak gerekir; örneğin "EC2'da sanal makine yaratabilir", "S3'te bucket yaratabilir" gibi. Bu listelere policy denir. Oluşturulan liste kullanıcıya atanır ve kullanıcı AWS'yi belirlenmiş yetkilerle kullanabilir hale gelir.

## Role

Yetkileri bir insana değil de doğrudan AWS üzerinde çalışan bir servise veya uygulamaya vermek istediğimizde, mimarinin en can alıcı parçalarından biri olan **Role** objesi devreye girer.

Role yapısal olarak bir user'a çok benzer; onun da neler yapabileceğini belirleyen ve üzerine iliştirilmiş policy listeleri vardır. Aralarındaki en büyük ve en kritik fark şudur: User'ların kalıcı kimlik bilgileri (kullanıcı adı/şifre veya statik erişim anahtarları) bulunurken Role'lerin kalıcı şifreleri yoktur. Bir Role, ihtiyaç anında geçici olarak "giyilen bir üniforma" veya "takılan bir şapka" gibidir.

### Örnek senaryo: EC2'dan S3'e erişim

Diyelim ki AWS üzerinde bir EC2 sanal sunucusu ayağa kaldırdınız ve içine yazdığınız bir deployment betiğinin S3 bucket'ınızdan bir yapılandırma dosyası okuması gerekiyor.

Bu işlemi bir User objesiyle yapmaya kalksaydınız, o kullanıcıya ait gizli erişim anahtarlarını sunucunun içine, script dosyalarınızın arasına sabit olarak yazmanız gerekirdi.

:::danger
Erişim anahtarlarını kodun içine sabit yazmak bulut güvenliğinde yapılan en büyük hatalardan biridir. Kodlarınız yanlışlıkla bir GitHub deposuna sızarsa tüm AWS hesabınızın kontrolü dakikalar içinde kötü niyetli kişilerin eline geçebilir.
:::

Role objesi bizi bu güvenlik riskinden kurtarır. Süreç tamamen otomatik ve şifresiz ilerler:

1. "S3'ten dosya okuyabilir" yetkisine sahip bir Policy oluşturulur.
2. Bir Role yaratılır ve bu Policy, Role'e bağlanır.
3. Role, kodların çalıştığı EC2 sunucusuna atanır. Artık EC2 sunucusu bu rolü üstlenmiştir.
4. Script çalıştığında EC2 sunucusu arka planda AWS'den bizim adımıza birkaç saatliğine geçerli geçici güvenlik anahtarları (temporary credentials) talep eder.
5. Sunucu S3'e gidip "Ben bu role sahibim ve yetkim var" diyerek işlemi güvenle gerçekleştirir. İşlem bitince veya süre dolunca bu geçici anahtarlar kendiliğinden imha olur.

Özetle User objesi "Sen kimsin?" sorusuna kalıcı bir cevap ararken, Role objesi servislerin ve uygulamaların birbiriyle güvenli, şifresiz ve esnek bir şekilde konuşmasını sağlayan bir yetki devri mekanizmasıdır. Rol oluşturma ve EC2'ya atama adımları [IAM rolleri ve ARN](/aws/iam/roller-ve-arn/) sayfasında.

## Root account

User'lar içinde en önemli ve özel olanı **root account**'tur. Bir AWS hesabı ilk oluşturulduğunda otomatik olarak ortaya çıkan bu hesap, sistemde mutlak güce sahip en yetkili kimliktir. Tüm hesap ayarları bu hesap üzerinden yönetilebilir.

:::caution
Root hesap günlük operasyonlar için kullanılmaz. Root hesapla ilk girişte günlük işleri yürütecek yetkili bir "Admin IAM User" oluşturulur, root hesabın güvenliği artırılır (ör. [MFA](/aws/iam/kullanici-mfa-access-key/#mfa-ekleme)) ve zorunlu haller (fatura ayarları, hesabı kapatmak vb.) dışında root hesap bir kenara bırakılır.
:::
