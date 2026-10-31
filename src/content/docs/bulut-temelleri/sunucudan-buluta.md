---
title: Sunucudan buluta
description: Sunucu-istemci mimarisinden sanallaştırmaya, colocation veri merkezlerinden IaaS ve bulut bilişim kavramına uzanan gelişim.
module: bulut-temelleri
lessons: [16]
order: 1
---

AWS'nin teknik detaylarına girmeden önce bulut bilişimin tarihine, neden böyle bir alana ihtiyaç duyulduğuna ve konuyu anlamak için gereken bazı kavramlara bakmak faydalıdır.

## Sunucu ve istemci

Bilgisayar dünyasında en temel anlamıyla iki çeşit bilgisayar vardır:

| | Sunucu (server) | İstemci (client) |
| --- | --- | --- |
| Kapasite | Güçlü ve yüksek kapasiteli | Görece daha düşük kapasite ve işlem gücü |
| Kullanım | Uzun süreli, kesintisiz çalışmak ve çoklu isteklere cevap vermek için tasarlanır | Tek bir kullanıcıya hizmet vermek için tasarlanır; uzun süreli ve kesintisiz çalışma önceliği yoktur |
| Rol | Hizmeti sunar | Hizmeti kullanır |

Farklı kullanıcıların kullanımına açmak istediğimiz uygulamayı, çoklu isteklere cevap verebilen yüksek kapasiteli sunucu bilgisayarlara yükleriz. Bu sunuculara bağlanarak hizmetin sonucunu görmemizi sağlayanlar istemci bilgisayarlardır. Bu çalışma mimarisi üzerine kurulan uygulamalara **sunucu-istemci mimarisindeki uygulamalar** denir.

DevOps süreci özetle bundan ibarettir: uygulamalarımızı sunucu denilen sistemlerin üzerinde en verimli, en az hatalı, en hızlı ve en uygun şekilde nasıl sunabiliriz?

## 2000'lerin başında sistem yönetimi

2000'lerin başında bir sistem admini olduğumuzu ve bizden bir muhasebe uygulamasını çalıştırmamızın istendiğini düşünelim. Uygulamanın kurulacağı ortamı hazırlamak için:

1. Bir sunucu bilgisayar sipariş edilir. Bilgisayarın gelmesi 6-8 hafta sürer.
2. Sipariş geldikten sonra CPU, RAM, disk gibi fiziksel kurulumların tamamlanıp sunucunun çalışmaya hazır hale gelmesi 1-2 hafta sürer.
3. Sunucuya uygun bir işletim sistemi kurulur ve muhasebe uygulaması yüklenir.

En baştan beri harcanan zaman yaklaşık 3 ayı bulur.

### Her uygulamaya bir sunucu

Sorun yalnızca zaman değildi. Her yeni uygulama için yeni bir sunucuya ihtiyaç vardı, çünkü uygulama izolasyonu gereği bir sunucuya birden fazla uygulama kurulmuyordu. Bunun sebepleri:

- Uygulamaların birbirine bağımlı (dependent) olması
- Bir uygulamada yaşanan sorunun diğerini de etkilemesi; örneğin hatayı çözmek için sunucu restart edildiğinde diğer uygulamanın da erişilemez hale gelmesi
- Uygulamaların çalışması gereken zamanların farklı olması
- Bir güvenlik açığında, önemli verileri barındıran diğer uygulamanın da risk altına girmesi

Bu da her seferinde 3 aylık sürecin baştan yaşanması demekti.

### Atıl kapasite

İzolasyon için her sunucuya tek uygulama kurulması yeni bir sorun getiriyordu: **atıl kapasite**. Uygulamalar sunucunun tüm kapasitesini kullanmadığı için disk, RAM gibi kaynaklar boşta kalıyordu.

## Sanallaştırma

Bu sorunları çözmek için sanallaştırma geliştirildi. Artık tek bir sunucu alınıp önce üzerine sanallaştırma yazılımı kuruluyordu. Bu sayede fiziksel makinenin üzerinde birbirinden tamamen izole, birbirinin kaynaklarına erişemeyen ama fiziksel donanım kaynaklarını ortak kullanan sanal makineler oluşturulabiliyordu.

