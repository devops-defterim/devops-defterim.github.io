#!/usr/bin/env python3
"""PDF'teki ekran görüntülerini sayfa üzerindeki konumlarıyla çıkarır.

Kullanım: python tools/screenshots/extract.py <pdf> <cikti_klasoru>
Her görüntü bölgesi, PDF'in metin katmanı kaldırılmış haliyle render edilir; böylece
görüntünün üstüne taşan sayfa metni görüntüye karışmaz, görüntü üzerindeki oklar/şekiller kalır.
Kırpma maskeli görüntülerde yalnızca sayfada görünen alan alınır (visible_rect).
Dosya adı: pNNN-k.png (N: PDF sayfası, k: sayfadaki yukarıdan aşağı sıra). meta.json bağlamı tutar.
"""
import json
import os
import sys

import pymupdf
from PIL import Image, ImageChops

SRC = sys.argv[1]
doc = pymupdf.open(SRC)
PROBE_ZOOM = 2


def render(pg):
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(PROBE_ZOOM, PROBE_ZOOM), alpha=False)
    return Image.frombytes('RGB', (pix.width, pix.height), pix.samples)


def visible_rect(pno, img_name, full_rect, base):
    """Görüntünün sayfada gerçekten görünen alanı (kırpma maskeleri uygulanmış).

    Sayfanın bir kopyasında yalnızca bu görüntü düz renkle değiştirilir; iki render
    arasındaki farkın sınırları görünen alanı verir.
    """
    tmp = pymupdf.open()
    tmp.insert_pdf(doc_orig, from_page=pno - 1, to_page=pno - 1)
    tp = tmp[0]
    for im in tp.get_images(full=True):
        if im[7] == img_name:
            fill = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 8, 8), False)
            fill.set_rect(fill.irect, (255, 0, 255))
            tp.replace_image(im[0], pixmap=fill)
            break
    changed = render(tp)
    tmp.close()
    diff = ImageChops.difference(base, changed).convert('L').point(lambda v: 255 if v > 24 else 0)
    box = diff.getbbox()
    page_rect = doc_orig[pno - 1].rect
    if not box:
        return full_rect & page_rect
    r = pymupdf.Rect(*(v / PROBE_ZOOM for v in box))
    return (r & full_rect) & page_rect


doc_orig = pymupdf.open(SRC)
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
meta = []
for pno, page in enumerate(doc, 1):
    rects = []
    for img in page.get_images(full=True):
        xref, w, h, name = img[0], img[2], img[3], img[7]
        for r in page.get_image_rects(xref):
            if r.width < 30 or r.height < 15:
                continue
            rects.append((r, w, h, name))
    uniq = []
    for r, w, h, name in sorted(rects, key=lambda t: (round(t[0].y0), t[0].x0)):
        if any(abs(r.x0 - u[0].x0) < 2 and abs(r.y0 - u[0].y0) < 2 and abs(r.x1 - u[0].x1) < 2 for u in uniq):
            continue
        uniq.append((r, w, h, name))
    if not uniq:
        continue
    blocks = page.get_text("blocks")
    base = render(doc_orig[pno - 1])
    uniq = [(visible_rect(pno, name, r, base), w, h, r) for r, w, h, name in uniq]
    # Metin katmanını kaldır (görüntüler ve çizimler kalır).
    page.add_redact_annot(page.rect, fill=False)
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                          text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    for i, (r, w, h, full) in enumerate(uniq, 1):
        zoom = min(max(w / full.width, 1.5), 1600 / max(r.width, 1))
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=r, alpha=False)
        name = f"p{pno:03d}-{i}"
        pix.save(os.path.join(out, name + ".png"))
        before = " ".join(b[4].replace("\n", " ") for b in blocks if b[3] <= r.y0 + 2 and b[6] == 0)[-300:]
        after = " ".join(b[4].replace("\n", " ") for b in blocks if b[1] >= r.y1 - 2 and b[6] == 0)[:200]
        meta.append({"id": name, "page": pno, "index": i, "native": [w, h], "px": [pix.width, pix.height],
                     "before": before.strip(), "after": after.strip()})
json.dump(meta, open(os.path.join(out, "meta.json"), "w"), ensure_ascii=False, indent=1)
print(len(meta), "görüntü")
