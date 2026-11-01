---
title: Sunucudan buluta
description: Sunucu-istemci mimarisinden sanallaştırmaya, colocation veri merkezlerinden IaaS ve bulut bilişim kavramına uzanan gelişim.
module: bulut-temelleri
lessons: [16]
order: 1
---

## Sunucu ve istemci

Bilgisayar dünyasında en temel anlamıyla iki çeşit bilgisayar vardır. Bunlardan ilki sunucu - server ikincisi ise istemci - client bilgisayarlardır.

Sunucu bilgisayarlar güçlü ve yüksek kapasiteli, uzun süreli-kesintisiz ve çoklu isteklere cevap vermek için tasarlanmıştır. Hizmeti sunarlar.

İstemci bilgisayarlar ise görece daha düşük kapasite işlem gücüne sahiptir. Tek bir kullanıcıya hizmet vermek için tasarlanmıştır. Uzun süreli ve kesintisiz çalışma öncelikleri yoktur. Hizmeti kullanırlar.

Farklı kullanıcılar tarafından kullanıma açmak, sunmak istediğimiz uygulamayı yüksek kapasiteli çoklu isteklere cevap verebilme özelliğine sahip olan sunucu bilgisayarlara yükleriz.

Bu bilgisayarlara bağlanarak server bilgisayarlardaki hizmetin sonucunu görmemizi sağlayanlar ise istemci bilgisayarlarıdır.

Bahsettiğimiz şekilde bir çalışma mimarisi üzerine uygulama kurma işlemine ise sunucu-istemci mimarisindeki uygulamalar diyoruz.

Aslında devops süreci özetle bundan ibarettir. Uygulamalarımızı sunucu denilen sistemlerin üzerine en verimli, en az hataya sahip, en hızlı ve en uygun şekilde nasıl sunabiliriz.

## 2000'lerin başında sistem yönetimi

Sunucu-istemci mimarisinden bahsettiğimize göre gelin kısa bir tarih yolculuğu yapalım ve 2000'lerin başına dönerek sanallaştırma kavramının nasıl ortaya çıktığını anlamaya çalışalım.

2000'lerin başında bir sistem admini olduğumuzu düşünelim ve yaşanılan sorunları anlamaya çalışalım. Bizden istenilen bir muhasebe uygulamasının çalıştırılması olsun. Bunun için uygulamayı üzerine kurmamız gereken ortamı hazırlamamız lazım. İlk olarak bir sunucu bilgisayarı sipariş vermemiz gerek, sipariş verdikten sonra bilgisayarımızın gelmesi 6-8 hafta gibi bir süre alacaktır. Sipariş elimize ulaştıktan sonra gerekli fiziksel kurulumlarını tamamlayıp (cpu, ram, disk gibi) çalışmaya hazır hale getirmemiz 1-2 hafta gibi bir zamanımıza mal olacaktır. Ardından tüm bu süreçler bittikten sonra sunucuya uygun bir işletim sistemini kurup muhasebe uygulamamızı yükleyecek duruma geldiğimizde görüldüğü gibi en başından beri harcanan zaman 3 ay gibi bir süreye tekabül ediyor.

### Her uygulamaya bir sunucu

Ancak bütün sorun zaman değil. Yaşanan bir diğer sorun her yeni uygulamada yeni bir sunucuya ihtiyacımız olması. Çünkü bir sunucu üzerine uygulama izolasyonundan dolayı birden fazla uygulama kuramıyorduk; bunun sebebi iki uygulamanın birbirine dependent yani bağımlı olmasıydı.

Uygulamaların birinde yaşanacak herhangi bir sorunun diğer uygulamayı da etkileyecek olması yani hata olduğunda çözmek için sunucuyu restart etmemiz gerektiğinde diğer uygulamanın da erişilmez hale gelmesi, uygulamaların çalışmaları gereken zamanlarının farklılığı, güvenlik açığı oluştuğunda önemli verilerimizin sunduğu uygulamanın risk altında olması gibi sebeplerden dolayı bir sunucuya birden fazla uygulama kurmuyorduk. Her uygulama için bir server bilgisayar gerekiyordu.

### Atıl kapasite

Bunun anlamı her seferinde tüm bu 3 aylık sürecin baştan yaşanacak olması demekti. Bunun yanında uygulama izolasyonunu sağlamak için her sunucu üzerine kurduğumuz uygulamalar yeni bir sorunu da beraberinde getiriyordu. Atıl kapasite sorunu.

Server bilgisayarlar üzerine kurduğumuz uygulamalar bu bilgisayarların tüm kapasitesini kullanmadığı için boşta kullanılmayan disk, ram gibi kaynaklar kalıyordu.

## Sanallaştırma

Bu yaşanan sorunları çözmek için sanallaştırma kavramı geliştirildi. Sanallaştırma ile uygulamaların izolasyonunu sağlayabilmek için makineleri ayrı ayrı tutma ihtiyacından kurtulduk. Artık tek bir tane server makine alıp öncelikle üzerine sanallaştırma yazılımını kuruyorduk. Bu sayede fiziksel makinenin üzerinde ayrı ayrı birbirlerinden tamamen izole, birbirlerinin kaynaklarına erişemeyen ama makinenin fiziksel donanım kaynaklarını ortak kullanan sanal makineler oluşturma imkanı sağlıyordu.

