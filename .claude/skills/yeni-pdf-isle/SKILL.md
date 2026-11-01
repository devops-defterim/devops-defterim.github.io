---
name: yeni-pdf-isle
description: Ders notlarının yeni bir PDF sürümünü işler. Hangi sayfaların yeni olduğunu bulur, yeni site sayfalarını hazırlar, kapsam tablosunu ve review notlarını günceller, yayına almadan önce kullanıcıya sorar. Kullanıcı yeni bir notlar PDF'i verdiğinde veya /yeni-pdf-isle dediğinde kullan.
disable-model-invocation: true
argument-hint: <pdf-yolu>
---

# Yeni PDF işle

Girdi: `$ARGUMENTS` (PDF yolu). Verilmediyse `sources/` altındaki en yeni PDF'i öner ve kullanıcıya doğrulat.

Proje kuralları `CLAUDE.md` içinde. Bu akış boyunca onlara uy.

## 1. Hazırlık

- PDF'i `sources/` altına koy (git'e girmez). Çalışma dosyaları `work/<tarih>/` altında olsun.
- `pdfinfo` ile sayfa sayısı ve metin katmanını kontrol et.
- Metin çıkar (`pdftotext -layout`, sayfa başına) ve sayfaları render et (`pdftoppm -r 150 -png`).

## 2. Ne değişti?

- Yeni PDF'in parmak izlerini çıkar: `python3 tools/pdf-fingerprints.py <pdf> > work/<tarih>/fingerprints.tsv`
- Önceki sürümün parmak izleri `private-notes/page-fingerprints.tsv` dosyasında. Karşılaştır:
  - Parmak izi aynı olan sayfalar zaten işlenmiş. Eski sayfa numarasını `private-notes/COVERAGE.md` tablosunda bularak site sayfasını eşle.
  - Eşleşmeyen sayfalar yeni ya da değişmiş. Değişmiş olanları ilk 80 karakter benzerliğinden ve konumdan ayırt et.
- Sonuç türünü belirle:
  - **Tam sürüm (Ders 0–N):** eski sayfaların çoğu eşleşir, sonda yeni sayfalar vardır.
  - **Sadece yeni dersler:** eski sayfaların neredeyse hiçbiri yoktur.
- Değişmiş eski sayfalar için mevcut site sayfasıyla farkı çıkar (yeni cümle, yeni komut, silinmiş kısım).

## 3. Plan (onay bekle)

Kullanıcıya şunları sun ve onayını bekle; onaysız dosya yazma:

- Yeni ve değişmiş PDF sayfalarının listesi.
- Önerilen yeni sayfalar: dosya yolu, başlık, `order`, `lessons`, PDF sayfa aralığı. Mevcut modül mü, yeni modül mü (yeni modülse `modules.mjs` girdisi).
- Mevcut sayfalarda yapılacak değişiklikler.
- Belirsiz noktalar için en fazla 5 soru.

## 4. Dönüştürme

- PDF uzunsa sayfa aralıklarını alt ajanlara paylaştır. Her ajana `CLAUDE.md` içindeki dönüştürme kurallarını ve kendi dosya listesini ver. Her ajan şunları üretir:
  - içerik dosyaları (`src/content/docs/...`)
  - review notu: belirsiz okumalar, düzeltilen komutlar, maskelenen veri türü ve yeri (orijinal değer yazılmaz), eksik yerler, görsel adayları
  - kapsam satırları: `pdf_sayfa<TAB>site_dosyası<TAB>not`
- Gerekirse `src/config/modules.mjs` ve `src/config/lessons.mjs`'i güncelle.

## 4b. Ekran görüntüleri

- `python tools/screenshots/pipeline.py <pdf> work/<tarih>/ekran` çalıştır. Gereken araçlar: `pymupdf`, `pillow`, `swiftc`, `tesseract`.
- Dosya adları PDF sayfa numarasına bağlıdır (`pNNN-k`). Tam sürüm PDF'te sayfa numaraları kaydıysa eski görüntüleri yeni numaralarla eşleyip sayfalardaki yolları güncelle.
- Her yeni görüntüyü gözle kontrol et (alt ajanlara paylaştırılabilir). Kaçakları `private-notes/redact-manual.json`'a oransal kutu olarak ekleyip hattı yeniden çalıştır.
- Görüntüleri ilgili sayfada, PDF'teki konumuna denk gelen metnin ardına anlamlı alt metinle ekle.

## 5. Güncelle ve doğrula

- `private-notes/COVERAGE.md`: yeni PDF'in sayfa numaralarıyla yeniden üret. Her sayfa en az bir site sayfasına eşlenmeli.
- `private-notes/REVIEW.md`: yeni notları ekle, tarih başlığıyla.
- `private-notes/page-fingerprints.tsv`: yeni PDF'in parmak izleriyle değiştir (eskisini `work/` altına yedekle).
- `npm run build && npm run check`. `private-notes/` altında ek kontrol script'i varsa onu da çalıştır.
- Yeni sayfalardan en az ikisinin 375px ve 1440px ekran görüntüsünü alıp incele.

## 6. Yayın kararı

- Değişiklikleri `icerik/<tarih>` adlı ayrı bir branch'e commit'le. `main`'e merge etme, push etme.
- Kullanıcıya özet ver: eklenen/değişen sayfalar, review'da bakılması gerekenler, kontrol sonuçları.
- **Yayına alma ve erişim kararını kullanıcıya bırak.** Kullanıcı açıkça isteyene kadar merge, push veya deploy yapma.
