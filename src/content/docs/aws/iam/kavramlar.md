---
title: IAM kavramları
description: IAM'in dört temel objesi olan user, group, policy ve role ile root account'un rolü ve güvenli kullanımı.
module: aws
lessons: [19]
order: 2
---

## Dört temel obje

IAM servisi altında dört adet temel obje bulunur. Bunlar **user**, **group**, **role**, **policy** isimli objelerdir. User, AWS hesabını kullanacak insanların veya uygulamaların kendilerini tanıtabilmeleri için kullanacakları objedir. Birden fazla hesabımız varsa ve bu hesapları daha kolay yönetmek istiyorsak group objesini kullanırız.

## Policy

AWS'nin bütün authorization altyapısının üzerine kurulmuş olduğu policy objeleri vardır. AWS üzerinde bir user oluşturup bu kullanıcı ile ilk giriş yaptığımız zaman bu hesapta hiçbir hak mevcut değildir. Bir user'ın neler yapabilmesini istiyorsak bunları bir dosyaya satır satır yazmak gerekir. Örneğin EC2'da sanal makine yaratabilir, S3'te bucket yaratabilir gibi. Bu oluşturulan listelere policy denir. Daha sonrasında oluşturulan bu listeyi kullanıcıya atıyoruz ve belirlenmiş yetkilerle AWS'yi kullanabilir hale geliyor.

## Role

Peki ya bu yetkileri bir insana değil de, doğrudan AWS üzerinde çalışan bir servise veya uygulamaya vermek istersek ne olacak? İşte bu noktada, mimarinin en can alıcı parçalarından biri olan **Role** objesi devreye giriyor. Role objesi, yapısal olarak bir User'a çok benzer; onun da neler yapabileceğini belirleyen ve üzerine iliştirilmiş Policy listeleri vardır. Ancak aralarındaki en büyük ve en kritik fark şudur: User'ların kalıcı kimlik bilgileri (kullanıcı adı/şifre veya statik erişim anahtarları) bulunurken, Role'lerin kalıcı şifreleri yoktur. Bir Role, ihtiyaç anında geçici olarak "giyilen bir üniforma" veya "takılan bir şapka" gibidir.

### Örnek senaryo: EC2'dan S3'e erişim

Sürecin pratikte nasıl işlediğini bir otomasyon senaryosu üzerinden anlatalım: Diyelim ki AWS üzerinde bir EC2 sanal sunucusu ayağa kaldırdınız ve içine yazdığınız bir deployment betiğinin, gidip S3 bucket'ınızdan bir yapılandırma dosyası okuması gerekiyor. Eğer bu işlemi bir "User" objesi kullanarak yapmaya kalksaydınız, o kullanıcıya ait gizli erişim anahtarlarını sunucunun içine, script dosyalarınızın arasına sabit olarak yazmanız gerekirdi. Bu, bulut güvenliğinde yapılan en büyük hatalardan biridir. Kodlarınızın yanlışlıkla bir GitHub deposuna sızması durumunda, tüm AWS hesabınızın kontrolü dakikalar içinde kötü niyetli kişilerin eline geçebilir. İşte Role objesi bizi bu dertten ve güvenlik riskinden kurtarır.

Süreç şu şekilde, tamamen otomatik ve şifresiz ilerler:

1. Önce "S3'ten dosya okuyabilir" yetkisine sahip bir Policy objesi oluşturulur.
2. Ardından bir Role yaratılır ve az önce oluşturduğumuz bu Policy, Role objesine bağlanır.
3. Son adımda, oluşturduğumuz bu Role, kodlarımızın çalıştığı EC2 sunucusuna "atanır". Artık EC2 sunucumuz bu rolü üstlenmiştir.
4. Script çalıştığında, EC2 sunucusu arka planda AWS'den bizim adımıza birkaç saatliğine geçerli olacak geçici güvenlik anahtarları (temporary credentials) talep eder.
5. Sunucu, S3'e gidip "Ben bu role sahibim ve yetkim var" diyerek işlemi güvenle gerçekleştirir. İşlem bitince veya süre dolunca bu şifreler kendiliğinden imha olur.

Özetle; User objesi "Sen kimsin?" sorusuna kalıcı bir cevap ararken, Role objesi servislerin ve uygulamaların birbiriyle güvenli, şifresiz ve esnek bir şekilde konuşmasını sağlayan bir yetki devri mekanizmasıdır.

## Root account

User'lar içinde en önemli ve özel olan user **Root Account**'tur. Bir AWS hesabı ilk oluşturulduğunda otomatik olarak ortaya çıkan bu hesap, sistemdeki mutlak güce sahip, en yetkili kimliktir. Merkezi AWS hesap yönetim servisidir, tüm hesap ayarları bu servis aracılığıyla yönetilir.

:::caution[Düzeltme]
Root account bir servis değil, hesabın sahibi olan kullanıcı kimliğidir. Tüm hesap ayarları bu kimlikle yönetilebilir.
:::

:::caution
Ancak AWS dünyasında çok kritik bir güvenlik kuralı vardır: Kök hesap günlük operasyonlar için kullanılmaz. Pratik olarak; root hesapla sisteme ilk giriş yapıldığında tüm günlük işleri yürütecek yetkili bir 'Admin IAM User' oluşturulur, root hesabın güvenliği artırılır ve zorunlu haller (fatura ayarları, hesabı kapatmak vb.) dışında root hesap bir daha kullanılmamak üzere bir kenara bırakılır.
:::
