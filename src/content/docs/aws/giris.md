---
title: AWS'ye giriş
description: Cloud türleri, AWS'nin ortaya çıkışı, region ve availability zone yapısı ile IAM servisine ilk bakış.
module: aws
lessons: [18]
order: 1
---

## Cloud computing

Temel kavramları burada noktalayarak uzun süre devam edeceğimiz AWS konusuna kısa bir giriş yapalım. [Daha önce bahsettiğimiz cloud kavramıyla](/bulut-temelleri/sunucudan-buluta/) başlayabiliriz. Cloud computing, en az düzeyde efor sarf ederek kendi programımız içinde bazı özellikleri yöneterek; istediğimiz anda kaynak oluşturup silebildiğimiz, bunlara anında internet üzerinden erişebildiğimiz ve kullandığımız hizmetlerin faturalandırılmasının gösteriminin olduğu bilgisayar kaynaklarıdır.

Cloud'u kendi içinde üç kısımda anlatabiliriz. İlki bir başka firma tarafından yönetilip sunulan altyapı üzerinden aldığımız **public cloud** hizmetleridir. Bunlardan bazıları AWS, Microsoft Azure ve Google Cloud Platform. Diğeri kendi veri merkeziyle işleri yürüten **private cloud** sistemlerdir. IBM, Red Hat, OpenStack, Dell, EMC, HPE, Microsoft bunlara örnek verilebilir. Son olarak hem private cloud altyapısını koruyan hem de public cloud özelliklerinden yararlanan sistemler de vardır.

## Amazon Web Services (AWS)

Amazon Web Services (AWS), işletmelerin ölçeklendirilmesine ve büyümesine yardımcı olan işlem gücü, veritabanı, depolama alanı ve içerik teslimatı gibi işlevler sunan güvenli bir bulut hizmetleri platformudur. Biraz daha detaylandıracak olursak Amazon bünyesinden çıkmış 130'dan fazla computing hizmeti sunan bulut servis sağlayıcısıdır. Bir yazılımı geliştirmekten tutun onu müşterilere ulaştırmaya kadar olan tüm süreçte kullanılabilecek hizmetleri tek bir çatı altında toplayarak yönetmemizi sağlayan platformdur.

### Kısa tarihçe

Amazon ilk olarak satış gerçekleştiren bir firma olarak ortaya çıksa da sonrasında satılan ürünler veritabanını genişletince oluşan veritabanını geliştiricilere açma fikri ortaya koyuldu. Ardından bu web mağazası o kadar genişledi ki firmanın en önemli unsuru IT altyapısı olmaya başladı. Sonrasında oluşturulan bu altyapıyı da geliştiricilere açma fikri konuşulmaya başlandı. Öncesinde hizmete sunulan database yanına SQS eklendi sonrasında S3 servisi bunu takip etti ve EC2 servisinin de kullanıcılara açılmasıyla cloud denilen konseptin temelleri atılmış, prensipleri belirginleşmeye başlamış oldu.

Tarihçe kısmına değindiğimize göre daha teknik olan kısımlara yavaşça geçebiliriz.

AWS, bilgi işlem gücü, veritabanı depolaması, içerik teslimi özelliklerine veya başka diğer işlevlere ihtiyaç duymanız fark etmeksizin daha yüksek esneklik, ölçeklenebilirlik ve güvenilirlik ile sofistike uygulamalar oluşturmanıza yardımcı olacak hizmetlere sahiptir.

## Region ve availability zone

AWS üzerindeki bu servisleri kullanma hızımızın en yüksek seviyelere çıkması için kullandığımız sunucuların fiziksel olarak yakınımızda olması gerekir. Bu yüzden AWS, dünyanın geneline yayılmış birçok veri merkezine sahiptir ve bu veri merkezlerinin de birbirleriyle bağlanabilecekleri altyapısı vardır. AWS terminolojisinde bu altyapıların olduğu bölgelere **regions** (bölgeler) denir. Her region en az üç adet veri merkezi grubundan oluşur. Bir veya birden fazla veri merkezinden oluşan bu gruplar **availability zone** ismini alır.

Bu veri merkezleri de birbirlerine çok hızlı bağlantılarla bağlanır. Hatta bu bağlantılar o kadar hızlı seviyelerde oluyor ki sanki üç merkez tek bir yerden yönetiliyormuş gibi aralarındaki gecikme çok az hale geliyor. Ayrıca fiziksel olarak birbirlerinden tamamen ayrı oldukları için de birinde yaşanan sorun diğerini etkilemiyor. Bu tüm duruma regions - availability zone denir.

## IAM'e ilk bakış

Artık AWS'de kullanılan servisleri tanımaya başlayabiliriz. İlk öğreneceğimiz [IAM (Identity and Access Management)](/aws/iam/kavramlar/) yani kimlik ve erişim yönetimi isimli servistir. AWS kullanmak istiyorsak ilk olarak kullanıcılar oluşturmamız ve bu kullanıcıların AWS üzerinden neleri yapabileceğine dair kuralları belirlememiz gerekmektedir. IAM servisi bu işlemleri yapmamızı sağlar.

AWS IAM, AWS servislerine ve kaynaklarına erişimi güvenli bir şekilde yönetmenizi sağlar. IAM'i kullanarak AWS kullanıcılarını yönetebilir, ayrıca AWS kaynaklarına erişmelerine izin vermek ve bunları reddetmek için izinleri kullanabilirsiniz.
