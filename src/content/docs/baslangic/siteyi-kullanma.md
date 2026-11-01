---
title: Siteyi kullanma
description: Menü, arama, kod blokları ve sayfa düzeni hakkında kısa bilgiler.
module: baslangic
order: 1
prev: false
next:
  link: /baslangic/calisma-makinesi/
  label: Çalışma makinesini açma
---

Notlar konulara göre gruplanmıştır: Linux, Git ve GitHub, mini proje, bulut bilişim temelleri ve AWS. Sıra, derslerin işlendiği sırayı büyük ölçüde izler. Derslere AWS'de bir çalışma makinesi açarak başlanır; ana sayfadaki **Başla** düğmesi oraya götürür.

## Menü

Sol üstteki menü düğmesi soldaki menüyü açar ve kapatır. Geniş ekranda kapattığın menü, sonraki ziyaretinde de kapalı kalır. Menünün en üstündeki **Bu sayfada** bölümü, okuduğun sayfanın başlıklarını listeler. Altında konu listesi vardır; bulunduğun sayfanın grubu otomatik olarak açık gelir.

## Arama

Arama kutusunu <kbd>Ctrl</kbd> + <kbd>K</kbd> (macOS'ta <kbd>⌘</kbd> + <kbd>K</kbd>) ya da <kbd>/</kbd> tuşuyla açabilirsin. Arama Türkçe kelimelerle çalışır. Örneğin "kopyalama" ya da "izinler" yazmayı dene.

## Kod blokları

Komutlar terminal çerçeveli bloklarda durur. Sağ üstteki düğme bloğu panoya kopyalar:

```bash frame="terminal"
ls -l
```

Komutun çıktısı, kopyalanmasın diye ayrı bir blokta verilir:

```text title="Çıktı"
total 0
```

## Yer tutucular

Metindeki komut ve çıktılarda kişisel ve hesaba özel değerler yer tutucularla yazıldı. Ekran görüntülerinde ise gerçek değerler görünür:

| Yer tutucu | Anlamı |
|---|---|
| `<AWS_ACCOUNT_ID>` | 12 haneli AWS hesap numaran |
| `<AWS_ACCESS_KEY_ID>`, `<AWS_SECRET_ACCESS_KEY>` | IAM kullanıcısının erişim anahtarları |
| `203.0.113.10` | Sunucunun public IP adresi |
| `172.31.0.10` | Sunucunun VPC içindeki private IP adresi |
| `kullanici@example.com` | E-posta adresi |

## Sayfa düzeni

Her sayfanın başlığının altında notun tutulduğu ders yazar. Sayfanın sonunda önceki ve sonraki sayfaya bağlantılar bulunur.
