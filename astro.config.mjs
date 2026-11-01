// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { modules } from './src/config/modules.mjs';
import { buildSidebar } from './src/config/sidebar.mjs';

// GitHub Pages: devops-defterim organizasyonunun devops-defterim.github.io reposu, kök adreste yayınlanır.
// Başka bir adreste/alt dizinde yayınlamak için SITE_URL ve SITE_BASE ortam değişkenleri kullanılabilir.
const SITE = process.env.SITE_URL ?? 'https://devops-defterim.github.io';
const BASE = process.env.SITE_BASE ?? '/';

export default defineConfig({
	site: SITE,
	base: BASE,
	output: 'static',
	trailingSlash: 'always',
	build: { inlineStylesheets: 'never' },
	// Küçük font dosyaları CSS'e data: URI olarak gömülmesin; CSP font-src 'self' kalsın.
	vite: { build: { assetsInlineLimit: 0 } },
	// Komutlardaki -- ve tırnaklar tipografik karakterlere dönüşmesin.
	markdown: { smartypants: false },
	integrations: [
		starlight({
			title: 'DevOps Defterim',
			description: 'Linux, Git ve AWS üzerine Türkçe ders notları.',
			defaultLocale: 'root',
			locales: { root: { label: 'Türkçe', lang: 'tr' } },
			sidebar: buildSidebar(modules),
			lastUpdated: false,
			disable404Route: true,
			pagination: true,
			tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
			customCss: [
				'@fontsource-variable/plus-jakarta-sans/wght.css',
				'@fontsource-variable/plus-jakarta-sans/wght-italic.css',
				'@fontsource-variable/bricolage-grotesque/wght.css',
				'@fontsource/jetbrains-mono/400.css',
				'@fontsource/jetbrains-mono/600.css',
				'./src/styles/theme.css',
			],
			expressiveCode: {
				themes: ['github-dark-default', 'github-light-default'],
				styleOverrides: {
					borderRadius: '6px',
					borderColor: 'var(--sl-color-hairline)',
					codeFontFamily: "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace",
					codeFontSize: '0.875rem',
					uiFontFamily: "'Plus Jakarta Sans Variable', system-ui, sans-serif",
					frames: {
						shadowColor: 'transparent',
						editorActiveTabIndicatorTopColor: 'var(--sl-color-accent)',
						editorActiveTabIndicatorBottomColor: 'transparent',
					},
				},
			},
			components: {
				Head: './src/components/Head.astro',
				Header: './src/components/Header.astro',
				MobileMenuToggle: './src/components/MobileMenuToggle.astro',
				PageTitle: './src/components/PageTitle.astro',
				Sidebar: './src/components/Sidebar.astro',
				TwoColumnContent: './src/components/TwoColumnContent.astro',
			},
		}),
	],
});
