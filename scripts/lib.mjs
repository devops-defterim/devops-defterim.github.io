import fs from 'node:fs';
import path from 'node:path';

export function walk(dir, filter = () => true) {
	const out = [];
	for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
		const abs = path.join(dir, entry.name);
		if (entry.isDirectory()) out.push(...walk(abs, filter));
		else if (filter(abs)) out.push(abs);
	}
	return out;
}
