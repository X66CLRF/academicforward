"""Crop a full-screen screenshot (user's own capture) and draw red click-markers.

Usage: python crop_mark.py <in> <out.png> --crop x0,y0,x1,y1 [--mark x0,y0,x1,y1]... [--width 1400]
Coordinates are in the source image pixels. Crop away browser tabs/address bar and the OS taskbar
(never show them on slides), keep the page region the step is about. Marker = #e11d48 rounded outline.
"""
import argparse
from PIL import Image, ImageDraw

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--crop", required=True)
ap.add_argument("--mark", action="append", default=[])
ap.add_argument("--width", type=int, default=1400)
a = ap.parse_args()
q = lambda s: [int(v) for v in s.split(",")]
im = Image.open(a.src).convert("RGB")
dr = ImageDraw.Draw(im)
for m in a.mark:
    x0, y0, x1, y1 = q(m)
    for k, (w, c) in enumerate([(10, (225, 29, 72, 60)), (5, (225, 29, 72))]):
        dr.rounded_rectangle((x0 - 8 - k * 0, y0 - 8, x1 + 8, y1 + 8), radius=16, outline=c[:3] if k else (246, 190, 200), width=w)
cx0, cy0, cx1, cy1 = q(a.crop)
out = im.crop((cx0, cy0, cx1, cy1))
if out.width > a.width:
    out = out.resize((a.width, round(out.height * a.width / out.width)), Image.LANCZOS)
out.save(a.out)
print(a.out, out.size)
