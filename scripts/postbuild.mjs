// Build sonrası:
// 1. dist/404/index.html → dist/404.html (GitHub Pages bulunamayan adreslerde bunu sunar).
// 2. "/" ile başlayan ama site öneki (base) taşımayan iç bağlantılara öneki ekler
//    (Markdown ve ön bilgi alanındaki /modul/sayfa/ bağlantıları).
// 3. Her HTML sayfasının <head> başına CSP ve referrer meta etiketlerini ekler.
//    GitHub Pages özel HTTP başlığı desteklemediği için güvenlik politikası meta etiketle verilir.
//    Inline script'lerin SHA-256 hash'leri CSP'ye eklenir; 'unsafe-inline' kullanılmaz.
//    Not: frame-ancestors ve X-Content-Type-Options meta etiketle verilemez (DEPLOY.md).
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { walk } from './lib.mjs';

const DIST = path.resolve('dist');
const BASE = (process.env.SITE_BASE ?? '/devops-defterim').replace(/\/$/, '');
const notFound = path.join(DIST, '404', 'index.html');
if (fs.existsSync(notFound)) fs.copyFileSync(notFound, path.join(DIST, '404.html'));

const INLINE_SCRIPT = /<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/gi;
const pages = walk(DIST, (f) => f.endsWith('.html'));

const hashes = new Set();
for (const file of pages) {
	for (const [, attrs, body] of fs.readFileSync(file, 'utf8').matchAll(INLINE_SCRIPT)) {
		if (/type=["']?application\/(ld\+)?json/i.test(attrs) || body.length === 0) continue;
		hashes.add(`'sha256-${crypto.createHash('sha256').update(body, 'utf8').digest('base64')}'`);
	}
}

const csp = [
	"default-src 'self'",
	`script-src 'self' 'wasm-unsafe-eval' ${[...hashes].sort().join(' ')}`.trim(),
	"style-src 'self' 'unsafe-inline'",
	"img-src 'self' data:",
	"font-src 'self'",
	"connect-src 'self'",
	"object-src 'none'",
	"base-uri 'self'",
	"form-action 'none'",
	'upgrade-insecure-requests',
].join('; ');

const meta =
	`<meta http-equiv="Content-Security-Policy" content="${csp}">` +
	'<meta name="referrer" content="strict-origin-when-cross-origin">';

let fixed = 0;
for (const file of pages) {
	let html = fs.readFileSync(file, 'utf8');
	if (BASE) {
		html = html.replace(/(<a\b[^>]*\shref=")(\/(?!\/)[^"]*)"/g, (m, pre, href) => {
			if (href === BASE || href.startsWith(`${BASE}/`)) return m;
			fixed++;
			return `${pre}${BASE}${href}"`;
		});
	}
	if (!html.includes('http-equiv="Content-Security-Policy"')) html = html.replace(/<head([^>]*)>/i, `<head$1>${meta}`);
	fs.writeFileSync(file, html);
}
console.log(`Base önekli bağlantı düzeltmesi: ${fixed}.`);
console.log(`CSP meta eklendi: ${pages.length} sayfa, ${hashes.size} inline script hash'i.`);
