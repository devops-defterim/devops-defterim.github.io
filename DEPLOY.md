# Yayın: Cloudflare Pages

Site `https://devops-defterim.pages.dev` adresinde, alan adı gerektirmeden ve ücretsiz olarak yayınlanır.

## Karar

Barındırma için **Cloudflare Pages** seçildi. Koşullar 2026-10-31 tarihinde web'den kontrol edildi. Değişebilecekleri için kurulum gününde resmi sayfalardan tekrar bak.

| Kriter | GitHub Pages | Cloudflare Pages | Netlify | Vercel |
|---|---|---|---|---|
| Ücretsiz HTTPS alt alan adı | `kullanici.github.io` | `proje.pages.dev` | `proje.netlify.app` | `proje.vercel.app` |
| Ücretsiz planda private kaynak repo | Hayır (Pages için Pro gerekir) | Evet | Evet | Evet |
| Özel HTTP başlıkları (CSP, HSTS vb.) | Hayır, sadece `<meta>` | Evet, `_headers` dosyası | Evet | Evet |
| Ücretsiz planda ticari kullanım | Ticari site olarak kullanım yasak | Kısıt yok | İzinli | Hobby planı kişisel ve ticari olmayan kullanım içindir |
| Ücretsiz plan limitleri | 1 GB site, 100 GB/ay soft bant genişliği | 500 build/ay, statik istekler sınırsız | Aylık 300 kredi; aşılınca projeler durur | Hobby limitleri |

Gerekçeler:

- **Güvenlik başlıkları:** GitHub Pages özel başlık desteklemiyor. CSP `<meta>` ile verilebilir ama `frame-ancestors`, meta etiketle çalışmaz. Bu yüzden tıklama korsanlığına karşı koruma ve `X-Content-Type-Options` gibi başlıklar verilemez. Cloudflare Pages `_headers` dosyasıyla bunların hepsini destekler.
- **Private repo:** İstersen kaynak repoyu private tutabilirsin; ücretsiz planda Cloudflare bunu destekliyor.
- **Limitler:** Statik dosya istekleri sınırsız. Ayda 500 build bu proje için fazlasıyla yeterli.
- **Netlify** de uygun bir alternatif, ama kredi sistemi aşımda siteyi durdurabiliyor. **Vercel**'in ücretsiz planı ticari olmayan kullanımla sınırlı.

Cloudflare yeni özellikleri "Workers static assets" ürününe ekliyor ama Pages destekleniyor. İleride geçiş gerekirse `_headers` dosyası Workers'ta da aynen çalışır.

Kaynaklar:
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- https://developers.cloudflare.com/pages/platform/limits/
- https://developers.cloudflare.com/pages/configuration/headers/
- https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/
- https://www.netlify.com/blog/introducing-netlify-free-plan/
- https://vercel.com/docs/plans/hobby

## 1. Hesap güvenliği (önce bunu yap)

- **GitHub:** Settings → Password and authentication → Two-factor authentication'ı aç. Mümkünse passkey veya authenticator uygulaması kullan; SMS'i tercih etme. Kurtarma kodlarını parola yöneticisinde sakla.
- **Cloudflare:** My Profile → Authentication → Two-Factor Authentication'ı aç. Kurtarma kodlarını sakla.
- **E-posta hesabın:** Her iki hesabın bağlı olduğu e-postada da 2FA açık olsun. Hesap kurtarma bu e-postadan yapılır.
- Commit'lerde gerçek e-posta görünmesin: GitHub → Settings → Emails → "Keep my email addresses private" seçili olsun. Bu repo yerelde zaten GitHub noreply adresini kullanıyor.

## 2. GitHub reposu

1. GitHub'da yeni repo oluştur: ad `devops-defterim`, görünürlük Public ya da Private. README, .gitignore ve lisans **ekleme**; repo boş kalsın.
2. Yerelde uzak adresi ekle ve gönder:

   ```bash
   git remote add origin https://github.com/<kullanici>/devops-defterim.git
   git push -u origin main
   ```

3. Göndermeden önce repoya ne gireceğini kontrol et. Listede PDF, PNG, `private-notes/` veya prompt dosyası olmamalı:

   ```bash
   git ls-files
   ```

4. **Settings → Code security** altında Dependabot alerts ve Dependabot security updates'i aç. Secret scanning ve push protection'ı da aç; public repoda ücretsizdir.

