import pymupdf, json, sys, os
doc = pymupdf.open(sys.argv[1]); out = sys.argv[2]
meta = []
for pno, page in enumerate(doc, 1):
    rects = []
    for img in page.get_images(full=True):
        xref, smask, w, h = img[0], img[1], img[2], img[3]
        for r in page.get_image_rects(xref):
            if r.width < 30 or r.height < 15: continue
            rects.append((r, w, h, xref))
    # aynı konumdaki tekrarları ele
    uniq = []
    for r, w, h, x in sorted(rects, key=lambda t: (round(t[0].y0), t[0].x0)):
        if any(abs(r.x0-u[0].x0)<2 and abs(r.y0-u[0].y0)<2 and abs(r.x1-u[0].x1)<2 for u in uniq): continue
        uniq.append((r, w, h, x))
    blocks = page.get_text("blocks")
    for i, (r, w, h, x) in enumerate(uniq, 1):
        zoom = min(max(w / r.width, 1.5), 1600 / r.width)
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=r, alpha=False)
        name = f"p{pno:03d}-{i}"
        pix.save(os.path.join(out, name + ".png"))
        before = " ".join(b[4].replace("\n", " ") for b in blocks if b[3] <= r.y0 + 2 and b[6] == 0)[-300:]
        after = " ".join(b[4].replace("\n", " ") for b in blocks if b[1] >= r.y1 - 2 and b[6] == 0)[:200]
        meta.append({"id": name, "page": pno, "index": i, "native": [w, h], "px": [pix.width, pix.height], "before": before.strip(), "after": after.strip()})
json.dump(meta, open(os.path.join(out, "meta.json"), "w"), ensure_ascii=False, indent=1)
print(len(meta), "görüntü")
