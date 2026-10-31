---
title: Siteyi kullanma
description: Menü, arama, kod blokları ve sayfa düzeni hakkında kısa bilgiler.
module: baslangic
order: 1
---

Notlar konulara göre gruplanmıştır: Linux, Git ve GitHub, mini proje, bulut bilişim temelleri ve AWS. Sıra, derslerin işlendiği sırayı büyük ölçüde izler.

## Menü

Sol üstteki menü düğmesi soldaki konu listesini açar ve kapatır. Geniş ekranda kapattığın menü, sonraki ziyaretinde de kapalı kalır. Bulunduğun sayfanın grubu menüde otomatik olarak açık gelir.

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

Ekran görüntülerinden aktarılan kişisel ve hesaba özel değerler yer tutucularla değiştirildi:

| Yer tutucu | Anlamı |
|---|---|
| `<AWS_ACCOUNT_ID>` | 12 haneli AWS hesap numaran |
| `<AWS_ACCESS_KEY_ID>`, `<AWS_SECRET_ACCESS_KEY>` | IAM kullanıcısının erişim anahtarları |
| `203.0.113.10` | Sunucunun public IP adresi |
| `172.31.0.10` | Sunucunun VPC içindeki private IP adresi |
| `kullanici@example.com` | E-posta adresi |

## Sayfa düzeni

Her sayfanın başlığının altında notun tutulduğu ders yazar. Sağ taraftaki "Bu sayfada" listesi sayfanın başlıklarını gösterir. Sayfanın sonunda önceki ve sonraki sayfaya bağlantılar bulunur.
