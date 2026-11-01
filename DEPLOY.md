# Yayın: GitHub Pages

Site `https://devops-defterim.github.io/` adresinde, alan adı gerektirmeden ve ücretsiz yayınlanır. Kaynak: `github.com/devops-defterim/devops-defterim.github.io` (public).

Adreste kişisel kullanıcı adı görünmesin diye site, kişisel hesaba bağlı ücretsiz bir GitHub **organizasyonunda** (`devops-defterim`) durur. Kişisel hesabın ayarları değişmez; organizasyon üyeliği varsayılan olarak gizlidir.

## Karar

Barındırma için **GitHub Pages** kullanılıyor (site sahibinin tercihi). Koşullar 2026-11-01 itibarıyla:

- Ücretsiz planda Pages yalnızca **public** repolarda çalışır. Repo herkese açıktır; `private-notes/`, kaynak PDF/PNG'ler ve çalışma dosyaları `.gitignore` ile repoya girmez.
- Limitler: yayınlanan site en fazla 1 GB, aylık ~100 GB bant genişliği (soft limit), dağıtım zaman aşımı 10 dakika.
- GitHub Pages ticari işlem amaçlı siteler için kullanılamaz; kişisel not sitesi için uygundur.
- **Özel HTTP başlığı tanımlanamaz.** Bu yüzden güvenlik politikası meta etiketle verilir (aşağıda).

Kaynak: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

## Nasıl yayınlanıyor

`.github/workflows/deploy.yml`, `main` dalına her push'ta:

1. Bağımlılıkları kurar (`npm ci`), siteyi derler (`npm run build`), bağlantı ve hassas veri kontrollerini çalıştırır (`npm run check`).
2. `dist/` klasörünü Pages artifact'i olarak yükler ve yayınlar.

Kontrollerden biri başarısız olursa yayın yapılmaz. Pull request'lerde `.github/workflows/ci.yml` aynı kontrolleri yayınlamadan çalıştırır.

Repo adı `devops-defterim.github.io` olduğu için site kök adreste yayınlanır; alt dizin öneki yoktur. Başka bir adreste veya alt dizinde yayınlamak gerekirse `SITE_URL` ve `SITE_BASE` ortam değişkenleri verilir (ör. `SITE_BASE=/devops-defterim`); `scripts/postbuild.mjs` iç bağlantılara öneki ekler, `scripts/check-links.mjs` buna göre kontrol eder.

## İlk kurulum

1. **Organizasyon (web arayüzü, bir kez):** https://github.com/account/organizations/new?plan=free adresinde
   - Organization name: `devops-defterim`
   - Contact email: kendi e-postan (herkese açık gösterilmez)
   - "This organization belongs to: My personal account"
   - Create organization. Davet ekranını "Skip this step" ile geç.
2. **Repo ve Pages:**

   ```bash
   gh repo create devops-defterim/devops-defterim.github.io --public --source . --remote origin
   gh api -X POST repos/devops-defterim/devops-defterim.github.io/pages -f build_type=workflow
   git push -u origin main
   ```

3. İlk yayın `deploy.yml` ile birkaç dakika içinde tamamlanır: repo → **Actions**.

## Güncelleme akışı

```bash
npm run build && npm run check   # yerelde kontrol
git add -A && git commit -m "..."
git push                          # Actions derler ve yayınlar (1-3 dakika)
```

Yayın durumunu repo → **Actions** sekmesinden izleyebilirsin. Hatalı bir yayını geri almak için ilgili commit'i `git revert` ile geri alıp push etmek yeterlidir.

## Güvenlik

### Sayfa içi güvenlik politikası

GitHub Pages özel başlık desteklemediği için `scripts/postbuild.mjs` her HTML sayfasının `<head>` başına şunları ekler:

- `Content-Security-Policy` (meta):
  - `script-src 'self'` + sayfalardaki inline script'lerin SHA-256 hash'leri (`'unsafe-inline'` yok); `'wasm-unsafe-eval'` yalnızca Pagefind araması için.
  - `default-src 'self'`, `object-src 'none'`, `base-uri 'self'`, `form-action 'none'`, `upgrade-insecure-requests`.
  - `style-src` için `'unsafe-inline'` var (Starlight ve Expressive Code inline `style` öznitelikleri kullanıyor; script çalıştırmaya izin vermez).
- `referrer` meta: `strict-origin-when-cross-origin`.

**Sınırlamalar** (meta etiketle verilemeyenler):

- `frame-ancestors` (ve `X-Frame-Options`): site başka bir sitede iframe içinde gösterilebilir. Sitede form veya oturum olmadığı için risk düşüktür.
- `X-Content-Type-Options`, `Permissions-Policy`: verilemez.
- HTTPS: `github.io` adresleri HTTPS ile sunulur; repo → **Settings → Pages → Enforce HTTPS** seçili olmalıdır.

Bu başlıklar gerekirse site, `_headers` destekleyen bir barındırıcıya (ör. Cloudflare Pages) taşınabilir.

### Hesap güvenliği

- **GitHub 2FA:** Settings → Password and authentication → Two-factor authentication. Authenticator uygulaması veya passkey kullan; kurtarma kodlarını parola yöneticisinde sakla.
- **E-posta gizliliği:** Settings → Emails → "Keep my email addresses private". Bu repo commit'lerde GitHub noreply adresini kullanır.
- **Token'lar:** Kullanılmayan personal access token'ları Settings → Developer settings altından sil.

### Repo ayarları

- **Branch protection:** Settings → Rules → Rulesets → New branch ruleset → hedef `main`:
  - Restrict deletions ve Block force pushes açık.
  - İstersen "Require a pull request before merging" ve "Require status checks to pass: build". Tek başına çalışıyorsan doğrudan push'a izin vermek için bu ikisini kapalı bırakabilirsin.
- **Code security:** Dependabot alerts, Dependabot security updates, Secret scanning ve Push protection açık olsun (public repoda ücretsiz).
- **Actions:** Settings → Actions → General → Workflow permissions: "Read repository contents and packages permissions". İş akışları gereken yetkileri kendileri tanımlar; action'lar commit SHA'sıyla sabitlenmiştir ve Dependabot günceller. Secret kullanılmaz.
