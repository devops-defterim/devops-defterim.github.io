#!/usr/bin/env python3
"""Ekran görüntülerinde yalnızca kritik bilgileri bulanıklaştırıp WebP'ye çevirir.

Kullanım:
  python tools/screenshots/blur.py <raw_klasoru> <ocr1.json,ocr2.json,...> [cikti_klasoru]

Kritik bilgi: AWS hesap ID'si, e-posta, AWS access key, secret access key, IAM benzersiz ID'leri
(AIDA/AIPA/AROA...), GitHub token, EC2 metadata (IMDS) token'ı, IAM'in gösterdiği konsol şifresi.
Ad, IP, hostname gibi diğer bilgiler olduğu gibi kalır.
Hesap ID'leri private-notes/critical-accounts.txt dosyasından okunur (repoya girmez).
OCR çıktıları pipeline.py ile üretilir (Vision + Tesseract geçişleri).
"""
import json
import os
import re
import sys

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
raw, ocr_paths = sys.argv[1], sys.argv[2].split(',')
out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(ROOT, 'src', 'assets', 'ekran')
os.makedirs(out, exist_ok=True)

acc_file = os.path.join(ROOT, 'private-notes', 'critical-accounts.txt')
ACCOUNTS = {l.strip() for l in open(acc_file) if l.strip().isdigit()} if os.path.exists(acc_file) else set()

PATTERNS = [
    ('account', re.compile(r'(?<!\d)(\d{4}[- ]\d{4}[- ]\d{4}|\d{12})(?!\d)')),
    ('email', re.compile(r'[\w.+-]+@[\w-]+\.(com|net|org|io|tr)\b[\w.]*', re.I)),
    ('awskey', re.compile(r'(AKIA|ASIA)[0-9A-Z]{8,}')),
    ('iamid', re.compile(r'\bA(IDA|ROA|IPA|NPA|NVA|SCA|GPA)[A-Z0-9]{10,}')),
    ('ghtoken', re.compile(r'gh[pousr]_[A-Za-z0-9]{6,}|github_pat_\w+')),
    ('imds', re.compile(r'AQAEA[\w\-=]{10,}')),
    ('secret', re.compile(r'(?<![A-Za-z0-9/+])[A-Za-z0-9/+]{30,}(?![A-Za-z0-9/+])')),
]


def critical(text):
    hits = []
    for kind, rx in PATTERNS:
        for m in rx.finditer(text):
            v = m.group(0)
            if kind == 'account' and re.sub(r'\D', '', v) not in ACCOUNTS:
                continue
            if kind == 'email' and re.search(r'@example\.(com|org|net)$', v, re.I):
                continue
            if kind == 'secret' and not re.search(r'secret', text, re.I):
                continue
            hits.append((kind, m.start(), m.end()))
    return hits


def to_px(b, W, H):
    x, y, w, h = b
    return [x * W, (1 - y - h) * H, (x + w) * W, (1 - y) * H]


def blur_box(img, box):
    x0, y0, x1, y1 = (int(round(v)) for v in box)
    x0, y0 = max(x0, 0), max(y0, 0)
    x1, y1 = min(x1, img.width), min(y1, img.height)
    if x1 - x0 < 2 or y1 - y0 < 2:
        return
    region = img.crop((x0, y0, x1, y1))
    small = region.resize((max(1, (x1 - x0) // 6), max(1, (y1 - y0) // 6)), Image.BILINEAR)
    region = small.resize(region.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(3, (y1 - y0) / 4)))
    img.paste(region, (x0, y0))


sources = [json.load(open(p)) for p in ocr_paths]
names = sorted(sources[0])
report = {}
for name in names:
    W, H = sources[0][name]['w'], sources[0][name]['h']
    lines = [l for s in sources for l in s.get(name, {}).get('lines', [])]
    img = Image.open(os.path.join(raw, name + '.png')).convert('RGB')
    boxes = []
    for line in lines:
        s = line['t']
        hits = critical(s)
        spans, idx = [], 0
        for w in line['w']:
            p = s.find(w['t'], idx)
            if p < 0:
                continue
            spans.append((p, p + len(w['t']), w['b']))
            idx = p + len(w['t'])
        for kind, a, b in hits:
            report.setdefault(name, set()).add(kind)
            found = False
            for ws, we, wb in spans:
                if we <= a or ws >= b:
                    continue
                x0, y0, x1, y1 = to_px(wb, W, H)
                n = max(we - ws, 1)
                cw = (x1 - x0) / n
                s0, s1 = max(a, ws) - ws, min(b, we) - ws
                boxes.append([x0 + cw * max(s0 - 0.8, 0), y0, x0 + cw * min(s1 + 0.8, n), y1])
                found = True
            if not found:
                boxes.append(to_px(line['b'], W, H))
    # IAM "Console password" etiketinin hemen altındaki şifre değeri
    for line in lines:
        if re.fullmatch(r'\s*Console password\s*', line['t'], re.I):
            lx0, ly0, lx1, ly1 = to_px(line['b'], W, H)
            below = [to_px(l['b'], W, H) for l in lines
                     if to_px(l['b'], W, H)[1] > ly1 - 2 and to_px(l['b'], W, H)[1] - ly1 < (ly1 - ly0) * 2.5
                     and abs(to_px(l['b'], W, H)[0] - lx0) < W * 0.05]
            if below:
                boxes.append(min(below, key=lambda b: b[1]))
                report.setdefault(name, set()).add('password')
    # AWS Console üst çubuğu: hesap menüsü (kullanıcı adı ve hesap ID)
    nav = next((to_px(l['b'], W, H) for l in lines if re.search(r'Option\+S|Alt\+S', l['t'])), None)
    if nav is not None:
        lh = nav[3] - nav[1]
        top, bot = max(nav[1] - 1.4 * lh, 0), min(nav[3] + 1.4 * lh, H)
        regions = ('Global', 'Ireland', 'Virginia', 'Ohio', 'Oregon', 'California', 'Frankfurt', 'London', 'Paris',
                   'Stockholm', 'Milan', 'Spain', 'Zurich', 'Mumbai', 'Tokyo', 'Seoul', 'Singapore', 'Sydney', 'Canada',
                   'Europe', 'United States')
        start = 0.88 * W
        for l in lines:
            x0, y0, x1, y1 = to_px(l['b'], W, H)
            if y1 >= top and y0 <= bot and x0 > 0.6 * W and any(r in l['t'] for r in regions):
                start = min(x1 + 0.03 * W, 0.95 * W)
        boxes.append([start, top, W, bot])
        report.setdefault(name, set()).add('console-account')
    for bx in boxes:
        pad = (bx[3] - bx[1]) * 0.15
        blur_box(img, [bx[0] - pad, bx[1] - pad, bx[2] + pad, bx[3] + pad])
    if img.width > 1400:
        img = img.resize((1400, round(img.height * 1400 / img.width)), Image.LANCZOS)
    img.save(os.path.join(out, name + '.webp'), 'WEBP', quality=80, method=6)

print(f'{len(names)} görüntü yazıldı, {len(report)} görüntüde kritik bilgi bulanıklaştırıldı.')
json.dump({k: sorted(v) for k, v in report.items()}, open(os.path.join(out, '..', '..', '..', 'private-notes', 'blur-report.json'), 'w'), indent=1)
