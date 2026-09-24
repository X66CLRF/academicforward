"""ภาพเชิญเสนอชื่อ (suggest card) 2160x2160 — ใช้แบบเดิมของ "เสนอหนังสือ" ปี 2565-2568
ส่วนบน: สติกเกอร์ไดคัท + หัวเรื่อง · กลาง: ข้อความเชิญ · แถบพู่กัน: ลิงก์ · ล่าง: ช่องทางติดต่อ
ห้ามใช้อีโมจิในภาพ ไอคอนวาดเป็น SVG
"""
import subprocess, os
from pathlib import Path

S = Path(__file__).parent
OUT = Path(r"G:\Shared drives\งานแนะนำทรัพยากรสารสนเทศ\เสนอหนังสือ\2569\เสนอบอร์ดเกม.png")

# [GRAPHIC-SPEC]
BG = "#4E6FB3"      # ส่วนบน น้ำเงิน
LINE = "#5B7CC0"    # (สำรอง) เส้นลายบนพื้นสี
ACCENT = "#F5B335"  # เหลืองลูกเต๋า
INK = "#2B2F3A"
CREAM = "#FFF8EC"
CREAM_LINE = "#F1E6D2"  # เส้นลายบนพื้นครีม

HEADLINE_CHIP = "ร่วมเสนอชื่อบอร์ดเกม"
HEADLINE = "ผ่านระบบ<br>ออนไลน์"
BODY = ["ขอเชิญนักศึกษา อาจารย์ และบุคลากรทุกท่าน",
        "ร่วมเสนอชื่อบอร์ดเกมที่สนใจหรือชื่นชอบ",
        "ให้ห้องสมุดจัดหา ผ่านระบบออนไลน์ได้แล้ววันนี้"]
LINK = "booktogether.nsru.ac.th"
NOTE = "เข้าสู่ระบบด้วยบัญชี Google @nsru.ac.th"


def wave(period=1080, gap=180, amp=60, height=1020):
    rows = []
    for y in range(-gap, height + gap * 2, gap):
        d = f"M{-period} {y} Q{-period * 3 // 4} {y - amp} {-period // 2} {y}"
        d += "".join(f" T{x} {y}" for x in range(0, 2160 + period * 2, period // 2))
        rows.append(f'<path d="{d}"/>')
    return "".join(rows)


def pips(cx, cy, n, r=15, s=42):
    pos = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)],
           4: [(-1, -1), (1, -1), (-1, 1), (1, 1)], 5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],
           6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}[n]
    return "".join(f'<circle cx="{cx + x * s}" cy="{cy + y * s}" r="{r}" fill="{INK}"/>' for x, y in pos)


def meeple(x, y, color, sc=1.0):
    return (f'<path transform="translate({x} {y}) scale({sc})" fill="{color}" d="M0 -120 a45 45 0 1 1 0.1 0 '
            'M-40 -75 C-110 -70 -140 -40 -130 -15 C-120 5 -75 0 -55 -5 L-95 110 L-20 110 L0 55 L20 110 L95 110 '
            'L55 -5 C75 0 120 5 130 -15 C140 -40 110 -70 40 -75 Z"/>')


STICKER = f"""
<svg style="position:absolute;left:90px;top:170px" width="900" height="760" viewBox="0 0 900 760">
 <defs><filter id="diecut" x="-10%" y="-10%" width="120%" height="120%">
  <feMorphology in="SourceAlpha" operator="dilate" radius="16" result="d"/>
  <feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/>
  <feDropShadow in="w" dx="0" dy="10" stdDeviation="12" flood-color="#14203c" flood-opacity=".30" result="ws"/>
  <feMerge><feMergeNode in="ws"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
 <g filter="url(#diecut)">
  <!-- การ์ดเกมคลี่เป็นพัด -->
  <g transform="translate(470 420)">
   <rect x="-110" y="-300" width="220" height="310" rx="22" fill="#E86A5C" transform="rotate(-22)"/>
   <rect x="-110" y="-300" width="220" height="310" rx="22" fill="#6BC4A6" transform="rotate(-4)"/>
   <rect x="-110" y="-300" width="220" height="310" rx="22" fill="#FFFFFF" stroke="{INK}" stroke-width="8" transform="rotate(14)"/>
   <g transform="rotate(14)"><circle cx="0" cy="-150" r="55" fill="{ACCENT}"/><path d="M-30 -150 L0 -185 L30 -150 L0 -115 Z" fill="#E86A5C"/></g>
  </g>
  <!-- ลูกเต๋า 2 ลูก -->
  <g transform="translate(250 520) rotate(-12)"><rect x="-120" y="-120" width="240" height="240" rx="40" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>{pips(0, 0, 5)}</g>
  <g transform="translate(470 610) rotate(10)"><rect x="-95" y="-95" width="190" height="190" rx="34" fill="{ACCENT}" stroke="{INK}" stroke-width="10"/>{pips(0, 0, 3, 13, 38)}</g>
  <!-- ตัวหมาก meeple -->
  {meeple(680, 560, "#E86A5C", 0.9)}
  {meeple(840, 690, "#6BC4A6", 0.6)}
 </g>
</svg>"""

