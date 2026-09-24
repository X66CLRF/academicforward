"""ภาพเชิญเสนอชื่อทรัพยากร — สไตล์เรขาคณิต + สี (ตาม slide-hub-agent 3.3 / design-system)

ออก 2 ขนาดจากโค้ดเดียว:
  square : 2160x2160 (โพสต์ Facebook)
  a4     : 2480x3508 (300 dpi, มี QR สำหรับติดบอร์ด)

กติกา: พื้นสว่าง + dot grid จาง · แผงกราฟิกเรขาคณิต 1 แผง (วงกลม/สี่เหลี่ยมมนซ้อน + ไอคอน lucide)
การ์ดขาวมุมมน · ป้ายเป็น pill · ตัวอักษรเทาเกือบดำ · สีเน้นเดียว · ห้ามอีโมจิ · ห้ามการ์ตูน
"""
import base64, io, os, subprocess
from pathlib import Path
import qrcode

S = Path(__file__).parent
OUT_DIR = Path(r"G:\Shared drives\งานแนะนำทรัพยากรสารสนเทศ\เสนอหนังสือ\2569")
LOGO = S / "nsru-library-logo.png"

# ---- เนื้อหา -------------------------------------------------------------
EYEBROW = "ห้องสมุดเปิดรับข้อเสนอ"
TITLE = "ร่วมเสนอชื่อ<br>บอร์ดเกม"   # ตัดบรรทัดเองที่รอยต่อคำ ห้ามให้เบราว์เซอร์ตัดกลางคำ
SUB = "ผ่านระบบออนไลน์"
BODY = "ขอเชิญนักศึกษา อาจารย์ และบุคลากร ร่วมเสนอชื่อบอร์ดเกมที่สนใจหรือชื่นชอบ ให้ห้องสมุดพิจารณาจัดหา"
URL = "https://booktogether.nsru.ac.th/"
LINK = "booktogether.nsru.ac.th"
NOTE = "เข้าสู่ระบบด้วยบัญชี Google @nsru.ac.th"

# ---- ธีม library-warm (slide-hub 3.3.1) -----------------------------------
BG, DOT = "#faf7f0", "#e6dfd1"
INK, MUTED = "#18181b", "#6b6b73"
SAGE, SAGE_1, SAGE_2 = "#5f7f67", "#dfe8e0", "#c4d5c7"
BRICK = "#d0694a"
BORDER = "#e4e4e7"

# ---- ไอคอน lucide (คัด path จาก lucide.dev ขนาด 24) -------------------------
def lucide(body, size, color, sw=2):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')

DICE5 = ('<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M16 8h.01"/><path d="M8 8h.01"/>'
         '<path d="M8 16h.01"/><path d="M16 16h.01"/><path d="M12 12h.01"/>')                  # dice-5
GLOBE = '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>'  # globe
PHONE = ('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 '
         '19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 '
         '2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 '
         '2.81.7A2 2 0 0 1 22 16.92z"/>')                                                       # phone
FB = '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'         # facebook
KEY = ('<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/>'
       '<circle cx="7.5" cy="15.5" r="5.5"/>')                                                 # key-round


def qr_data_uri():
    q = qrcode.QRCode(border=0, box_size=20, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(URL); q.make(fit=True)
    buf = io.BytesIO(); q.make_image(fill_color=INK, back_color="white").save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def logo_uri():
    return "data:image/png;base64," + base64.b64encode(LOGO.read_bytes()).decode()


def panel(w, h):
    """แผงกราฟิกเรขาคณิต: วงกลมซ้อน 3 ชั้น + วงกลมขาวมีเงา + ไอคอนลูกเต๋า"""
    c = min(w, h)
    return f"""
<div class="panel" style="width:{w}px;height:{h}px">
 <svg class="rings" width="{w}" height="{h}">
  <circle cx="{w*0.78}" cy="{h*0.2}" r="{c*0.46}" fill="{SAGE_2}" opacity=".55"/>
  <circle cx="{w*0.2}" cy="{h*0.85}" r="{c*0.34}" fill="{SAGE_2}" opacity=".45"/>
  <circle cx="{w/2}" cy="{h/2}" r="{c*0.36}" fill="none" stroke="{SAGE}" stroke-width="2" opacity=".35"/>
  <circle cx="{w/2}" cy="{h/2}" r="{c*0.44}" fill="none" stroke="{SAGE}" stroke-width="2" stroke-dasharray="6 10" opacity=".35"/>
  <circle cx="{w*0.86}" cy="{h*0.8}" r="{c*0.05}" fill="{BRICK}"/>
 </svg>
 <div class="disc" style="width:{c*0.54}px;height:{c*0.54}px">{lucide(DICE5, int(c*0.3), SAGE, 1.6)}</div>
</div>"""


CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&display=swap');
*{{box-sizing:border-box}}
html,body{{margin:0;overflow:hidden;font-family:Sarabun,sans-serif;color:{INK};
 background:{BG} radial-gradient(circle,{DOT} 2px,transparent 2.5px) 0 0/24px 24px}}
.deco{{position:absolute;border-radius:50%;border:1.5px solid {SAGE_2}}}
.logo{{position:absolute;width:150px}}
.eyebrow{{display:inline-block;background:{SAGE_1};color:{SAGE};font-weight:700;border-radius:9999px;line-height:1.6}}
h1{{margin:0;font-weight:800;line-height:1.4;letter-spacing:0;white-space:nowrap}}
.sub{{font-weight:700;color:{SAGE};line-height:1.4}}
.panel{{position:relative;border-radius:24px;background:{SAGE_1};overflow:hidden;flex:none}}
.rings{{position:absolute;inset:0}}
.disc{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;background:#fff;
 display:flex;align-items:center;justify-content:center;box-shadow:0 20px 45px -15px rgba(0,0,0,.18)}}
