---
title: Servis modelleri
description: On-premises, IaaS, PaaS ve SaaS modellerinde sorumluluk paylaşımı, pizza benzetmesi ve modellerin birbirine göre avantajları.
module: bulut-temelleri
lessons: [16]
order: 2
---

[Sunucudan buluta](/bulut-temelleri/sunucudan-buluta/) sayfasında anlatılan Infrastructure as a Service, bulut hizmetini satın almanın ilk şekliydi. Zamanla hizmeti sağlayan firmanın üstlendiği katmanlar arttı.

## IaaS, PaaS ve SaaS

- **Infrastructure as a Service (IaaS)**: On-premises sisteme kıyasla IaaS kullanan şirketler altyapının fiziksel sorunları ve bakımıyla ilgilenmez, ancak bu altyapıya kuracakları uygulamanın tüm sorumluluğunu üstlenir.
- **Platform as a Service (PaaS)**: IaaS'tan sonra gelen bu modelde runtime, middleware ve işletim sisteminin (O/S) yönetimi de hizmeti verenler tarafından sağlanır. Sanal makinelere kurulan işletim sistemleri, isteğe bağlı olarak örneğin Java runtime ve gerekli kütüphaneler hizmet sağlayıcı tarafından yönetilir. Böylece örneğin bir Java developer yalnızca uygulamayı oluşturup yükler; uygulamanın yazılması ve verilerinin yönetimi onun sorumluluğunda kalır.
- **Software as a Service (SaaS)**: Yalnızca bir uygulamayı kullanmak isteyen, arka planda gerçekleşen hiçbir işlemle ilgilenmeyen şirketler için ortaya çıkmış bir modeldir. Bütün altyapı hizmet sağlayıcı tarafından karşılanır; kullanıcı yalnızca bir arayüz üzerinden kullanıcı adı ve şifre girerek sisteme bağlanır ve hizmeti kullanır.

## Kim neyi yönetir

| Katman | On-Premises | IaaS | PaaS | SaaS |
| --- | --- | --- | --- | --- |
| Applications | Siz | Siz | Siz | Sağlayıcı |
| Data | Siz | Siz | Siz | Sağlayıcı |
| Runtime | Siz | Siz | Sağlayıcı | Sağlayıcı |
| Middleware | Siz | Siz | Sağlayıcı | Sağlayıcı |
| O/S | Siz | Siz | Sağlayıcı | Sağlayıcı |
| Virtualization | Siz | Sağlayıcı | Sağlayıcı | Sağlayıcı |
| Servers | Siz | Sağlayıcı | Sağlayıcı | Sağlayıcı |
| Storage | Siz | Sağlayıcı | Sağlayıcı | Sağlayıcı |
| Networking | Siz | Sağlayıcı | Sağlayıcı | Sağlayıcı |

## Pizza benzetmesi

Pizza yemek istediğimizi ve bunu dört farklı şekilde yapabileceğimizi düşünelim:

- **On-Premises (Made at Home)**: Pizzanın hamurunu yapmaktan pişirmeye, masayı kurmaktan içeceğe kadar her şeyle siz ilgilenirsiniz.
- **IaaS (Take and Bake)**: Marketten hazır pizza alıp evde pişirir, masayı kurup yersiniz.
- **PaaS (Pizza Delivered)**: Pizzayı internetten sipariş edersiniz; hiçbir yapım aşamasına karışmadan yalnızca masayı kurup yersiniz.
- **SaaS (Dined Out)**: Bir restorana gidersiniz; masanın kurulması dahil hiçbir aşamada çaba harcamadan yalnızca pizzanızı yersiniz.

| Katman | On-Premises | IaaS | PaaS | SaaS |
| --- | --- | --- | --- | --- |
| Dining Table | Siz | Siz | Siz | Sağlayıcı |
| Soda | Siz | Siz | Siz | Sağlayıcı |
| Electric / Gas | Siz | Siz | Sağlayıcı | Sağlayıcı |
| Oven | Siz | Siz | Sağlayıcı | Sağlayıcı |
| Fire | Siz | Siz | Sağlayıcı | Sağlayıcı |
| Pizza Dough | Siz | Sağlayıcı | Sağlayıcı | Sağlayıcı |
| Tomato Sauce | Siz | Sağlayıcı | Sağlayıcı | Sağlayıcı |
| Cheese | Siz | Sağlayıcı | Sağlayıcı | Sağlayıcı |
| Toppings | Siz | Sağlayıcı | Sağlayıcı | Sağlayıcı |

## Modellerin birbirine göre avantajları

### On-premises neden hâlâ kullanılıyor

- Bazı durumlarda uzaktaki bir sunucuda bir şeyleri barındırmak, lokaldeki bir sunucuda barındırmaktan çok daha yavaştır.
- Güvenlik: tamamen kapalı sistemlere ihtiyaç duyulması ve verilerin gizliliği.
- En önemlisi, bazı regülasyonlar nedeniyle verilerin başka bir yerde tutulmasına izin verilmemesi (örneğin bankalar, devlet kurumları).

### IaaS neden hâlâ kullanılıyor

- PaaS'ta runtime, middleware ve işletim sistemi karşı firma tarafından yönetildiği için, daha eski bir sürüm kullanan bir uygulamayı çalıştırmak mümkün olmayabilir. Bu üç katmanda değişikliğe ihtiyaç duyulan durumlarda IaaS daha avantajlıdır.
- Örneğin 100-200 gibi çok sayıda uygulama varsa, bunları PaaS'ta yönettirmenin maliyeti, IaaS'ta bu uygulamaları yönetmek için kurulacak altyapının maliyetinden çok daha yüksek olur; IaaS bu durumda daha verimlidir.

### PaaS ne zaman SaaS'a tercih edilir

Uygulamada değişiklik yapmak istediğimiz durumlarda SaaS yerine PaaS tercih edilir.
