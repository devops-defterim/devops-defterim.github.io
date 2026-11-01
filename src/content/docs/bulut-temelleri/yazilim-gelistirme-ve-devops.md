---
title: Yazılım geliştirme döngüsü ve DevOps
description: Geleneksel yazılım geliştirme döngüsü, SaaS ile gelen değişim, DevOps'un doğuşu ve monolith'ten microservice mimarisine geçiş.
module: bulut-temelleri
lessons: [17]
order: 3
---

Bu değişimlerin yazılım geliştirme döngüsüne nasıl etki ettiğini öğrenmek için yazımıza devam edelim.

Bir yazılım ekibinin yazılım projesini nasıl ele aldığına ve bunun nasıl değişim gösterdiğine gelin birlikte bakalım.

## Geleneksel yazılım geliştirme döngüsü

Geleneksel olarak yazılımlar şu süreçlerden geçer; ilk olarak ekipçe bir gereksinim analizi yapılır. Burada yazdığımız yazılımın ne yapması gerektiği üzerine konuşuruz. Daha sonra belirlenen gereksinimleri dizayn aşamasında yazılım haline getirmemiz için ne yapmamız gerektiği hakkında tartışırız ve yapılacak işin yol haritasını çıkartırız. Ardından dizayn aşamasında belirlediğimiz bu listeyi kodlama-oluşturma adımına geçirerek kodunu yazmaya başlarız. Yazılan bu kodla ilgili test aşamasında dizayna göre oluşturulan kodlamanın gereksinimlerimizi karşılayıp karşılamadığını kontrol ederiz. Aynı zamanda kodun kalitesi ve hızı gibi özelliklerini de test ederiz. Son olarak ortaya bir versiyon yani uygulama çıkartılarak tekrar başa döneriz ve gereksinimleri yeniden analiz ederiz. İşte eskiden günümüze bir yazılım sürecini bu döngüyü takip ederek yürütüyorduk. Bu sürece döngü denmesinin temel sebebi, bir yazılımın bütün gereksinimlerini, yapması gerekenleri tek seferde belirleyip, kodlayıp, test edebilme imkanının olmamasıdır.

### Beta aşaması

Anlatılan bu döngüde gereksinim analizleriyle hedef olarak belirlediklerimizi tamamlayıp ilk versiyonu çıkartmaya çok yakın bir dönemde kodumuza beta aşaması gelir. Beta aşaması kodun neredeyse müşteriye gönderilmeye hazır olduğu ama tüm özellikleri kapsamayan ve bütün fonksiyonlarının çalıştığını garanti etmeyen bir halidir. Eskiden uygulamaya eklenecek her şey yazılım geliştirme ekibi tarafından dışarıdaki müşterilerden herhangi bir feedback almadan gerçekleştiği için beta aşaması müşterilere sunularak az da olsa sağlanan bu geri dönüşlerle uygulamamızdaki hataları düzeltirdik ve böylece nihai sürüme ulaşırdık.

## Eskiden dağıtım nasıl yapılırdı

Yazılımın son halini dağıtım aşamasına geldiğimizde eskiden bu süreç şöyle işlerdi; geliştirmiş olduğumuz yazılımın son halini müşteriye ulaştırmak istediğimizde öncelikle bu yazılımı bir cd veya dvd'ye yüklerdik. Kendi sistemlerine nasıl kuracaklarına dair yönergeyle birlikte gönderirdik. Müşteri aldığı yazılımı kendi ekibiyle çalıştırarak kullanırdı. Herhangi bir sorunla karşılaştığında ise bize geri bildirim gönderirdi. Biz de yazılımın destek paketinde varsa yazılım ekiplerimizle bu sorunu çözen fix'i müşteriye gönderirdik. Müşteri bunu kendi sistemine kurardı ve sorun çözülmüş oluyordu. Ancak bu sayede yazılımla ilgili feedback toplamış oluyorduk çünkü yazılımın çalıştırıldığı sistemler bizim yönetimimizde değildi ve doğrudan müdahale edemiyorduk. Bu durumu yazılım firması tarafından ele alırsak geri bildirimin zor oluşu, yazılımın kurulduğu sistemin kontrolüne sahip olamayışı ve yüzlerce değişik sistem konfigürasyonu için uyumluluk sağlamanın zorluğu olumsuz sonuçlar doğuruyordu. Aynı zamanda problem çözmenin zahmetli ve yavaş olması, en ufak bir yeni özelliği barındıran sürümlere erişmenin aylar sürmesi, altyapı oluşturma ve yönetme işlemlerinin zahmetli ve pahalı olması da müşteri için oluşan olumsuzlukların başında geliyordu.

Bu döngüyü takip ederek bir yazılımı oluşturmak bir yıldan daha fazla sürüyordu.

## Günümüzdeki değişim

Yirmi yıl öncesine kadar yazılım geliştirme süreci kısaca böyle işlerdi. Günümüzde bu döngüde takip edilen aşamalar çoğunlukta olmakla birlikte gereksinim analizi sürece yayıldı ve müşterilerden çok daha fazla alınan geri dönüşler sayesinde yazılımımız şekillenmeye başladı. Ayrıca en önemli değişim burada hız faktörü oldu.

Network'lerin bağlantı hızlarının artması, sanallaştırma gibi kavramlarla bilgisayarlar daha kolay yönetilebiliyor hale geldi. Bu değişimler sayesinde software as a service modeli ortaya çıktı ve bu modelle birlikte bahsettiğimiz sıkıntıların çoğunu ortadan kaldıran bir yaklaşım geliştirildi.