.card{{background:#fff;border:1px solid {BORDER};border-radius:24px;box-shadow:0 20px 45px -15px rgba(0,0,0,.07)}}
.body{{line-height:1.7;text-wrap:balance;text-align:center}}
.link{{display:flex;align-items:center;gap:14px;background:{SAGE};color:#fff;border-radius:9999px;font-weight:700;white-space:nowrap}}
.note{{display:flex;align-items:center;gap:10px;color:{MUTED}}}
.foot{{position:absolute;left:0;right:0;display:flex;justify-content:center;gap:44px;color:{MUTED}}}
.foot span{{display:flex;align-items:center;gap:10px}}
"""

FOOT = (f'<span>{lucide(PHONE, 22, MUTED)}0-5621-9100 ต่อ 1534</span>'
        f'<span>{lucide(FB, 22, MUTED)}Library.NSRU</span>'
        f'<span>{lucide(GLOBE, 22, MUTED)}aritc.nsru.ac.th</span>')


def square():  # ออกแบบที่ 1080 แล้วคูณ 2 = 2160
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{CSS}
html,body{{width:1080px;height:1080px}}
.eyebrow{{font-size:24px;padding:4px 22px}} h1{{font-size:70px}} .sub{{font-size:52px}}
.body{{font-size:32px}} .link{{font-size:40px;padding:14px 34px}} .note{{font-size:22px}} .foot{{font-size:20px;bottom:36px}}
</style></head><body>
<div class="deco" style="width:260px;height:260px;left:-90px;top:-90px"></div>
<div class="deco" style="width:180px;height:180px;right:-60px;bottom:120px"></div>
<img class="logo" src="{logo_uri()}" style="right:56px;top:48px">
<div style="position:absolute;left:64px;top:96px;width:540px">
 <span class="eyebrow">{EYEBROW}</span>
 <h1 style="margin-top:14px">{TITLE}</h1>
 <div class="sub">{SUB}</div>
</div>
<div style="position:absolute;right:64px;top:170px">{panel(360, 380)}</div>
<div class="card" style="position:absolute;left:64px;right:64px;top:590px;padding:40px 48px 36px">
 <div class="body">{BODY}</div>
 <div style="display:flex;flex-direction:column;align-items:center;gap:16px;margin-top:26px">
  <div class="link">{lucide(GLOBE, 40, "#fff")}{LINK}</div>
  <div class="note">{lucide(KEY, 22, MUTED)}{NOTE}</div>
 </div>
</div>
<div class="foot">{FOOT}</div>
</body></html>""", (1080, 1080), "เสนอบอร์ดเกม.png"


def a4():  # ออกแบบที่ 1240x1754 แล้วคูณ 2 = 2480x3508 (A4 300 dpi)
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><style>{CSS}
html,body{{width:1240px;height:1754px}}
.eyebrow{{font-size:28px;padding:6px 26px}} h1{{font-size:92px}} .sub{{font-size:66px}}
.body{{font-size:36px;text-align:center}} .link{{font-size:46px;padding:16px 40px}} .note{{font-size:26px}} .foot{{font-size:24px;bottom:48px}}
</style></head><body>
<div class="deco" style="width:340px;height:340px;left:-120px;top:-120px"></div>
<div class="deco" style="width:260px;height:260px;right:-90px;bottom:220px"></div>
<img class="logo" src="{logo_uri()}" style="right:72px;top:64px;width:180px">
<div style="position:absolute;left:84px;top:130px;width:640px">
 <span class="eyebrow">{EYEBROW}</span>
 <h1 style="margin-top:18px">{TITLE}</h1>
 <div class="sub">{SUB}</div>
</div>
<div style="position:absolute;right:84px;top:270px">{panel(400, 420)}</div>
<div class="card" style="position:absolute;left:84px;right:84px;top:730px;padding:40px 64px">
 <div class="body">{BODY}</div>
</div>
<div class="card" style="position:absolute;left:50%;transform:translateX(-50%);top:990px;width:420px;padding:32px;text-align:center">
 <img src="{qr_data_uri()}" style="width:356px;height:356px;display:block">
 <div style="margin-top:18px;font-size:26px;color:{MUTED}">สแกนเพื่อเสนอชื่อ</div>
</div>
<div style="position:absolute;left:0;right:0;top:1520px;display:flex;flex-direction:column;align-items:center;gap:16px">
 <div class="link">{lucide(GLOBE, 46, "#fff")}{LINK}</div>
 <div class="note">{lucide(KEY, 26, MUTED)}{NOTE}</div>
</div>
<div class="foot">{FOOT}</div>
</body></html>""", (1240, 1754), "เสนอบอร์ดเกม A4.png"


EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT_DIR.mkdir(parents=True, exist_ok=True)
for build in (square, a4):
    html, (w, h), name = build()
    src = S / f"geo_{build.__name__}.html"
    src.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    f"--window-size={w},{h}", "--virtual-time-budget=15000",
                    rf"--user-data-dir={os.environ['TEMP']}\edgeshot", f"--screenshot={OUT_DIR / name}", src.as_uri()],
                   check=True)
    print(name)
