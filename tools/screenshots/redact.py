import json, sys, os, collections, re
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__)); from sensitive import find
raw, ocrp, out, manualp, reportp = sys.argv[1:6]
sources = [json.load(open(p)) for p in ocrp.split(',')]
ocr = {k: {'w': v['w'], 'h': v['h'], 'lines': [l for src in sources for l in src.get(k, {}).get('lines', [])]} for k, v in sources[0].items()}; manual = json.load(open(manualp)) if os.path.exists(manualp) else {}
os.makedirs(out, exist_ok=True)
FILL = (128, 128, 128)
report = {}
def to_px(b, W, H):
    x, y, w, h = b
    return [x * W, (1 - y - h) * H, (x + w) * W, (1 - y) * H]
for name in sorted(ocr):
    info = ocr[name]; W, H = info['w'], info['h']
    img = Image.open(os.path.join(raw, name + '.png')).convert('RGB')
    d = ImageDraw.Draw(img); counts = collections.Counter()
    for line in info['lines']:
        s = line['t']; hits = find(s)
        if not hits: continue
        # kelimelerin karakter aralıkları
        spans = []; idx = 0
        for w in line['w']:
            p = s.find(w['t'], idx)
            if p < 0: continue
            spans.append((p, p + len(w['t']), w['b'])); idx = p + len(w['t'])
        for kind, a, b in hits:
            counts[kind] += 1
            boxes = []
            for (ws, we, wb) in spans:
                if we <= a or ws >= b: continue
                x0, y0, x1, y1 = to_px(wb, W, H)
                n = max(we - ws, 1); cw = (x1 - x0) / n
                s0 = max(a, ws) - ws; s1 = min(b, we) - ws
                boxes.append([x0 + cw * max(s0 - 0.6, 0), y0, x0 + cw * min(s1 + 0.6, n), y1])
            if not boxes:  # kelime eşleşmesi yoksa satırın tamamı
                boxes = [to_px(line['b'], W, H)]
            for bx in boxes:
                pad = (bx[3] - bx[1]) * 0.18
                d.rectangle([bx[0] - pad, bx[1] - pad, bx[2] + pad, bx[3] + pad], fill=FILL)
    # AWS Console üst çubuğu: hesap menüsü (kullanıcı adı ve hesap ID) OCR'dan bağımsız karartılır.
    REGIONS = ('Global','Ireland','Virginia','Ohio','Oregon','California','Frankfurt','London','Paris','Stockholm','Milan','Spain','Zurich','Mumbai','Tokyo','Seoul','Singapore','Sydney','Canada','Europe','United States')
    nav = None
    for line in info['lines']:
        if re.search(r'Option\+S|Alt\+S', line['t']):
            nav = to_px(line['b'], W, H); break
    if nav is None:
        for line in info['lines']:
            x0, y0, x1, y1 = to_px(line['b'], W, H)
            if line['t'].strip().lower() == 'aws' and x0 < 0.1 * W and y1 < 0.12 * H:
                nav = [x0, y0, x1, y1]; break
    if nav is not None:
        lh = nav[3] - nav[1]; top = max(nav[1] - 1.6 * lh, 0); bot = min(nav[3] + 1.6 * lh, H)
        start = 0.88 * W
        for line in info['lines']:
            x0, y0, x1, y1 = to_px(line['b'], W, H)
            if y1 >= top and y0 <= bot and x0 > 0.6 * W and any(r in line['t'] for r in REGIONS):
                start = min(x1 + 0.022 * W, 0.95 * W)
        d.rectangle([start, top, W, bot], fill=FILL); counts['console-account'] += 1
    # GitHub üst çubuğu: sağ uçtaki profil fotoğrafı karartılır.
    for line in info['lines']:
        x0, y0, x1, y1 = to_px(line['b'], W, H)
        if re.search(r'Type\W{0,4}\S?\W{0,4}to search', line['t'], re.I) and y1 < 0.2 * H and x0 > 0.45 * W:
            lh = y1 - y0
            d.rectangle([0.955 * W, max(y0 - 1.5 * lh, 0), W, min(y1 + 1.5 * lh, H)], fill=FILL); counts['github-avatar'] += 1
            break
    for bx in manual.get(name, []):  # elle eklenen kutular: oransal [x0,y0,x1,y1]
        d.rectangle([bx[0] * W, bx[1] * H, bx[2] * W, bx[3] * H], fill=FILL); counts['manual'] += 1
    if img.width > 1400:
        img = img.resize((1400, round(img.height * 1400 / img.width)), Image.LANCZOS)
    img.save(os.path.join(out, name + '.webp'), 'WEBP', quality=80, method=6)
    if counts: report[name] = dict(counts)
json.dump(report, open(reportp, 'w'), indent=1)
print('görüntü:', len(ocr), 'karartılan:', len(report), 'toplam kutu:', sum(sum(v.values()) for v in report.values()))
