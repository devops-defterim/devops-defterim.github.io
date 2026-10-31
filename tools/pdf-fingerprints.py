#!/usr/bin/env python3
"""PDF sayfalarının metin parmak izlerini çıkarır.

Kullanım: python3 tools/pdf-fingerprints.py <pdf> > cikti.tsv
Çıktı: sayfa<TAB>sha1(normalize metin)<TAB>ilk 80 karakter
Yeni bir PDF'teki sayfaların daha önce işlenip işlenmediğini bulmak için kullanılır.
Gerekli: poppler (pdftotext).
"""
import hashlib
import re
import subprocess
import sys


def page_count(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"^Pages:\s+(\d+)", out, re.M).group(1))


def page_text(pdf, n):
    return subprocess.run(
        ["pdftotext", "-f", str(n), "-l", str(n), pdf, "-"], capture_output=True, text=True, check=True
    ).stdout


def normalize(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def main():
    pdf = sys.argv[1]
    for n in range(1, page_count(pdf) + 1):
        text = normalize(page_text(pdf, n))
        digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
        print(f"{n}\t{digest}\t{text[:80]}")


if __name__ == "__main__":
    main()
