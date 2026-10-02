# วารสาร ต.ค. 69 v2 — แม่แบบ novel-set (Pattaya + ขอบขาว + แถบโลโก้ + สติกเกอร์ไดคัท) + ลาย topo + วงแหวน/จุดแบบ slide-hub
import subprocess, os, math, random
from pathlib import Path
from PIL import Image

S = Path(__file__).parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def wait_file(path, timeout=40):
    """msedge.exe คืนค่าก่อนเขียนภาพเสร็จ (เครื่องนี้) — รอจนไฟล์มีและขนาดนิ่ง"""
    import time
    path, last, t0 = Path(path), -1, time.time()
    while time.time() - t0 < timeout:
        if path.exists() and path.stat().st_size == last > 0:
            return
        last = path.stat().st_size if path.exists() else -1
        time.sleep(0.5)
    raise SystemExit(f"Edge ไม่เขียน {path} ภายใน {timeout} วินาที")

# [GRAPHIC-SPEC] จากปกทั้ง 4 เล่ม
BG, LINE = "#F1F5EE", "#E2EBDF"          # เขียวใบไม้จาง (แปลงผัก เกษตรผสม-ผสาน)
NAVY = "#2B3A55"
GREEN, PINK, MAROON, YELLOW = "#2E7D4F", "#E8579A", "#7A2E2A", "#F2C200"


def topo(seed=7):
    """วงแหวนเส้นชั้นความสูงรอบหลายศูนย์ วาดซ้ำที่ +-2160 ให้ต่อกันได้"""
    rnd = random.Random(seed)
    out = []
    centers = [(380, 420), (1700, 300), (1150, 1250), (300, 1800), (1900, 1750)]
    for cx, cy in centers:
        ph = [rnd.uniform(0, 6.28) for _ in range(3)]
        for k in range(1, 7):
            r0 = 85 * k
            pts = []
            for i in range(73):
                t = i / 72 * 2 * math.pi
                r = r0 * (1 + .16 * math.sin(3 * t + ph[0]) + .09 * math.sin(5 * t + ph[1]) + .05 * math.sin(2 * t + ph[2]))
                pts.append((r * math.cos(t), r * math.sin(t)))
            d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
            for dx in (-2160, 0, 2160):
                for dy in (-2160, 0, 2160):
                    out.append(f'<path transform="translate({cx + dx} {cy + dy})" d="{d}"/>')
    return "".join(out)


dots = "".join(f'<i style="width:22px;height:22px;border-radius:50%;background:{c}"></i>' for c in [GREEN, PINK, YELLOW] * 3)
RINGS = f"""<svg style="position:absolute;right:-260px;top:-260px" width="760" height="760" viewBox="0 0 760 760" fill="none">
 <circle cx="380" cy="380" r="360" stroke="{GREEN}" stroke-opacity=".25" stroke-width="6"/>
 <circle cx="380" cy="380" r="270" stroke="{GREEN}" stroke-opacity=".25" stroke-width="6" stroke-dasharray="18 22"/>
 <circle cx="380" cy="380" r="180" fill="{GREEN}" fill-opacity=".10"/></svg>
<svg style="position:absolute;left:-220px;bottom:-220px" width="640" height="640" viewBox="0 0 640 640" fill="none">
 <circle cx="320" cy="320" r="300" fill="{PINK}" fill-opacity=".12"/>
 <circle cx="320" cy="320" r="220" stroke="{PINK}" stroke-opacity=".35" stroke-width="6"/></svg>
<div style="position:absolute;left:120px;top:150px;display:grid;grid-template-columns:repeat(3,22px);gap:22px">{dots}</div>"""

HEAD = f"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Pattaya&display=swap" rel="stylesheet">
<style>
html,body{{margin:0;width:2160px;height:2160px;overflow:hidden;background:{BG};position:relative}}
.bg{{position:absolute;inset:0}}
.tab{{position:absolute;left:918px;top:0;width:324px;height:336px;background:#fff;border-radius:0 0 22px 22px;
 display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(43,58,85,.10)}}
