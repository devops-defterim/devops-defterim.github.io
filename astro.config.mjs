// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { modules } from './src/config/modules.mjs';
import { buildSidebar } from './src/config/sidebar.mjs';

export default defineConfig({
	site: 'https://bulut-defteri.pages.dev',
	output: 'static',
	trailingSlash: 'always',
	build: { inlineStylesheets: 'never' },
	integrations: [
		starlight({
			title: 'Bulut Defteri',
			description: 'Linux, Git ve AWS üzerine Türkçe ders notları.',
			defaultLocale: 'root',
			locales: { root: { label: 'Türkçe', lang: 'tr' } },
			sidebar: buildSidebar(modules),
			lastUpdated: false,
			pagination: true,
			tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
			customCss: [
				'@fontsource/ibm-plex-sans/400.css',
				'@fontsource/ibm-plex-sans/400-italic.css',
				'@fontsource/ibm-plex-sans/500.css',
				'@fontsource/ibm-plex-sans/600.css',
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
					uiFontFamily: "'IBM Plex Sans', system-ui, sans-serif",
					frames: { shadowColor: 'transparent' },
				},
			},
			components: {
				Head: './src/components/Head.astro',
				Header: './src/components/Header.astro',
				MobileMenuToggle: './src/components/MobileMenuToggle.astro',
				PageTitle: './src/components/PageTitle.astro',
			},
		}),
	],
});
