---
title: İşletim sistemi, terminal ve shell
description: İşletim sisteminin ortaya çıkışı, kernel ve sistem çağrıları, sanallaştırma ile terminal ve shell arasındaki fark.
module: linux
lessons: [1]
order: 1
---

## İşletim sistemi neden ortaya çıktı

Bilgisayarlar ilk ortaya çıktığında işletim sistemleri yoktu. Bilgisayara doğrudan bir program yükleniyor ve o programa ne yapması gerektiği söyleniyordu. Farklı bir uygulama çalıştırmak için ikinci bir bilgisayar gerekiyordu; yani bilgisayarlar tek bir programı çalıştırmak üzerine kuruluydu.

Zamanla bir bilgisayara birden fazla uygulama kurulabilir hale geldi, fakat bu sefer de her uygulamayı tek tek çalıştırmak gerekiyordu.

İlk bilgisayarlara yüklenen bu programlar, monitöre gelecek veriden donanım parçalarına kadar her şeyi kendileri kontrol ediyordu. Makineyi kontrol etme işini uygulamaların üzerinden almak ve uygulamalarla makine arasında köprü görevi görmek için bir katman daha yazıldı. İşletim sistemi kavramı böyle ortaya çıktı.

Artık uygulamalar donanıma doğrudan ulaşmak yerine önce işletim sistemine ulaşır, ne istediğini söyler ve işlemi işletim sistemi yapar.

## İşletim sisteminin bileşenleri

Tam anlamıyla bir işletim sistemi üç bileşenden oluşur:

- Kernel
- Kullanıcı arayüzü
- Uygulamalar

**Kernel**, işletim sisteminin bütün işlerini yapan ve bilgisayarın bütün donanımını yöneten ana kısımdır. Donanımı yöneterek uygulamaların onu kullanabilmesini sağlar. Bunun için uygulamaların kernel ile konuşabilmesi gerekir; bu konuşma **sistem çağrıları (system call)** ile yapılır.

## Sanallaştırma

Eskiden bir sunucu bilgisayarda tek bir uygulama çalıştırılabiliyordu, çünkü aynı sunucuya birden fazla uygulama kurulduğunda uygulamalar birbirine bağımlı hale geliyordu. Her uygulama için ayrı bir sunucu kurmak hem zahmetliydi hem de kaynak israfına yol açıyordu.

Sanallaştırma bu sorunları çözerek tek bir donanım üzerinde birden fazla işletim sistemi kullanabilmeyi sağladı.

## Terminal ve shell

**Terminal**, bir Linux sunucuya uzaktan bağlanıp komut göndermeyi sağlayan, fakat kendi üzerinde hiçbir işlem yapılmayan arayüzdür.

Bir bilgisayarı yönetmenin iki yolu vardır: grafik arayüz üzerinden ya da komut satırından. **Shell**, komut satırına verilen komutları işleyerek sistemi yönetmeyi sağlayan altyapıdır. Linux'un kullandığı shell, **bash** uygulamasıdır.

Bir sonraki adımda [oluşturulan sanal makineye](/baslangic/calisma-makinesi/) bağlanıp [temel Linux komutlarına](/linux/temel-komutlar/) geçilir.
