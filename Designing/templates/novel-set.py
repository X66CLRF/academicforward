import subprocess, os
from pathlib import Path

S = Path(__file__).parent
OUT = Path(r"G:\Shared drives\งานแนะนำทรัพยากรสารสนเทศ\นิยาย\ก.ย.69รอบ2")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

BG = "#EFEAF6"      # ม่วงอ่อนโทนพลบค่ำ (รอบ 1 ใช้ชมพู)
LINE = "#E2DAEE"
NAVY = "#3B4A73"
RED = "#C8404A"

# ---------------------------------------------------------------------------
# ลายพื้นหลัง (seamless) — ทุกลายต้อง "ต่อกันได้" เมื่อวางภาพชิดกัน
#   กติกา: คาบของลายทั้งแนวนอนและแนวตั้งต้องหาร 2160 ลงตัว (เช่น 1080, 540, 360, 270, 216, 180)
#   ขอบซ้ายของภาพจึงตรงกับขอบขวา และขอบบนตรงกับขอบล่าง
#
# เลย์เอาต์ Facebook ที่วางแผนไว้ (ยังไม่ทำ — เพิ่มทีละแบบเมื่อใช้จริง):
#   1 ภาพ   : ภาพเดี่ยว ไม่ต้องต่อกัน
#   2 ภาพ   : วางซ้าย-ขวา  -> ต้องต่อกันแนวนอน
#   3 ภาพ   : ใหญ่ 1 + เล็ก 2 (Facebook ย่อ/ครอปไม่เท่ากัน ต่อกันได้แค่โดยประมาณ)
#   4 ภาพ   : ตาราง 2x2   -> ต่อกันทั้งแนวนอน/แนวตั้ง  <- ชุดนี้
#   แนวนอน  : แบนเนอร์/ภาพกว้าง (เช่น 2160x1080) ใช้คาบเดิม ลายจึงยังเข้าชุดกัน
# ---------------------------------------------------------------------------

def wave(period=1080, gap=180, amp=70):
    """คลื่นแนวนอน คาบ period px ระยะห่างแถว gap px (ทั้งคู่ต้องหาร 2160 ลงตัว)."""
    rows = []
    for y in range(-gap, 2160 + gap * 2, gap):
        d = f"M{-period} {y} Q{-period * 3 // 4} {y - amp} {-period // 2} {y}"
        d += "".join(f" T{x} {y}" for x in range(0, 2160 + period * 2, period // 2))
        rows.append(f'<path d="{d}"/>')
    return "".join(rows)

PATTERNS = {"wave": wave}   # เพิ่มลายใหม่ที่นี่ เช่น "dots", "petals", "grid"
PATTERN = "wave"

HEAD = f"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Pattaya&display=swap" rel="stylesheet">
<style>
html,body{{margin:0;width:2160px;height:2160px;overflow:hidden;background:{BG}}}
.bg{{position:absolute;inset:0}}
.tab{{position:absolute;left:918px;top:0;width:324px;height:336px;background:#fff;border-radius:0 0 22px 22px;
 display:flex;align-items:center;justify-content:center}}
.tab img{{width:260px}}
h1{{position:absolute;top:400px;width:100%;text-align:center;margin:0;font-family:Pattaya;font-weight:400;
 font-size:270px;line-height:1.2;color:{NAVY};-webkit-text-stroke:36px #fff;paint-order:stroke fill}}
.chip{{position:absolute;top:780px;left:50%;transform:translateX(-50%);background:#fff;padding:6px 44px;border-radius:12px;
 font-family:Pattaya;font-weight:400;font-size:112px;color:{RED};white-space:nowrap}}
.cover{{position:absolute;left:50%;top:420px;height:1560px;transform:translateX(-50%);box-shadow:0 30px 60px rgba(40,30,70,.30)}}
</style></head><body>
<svg class="bg" viewBox="0 0 2160 2160"><g fill="none" stroke="{LINE}" stroke-width="10">
""" + PATTERNS[PATTERN]() + """</g></svg>
<div class="tab"><img src="aritc-logo.png"></div>
"""

MOON = f"""
<svg style="position:absolute;left:440px;top:1000px" width="1200" height="1120" viewBox="0 0 800 900">
 <defs><filter id="diecut" x="-10%" y="-10%" width="120%" height="120%">
  <feMorphology in="SourceAlpha" operator="dilate" radius="16" result="d"/>
  <feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/>
  <feDropShadow in="w" dx="0" dy="8" stdDeviation="10" flood-color="#281e46" flood-opacity=".22" result="ws"/>
  <feMerge><feMergeNode in="ws"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
 <g filter="url(#diecut)">
 <mask id="m"><rect width="800" height="900" fill="#fff"/><circle cx="530" cy="330" r="270" fill="#000"/></mask>
 <circle cx="420" cy="400" r="300" fill="#F7E9B0" mask="url(#m)"/>
 <path d="M60 860 C 200 700, 300 620, 470 560 S 700 470, 760 380" stroke="#5B3A3A" stroke-width="26" fill="none" stroke-linecap="round"/>
 <path d="M300 640 C 320 560, 360 520, 400 500" stroke="#5B3A3A" stroke-width="16" fill="none" stroke-linecap="round"/>
 <path d="M590 500 C 600 440, 640 410, 680 400" stroke="#5B3A3A" stroke-width="14" fill="none" stroke-linecap="round"/>
""" + "".join(
    f'<g transform="translate({x} {y}) scale({s})">' + "".join(
        f'<circle cx="0" cy="-34" r="30" fill="{RED}" transform="rotate({a})"/>' for a in range(0, 360, 72))
    + '<circle r="18" fill="#F7D36B"/></g>'
    for x, y, s in [(160, 760, 1.1), (330, 640, 0.9), (400, 490, 1.2), (560, 520, 1.0), (690, 395, 1.1), (470, 575, 0.7), (250, 700, 0.6)]
) + "</g></svg>"

pages = {
    "1.png": HEAD + '<h1>แนะนำนวนิยาย</h1><div class="chip">ประจำเดือน ก.ย. 69</div>' + MOON,
    "2.png": HEAD + '<img class="cover" src="h1.jpg">',
    "3.png": HEAD + '<img class="cover" src="h2.jpg">',
    "4.png": HEAD + '<img class="cover" src="h3.jpg">',
}
for name, html in pages.items():
    src = S / f"p_{name}.html"
    src.write_text(html + "</body></html>", encoding="utf-8")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=2160,2160", "--virtual-time-budget=15000",
                    rf"--user-data-dir={os.environ['TEMP']}\edgeshot", f"--screenshot={OUT / name}", src.as_uri()], check=True)
    print(name)
