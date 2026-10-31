---
title: AWS'ye giriş
description: Cloud türleri, AWS'nin ortaya çıkışı, region ve availability zone yapısı ile IAM servisine ilk bakış.
module: aws
lessons: [18]
order: 1
---

## Cloud computing

[Daha önce bahsettiğimiz](/bulut-temelleri/sunucudan-buluta/) cloud kavramıyla başlayalım. Cloud computing; en az düzeyde efor sarf ederek, bazı özellikleri kendi programımız içinde yöneterek istediğimiz anda kaynak oluşturup silebildiğimiz, bunlara anında internet üzerinden erişebildiğimiz ve kullandığımız hizmetlerin faturalandırmasının gösterildiği bilgisayar kaynaklarıdır.

Cloud'u üç kısımda anlatabiliriz:

| Tür | Açıklama | Örnekler |
| --- | --- | --- |
| Public cloud | Başka bir firma tarafından yönetilip sunulan altyapı üzerinden alınan hizmetler | AWS, Microsoft Azure, Google Cloud Platform |
| Private cloud | Kendi veri merkeziyle işleri yürüten sistemler | IBM, Red Hat, OpenStack, Dell, EMC, HPE, Microsoft |
| Hybrid | Hem private cloud altyapısını koruyan hem de public cloud özelliklerinden yararlanan sistemler | |

## Amazon Web Services (AWS)

AWS, işletmelerin ölçeklenmesine ve büyümesine yardımcı olan işlem gücü, veritabanı, depolama alanı ve içerik teslimatı gibi işlevler sunan güvenli bir bulut hizmetleri platformudur. Amazon bünyesinden çıkmış, 130'dan fazla computing hizmeti sunan bir bulut servis sağlayıcısıdır. Bir yazılımı geliştirmekten müşterilere ulaştırmaya kadar olan tüm süreçte kullanılabilecek hizmetleri tek bir çatı altında toplayarak yönetmemizi sağlar.

### Kısa tarihçe

Amazon ilk olarak satış yapan bir firma olarak ortaya çıktı. Satılan ürünlerin veritabanı genişleyince bu veritabanını geliştiricilere açma fikri ortaya kondu. Ardından web mağazası o kadar büyüdü ki firmanın en önemli unsuru IT altyapısı olmaya başladı ve bu altyapıyı da geliştiricilere açma fikri konuşulmaya başlandı. Önce hizmete sunulan veritabanının yanına SQS eklendi, ardından S3 geldi. EC2 servisinin de kullanıcılara açılmasıyla cloud denilen konseptin temelleri atılmış, prensipleri belirginleşmeye başlamış oldu.

AWS; bilgi işlem gücü, veritabanı, depolama, içerik teslimi ya da başka bir işleve ihtiyaç duymanız fark etmeksizin, daha yüksek esneklik, ölçeklenebilirlik ve güvenilirlikle sofistike uygulamalar oluşturmanıza yardımcı olacak hizmetlere sahiptir.

## Region ve availability zone

AWS servislerini en yüksek hızda kullanabilmemiz için kullandığımız sunucuların fiziksel olarak bize yakın olması gerekir. Bu yüzden AWS'nin dünyanın geneline yayılmış birçok veri merkezi ve bu veri merkezlerinin birbirine bağlandığı bir altyapısı vardır.

- **Region (bölge):** Bu altyapıların bulunduğu coğrafi bölgelerdir. Her region en az üç veri merkezinden oluşur.
- **Availability zone:** Region içindeki veri merkezlerine verilen isimdir.

Bir region içindeki veri merkezleri birbirine çok hızlı bağlantılarla bağlanır. Bu bağlantılar o kadar hızlıdır ki aralarındaki gecikme çok azalır ve üç merkez sanki tek bir yerden yönetiliyormuş gibi çalışır. Veri merkezleri fiziksel olarak birbirinden tamamen ayrı olduğu için birinde yaşanan sorun diğerini etkilemez. Bu yapının tamamına region - availability zone yapısı denir.

## IAM'e ilk bakış

AWS'de ilk öğreneceğimiz servis IAM (Identity and Access Management), yani kimlik ve erişim yönetimi servisidir. AWS kullanmak istiyorsak önce kullanıcılar oluşturmamız ve bu kullanıcıların AWS üzerinde neleri yapabileceğine dair kuralları belirlememiz gerekir. IAM bu işlemleri yapmamızı sağlar.

AWS IAM, AWS servislerine ve kaynaklarına erişimi güvenli bir şekilde yönetmenizi sağlar. IAM ile AWS kullanıcılarını yönetebilir, ayrıca AWS kaynaklarına erişime izin vermek veya erişimi reddetmek için izinleri kullanabilirsiniz. Ayrıntılar için [IAM kavramları](/aws/iam/kavramlar/) sayfasına bakın.
