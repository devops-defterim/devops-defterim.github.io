---
title: API
description: API kavramı, REST API, microservice mimarisinin getirdiği yönetim yükü, Docker'ın ortaya çıkışı ve API Gateway.
module: bulut-temelleri
lessons: [17]
order: 4
---

## API nedir

Şimdi öğreneceğimiz bir sonraki kavram olan API'ye geçelim. Yazılımı üretip sattığımız kişiler bir web adresi üzerinden klavye ve fare kullanarak bu yazılıma erişebiliyorlardı. Bazı müşteriler kullanılan verileri kendi excel'inde görmek istediğinde ürettiğimiz yazılımın bir başka yazılım tarafından kullanılamadığını fark ettiğimizde ürettiğimiz yazılımı bir başka yazılım tarafından da kullanılabilir hale getirerek onlara bir kapı açmamız gerekti. İşte burada API devreye girerek bu sorunumuzu çözüyor. API (Application Programming Interface) uygulamaların diğer uygulamalar ile konuşmak için oluşturdukları ve en baştan protokollerinin, iletişim becerilerinin ve neler yapabildiklerinin belli olduğu kapılardır. Bu kapılar sayesinde daha önce de bahsettiğimiz [microservice mimarisinde](/bulut-temelleri/yazilim-gelistirme-ve-devops/#monolithten-microservice-mimarisine) oluşturulan her sistem kendi arasında haberleşebilir hale geldi.

RestAPI, fastAPI, windows API gibi çeşitleri vardır. RestAPI Protokolü, birbirinden uzakta olan iki uygulamanın birbiriyle haberleşmesini API üzerinden gerçekleştirerek istekleri HTTP olarak gönderen bir protokoldür.

## Microservice'lerin getirdiği yük ve Docker

Microservice mimarisiyle birlikte hayatımıza giren kolaylıklar zaman ilerledikçe yönetmemiz gereken ondan çok işletim sistemini ortaya çıkardı. Çünkü monolith sistemde back-end için tek binary üzerinden işlemleri gerçekleştirirken microservice ile birlikte bu durum farklı sistemlere ayrılarak birden çok yönetilmesi gereken makine ortaya çıkardı. Evet sanallaştırma teknolojisiyle birlikte artık makineleri kurmak daha kolay, bir makine üzerinde onlarca sanal makine çalıştırabiliyoruz ancak artık ortada yönetilmesi gereken, bakımının yapılması gereken onlarca sunucu ortaya çıktı. Bu da büyük bir problem ortaya çıkardı.

Bu probleme çözüm aranırken, kullanılan tüm bu uygulamaların tek bir işletim sistemi üzerinden birbirinden izole olarak yönetilip yönetilemeyeceği üzerine düşünüldü ve cevap olarak Docker ortaya çıktı. Docker container teknolojisi ile tek bir işletim sistemi üzerinde birden fazla uygulamayı tamamen birbirlerinden bağımsız ve izole şekilde çalışabilecek hale getirdi. Böylece uygulamaları birbirinden izole çalışması için ayrı ayrı işletim sistemleri üzerine kurmamıza gerek kalmadı ve yönetilmesi gereken onlarca sunucu yükünden kurtulmuş olduk. Docker'ın hayatımıza girmesiyle birlikte yalnızca bu sorun çözülmekle kalmadı yaşanılan diğer birçok sorun da çözülmüş oldu. Tüm bu sürece baştan sona değinip detaylı anlatacağımız kısma yazımızın ilerleyen yerlerinde geleceğiz. Şimdilik kavramları basitçe anlamamız yeterli olacaktır.

## API Gateway

Şimdi sıradaki kavramımız olan API Gateway üzerinde biraz duralım. Mikroservis mimarisini kullanan bir web sitesine girdiğimiz zaman biz burada kullanılan mikroservislerle tek tek haberleşip erişim sağlamayız. Zaten bu durum oldukça anlamsız olacaktır. Front-end bu haberleşmeyi yapıp bize web sitesinin son halini sunar. Bunu yapabilmek için de API Gateway isimli mikroservisi kullanır. API Gateway mikroservisi diğer tüm mikroservislerin bağlı olduğu ve bazı görevlerin merkezileştirildiği yerdir. İstemciler diğer mikroservislerle API Gateway mikroservisi üzerinden haberleşir.
