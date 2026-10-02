# แยกชั้นงานวารสาร ต.ค. 69 v2 → PNG พื้นใสทีละชิ้น ครอปพอดีชิ้น + ตำแหน่งบนหน้า 2160 (layers.json)
# ใช้ค่าเดียวกับ journal-set.py · กติกา: ../canva-handover.md — ผู้ใช้ขยาย/ย้าย/ซ้อนเองใน Canva ได้ทีละชิ้น
import json, os, subprocess
from pathlib import Path
from PIL import Image
import importlib.util
_spec = importlib.util.spec_from_file_location("B", Path(__file__).with_name("journal-set.py"))
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)  # สี ลาย สติกเกอร์ ตำแหน่งปก (รัน journal-set.py ซ้ำ — ไม่เป็นไร)

S = Path(__file__).parent
OUT = S / "layers"
OUT.mkdir(exist_ok=True)

BASE = """<!doctype html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Pattaya&display=swap" rel="stylesheet">
<style>html,body{margin:0;width:2160px;height:2160px;overflow:hidden;background:transparent;position:relative}</style>
""" + B.HEAD.split("<style>")[1].split("</style>")[0].join(["<style>", "</style>"]).replace(f"background:{B.BG};", "background:transparent;") + "</head><body>"

DIECUT = """<defs><filter id="diecut" x="-15%" y="-15%" width="130%" height="130%">
  <feMorphology in="SourceAlpha" operator="dilate" radius="20" result="d"/>
  <feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/>
  <feDropShadow in="w" dx="0" dy="10" stdDeviation="12" flood-color="#2b3a55" flood-opacity=".22" result="ws"/>
  <feMerge><feMergeNode in="ws"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="glass"><path d="GLASSPATH"/></clipPath></defs>""".replace("GLASSPATH", B.GLASS)


def sticker(inner):
    return (f'<svg style="position:absolute;left:500px;top:1000px" width="1160" height="1100" viewBox="0 0 1000 1040">'
            f'{DIECUT}<g filter="url(#diecut)">{inner}</g></svg>')


G, M, Y, P = B.GREEN, B.MAROON, B.YELLOW, B.PINK
HOURGLASS = f"""<rect x="290" y="270" width="420" height="70" rx="35" fill="{M}"/>
  <rect x="290" y="890" width="420" height="70" rx="35" fill="{M}"/>
  <path d="{B.GLASS}" fill="#DDF0F4"/>
  <g clip-path="url(#glass)"><path d="M360 420 L640 420 L500 590 Z" fill="{Y}"/>
   <path d="M330 900 C380 790 450 760 500 760 C550 760 620 790 670 900 Z" fill="{Y}"/>
   <rect x="494" y="590" width="12" height="170" fill="{Y}"/></g>
  <rect x="300" y="330" width="26" height="560" rx="13" fill="{M}"/>
  <rect x="674" y="330" width="26" height="560" rx="13" fill="{M}"/>"""
SPROUT = f"""<path d="M500 270 C500 200 495 150 505 90" stroke="{G}" stroke-width="26" fill="none" stroke-linecap="round"/>
  <path d="M502 170 C410 175 330 120 320 40 C410 40 480 90 502 170 Z" fill="#5DAE5B"/>
  <path d="M505 125 C570 40 670 15 740 45 C710 130 610 160 505 125 Z" fill="#7CC36A"/>"""
FLOWER = (f'<g transform="translate(220 900) scale(1.1)">'
          + "".join(f'<circle cx="0" cy="-30" r="26" fill="{P}" transform="rotate({a})"/>' for a in range(0, 360, 72))
          + f'<circle r="16" fill="{Y}"/></g>')

rings_tr, rings_bl, dots = B.RINGS.split("</svg>")[0] + "</svg>", B.RINGS.split("</svg>")[1] + "</svg>", B.RINGS.split("</svg>")[2]

layers = {
    "topo": f'<svg class="bg" viewBox="0 0 2160 2160"><g fill="none" stroke="{B.LINE}" stroke-width="7">{B.topo()}</g></svg>',
    "ring-tr": rings_tr, "ring-bl": rings_bl, "dots": dots,
    "logo-tab": '<div class="tab"><img src="../aritc-logo.png"></div>',
    "title": "<h1>แนะนำวารสาร</h1>",
    "chip": '<div class="chip">ประจำเดือน ต.ค. 69</div>',
    "hourglass": sticker(HOURGLASS), "sprout": sticker(SPROUT), "flower": sticker(FLOWER),
}
cols = [G, P, M, "#B88A00"]
for i, (f, left, top, cw, h) in enumerate(B.layout, 1):
    layers[f"shadow{i}"] = f'<div class="shadow" style="left:{left}px;top:{top}px;width:{cw}px;height:{h}px;background:#fff"></div>'
    layers[f"num{i}"] = f'<div class="num" style="--c:{cols[i - 1]}">0{i}</div>'

pos = {}
for name, html in layers.items():
    src = OUT / f"{name}.html"
    src.write_text(BASE + html + "</body></html>", encoding="utf-8")
    png = OUT / f"{name}_full.png"
    subprocess.run([B.EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--default-background-color=00000000", "--window-size=2160,2160", "--virtual-time-budget=15000",
                    rf"--user-data-dir={os.environ['TEMP']}\edgeshot", f"--screenshot={png}", src.as_uri()], check=True)
    B.wait_file(png)
    im = Image.open(png).convert("RGBA")
    box = im.getchannel("A").getbbox()
    if name.startswith("shadow"):  # เงา: ลบตัวกล่องขาวออก เหลือแต่เงา (ปกจริงวางทับตรงกลาง)
        f, left, top, cw, h = B.layout[int(name[-1]) - 1]
        im.paste((0, 0, 0, 0), (left, top, left + cw, top + h))
    im.crop(box).save(OUT / f"{name}.png")
    pos[name] = {"left": box[0], "top": box[1], "width": box[2] - box[0], "height": box[3] - box[1]}
    png.unlink()
(OUT / "layers.json").write_text(json.dumps(pos, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(pos, ensure_ascii=False))