Sanallaştırmanın çözdüğü sorunlar:

- **İzolasyon**: Uygulamaları izole etmek için makineleri ayrı ayrı tutma ihtiyacı ortadan kalktı.
- **Atıl kapasite**: Tek fiziksel makinenin kaynakları birden fazla sanal makine arasında paylaşıldı.
- **Zaman**: Bir fiziksel makinede birden fazla uygulama çalıştırılabildiği için her uygulamaya ayrı sunucu alma ihtiyacı ve bununla gelen bekleme süresi ortadan kalktı.
- **Donanım arızası**: Eskiden fiziksel makinede bir parça bozulduğunda yenisi sipariş edilip beklenir, varsa boştaki bir sunucuya uygulama yüklenerek idare edilirdi. Sanallaştırma ile işletim sistemleri bir dosya haline geldi; fiziksel makine bozulsa bile bu dosya kesintisiz olarak başka makinelere taşınabilir hale geldi.

## On-premises veri merkezlerinin sorunları

2000'li yıllarda bir şirketin kendi lokal (on-premises) veri merkezini kurması da birçok sorun getiriyordu:

- Veri merkezinin bugünkü ihtiyaca göre mi yoksa gelecekteki ihtiyaçlar düşünülerek mi kurulacağı
- İlk yatırım ve bakım maliyetlerinin yüksekliği
- Planlamanın zorluğu
- Esnek ve genişletilebilir olmaması

## Colocation veri merkezleri

2000'lerin ortalarına doğru yaygınlaşan bazı yöntemler bu sorunların birkaçına çözüm oldu. Bunlardan biri **colocation veri merkezleri**dir. Her şirketin kendi veri merkezine ihtiyacı olmadığı fikrinden yola çıkarak büyük veri merkezleri kurup bu hizmeti firmalara kiralayan şirketler ortaya çıktı.

- Şirketler ilk yatırım maliyetinden kurtuldu.
- Veri merkezleri büyük olduğu için birim başına düşen makine maliyeti azaldı ve hizmet daha uygun fiyata satılabildi.
- Şirketler veri merkezinin bakım zahmetinden kurtulup bunu hizmet olarak almaya başladı.

Bu senaryoda colocation firmaları veri merkezinden, müşteri firmalar ise kendi sunucu altyapılarından sorumluydu. Sunucuların fiziksel parçaları ve bunların sorunları yine müşteri firmanın sorumluluğundaydı.

## Infrastructure as a Service

Sanallaştırma yaygınlaştıkça veri merkezi kiralayan firmalar sunucuları da kiralamayı düşündü ve bu hizmeti vermeye başlayanlar oldu. Sonraki aşamada çok sayıda sunucu alınarak sanal makinelerin firmalara kiralanması fikri hayata geçti. Colocation firmaları fiziksel makineler dahil tüm altyapıyı önceden kurup yöneterek müşterilere sanal makineler halinde sunmaya başladı. Altyapının bu şekilde servis olarak kullanılmasına **Infrastructure as a Service (IaaS)** denir.

## Bulut bilişim

**Bulut bilişim (cloud computing)**, bu şekilde başka firmalar tarafından yönetilen altyapılar üzerinden bilgisayar hizmetini satın alıp kullanmamıza verilen genel isimdir. Bizim lokasyonumuzda değil, başka bir firmanın farklı bir lokasyonda kurduğu altyapı üzerinden bilgisayar altyapılarının bize hizmet olarak kullandırılmasıdır.

- Bulut bilişim bir ürün değil, hizmettir.
- Yeni bir teknoloji değildir; esasında bir bilgisayar altyapısının bize hizmet olarak sunulmasıdır.
- Gökyüzüne baktığımızda yalnızca bulutları görüp arkasındaki soyutlanmış (abstract) iklim sistemini görmememize benzetilebilir: hizmeti alırız ama arkasındaki teknolojiyle ilgilenmeyiz.
- Bu konsept bilgisayarlar ortaya çıktığından beri vardı; internetin hızlanmasıyla yaygınlaştı.

Hizmeti satın alma şekli her zaman IaaS olarak kalmadı. Sonraki modeller [Servis modelleri](/bulut-temelleri/servis-modelleri/) sayfasında anlatılır.
