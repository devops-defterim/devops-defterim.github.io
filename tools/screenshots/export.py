#!/usr/bin/env python3
"""Çıkarılmış ekran görüntülerini karartma yapmadan WebP'ye çevirir.

Kullanım: python tools/screenshots/export.py <raw_klasoru> [cikti_klasoru]
Varsayılan çıktı: src/assets/ekran/
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
raw = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', '..', 'src', 'assets', 'ekran')
os.makedirs(out, exist_ok=True)
n = 0
for f in sorted(os.listdir(raw)):
    if not f.endswith('.png'):
        continue
    img = Image.open(os.path.join(raw, f)).convert('RGB')
    if img.width > 1400:
        img = img.resize((1400, round(img.height * 1400 / img.width)), Image.LANCZOS)
    img.save(os.path.join(out, f[:-4] + '.webp'), 'WEBP', quality=80, method=6)
    n += 1
print(n, 'görüntü yazıldı')
