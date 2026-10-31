// Build sonrası dist/_headers dosyasını üretir.
// HTML içindeki inline script'lerin SHA-256 hash'lerini toplayıp CSP'ye ekler,
// böylece script-src 'unsafe-inline' gerekmez.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { walk } from './lib.mjs';

const DIST = path.resolve('dist');
const INLINE_SCRIPT = /<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/gi;

const hashes = new Set();
for (const file of walk(DIST, (f) => f.endsWith('.html'))) {
	const html = fs.readFileSync(file, 'utf8');
	for (const [, attrs, body] of html.matchAll(INLINE_SCRIPT)) {
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
	"frame-ancestors 'none'",
	'upgrade-insecure-requests',
].join('; ');

if (csp.length > 2000) {
	console.error(`CSP satırı ${csp.length} karakter; Cloudflare sınırı 2000. Inline script sayısını azalt.`);
	process.exit(1);
}

const headers = `/*
  Content-Security-Policy: ${csp}
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), usb=()
  Strict-Transport-Security: max-age=31536000

/_astro/*
  Cache-Control: public, max-age=31536000, immutable
`;

fs.writeFileSync(path.join(DIST, '_headers'), headers);
console.log(`_headers yazıldı: ${hashes.size} inline script hash'i, CSP ${csp.length} karakter.`);
