# DevOps Defterim

Kişisel ders notlarından (Bulut Bilişim ve DevOps Bootcamp) üretilen statik dokümantasyon sitesi. Astro + Starlight, tamamen statik çıktı. İç planlama notları `private-notes/` altında (git'e girmez).

## Yapı

```
src/content/docs/<modul>/<sayfa>.md   içerik (alt klasör = menüde grup)
src/config/modules.mjs                menü sırası, modül adları, grup adları
src/config/lessons.mjs                ders no → video başlığı (sayfa meta satırı)
src/config/sidebar.mjs                menüyü klasör + frontmatter order'dan üretir
src/components/                       Starlight override'ları (Header, Head, PageTitle, ...)
src/styles/theme.css                  palet, tipografi
scripts/                              build sonrası CSP meta/base önek, link ve hassas veri kontrolü
tools/pdf-fingerprints.py             PDF sayfa parmak izleri
tools/screenshots/                    ekran görüntüsü çıkarma ve WebP'ye çevirme (isteğe bağlı karartma)
src/assets/ekran/                     PDF'teki ekran görüntüleri (WebP)
.claude/skills/yeni-pdf-isle/         yeni PDF işleme akışı
```

Kaynak PDF/PNG'ler, render'lar ve çalışma dosyaları repoya girmez (`.gitignore`). Bunları `sources/` ve `work/` altında tut.

## Komutlar

```bash
npm ci                    # bağımlılıklar
npm run dev               # yerel geliştirme
npm run build             # dist/ + CSP meta etiketleri ve base önekli bağlantılar (scripts/postbuild.mjs)
npm run check             # iç bağlantı + hassas veri kontrolü (build sonrası)
```

## Yeni modül eklemek

1. `src/content/docs/<modul>/` klasörünü oluştur.
2. `src/config/modules.mjs` listesine `{ dir, label, summary, groups? }` girdisi ekle.
3. Gerekirse `src/config/lessons.mjs`'e ders başlıklarını ekle.

## Frontmatter

```yaml
---
title: cp komutu                 # zorunlu
description: Dosya ve dizin kopyalama   # tek cümle
module: linux                    # klasör adı
lessons: [2, 3]                  # ders numaraları; mini proje talimat videosu için "talimat"
order: 3                         # modül içindeki sıra (menü ve önceki/sonraki)
---
```

Dosya ve klasör adları ASCII (ç→c, ğ→g, ı/İ→i, ö→o, ş→s, ü→u). H1 yazılmaz; gövde `##`/`###` ile bölünür.

## İçerik dönüştürme kuralları

- PDF'in her sayfası hem metin olarak (pdftotext) hem görsel olarak (pdftoppm, ~150 dpi) okunur. Ekran görüntülerindeki komutlar metin katmanında yoktur.
- Ekran görüntüsünün içeriği metne dökülür:
  - Terminal → kod bloğu. Prompt atılır. Komut `bash frame="terminal"` bloğunda, çıktı ayrı `text title="Çıktı"` bloğunda.
  - Konsol adımları → numaralı liste (**EC2 → Instances → Launch instance**).
  - Tablo → Markdown tablo. Şema → tablo/metin.
- PDF'teki ekran görüntülerinin hepsi, karartma yapılmadan, PDF'teki yerine eklenir:
  - Çıkarma: `python tools/screenshots/extract.py <pdf> work/<tarih>/raw`, WebP'ye çevirme: `python tools/screenshots/export.py work/<tarih>/raw` → `src/assets/ekran/<pNNN-k>.webp` (N: PDF sayfası, k: sayfadaki sıra).
  - Sayfada: `![Anlamlı alt metin](../../../assets/ekran/p018-1.webp)`. O görüntüden aktarılan kod bloğu/tablo hemen altına gelir.
  - `pipeline.py` / `redact.py` isteğe bağlı karartma hattıdır; varsayılan akışta kullanılmaz.
- Metin, kullanıcının PDF'teki cümleleridir. Sadece yazım/noktalama düzeltilir, komut ve buton adları `kod`/**kalın** yapılır, metin `##` başlıklarla bölünür, konsol adımları aynı kelimelerle numaralı listeye çevrilir. Cümleler yeniden yazılmaz, özetlenmez; notta olmayan açıklama eklenmez.
- Kullanıcının cümlesinde teknik hata varsa cümle kalır, altına `:::caution[Düzeltme]` kutusu eklenir ve review notlarına yazılır.
- Komutlar harfi harfine aktarılır. Emin olunamayan karakter tahmin edilmez, review notlarına sayfa numarasıyla yazılır.
- Hassas veri yer tutucuyla değişir, orijinal değer hiçbir yere yazılmaz: `<AWS_ACCOUNT_ID>`, `<AWS_ACCESS_KEY_ID>`, `<AWS_SECRET_ACCESS_KEY>`, `<GITHUB_TOKEN>`, `kullanici@example.com`, kişi adı → `Ad Soyad` / `ornek` / `ornekkullanici`, public IP → `203.0.113.x`, private IP → `172.31.0.x`, hostname → `ip-172-31-0-10`, kaynak ID'leri → `i-0123456789abcdef0` vb.
- Uyarı kutuları: `:::note`, `:::tip`, `:::caution`, `:::danger` (notta geçen uyarı cümleleri için, metin aynen).
- İç bağlantılar `/modul/sayfa/` biçiminde ve sadece var olan sayfalara.

## Yeni PDF akışı

`/yeni-pdf-isle <pdf-yolu>` skill'ini kullan. Özet: parmak izleriyle yeni sayfaları bul → plan sun → onay sonrası dönüştür → kapsam tablosu ve review notlarını güncelle → build ve kontroller → yayına alma kararını kullanıcıya bırak.

## Kurallar

- Push (= yayın) kullanıcı istemeden yapılmaz.
- Harici script, analitik, font CDN'i eklenmez. Fontlar `@fontsource` paketleriyle self-host.
- Yeni inline script eklenirse CSP hash'i build sonrası otomatik eklenir; harici kaynak eklenmez.
- Site GitHub Pages'te `https://devops-defterim.github.io/` adresinde, `devops-defterim` organizasyonunun `devops-defterim.github.io` reposundan yayınlanır (`main`'e push = yayın, `.github/workflows/deploy.yml`). İç bağlantılar `/modul/sayfa/` yazılır.
- Bağımlılıklar minimumda; `npm audit` temiz kalmalı.
