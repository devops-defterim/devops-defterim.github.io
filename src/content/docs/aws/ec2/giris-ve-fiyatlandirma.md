---
title: Giriş ve fiyatlandırma modelleri
description: EC2 servisinin ne olduğu ve On-Demand, Reserved Instance, Savings Plans, Spot ve Dedicated Host fiyatlandırma modelleri.
module: aws
lessons: [24]
order: 15
---

## EC2 nedir?

S3 ile bulut depolama mimarisini tüm detaylarıyla kavradığımıza göre bu uzun konuyu burada tamamlıyoruz. Şimdi vakit kaybetmeden AWS'yi kullanmaya başladığımız ilk servis, altyapımızın temelini oluşturacak olan EC2 servisimizi tanımaya geçiyoruz. Açılımı **Elastic Compute Cloud** olan ve kendi sanal sunucularımızı dakikalar içinde ayağa kaldırmamızı sağlayan EC2 servisini tanımaya başlayalım.

Sanallaştırma teknolojisi EC2 ortaya çıkmadan yıllar önce de vardı. Ancak AWS, bu teknolojiyi tek bir komutla sanal makine açma, yönetme ve kapatma kolaylığıyla birleştirdi. Her şeyi kodla yönetilebilir kılan API desteği ve kullandığın kadar ödeme modeli ile öne çıkarak iş yapış şeklini tamamıyla değiştirdi.

## Fiyatlandırma modelleri

Kullanımın karşılığında ödediğimiz hizmet bedeli konusunun detayına bir göz atacak olursak bu ödeme üç şekilde gerçekleşebilir;

### On-Demand

On-Demand, tamamen "kullandığın kadar öde" mantığıyla çalışır. Sanal makinenizi oluşturduktan sonra, açık kaldığı her saniye için ücretlendirilirsiniz. Makineyi ne kadar süreyle kullanacağınızı net olarak öngöremediğiniz, esneklik gerektiren durumlarda tercih edilir. Ancak sürekli çalışan Production sistemleri için uzun vadede maliyetli olacağından pek uygun bir yöntem değildir.

### Reserved Instance (RI) ve Savings Plans

Reserved Instance 'RI' & Savings Plan, eğer sanal makinenizi ne kadar süre kullanacağınız baştan belliyse, AWS ile önceden bir anlaşma yaparak ciddi indirimler kazanabilirsiniz. AWS bunu iki farklı yaklaşımla sunar:

**Reserved Instances (RI):** Daha geleneksel olan bu yöntemde, donanımı net bir şekilde rezerve edersiniz. Örneğin, "Önümüzdeki bir yıl boyunca şu özelliklerde 5 adet makine kullanacağım" dersiniz. Ödemeyi tek seferde, aylık veya parçalı olarak yapma seçenekleriniz vardır ve her durumda size büyük bir indirim yansır.

**Savings Plans:** RI modelinin daha esnek ve geliştirilmiş halidir. Belirli bir makine tipine sıkışmak veya makine ihtiyacınızın bitmesi gibi durumlar göz önüne alınarak tasarlanmıştır. Bu modelde, örneğin "Önümüzdeki üç yıl boyunca saatte 10 dolar ödemeyi taahhüt ediyorum" gibi bir anlaşma yaparsınız. Bu saatlik 10 dolarlık limit dâhilinde istediğiniz tipte sanal makineyi açıp kullanmakta özgürsünüzdür. Eğer limitinizi aşarsanız, aşan miktar standart On-Demand fiyatları üzerinden hesaplanır.

### Spot

AWS, sunucularındaki kullanılmayan kapasiteyi değerlendirmek için bu makineleri devasa indirimlerle sunar. Sistem tıpkı bir borsa gibi çalışır; fiyatlar anlık talebe göre değişir. Burada kullanıcı olarak bütçenize göre bir sınır belirleyebilirsiniz; örneğin, "Bu sanal makine için saatlik en fazla 0.7 Dolar öderim" şeklinde bir talep açarsınız. Eğer AWS'nin güncel fiyatı sizin teklifinizle uyuşuyorsa makineyi bu çok düşük fiyattan kullanmaya başlarsınız. Ancak ufak bir risk vardır: Eğer o makinelere olan genel talep artar ve güncel fiyat sizin belirlediğiniz 0.7 Dolar sınırını aşarsa, AWS size kısa bir bildirim göndererek makineyi otomatik olarak kapatır. Bu yüzden anlık kesintiye tahammülü olan ve arka planda çalışan esnek işler için harika bir seçenektir.

### Dedicated Host

Dedicated Host, sanal makine dünyasında genellikle bir fiziksel sunucu içinde birçok farklı AWS kullanıcısının sanal makinesi bir arada, yan yana çalışır. Ancak Dedicated Host, AWS veri merkezindeki koca bir fiziksel sunucunun tamamen size ve sizin şirketinize tahsis edilmesidir.

Mantığı nasıl çalışır ve neden kullanılır? Bu modelde, o fiziksel sunucunun içinde kaç tane sanal makine açtığınızdan ziyade, doğrudan donanımın kendisini kiraladığınız için aktif kaldığı süre boyunca tüm sunucunun bedelini ödersiniz. Bu kadar maliyetli ve özel bir yöntemin seçilmesinin arkasında iki büyük neden yatar:

- **Lisanslama Avantajı:** Windows Server, SQL Server veya bazı özel veri tabanı yazılımlarının lisansları sanal makineye göre değil, doğrudan fiziksel sunucunun işlemci sayısına göre satılır. Dedicated Host sayesinde, şirketinizin daha önceden milyonlarca lira ödeyip satın aldığı bu fiziksel donanıma kilitli lisansları çöpe atmadan, AWS bulutunda da yasal olarak kullanmaya devam edebilirsiniz.
- **Katı Güvenlik ve Regülasyonlar:** Bazı devlet kurumları, bankalar veya sağlık kuruluşları, sahip oldukları regülasyonlar gereği kendi verilerinin başka şirketlerle aynı fiziksel donanımı paylaşmasını kesinlikle yasaklar. Verilerin donanım seviyesinde tamamen izole edilmesi gerektiğinde bu altyapı tercih edilir.
