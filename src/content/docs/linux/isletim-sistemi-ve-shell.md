---
title: İşletim sistemi, terminal ve shell
description: İşletim sisteminin ortaya çıkışı, kernel ve sistem çağrıları, sanallaştırma ile terminal ve shell arasındaki fark.
module: linux
lessons: [1]
order: 1
prev:
  link: /baslangic/calisma-makinesi/
  label: Çalışma makinesini açma
---

[Sanal makinemizi oluşturduk](/baslangic/calisma-makinesi/) şimdi biraz teorik kısma geçelim.

## İşletim sistemi neden ortaya çıktı

Bilgisayarlar ilk ortaya çıktığı zaman işletim sistemleri yoktu. Bilgisayara direkt bir program yüklüyorduk ve o programa ne yapmasını istiyorsak onu söylüyorduk. Farklı bir uygulama yüklemek istersek ikinci bir bilgisayara ihtiyaç duyuyorduk. Yani eskiden bilgisayarlar tek bir programın çalıştırılması üzerine kurulmuştu.

Zaman içerisinde bu gelişti ve bir bilgisayar üzerine birden fazla uygulama kurabilir hale geldi. Fakat bu sefer de her uygulamayı tek tek çalıştırmamız gerekti.

İlk bilgisayarlara yüklediğimiz bu programlar monitör ekranına gelecek veriden donanım parçalarına kadar her şeyi kontrol ediyordu.

Bilgisayarlara yüklenen bu uygulamaların üzerinden makineyi kontrol etme işini almak ve uygulamalar ile makine ile arasına bir köprü görevi görmesi amacıyla bir katman daha yazılmış ve işletim sistemi konsepti ortaya çıkmıştır.

Böylece uygulamalar direkt donanıma ulaşmak yerine önce işletim sistemine ulaşırlar ne istediğini söylerler ve işletim sistemi o işlemi yapar.

## İşletim sisteminin bileşenleri

Tam anlamıyla bir işletim sistemi kernel, kullanıcı arayüzü ve uygulamalar olmak üzere üç bileşenden oluşur.

**Kernel** işletim sisteminin bütün işlerini yapan, bilgisayarın bütün donanımını yöneten ana kısımdır. Bütün donanımı yöneterek bunların uygulamalar tarafından kullanılabilmesini sağlar. Bunun sağlanması için uygulamaların kernel ile konuşabilmesi gerekir. Bu konuşma **sistem çağrıları (system call)** ile sağlanır.

## Sanallaştırma

Bir sunucu bilgisayar üzerinde eskiden tek bir uygulama çalıştırabiliyorduk. Çünkü bir sunucu bilgisayar üzerine birden fazla uygulama kurmak istediğimizde uygulamalar birbirlerine bağımlı hale geliyorlardı.

Her seferinde bu şekilde bir uygulama için bir sunucu bilgisayar kurmak oldukça zahmetli ve kaynak israfına yol açıyordu.

Sanallaştırma bu sorunları çözerek tek bir donanım üzerinde birden fazla işletim sistemi kullanabilmemize imkan sağladı.

## Terminal ve shell

Şimdi linux dünyasına girmeden önce terminal ve shell farkını anlatarak başlayalım.

**Terminal**, bir linux sunucuya uzaktan bağlanıp komutlar göndermemizi sağlayan fakat üzerinde hiçbir işlem yapılmayan arayüzdür.

Bir bilgisayarı yönetmenin iki yolu vardır. Birincisi grafiksel arayüz üzerinden, diğeri komut satırı ile yönetmektir. **Shell** bu komut satırına komutlar vererek sistemi yönetmemizi sağlayan, verdiğimiz komutları işleyen altyapıdır.

Linux'un kullandığı shell, **bash** uygulamasıdır.

Şimdi oluşturduğumuz sanal makineye bağlanarak [linux komutlarını](/linux/temel-komutlar/) öğrenmeye başlayabiliriz.