Bu yaklaşım müşterilerin isteği doğrultusunda hareket ederek; gerekirse eski usulde olduğu gibi yazılımı yönetimiyle birlikte müşteriye verip gerekirse de yazılımın kurulumunu ve yönetimini şirkete bırakarak hizmet sağlamaya devam edildi. Müşteriler yeni yöntemde yazılıma internet üzerinden bilgisayarlarına yüklenen bir client aracılığıyla ya da internet sitesi üzerinden kullanıcı şifre girerek ulaşmaya başladı. Böylece ortaya çıkan sorunları anında kendi sistemlerimiz üzerinden çözer hale geldik. Ayrıca yazılımlar bizim sistemlerimizde çalıştığı için feedback toplamak amacıyla müşterilere gitmemize gerek kalmadı. Tüm bu olumlu gelişimler sayesinde işler çok hızlı hale geldi ve müşteri memnuniyeti de arttı.

## DevOps'un ortaya çıkışı

Bu kısımda Infrastructure ve yazılım tarafında olan değişimlerden bahsettik şimdi gelin bu yazılım ve operasyondaki değişimlerin altyapıda birlikte çalışma şeklinin nasıl değiştiğine kısaca göz atalım.

Eskiden yazılım ve operasyon olmak üzere amaçları, yöneticileri farklı iki ekip vardı. Bir yazılım geliştirmek istediğimizde, yazılım ekibi bu süreci yönetiyordu. Yazılımın yeni bir sürümü ortaya çıktığında ise bu sürümü alarak operasyon ekiplerine devrediyordu. Operasyon ekipleri de bu sürümü alıp operasyon yapılacak sistemlere geçirerek yazılımı ayakta tutmaya çalışıyordu.

Yazılım ekibinin nihai amacı müşterilerden topladığı feedback'ler doğrultusunda yazılım geliştirme kodlarını operasyon ekiplerine göndermekti ne kadar kod gönderirse o kadar başarılı sayılırlardı. Operasyon ekiplerinin amacıysa gönderilen bu kodları hayata geçirirken en az hata almak ve uzun süre ayakta kalmasını sağlamaktı. Burada bir çıkar çatışması oluyordu ve bu iki ekip süreçte sorunlar yaşıyordu. Çünkü yazılım ekibi ne kadar yeni kod gönderirse o kadar başarılı sayılırken operasyon ekibi sistemde en az hata almaya çalışıyordu ancak gelen kodları hayata geçirirken hata yapma olasılıkları artıyordu. Sürecin bu kadar sancılı hale gelmesi sürecin hızını oldukça düşürdü ve verimsizleştirdi.

İşte bu noktada iki ekibi birleştirip kaybedilen hızı yeniden kazanmak ve süreçte yaşanan sorunları ortadan kaldırmak hedeflendi. İki ekip yine farklı yöneticiler altında veya farklı şekillerde yönetilebilir ancak hedefler ortak olarak belirlendi. Bu ortak amaç ilk ortaya çıktığında basit olarak şu şekildeydi; "bir yazılım fikri ortaya çıktığı andan müşteriye sorunsuz şekilde iletileceği ana kadar olan süreyi ölçelim ve hedefimiz bu süreci kısaltmak olsun" dendi. Daha sonra bu fikir üzerine birçok yeni yöntemler eklenerek günümüzdeki DevOps şeklini aldı.

Hedeflenen doğrultuda bu süreci kısaltmak için yapılabilecekler; süreci otomatize etmek, süreci monitör etmek ve tüm sistemde olan değişikliklerin daha kaliteli hale getirilmesi sorunların giderilmesi gibi yöntemlerdi.

Bahsedilen yöntemlerin uygulanması amacıyla geliştirilen Docker, Jenkins, Chef, Ansible, GitHub gibi araçlardı.

DevOps kısmını daha sonra araçlarıyla birlikte ayrıntılı şekilde anlatmak üzere burada noktalayarak yazılım mimarisinde olan değişimlere geçiyoruz.

## Monolith'ten microservice mimarisine

Mikroservis mimarisinde olan değişimleri incelemeden önce bazı tanımlamaları yaparak başlayalım; bir yazılım Front-End ve Back-End olmak üzere iki katmandan oluşur. Front-End yazılımın müşteriyle etkileşime girdiği son kısımdır burada doğrulama, veri giriş çıkışı gibi işlemler gerçekleşir. Back-End katmanında ise uygulamanın esas yapması gereken işlemler gerçekleşir bunlar; hesaplama, depolama, iletişim, loglama, analiz ve benzeri işlemlerdir.

Eskiden Back-end katmanında gerçekleştirilen tüm işlem kodları tek bir kod bloğunda tutulurdu. Bu yöntem büyük sistemlerde esnek olmayışı, düzeltilmesinin zorluğu, tek kod tabanında tutulması ve yazmasının karmaşık oluşu gibi birçok sorun oluşturuyordu.

Bu monolith sistemi microservice mimarisine çevirerek her işlemi bir servis haline getirdik ve sorunların önüne geçtik. Örneğin önceden hesaplama ve iletişim aynı kodun içinde olduğu için birinde yapılan değişiklik diğerini de etkiliyordu ancak microservice mimarisi ile her işlem ayrılarak birbirinden bağımsız ve gerektiğinde sadece birbirleriyle iletişim kurabilen servisler haline getirildi.
