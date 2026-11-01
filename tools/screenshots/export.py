#!/usr/bin/env python3
"""Çıkarılmış ekran görüntülerini WebP'ye çevirir (karartma yapmaz).

Kullanım: python tools/screenshots/export.py <raw_klasoru> [cikti_klasoru] [--trim id1,id2,...]
Varsayılan çıktı: src/assets/ekran/
--trim: verilen görüntülerin kenarlarındaki tamamen beyaz şeritleri kırpar (PDF metninin
görüntü çerçevesine taştığı yerlerde metin kaldırıldıktan sonra kalan boşluk için).
"""
import os
import sys

from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith('--trim')]
trim = set()
for a in sys.argv[1:]:
    if a.startswith('--trim='):
        trim = set(a.split('=', 1)[1].split(','))
raw = args[0]
out = args[1] if len(args) > 1 else os.path.join(HERE, '..', '..', 'src', 'assets', 'ekran')
os.makedirs(out, exist_ok=True)


def trim_white(img):
    bg = Image.new('RGB', img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg).convert('L').point(lambda v: 255 if v > 6 else 0)
    box = diff.getbbox()
    return img.crop(box) if box else img


n = 0
for f in sorted(os.listdir(raw)):
    if not f.endswith('.png'):
        continue
    img = Image.open(os.path.join(raw, f)).convert('RGB')
    if f[:-4] in trim:
        img = trim_white(img)
    if img.width > 1400:
        img = img.resize((1400, round(img.height * 1400 / img.width)), Image.LANCZOS)
    img.save(os.path.join(out, f[:-4] + '.webp'), 'WEBP', quality=80, method=6)
    n += 1
print(n, 'görüntü yazıldı')