Sanallaştırma bu sayede atıl kapasite sorununu çözmüş oldu. Ayrıca bir fiziksel makine üzerine kurduğumuz birden fazla sanal makine sayesinde çalıştırdığımız birden fazla uygulama ile her uygulama için bir server bilgisayara olan ihtiyacımız ortadan kalkmış, yaşadığımız zaman sorununa da çözüm getirmiş oldu.

Sanallaştırma ile çözülen bir diğer bahsetmemiz gereken sorun ise; eskiden fiziksel makine üzerinde yaşanan bir parça sorunu, parçanın yenisini sipariş edip gelmesini beklemek, o süreçte elimizde varsa boş bir server bilgisayar varsa uygulamamızı ona yükleyip çalıştırmakla çözülüyordu. Sanallaştırma ile fiziksel makineler üzerine kurduğumuz işletim sistemlerini bir dosya haline getirdik. Bu sayede kullandığımız fiziksel makine bozulsa bile elimizdeki dosyayı hiçbir kesinti olmadan diğer makinelere taşıyabilir hale geldik.

## On-premises veri merkezlerinin sorunları

Gelelim 2000'li yıllarda yaşanan diğer bir önemli soruna. Bir şirkette kurulacak lokal (on-premises) veri merkezinin şu anki ihtiyaca göre mi kurulacağı yoksa gelecekteki ihtiyaçlar göz önüne alınarak mı yapılandırılacağı, ilk yatırım maliyetinin ve bakım maliyetlerinin yüksekliği, planlamasının zorluğu, esnek ve genişletilebilir olmayışı gibi birçok sorunu da beraberinde getirdiğini biliyoruz.

## Colocation veri merkezleri

2000'lerin ortalarına doğru hayatımıza daha yoğun olarak giren bazı yöntemler bu sorunlardan birkaçına merhem olmuştu. Bunlardan bir tanesi colocation veri merkezleri. Her şirketin kendi veri merkezinin olmasına ihtiyaç olmadığını ve bundan yola çıkarak büyük veri merkezleri kurarak bu hizmeti firmalara kiralayan şirketler oluşmaya başladı. Böylece şirketler ilk yatırım maliyetinden kurtuldu, ve veri merkezleri büyük olduğu için birim başına düşen makine maliyeti az olduğundan daha uygun fiyata müşterilere satabilir hale geldiler. Ayrıca şirketler veri merkezlerinin bakım zahmetinden de kurtularak artık bunu bir hizmet şeklinde almaya başladılar.

Bu senaryoda colocation firmaları veri merkezlerinden, firmalar ise kendi sunucu altyapılarından sorumluydular. Yani sunucular üzerindeki fiziksel olan parçalardan bunların sorunlarından yine firmalar sorumluydu.

## Infrastructure as a Service

İlerleyen zamanlarda sanallaştırma daha çok hayatımıza girmeye başlarken veri merkezlerini kiralayan firmalar acaba sunucuları da veri merkezleri gibi kiralamaya başlasak mı diye düşündüler ve bunun hizmetini de vermeye başlayan firmalar oldu.

Daha sonraki süreçte ise bu sunuculardan bir sürü alarak sanal makineleri firmalara kiralama fikri hayata geçmeye başladı. Böylece colocation firmaları fiziksel makineler dahil tüm altyapıyı kendileri önceden kurup yöneterek müşterilere sanal makineler halinde sunmaya başladılar. Bu şekilde altyapının servis olarak kullanılma işlemine Infrastructure as a Service denmektedir.

## Bulut bilişim

Şimdi ise buradan yola çıkarak bulut bilişim-cloud computing kavramını anlamaya çalışalım. Bulut bilişim bu colocation firmaları tarafından yönetilen altyapıların üzerinden bilgisayar hizmetini satın almamıza, o bilgisayar hizmetini kullanmamıza verilen genel isimdir.

Bizim lokasyonumuzda değil de başka bir firma tarafından farklı bir lokasyonda oluşturmuş olduğu altyapı üzerinden bize hizmetler şeklinde bilgisayar altyapılarını kullandırılmasına genel adıyla bulut bilişim-cloud computing denir.

Bulut bilişim bir ürün değil hizmettir. Bu yeni bir teknoloji değildir. Esasında bir bilgisayar altyapısının bize hizmet olarak sunulmasıdır. Bu kavramı gökyüzüne baktığımızda yalnızca bulutları görüp arkasındaki abstract edilmiş iklim sistemini görmeyişimize benzetebiliriz. Biz hizmeti alıyoruz ancak arkasında bulunan teknoloji ile ilgilenmiyoruz.

Aslında bu konsept bilgisayar ortaya çıktığından beri kullanılmasına karşın internetin hızlanmasıyla yaygınlaşıp uygulanmaya başlandı.
