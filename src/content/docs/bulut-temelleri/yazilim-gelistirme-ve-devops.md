---
title: Yazılım geliştirme döngüsü ve DevOps
description: Geleneksel yazılım geliştirme döngüsü, SaaS ile gelen değişim, DevOps'un doğuşu ve monolith'ten microservice mimarisine geçiş.
module: bulut-temelleri
lessons: [17]
order: 3
---

[Servis modelleri](/bulut-temelleri/servis-modelleri/) sayfasında anlatılan değişimler, bir yazılım ekibinin projeyi ele alış biçimini de değiştirdi.

## Geleneksel yazılım geliştirme döngüsü

Yazılımlar geleneksel olarak şu aşamalardan geçer:

1. **Gereksinim analizi**: Ekipçe yazılımın ne yapması gerektiği konuşulur.
2. **Dizayn**: Belirlenen gereksinimlerin yazılıma dönüşmesi için ne yapılması gerektiği tartışılır ve işin yol haritası çıkarılır.
3. **Kodlama / oluşturma**: Dizayn aşamasında belirlenen liste koda dökülür.
4. **Test**: Yazılan kodun dizayna göre gereksinimleri karşılayıp karşılamadığı kontrol edilir; kodun kalitesi ve hızı gibi özellikleri de test edilir.
5. **Versiyon**: Ortaya bir versiyon, yani uygulama çıkarılır ve başa dönülerek gereksinimler yeniden analiz edilir.

Bu sürece döngü denmesinin temel sebebi, bir yazılımın bütün gereksinimlerini tek seferde belirleyip kodlayıp test etmenin mümkün olmamasıdır.

### Beta aşaması

Döngüde hedeflenen gereksinimler tamamlanıp ilk versiyonun çıkmasına çok yakın bir dönemde kod **beta** aşamasına gelir. Beta, kodun neredeyse müşteriye gönderilmeye hazır olduğu ama tüm özellikleri kapsamayan ve bütün fonksiyonlarının çalıştığını garanti etmeyen halidir. Eskiden uygulamaya eklenecek her şey dışarıdaki müşterilerden geri bildirim (feedback) alınmadan geliştirildiği için beta sürüm müşterilere sunulur, bu sınırlı geri dönüşlerle hatalar düzeltilir ve nihai sürüme ulaşılırdı.

## Eskiden dağıtım nasıl yapılırdı

Yazılımın son hali müşteriye şöyle ulaştırılırdı:

1. Yazılım bir CD veya DVD'ye yüklenir, müşterinin kendi sistemine nasıl kuracağını anlatan yönergeyle birlikte gönderilirdi.
2. Müşteri yazılımı kendi ekibiyle kurup kullanırdı.
3. Bir sorunla karşılaştığında geri bildirim gönderirdi.
4. Yazılımın destek paketinde varsa, sorunu çözen fix müşteriye gönderilir, müşteri bunu kendi sistemine kurardı.

Geri bildirim ancak bu yolla toplanabiliyordu, çünkü yazılımın çalıştığı sistemler yazılım firmasının yönetiminde değildi ve doğrudan müdahale edilemiyordu.

| Taraf | Olumsuz sonuçlar |
| --- | --- |
| Yazılım firması | Geri bildirim almanın zorluğu, yazılımın kurulduğu sistemin kontrolüne sahip olamamak, yüzlerce farklı sistem konfigürasyonuyla uyumluluk sağlamanın zorluğu |
| Müşteri | Problemlerin çözümünün zahmetli ve yavaş olması, en ufak yeni özelliği içeren sürüme erişmenin aylar sürmesi, altyapı oluşturma ve yönetmenin zahmetli ve pahalı olması |

Bu döngüyü takip ederek bir yazılımı oluşturmak bir yıldan fazla sürüyordu.

## Günümüzdeki değişim

Yirmi yıl öncesine kadar yazılım geliştirme kısaca böyle işliyordu. Bugün döngüdeki aşamaların çoğu hâlâ takip edilse de gereksinim analizi sürece yayıldı ve müşterilerden çok daha fazla alınan geri bildirimlerle yazılım şekillenmeye başladı. En önemli değişim ise hız oldu.

Network bağlantı hızlarının artması ve sanallaştırma gibi kavramlarla bilgisayarlar daha kolay yönetilir hale geldi. Bu sayede software as a service modeli ortaya çıktı ve bahsedilen sıkıntıların çoğunu ortadan kaldıran bir yaklaşım geliştirildi:

