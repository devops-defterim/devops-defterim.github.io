// Repodaki dosyalarda ve dist çıktısında sızmış olabilecek gizli bilgileri arar.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { walk } from './lib.mjs';

// dist/_astro altındaki üçüncü parti paket kodu taranmaz; içerik ve repo dosyaları taranır.

const ALLOWED_IPS = new Set(['127.0.0.1', '0.0.0.0', '8.8.8.8', '1.1.1.1', '169.254.169.254', '255.255.255.0', '255.255.255.255']);
const isAllowedIp = (ip) =>
	ALLOWED_IPS.has(ip) ||
	/^255\./.test(ip) ||
	/(^|\.)0\d/.test(ip) ||
	/^(10|192\.168|172\.(1[6-9]|2\d|3[01]))\./.test(ip) ||
	/^(192\.0\.2|198\.51\.100|203\.0\.113)\./.test(ip);

const RULES = [
	['AWS access key', /\b(AKIA|ASIA)[0-9A-Z]{16}\b/g],
	['Private key', /-----BEGIN [A-Z ]*PRIVATE KEY-----/g],
	['GitHub token', /\b(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b/g],
	['12 haneli sayı (hesap ID olabilir)', /(?<![\d.-])\d{12}(?![\d.])/g],
	['E-posta', /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g],
	['IPv4', /\b(?:\d{1,3}\.){3}\d{1,3}\b/g],
];
const ALLOWLIST = new Set(
	fs
		.readFileSync(new URL('./sensitive-allowlist.txt', import.meta.url), 'utf8')
		.split('\n')
		.map((l) => l.trim())
		.filter((l) => l && !l.startsWith('#')),
);
const ALLOWED_EMAIL = /@(example\.(com|org|net)|users\.noreply\.github\.com|anthropic\.com)$/i;

const TEXT = /\.(md|mdx|astro|mjs|js|ts|json|yml|yaml|css|html|txt|toml)$|^_headers$/;
const files = [
	...execFileSync('git', ['ls-files'], { encoding: 'utf8' }).split('\n').filter(Boolean),
	...(fs.existsSync('dist') ? walk('dist') : []),
].filter((f) => TEXT.test(path.basename(f)) && !f.endsWith('package-lock.json') && !f.includes('pagefind/') && !f.startsWith('dist/_astro/'));

const findings = [];
for (const file of files) {
	const text = fs.readFileSync(file, 'utf8');
	for (const [name, re] of RULES) {
		for (const m of text.matchAll(re)) {
			const value = m[0];
			if (ALLOWLIST.has(value)) continue;
			if (name === 'E-posta' && ALLOWED_EMAIL.test(value)) continue;
			if (name === 'IPv4' && (isAllowedIp(value) || !value.split('.').every((p) => Number(p) <= 255))) continue;
			findings.push(`${file}: ${name}: ${value}`);
		}
	}
}

if (findings.length) {
	console.error([...new Set(findings)].join('\n'));
	console.error(`\n${findings.length} olası hassas veri. Her birini elle kontrol et.`);
	process.exit(1);
}
console.log(`Hassas veri bulunmadı (${files.length} dosya).`);
