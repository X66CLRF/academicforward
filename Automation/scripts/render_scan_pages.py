# -*- coding: utf-8 -*-
"""
render_scan_pages.py - แปลงหน้า PDF สแกนเป็นภาพ PNG เพื่อให้ผู้ช่วย AI อ่านด้วย vision
ใช้แทน poppler/pdftoppm บน Windows

    python render_scan_pages.py "<file.pdf>" --out "<folder>" --tag book1 --dpi 130 --pages 1-5,20-24
"""
import argparse
import os
import sys


def parse_pages(spec, n):
    if not spec:
        return list(range(1, n + 1))
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return [p for p in out if 1 <= p <= n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default="page")
    ap.add_argument("--dpi", type=int, default=130)
    ap.add_argument("--pages", default="")
    ap.add_argument("--color", action="store_true", help="เก็บสี (ค่าเริ่มต้นเป็นสีเทา)")
    a = ap.parse_args()
    import pymupdf
    os.makedirs(a.out, exist_ok=True)
    doc = pymupdf.open(a.pdf)
    cs = None if a.color else pymupdf.csGRAY
    pages = parse_pages(a.pages, doc.page_count)
    for p in pages:
        pix = doc[p - 1].get_pixmap(dpi=a.dpi, colorspace=cs)
        pix.save(os.path.join(a.out, "%s_%02d.png" % (a.tag, p)))
    sys.stdout.reconfigure(encoding="utf-8")
    print("%s: %d/%d หน้า -> %s" % (a.tag, len(pages), doc.page_count, a.out))


if __name__ == "__main__":
    main()
