import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DOCS_DIR = fileURLToPath(new URL('../content/docs/', import.meta.url));
const PAGE_EXT = /\.mdx?$/;

function readOrder(file) {
	const source = fs.readFileSync(file, 'utf8');
	const frontmatter = source.match(/^---\r?\n([\s\S]*?)\r?\n---/);
	const order = frontmatter?.[1].match(/^order:\s*(\d+(?:\.\d+)?)\s*$/m);
	return order ? Number(order[1]) : Number.MAX_SAFE_INTEGER;
}

function collect(dirAbs, slugPrefix, groupLabels) {
	const entries = [];
	for (const name of fs.readdirSync(dirAbs).sort()) {
		const abs = path.join(dirAbs, name);
		if (fs.statSync(abs).isDirectory()) {
			const children = collect(abs, `${slugPrefix}${name}/`, groupLabels);
			if (children.length === 0) continue;
			entries.push({
				order: Math.min(...children.map((c) => c.order)),
				item: { label: groupLabels[name] ?? name, collapsed: true, items: children.map((c) => c.item) },
			});
		} else if (PAGE_EXT.test(name) && !name.startsWith('index.')) {
			entries.push({ order: readOrder(abs), item: { slug: slugPrefix + name.replace(PAGE_EXT, '') } });
		}
	}
	return entries.sort((a, b) => a.order - b.order);
}

export function buildSidebar(modules) {
	const groups = modules
		.filter((m) => m.sidebar !== false && fs.existsSync(path.join(DOCS_DIR, m.dir)))
		.map((m) => ({
			label: m.label,
			collapsed: true,
			items: collect(path.join(DOCS_DIR, m.dir), `${m.dir}/`, m.groups ?? {}).map((e) => e.item),
		}))
		.filter((g) => g.items.length > 0);
	return groups;
}
