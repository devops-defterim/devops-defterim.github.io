---
title: Siteyi kullanma
description: Menü, arama, kod blokları ve sayfa düzeni hakkında kısa bilgiler.
module: baslangic
order: 1
sidebar:
  hidden: true
prev: false
next:
  link: /baslangic/calisma-makinesi/
  label: Çalışma makinesini açma
---

Notlar konulara göre gruplanmıştır: Linux, Git ve GitHub, mini proje, bulut bilişim temelleri ve AWS. Sıra, derslerin işlendiği sırayı büyük ölçüde izler. Derslere AWS'de bir çalışma makinesi açarak başlanır; ana sayfadaki **Öğrenmeye başla** düğmesi oraya götürür.

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

## Gizlenen bilgiler

Hesap numarası, erişim anahtarları, şifreler, token'lar ve e-posta adresleri gibi kritik bilgiler ekran görüntülerinde bulanıklaştırıldı, metinlerde yıldızla gösterildi:

| Gösterim | Anlamı |
|---|---|
| `************` | 12 haneli AWS hesap numarası |
| `********************` | AWS access key ID |
| `****************************************` | AWS secret access key veya GitHub token |
| `**********@*****.com` | E-posta adresi |

Komutları kendin denerken bu yerlere kendi değerlerini yazmalısın. Kod bloklarındaki `203.0.113.10` gibi IP adresleri ve `ornekkullanici` gibi adlar da örnek değerlerdir.

Sayfanın sonunda önceki ve sonraki sayfaya bağlantılar bulunur.
