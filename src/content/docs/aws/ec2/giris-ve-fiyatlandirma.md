---
title: Giriş ve fiyatlandırma modelleri
description: EC2 servisinin ne olduğu ve On-Demand, Reserved Instance, Savings Plans, Spot ve Dedicated Host fiyatlandırma modelleri.
module: aws
lessons: [24]
order: 15
---

## EC2 nedir?

EC2'nin açılımı **Elastic Compute Cloud**'dur. Kendi sanal sunucularımızı dakikalar içinde ayağa kaldırmamızı sağlar ve altyapının temelini oluşturan servistir.

Sanallaştırma teknolojisi EC2 ortaya çıkmadan yıllar önce de vardı. AWS bu teknolojiyi tek bir komutla sanal makine açma, yönetme ve kapatma kolaylığıyla birleştirdi. Her şeyi kodla yönetilebilir kılan API desteği ve "kullandığın kadar öde" modeliyle öne çıkarak iş yapış şeklini tamamen değiştirdi.

## Fiyatlandırma modelleri

Kullanım karşılığında ödediğimiz hizmet bedeli farklı fiyatlandırma modelleriyle hesaplanabilir.

### On-Demand

Tamamen "kullandığın kadar öde" mantığıyla çalışır. Sanal makineyi oluşturduktan sonra açık kaldığı her saniye için ücretlendirilirsiniz.

- Makineyi ne kadar süre kullanacağınızı net olarak öngöremediğiniz, esneklik gerektiren durumlarda tercih edilir.
- Sürekli çalışan Production sistemleri için uzun vadede maliyetli olacağından pek uygun değildir.

### Reserved Instance (RI) ve Savings Plans

Sanal makineyi ne kadar süre kullanacağınız baştan belliyse AWS ile önceden anlaşma yaparak ciddi indirimler kazanabilirsiniz. AWS bunu iki farklı yaklaşımla sunar:

**Reserved Instances (RI):** Daha geleneksel olan bu yöntemde donanımı net bir şekilde rezerve edersiniz. Örneğin, *"Önümüzdeki bir yıl boyunca şu özelliklerde 5 adet makine kullanacağım"* dersiniz. Ücreti tek seferde, aylık veya parçalı olarak karşılama seçenekleriniz vardır ve her durumda büyük bir indirim yansır.

**Savings Plans:** RI modelinin daha esnek ve geliştirilmiş halidir. Belirli bir makine tipine sıkışmak veya makine ihtiyacının bitmesi gibi durumlar göz önüne alınarak tasarlanmıştır. Bu modelde örneğin *"Önümüzdeki üç yıl boyunca günde 10 dolar harcamayı taahhüt ediyorum"* gibi bir anlaşma yaparsınız. Bu günlük 10 dolarlık limit dahilinde istediğiniz tipte sanal makineyi açıp kullanmakta özgürsünüz. Limiti aşarsanız aşan miktar standart On-Demand fiyatları üzerinden hesaplanır.

### Spot

AWS, sunucularındaki kullanılmayan kapasiteyi değerlendirmek için bu makineleri çok büyük indirimlerle sunar. Sistem bir borsa gibi çalışır; fiyatlar anlık talebe göre değişir.

- Kullanıcı olarak bütçenize göre bir sınır belirlersiniz. Örneğin *"Bu sanal makine için saatlik en fazla 0.7 dolar veririm"* şeklinde bir talep açarsınız.
- AWS'nin güncel fiyatı teklifinizle uyuşuyorsa makineyi bu çok düşük fiyattan kullanmaya başlarsınız.

:::caution
Bu makinelere olan genel talep artar ve güncel fiyat belirlediğiniz 0.7 dolar sınırını aşarsa AWS kısa bir bildirim göndererek makineyi otomatik olarak kapatır. Bu yüzden Spot, anlık kesintiye tahammülü olan ve arka planda çalışan esnek işler için uygundur.
:::

### Dedicated Host

Sanal makine dünyasında genellikle bir fiziksel sunucu içinde birçok farklı AWS kullanıcısının sanal makinesi yan yana çalışır. **Dedicated Host** ise AWS veri merkezindeki bir fiziksel sunucunun tamamen size ve şirketinize tahsis edilmesidir.

Bu modelde fiziksel sunucunun içinde kaç sanal makine açtığınızdan bağımsız olarak doğrudan donanımın kendisini kiraladığınız için, aktif kaldığı süre boyunca tüm sunucunun bedelini ödersiniz. Bu kadar maliyetli ve özel bir yöntemin seçilmesinin iki büyük nedeni vardır:

- **Lisanslama avantajı:** Windows Server, SQL Server veya bazı özel veritabanı yazılımlarının lisansları sanal makineye göre değil, doğrudan fiziksel sunucunun işlemci sayısına göre satılır. Dedicated Host sayesinde şirketinizin daha önce milyonlarca lira harcayarak satın aldığı, fiziksel donanıma bağlı bu lisansları çöpe atmadan AWS bulutunda da yasal olarak kullanmaya devam edebilirsiniz.
- **Katı güvenlik ve regülasyonlar:** Bazı devlet kurumları, bankalar veya sağlık kuruluşları, regülasyonlar gereği verilerinin başka şirketlerle aynı fiziksel donanımı paylaşmasını kesinlikle yasaklar. Verilerin donanım seviyesinde tamamen izole edilmesi gerektiğinde bu altyapı tercih edilir.

Instance oluştururken bu modellerin hangi ayarlarla seçildiği [Instance oluşturma](/aws/ec2/instance-olusturma/) sayfasındaki **Purchasing option** ve **Tenancy** alanlarında anlatılıyor.
