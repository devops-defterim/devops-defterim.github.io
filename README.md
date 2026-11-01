# DevOps Defterim

Linux, Git ve GitHub, bulut bilişim temelleri ve AWS üzerine Türkçe ders notları. Notlar, Ottoo ve Ayti.tech iş birliğiyle düzenlenen "Bulut Bilişim ve DevOps Bootcamp" eğitiminden tutulmuş kişisel notlardır; resmi materyal değildir.

Site [Astro](https://astro.build) ve [Starlight](https://starlight.astro.build) ile üretilen tamamen statik bir dokümantasyon sitesidir.

## Çalıştırma

Node.js 22.23.4 veya üstü gerekir (`.node-version`).

```bash
npm ci
npm run dev        # http://localhost:4321
npm run build      # statik çıktı: dist/
npm run check      # build sonrası bağlantı ve hassas veri kontrolü
```

İçerik `src/content/docs/` altındaki Markdown dosyalarındadır. Menü sırası `src/config/modules.mjs` dosyasından yönetilir. Ayrıntılar için `CLAUDE.md`, yayın için `DEPLOY.md`.