## 3. Cloudflare Pages projesi

1. https://dash.cloudflare.com adresinde ücretsiz hesap aç ve 2FA'yı etkinleştir.
2. **Workers & Pages → Create → Pages → Connect to Git** yolunu izle.
3. GitHub'ı bağla. Cloudflare GitHub uygulamasına **sadece** `devops-defterim` reposuna erişim ver ("Only select repositories").
4. Build ayarları:

   | Alan | Değer |
   |---|---|
   | Project name | `devops-defterim` (adres: `devops-defterim.pages.dev`; doluysa başka bir ad seç ve `astro.config.mjs` içindeki `site` değerini güncelle) |
   | Production branch | `main` |
   | Framework preset | None |
   | Build command | `npm run build` |
   | Build output directory | `dist` |
   | Root directory | boş |

   Node sürümü repodaki `.node-version` dosyasından okunur. Okunmazsa **Settings → Variables** altına `NODE_VERSION = 24` ekle.

5. **Save and Deploy**. İlk build birkaç dakika sürer.

## 4. İlk yayını doğrula

1. `https://devops-defterim.pages.dev` adresini aç. Menü, arama ve açık/koyu mod çalışmalı.
2. Güvenlik başlıklarını kontrol et:

   ```bash
   curl -sI https://devops-defterim.pages.dev/ | grep -iE 'content-security|x-frame|x-content|referrer|permissions|strict-transport'
   ```

3. Tarayıcı geliştirici araçlarında Console sekmesinde CSP hatası olmamalı.

## 5. Güvenlik başlıkları

Başlıklar `npm run build` sırasında `scripts/postbuild-headers.mjs` tarafından `dist/_headers` dosyasına yazılır:

- `Content-Security-Policy`:
  - `script-src 'self'` ve sayfalardaki inline script'lerin SHA-256 hash'leri. `'unsafe-inline'` yoktur.
  - `'wasm-unsafe-eval'` sadece Pagefind aramasının WebAssembly modülü için.
  - `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'self'`, `form-action 'none'`.
  - `style-src` için `'unsafe-inline'` var, çünkü Starlight ve Expressive Code inline `style` öznitelikleri kullanıyor. Script çalıştırmaya izin vermediği için risk düşük.
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`, eski tarayıcılar için.
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy`: kamera, mikrofon, konum ve benzerleri kapalı.
- `Strict-Transport-Security: max-age=31536000`

Yeni bir inline script eklenirse hash otomatik hesaplanır. CSP satırı Cloudflare'in 2000 karakter sınırını aşarsa build hata verir. Harici script, analitik ve font CDN'i eklenmemelidir.

Pages, `*.pages.dev` alt alan adında HTTPS'i otomatik sağlar.

## 6. Güncelleme akışı

1. Değişikliği yerelde yap.
2. Kontrol et:

   ```bash
   npm run build && npm run check
   ```

3. Commit'le ve `main`'e gönder. Cloudflare Pages otomatik olarak yeni build alır ve yayınlar.
4. Pull request açarsan Cloudflare her PR için bir önizleme adresi üretir, GitHub Actions da build ve kontrolleri çalıştırır (`.github/workflows/ci.yml`).
5. Dependabot haftalık güncelleme PR'ları açar. CI geçerse merge et.

Geri almak için Cloudflare'de **Deployments** listesinden önceki bir yayında **Rollback** seçilebilir.

## 7. Branch protection

GitHub → repo → **Settings → Rules → Rulesets → New branch ruleset**:

- Target: `main` (Default branch).
- **Restrict deletions** ve **Block force pushes** açık.
- **Require a pull request before merging**: tek başına çalışıyorsan onay sayısını 0 bırakabilirsin.
- **Require status checks to pass**: `build` (CI iş akışı).
- Bypass listesine kimseyi ekleme. Acil durumda kuralı geçici olarak kapatırsın.

## 8. CI güvenliği

- İş akışı sadece `contents: read` yetkisiyle çalışır.
- Action'lar commit SHA'sıyla sabitlenmiştir. Dependabot bunları da günceller.
- `persist-credentials: false` ayarı token'ın checkout sonrası diskte kalmasını engeller.
- Hiç secret kullanılmaz. Deploy'u Cloudflare kendi Git entegrasyonuyla yapar.