- Müşterinin isteğine göre, gerekirse eski usulde olduğu gibi yazılım yönetimiyle birlikte müşteriye verildi, gerekirse kurulum ve yönetim yazılım şirketine bırakıldı.
- Müşteriler yazılıma internet üzerinden, bilgisayarlarına yüklenen bir client aracılığıyla ya da bir internet sitesine kullanıcı adı ve şifreyle girerek ulaşmaya başladı.
- Ortaya çıkan sorunlar anında yazılım firmasının kendi sistemleri üzerinden çözülebilir hale geldi.
- Yazılımlar firmanın sistemlerinde çalıştığı için geri bildirim toplamak amacıyla müşteriye gitmeye gerek kalmadı.

Bu gelişmeler sayesinde işler çok hızlandı ve müşteri memnuniyeti arttı.

## DevOps'un ortaya çıkışı

Altyapı ve yazılım tarafındaki bu değişimler, ekiplerin birlikte çalışma şeklini de değiştirdi.

Eskiden amaçları ve yöneticileri farklı iki ekip vardı:

- **Yazılım ekibi** yazılım geliştirme sürecini yönetir, yeni bir sürüm çıktığında bunu operasyon ekibine devrederdi. Nihai amacı müşterilerden toplanan geri bildirimler doğrultusunda operasyon ekibine kod göndermekti; ne kadar çok kod gönderirse o kadar başarılı sayılırdı.
- **Operasyon ekibi** bu sürümü alıp operasyon yapılacak sistemlere geçirir ve yazılımı ayakta tutmaya çalışırdı. Amacı gönderilen kodu hayata geçirirken en az hatayı almak ve sistemin uzun süre ayakta kalmasını sağlamaktı.

Burada bir çıkar çatışması vardı: yazılım ekibi ne kadar çok yeni kod gönderirse o kadar başarılı sayılırken, operasyon ekibi en az hatayı hedefliyordu; ancak gelen her yeni kod, hayata geçirilirken hata olasılığını artırıyordu. Bu sancılı süreç hızı oldukça düşürdü ve verimsizleştirdi.

Bu noktada iki ekibi birleştirip kaybedilen hızı yeniden kazanmak ve sorunları ortadan kaldırmak hedeflendi. İki ekip yine farklı yöneticiler altında veya farklı şekillerde yönetilebilir, ancak hedefler ortak belirlendi. Bu ortak amaç ilk ortaya çıktığında basitçe şuydu:

> Bir yazılım fikrinin ortaya çıktığı andan müşteriye sorunsuz şekilde iletileceği ana kadar geçen süreyi ölçelim ve hedefimiz bu süreyi kısaltmak olsun.

Bu fikrin üzerine birçok yeni yöntem eklenerek bugünkü **DevOps** şekillendi. Süreyi kısaltmak için başvurulan yöntemler:

- Süreci otomatize etmek
- Süreci monitör etmek
- Sistemdeki tüm değişikliklerin kalitesini artırmak ve sorunları gidermek

Bu yöntemleri uygulamak için Docker, Jenkins, Chef, Ansible, GitHub gibi araçlar geliştirildi. DevOps, araçlarıyla birlikte ileride ayrıntılı olarak anlatılacaktır.

## Monolith'ten microservice mimarisine

Bir yazılım iki katmandan oluşur:

- **Front-End**: Yazılımın müşteriyle etkileşime girdiği son kısımdır. Doğrulama, veri giriş-çıkışı gibi işlemler burada gerçekleşir.
- **Back-End**: Uygulamanın asıl yapması gereken işlemler burada gerçekleşir: hesaplama, depolama, iletişim, loglama, analiz ve benzeri.

Eskiden back-end katmanındaki tüm işlem kodları tek bir kod bloğunda tutulurdu (**monolith**). Bu yöntem büyük sistemlerde esnek olmaması, düzeltilmesinin zor olması, tek kod tabanında tutulması ve yazılmasının karmaşık olması gibi birçok sorun yaratıyordu.

Monolith sistem **microservice** mimarisine çevrilerek her işlem bir servis haline getirildi. Örneğin önceden hesaplama ve iletişim aynı kodun içinde olduğu için birinde yapılan değişiklik diğerini de etkiliyordu. Microservice mimarisinde her işlem ayrılarak birbirinden bağımsız, gerektiğinde yalnızca birbiriyle iletişim kuran servisler haline getirildi. Servislerin birbiriyle nasıl konuştuğu [API](/bulut-temelleri/api/) sayfasında anlatılır.
