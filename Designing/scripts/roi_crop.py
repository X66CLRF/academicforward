"""Crop a screenshot around its red click-marker (from capture_page.py --mark) so the key spot stays readable.

Usage: python roi_crop.py <in.png> <out.png> [--aspect 1.6] [--pad 0.9]
Finds the #e11d48 outline, keeps it centred with context (--pad = extra size relative to the marker box,
capped by image size) at the target aspect (w/h), then saves. No marker -> copies the image unchanged.
"""
import sys
from PIL import Image


def main():
    src, out = sys.argv[1], sys.argv[2]
    aspect = float(sys.argv[sys.argv.index("--aspect") + 1]) if "--aspect" in sys.argv else 1.6
    pad = float(sys.argv[sys.argv.index("--pad") + 1]) if "--pad" in sys.argv else 0.9
    im = Image.open(src).convert("RGB")
    W, H = im.size
    sm = im.resize((W // 4, H // 4))
    pts = [(x * 4, y * 4) for y in range(sm.height) for x in range(sm.width)
           if (lambda p: p[0] > 200 and p[1] < 70 and 40 < p[2] < 110)(sm.getpixel((x, y)))]
    if not pts:
        im.save(out); print("no marker, copied"); return
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    w = max((max(xs) - min(xs)) * (1 + pad) * 3, W * 0.38)
    h = w / aspect
    if h > H: h = H; w = h * aspect
    if w > W: w = W; h = w / aspect
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).save(out)
    print(out, int(w), int(h))


if __name__ == "__main__":
    main()