ICON_PHONE = f'<svg width="70" height="70" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#E8F0FE"/><path fill="#4E6FB3" d="M8.2 5.5l1.7 3-1.3 1.3a8 8 0 0 0 5.6 5.6l1.3-1.3 3 1.7-.8 2.6c-6 .4-12-5.6-11.6-11.6z"/></svg>'
ICON_FB = '<svg width="70" height="70" viewBox="0 0 24 24"><rect width="24" height="24" rx="5" fill="#1877F2"/><path fill="#fff" d="M13.5 20v-6.3h2.1l.3-2.5h-2.4V9.6c0-.7.2-1.2 1.2-1.2h1.3V6.2c-.2 0-1-.1-1.9-.1-1.9 0-3.1 1.1-3.1 3.2v1.9H8.9v2.5H11V20z"/></svg>'
ICON_WEB = '<svg width="70" height="70" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#FDE2E4"/><g fill="none" stroke="#E86A8A" stroke-width="1.4"><circle cx="12" cy="12" r="6.5"/><ellipse cx="12" cy="12" rx="2.8" ry="6.5"/><path d="M5.5 12h13M6.5 8.8h11M6.5 15.2h11"/></g></svg>'
ICON_GLOBE = f'<svg width="150" height="150" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="none" stroke="#fff" stroke-width="1.6"/><g fill="none" stroke="#fff" stroke-width="1.3"><ellipse cx="12" cy="12" rx="4.5" ry="11"/><path d="M1 12h22M3 6.5h18M3 17.5h18"/></g></svg>'

HTML = f"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
html,body{{margin:0;width:2160px;height:2160px;overflow:hidden;background:{CREAM};font-family:Kanit;color:{INK}}}
.deco{{position:absolute;left:0;top:0}}
.logo{{position:absolute;right:70px;top:60px;width:300px}}
.logo img{{width:100%;display:block}}
.title{{position:absolute;left:1010px;top:300px}}
.chip{{display:inline-block;white-space:nowrap;background:{BG};color:#fff;font-weight:600;font-size:104px;padding:4px 56px;border-radius:999px;line-height:1.35}}
.head{{color:{INK};font-weight:700;font-size:170px;line-height:1.15;margin-top:20px}}
.body{{position:absolute;top:1100px;width:100%;text-align:center;font-weight:500;font-size:96px;line-height:1.5}}
.bar{{position:absolute;left:180px;top:1560px;width:1800px;height:300px}}
.bar .t{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:50px;color:#fff;font-weight:600;font-size:124px}}
.note{{position:absolute;top:1868px;width:100%;text-align:center;font-size:58px;color:#6a6f7c}}
.foot{{position:absolute;left:0;bottom:0;width:2160px;height:170px;display:flex;align-items:center;justify-content:center;gap:120px;font-size:54px}}
.foot div{{display:flex;align-items:center;gap:24px}}
</style></head><body>
<svg class="deco" width="2160" height="2160">
 <g fill="none" stroke="{CREAM_LINE}" stroke-width="8">{wave(height=2160)}</g>
 <path fill="{BG}" d="M-60 -60 H1180 C1240 180 1150 380 1020 520 C880 680 1010 900 820 1010 C640 1110 420 980 260 1040 C120 1090 20 1060 -60 1000 Z"/>
 <circle cx="1980" cy="1030" r="120" fill="{ACCENT}" opacity=".85"/>
 <g fill="#E86A5C">{"".join(f'<circle cx="{1850 + (i % 4) * 44}" cy="{930 + (i // 4) * 44}" r="11"/>' for i in range(12))}</g>
 <path fill="#fff" d="M0 1990 C360 1950 720 2010 1080 1985 S1800 1950 2160 1990 V2160 H0 Z"/>
</svg>
{STICKER}
<div class="logo"><img src="nsru-library-logo.png"></div>
<div class="title"><div class="chip">{HEADLINE_CHIP}</div><div class="head">{HEADLINE}</div></div>
<div class="body">{"<br>".join(BODY)}</div>
<svg class="bar" viewBox="0 0 1800 300" preserveAspectRatio="none"><path fill="{BG}" d="M40 40 C300 10 600 30 900 18 S1500 8 1770 30 L1740 90 L1790 140 L1750 200 L1785 260 C1500 290 1100 272 800 285 S250 292 30 270 L60 210 L12 150 L55 95 Z"/></svg>
<div class="bar"><div class="t">{ICON_GLOBE}<span>{LINK}</span></div></div>
<div class="note">{NOTE}</div>
<div class="foot"><div>{ICON_PHONE}0-5621-9100 ต่อ 1534</div><div>{ICON_FB}Library.NSRU</div><div>{ICON_WEB}aritc.nsru.ac.th</div></div>
</body></html>"""

src = S / "suggest.html"
src.write_text(HTML, encoding="utf-8")
OUT.parent.mkdir(parents=True, exist_ok=True)
subprocess.run([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "--headless=new", "--disable-gpu",
                "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=2160,2160", "--virtual-time-budget=15000",
                rf"--user-data-dir={os.environ['TEMP']}\edgeshot", f"--screenshot={OUT}", src.as_uri()], check=True)
print(OUT)
