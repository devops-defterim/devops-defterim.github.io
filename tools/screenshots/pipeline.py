#!/usr/bin/env python3
"""PDF'teki ekran görüntülerini çıkarır, hassas alanları karartır ve WebP olarak kaydeder.

Kullanım:
  python tools/screenshots/pipeline.py <pdf> <calisma_klasoru> [cikti_klasoru]

Varsayılan çıktı: src/assets/ekran/<pNNN-k>.webp
Gerekenler: Python paketleri pymupdf ve pillow, macOS'ta swiftc (Vision OCR), tesseract.
Kişisel desenler: private-notes/redact-names.txt. Elle kutular: private-notes/redact-manual.json.

Adımlar:
  1. extract.py: her görüntü bölgesini sayfadan render eder, meta.json'a bağlamıyla yazar.
  2. OCR geçişleri: Vision (orijinal), Vision (2x + kontrast), Vision (şeritler), Tesseract (2x, koyu ise ters).
  3. redact.py: dört geçişin birleşiminde desen eşleşmelerini, AWS Console hesap menüsünü
     ve elle verilen kutuları karartır.
Karartma otomatik olduğu için her görüntü yayından önce gözle kontrol edilmelidir.
"""
import csv
import collections
import json
import os
import subprocess
import sys

from PIL import Image, ImageEnhance, ImageOps, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


def run(*cmd):
    subprocess.run(cmd, check=True)


def enhanced(src, dst):
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(src):
        if f.endswith('.png'):
            im = Image.open(os.path.join(src, f)).convert('L')
            im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
            ImageEnhance.Contrast(im).enhance(1.6).save(os.path.join(dst, f))


def tiles(src, dst):
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(src):
        if not f.endswith('.png'):
            continue
        im = Image.open(os.path.join(src, f)).convert('L')
        W, H = im.size
        y = 0
        while True:
            y1 = min(y + 300, H)
            t = im.crop((0, y, W, y1)).resize((W * 2, (y1 - y) * 2), Image.LANCZOS)
            ImageEnhance.Contrast(t).enhance(1.6).save(os.path.join(dst, f'{f[:-4]}__{y}_{y1}.png'))
            if y1 >= H:
                break
            y += 200


def merge_tiles(raw_json, sizes, out_json):
    raw = json.load(open(raw_json))
    out = {k: {'w': v['w'], 'h': v['h'], 'lines': []} for k, v in sizes.items()}
    for k, v in raw.items():
        name, rng = k.split('__')
        y0, y1 = map(int, rng.split('_'))
        H = sizes[name]['h']
        th = y1 - y0

        def conv(b):
            x, y, w, h = b
            top = y0 + (1 - y - h) * th
            bottom = y0 + (1 - y) * th
            return [x, 1 - bottom / H, w, (bottom - top) / H]

        for l in v['lines']:
            out[name]['lines'].append({'t': l['t'], 'b': conv(l['b']), 'w': [{'t': w['t'], 'b': conv(w['b'])} for w in l['w']]})
    json.dump(out, open(out_json, 'w'))


def tesseract(src, tmp, sizes, out_json):
    os.makedirs(tmp, exist_ok=True)
    out = {}
    for name, s in sizes.items():
        im = Image.open(os.path.join(src, name + '.png')).convert('L')
        if ImageStat.Stat(im).mean[0] < 110:
            im = ImageOps.invert(im)
        p = os.path.join(tmp, name + '.png')
        im.save(p)
        subprocess.run(['tesseract', p, os.path.join(tmp, name), '--psm', '11', 'tsv'], capture_output=True)
        W, H = im.size
        groups = collections.OrderedDict()
        for r in csv.DictReader(open(os.path.join(tmp, name + '.tsv'), encoding='utf-8', errors='ignore'), delimiter='\t', quoting=csv.QUOTE_NONE):
            if r['level'] != '5' or not r['text'].strip():
                continue
            l, t, w, h = (int(r[x]) for x in ('left', 'top', 'width', 'height'))
            groups.setdefault((r['block_num'], r['par_num'], r['line_num']), []).append({'t': r['text'], 'b': [l / W, 1 - (t + h) / H, w / W, h / H]})
        lines = []
        for ws in groups.values():
            x0 = min(w['b'][0] for w in ws); x1 = max(w['b'][0] + w['b'][2] for w in ws)
            y0 = min(w['b'][1] for w in ws); y1 = max(w['b'][1] + w['b'][3] for w in ws)
            lines.append({'t': ' '.join(w['t'] for w in ws), 'b': [x0, y0, x1 - x0, y1 - y0], 'w': ws})
        out[name] = {'w': s['w'], 'h': s['h'], 'lines': lines}
    json.dump(out, open(out_json, 'w'))


def main():
    pdf, work = sys.argv[1], os.path.abspath(sys.argv[2])
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(ROOT, 'src', 'assets', 'ekran')
    raw, up, tl, tess = (os.path.join(work, d) for d in ('raw', 'up', 'tiles', 'tess'))
    os.makedirs(raw, exist_ok=True)
    run(sys.executable, os.path.join(HERE, 'extract.py'), pdf, raw)
    ocr_bin = os.path.join(work, 'ocr')
    run('swiftc', '-O', os.path.join(HERE, 'ocr.swift'), '-o', ocr_bin)
    j = lambda n: os.path.join(work, n)
    run(ocr_bin, raw, j('ocr1.json'))
    sizes = {k: {'w': v['w'], 'h': v['h']} for k, v in json.load(open(j('ocr1.json'))).items()}
    enhanced(raw, up)
    run(ocr_bin, up, j('ocr2.json'))
    tiles(raw, tl)
    run(ocr_bin, tl, j('ocr3raw.json'))
    merge_tiles(j('ocr3raw.json'), sizes, j('ocr3.json'))
    tesseract(up, tess, sizes, j('ocr4.json'))
    sources = ','.join(j(f'ocr{i}.json') for i in (1, 2, 3, 4))
    run(sys.executable, os.path.join(HERE, 'redact.py'), raw, sources, out,
        os.path.join(ROOT, 'private-notes', 'redact-manual.json'), j('report.json'))


if __name__ == '__main__':
    main()