.tab img{{width:260px}}
h1{{position:absolute;top:430px;width:100%;text-align:center;margin:0;font-family:Pattaya;font-weight:400;
 font-size:280px;line-height:1.25;color:{NAVY};-webkit-text-stroke:38px #fff;paint-order:stroke fill}}
.chip{{position:absolute;top:804px;left:50%;transform:translateX(-50%);background:#fff;padding:10px 56px;border-radius:999px;
 font-family:Pattaya;font-size:116px;line-height:1.3;color:{MAROON};white-space:nowrap;box-shadow:0 12px 30px rgba(43,58,85,.10)}}
.shadow{{position:absolute;box-shadow:0 40px 80px rgba(43,58,85,.28)}}
.num{{position:absolute;right:190px;bottom:205px;width:220px;height:220px;border-radius:50%;background:#fff;
 box-shadow:0 20px 45px -10px rgba(43,58,85,.25);display:flex;align-items:center;justify-content:center;
 font-family:Pattaya;font-size:120px;color:var(--c)}}
</style></head><body>
<svg class="bg" viewBox="0 0 2160 2160"><g fill="none" stroke="{LINE}" stroke-width="7">{topo()}</g></svg>
{RINGS}
<div class="tab"><img src="aritc-logo.png"></div>
"""

flowers = "".join(
    f'<g transform="translate({x} {y}) scale({s})">'
    + "".join(f'<circle cx="0" cy="-30" r="26" fill="{PINK}" transform="rotate({a})"/>' for a in range(0, 360, 72))
    + f'<circle r="16" fill="{YELLOW}"/></g>'
    for x, y, s in [(220, 900, 1.1), (790, 880, 1.0), (130, 960, .7), (880, 970, .75)])
GLASS = ("M330 330 C330 470 470 520 500 600 C530 520 670 470 670 330 Z "
         "M500 600 C470 680 330 730 330 900 L670 900 C670 730 530 680 500 600 Z")
# สติกเกอร์: นาฬิกาทรายมีต้นกล้างอกด้านบน = เวลา + การฟื้นคืน
# (ฟื้นแปลงหลังน้ำท่วม · บ้าน 50 ปี · บางรักในประวัติศาสตร์ · ศาสตร์ชะลอวัย)
STICKER = f"""
<svg style="position:absolute;left:500px;top:1000px" width="1160" height="1100" viewBox="0 0 1000 1040">
 <defs><filter id="diecut" x="-10%" y="-10%" width="120%" height="120%">
  <feMorphology in="SourceAlpha" operator="dilate" radius="20" result="d"/>
  <feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/>
  <feDropShadow in="w" dx="0" dy="10" stdDeviation="12" flood-color="#2b3a55" flood-opacity=".22" result="ws"/>
  <feMerge><feMergeNode in="ws"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="glass"><path d="{GLASS}"/></clipPath></defs>
 <g filter="url(#diecut)">
  <path d="M500 270 C500 200 495 150 505 90" stroke="{GREEN}" stroke-width="26" fill="none" stroke-linecap="round"/>
  <path d="M502 170 C410 175 330 120 320 40 C410 40 480 90 502 170 Z" fill="#5DAE5B"/>
  <path d="M505 125 C570 40 670 15 740 45 C710 130 610 160 505 125 Z" fill="#7CC36A"/>
  <rect x="290" y="270" width="420" height="70" rx="35" fill="{MAROON}"/>
  <rect x="290" y="890" width="420" height="70" rx="35" fill="{MAROON}"/>
  <path d="{GLASS}" fill="#DDF0F4"/>
  <g clip-path="url(#glass)">
   <path d="M360 420 L640 420 L500 590 Z" fill="{YELLOW}"/>
   <path d="M330 900 C380 790 450 760 500 760 C550 760 620 790 670 900 Z" fill="{YELLOW}"/>
   <rect x="494" y="590" width="12" height="170" fill="{YELLOW}"/>
  </g>
  <rect x="300" y="330" width="26" height="560" rx="13" fill="{MAROON}"/>
  <rect x="674" y="330" width="26" height="560" rx="13" fill="{MAROON}"/>
  {flowers}
 </g></svg>"""

covers = [("cover1.jpg", 1335, 1800), ("cover2.jpg", 1366, 1800), ("cover3.jpg", 1285, 1800), ("cover4.jpg", 1234, 1800)]
H, TOP = 1500, 470
cols = [GREEN, PINK, MAROON, "#B88A00"]
pages = {"p1": HEAD + '<h1>แนะนำวารสาร</h1><div class="chip">ประจำเดือน ต.ค. 69</div>' + STICKER}
layout = []
for i, (f, w, h) in enumerate(covers, 1):
    cw = round(w * H / h)
    left = (2160 - cw) // 2
    layout.append((f, left, TOP, cw, H))
    deco = HEAD + f'<div class="shadow" style="left:{left}px;top:{TOP}px;width:{cw}px;height:{H}px"></div>' \
        + f'<div class="num" style="--c:{cols[i - 1]}">0{i}</div>'
    pages[f"p{i + 1}"] = deco
    pages[f"prev{i + 1}"] = deco + f'<img src="{f}" style="position:absolute;left:{left}px;top:{TOP}px;width:{cw}px;height:{H}px">'

for name, html in pages.items():
    src = S / f"{name}.html"
    src.write_text(html + "</body></html>", encoding="utf-8")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=2160,2160", "--virtual-time-budget=15000", rf"--user-data-dir={os.environ['TEMP']}\edgeshot",
                    f"--screenshot={S / (name + '.png')}", src.as_uri()], check=True)
    wait_file(S / (name + ".png"))
print(layout)

ims = [Image.open(S / f).convert("RGB").resize((540, 540)) for f in ["p1.png", "prev2.png", "prev3.png", "prev5.png"]]
sheet = Image.new("RGB", (1080, 1080))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % 2) * 540, (i // 2) * 540))
sheet.save(S / "sheet.jpg", quality=85)
