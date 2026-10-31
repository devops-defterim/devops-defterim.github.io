---
title: API
description: API kavramı, REST API, microservice mimarisinin getirdiği yönetim yükü, Docker'ın ortaya çıkışı ve API Gateway.
module: bulut-temelleri
lessons: [17]
order: 4
---

## API nedir

Yazılımı satın alan kişiler ona bir web adresi üzerinden, klavye ve fare kullanarak erişebiliyordu. Bazı müşteriler kullanılan verileri kendi Excel'lerinde görmek istediğinde, üretilen yazılımın başka bir yazılım tarafından kullanılamadığı fark edildi. Yazılımın başka yazılımlar tarafından da kullanılabilmesi için onlara bir kapı açmak gerekiyordu. API bu sorunu çözer.

**API (Application Programming Interface)**, uygulamaların diğer uygulamalarla konuşmak için oluşturduğu; protokolleri, iletişim yetenekleri ve neler yapabildiği en baştan belli olan kapılardır. Bu kapılar sayesinde [microservice mimarisinde](/bulut-temelleri/yazilim-gelistirme-ve-devops/#monolithten-microservice-mimarisine) oluşturulan her servis birbiriyle haberleşebilir hale geldi.

REST API, FastAPI, Windows API gibi çeşitleri vardır. **REST API protokolü**, birbirinden uzakta olan iki uygulamanın API üzerinden haberleşmesini sağlayan ve istekleri HTTP olarak gönderen bir protokoldür.

## Microservice'lerin getirdiği yük ve Docker

Microservice mimarisinin getirdiği kolaylıklar, zaman ilerledikçe yönetilmesi gereken onlarca işletim sistemini de ortaya çıkardı. Monolith sistemde back-end işlemleri tek bir binary üzerinden yürürken, microservice ile bu işlemler farklı sistemlere ayrıldı ve yönetilmesi gereken çok sayıda makine oluştu. Sanallaştırma sayesinde makine kurmak kolaylaşmış, bir makine üzerinde onlarca sanal makine çalıştırılabiliyordu; ancak artık bakımı yapılması gereken onlarca sunucu vardı ve bu büyük bir problemdi.

Çözüm ararken, tüm bu uygulamaların tek bir işletim sistemi üzerinde birbirinden izole olarak yönetilip yönetilemeyeceği düşünüldü ve cevap olarak **Docker** ortaya çıktı. Docker container teknolojisi, tek bir işletim sistemi üzerinde birden fazla uygulamayı birbirinden tamamen bağımsız ve izole şekilde çalıştırmayı mümkün kıldı. Böylece uygulamaları izole etmek için ayrı ayrı işletim sistemlerine kurmaya gerek kalmadı ve onlarca sunucuyu yönetme yükü ortadan kalktı. Docker bu sorunun yanında başka birçok sorunu da çözdü; bu konu ileride ayrıntılı olarak anlatılacaktır. Şimdilik kavramı basitçe anlamak yeterlidir.

## API Gateway

Microservice mimarisini kullanan bir web sitesine girdiğimizde, kullanılan microservice'lerle tek tek haberleşmeyiz; bu oldukça anlamsız olurdu. Bu haberleşmeyi front-end yapar ve bize web sitesinin son halini sunar. Bunun için **API Gateway** adlı microservice'i kullanır.

API Gateway, diğer tüm microservice'lerin bağlı olduğu ve bazı görevlerin merkezileştirildiği yerdir. İstemciler diğer microservice'lerle API Gateway üzerinden haberleşir.
