// dist içindeki tüm HTML sayfalarında iç bağlantıları ve sayfa içi çapaları kontrol eder.
import fs from 'node:fs';
import path from 'node:path';
import { walk } from './lib.mjs';

const DIST = path.resolve('dist');
// Site bir alt dizinde yayınlanıyor (GitHub Pages proje sitesi); kontrol ederken bu önek atılır.
const BASE = (process.env.SITE_BASE ?? '/devops-defterim').replace(/\/$/, '');
if (!fs.existsSync(DIST)) {
	console.error('dist yok. Önce npm run build çalıştır.');
	process.exit(1);
}

const pages = walk(DIST, (f) => f.endsWith('.html'));
const idCache = new Map();
function idsOf(file) {
	if (!idCache.has(file)) {
		const html = fs.readFileSync(file, 'utf8');
		idCache.set(file, new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])));
	}
	return idCache.get(file);
}

function resolveTarget(urlPath) {
	let clean = decodeURIComponent(urlPath);
	if (BASE && (clean === BASE || clean.startsWith(`${BASE}/`))) clean = clean.slice(BASE.length) || '/';
	const candidates = [path.join(DIST, clean), path.join(DIST, clean, 'index.html')];
	return candidates.find((c) => fs.existsSync(c) && fs.statSync(c).isFile());
}

const errors = [];
let checked = 0;
for (const page of pages) {
	const html = fs.readFileSync(page, 'utf8');
	const pageUrl = `${BASE}/` + path.relative(DIST, page).replace(/index\.html$/, '');
	for (const [, attr, raw] of html.matchAll(/\s(href|src)="([^"]+)"/g)) {
		if (/^(https?:|mailto:|data:|javascript:)/.test(raw) || raw.startsWith('//')) continue;
		const url = new URL(raw.replace(/&amp;/g, '&'), `https://local${pageUrl}`);
		checked++;
		const target = resolveTarget(url.pathname);
		if (!target) {
			errors.push(`${pageUrl}: kırık ${attr} → ${raw}`);
			continue;
		}
		const hash = decodeURIComponent(url.hash.slice(1));
		if (hash && target.endsWith('.html') && !idsOf(target).has(hash)) {
			errors.push(`${pageUrl}: çapa bulunamadı → ${raw}`);
		}
	}
}

if (errors.length) {
	console.error(errors.join('\n'));
	console.error(`\n${errors.length} sorun (${checked} bağlantı, ${pages.length} sayfa).`);
	process.exit(1);
}
console.log(`Bağlantılar temiz: ${checked} bağlantı, ${pages.length} sayfa.`);
