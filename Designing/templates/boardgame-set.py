# boardgame-set.py — แม่แบบกราฟิกแนะนำบอร์ดเกม (2160×2160) ประจำสำนักวิทยบริการฯ (ARITC)
# มาตรฐาน: ฟอนต์ Mitr, ลาย Tabletop Grid, แถบโลโก้ ARITC, Badges ข้อมูล (แนวเกม/ผู้เล่น/รหัส), ขอบมนและเงานุ่ม
import subprocess, os, time, sys
from pathlib import Path

S = Path(__file__).parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
DEFAULT_LOGO = S / "aritc-logo.png"

def wait_file(path, timeout=40):
    """msedge คืนค่าก่อนเขียนภาพเสร็จบน Windows — รอจนไฟล์มีและขนาดนิ่ง"""
    path, last, t0 = Path(path), -1, time.time()
    while time.time() - t0 < timeout:
        if path.exists() and path.stat().st_size == last > 0:
            return
        last = path.stat().st_size if path.exists() else -1
        time.sleep(0.5)
    raise SystemExit(f"Edge ไม่เขียน {path} ภายใน {timeout} วินาที")

# Lucide-style SVG Icons (Vector, No Emojis)
ICON_GENRE = """<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 7V3.5a2.5 2.5 0 0 0-5 0V7H4a2 2 0 0 0-2 2v4.5a2.5 2.5 0 0 1 0 5V21a2 2 0 0 0 2 2h4.5a2.5 2.5 0 0 1 5 0H20a2 2 0 0 0 2-2v-2.5a2.5 2.5 0 0 0 0-5V9a2 2 0 0 0-2-2h-6z"/></svg>"""
ICON_PLAYERS = """<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>"""
ICON_CODE = """<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2H2v10l9.29 9.29c.94.94 2.48.94 3.42 0l6.58-6.58c.94-.94.94-2.48 0-3.42L12 2Z"/><circle cx="7" cy="7" r="1.5" fill="currentColor"/></svg>"""
ICON_PIN = """<svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#E11D48" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3" fill="#E11D48"/></svg>"""

MEEPLE_D = ("M 100 25 "
            "C 114 25 125 36 125 50 "
            "C 125 59 120 67 113 72 "
            "C 125 78 145 92 165 98 "
            "C 172 100 175 108 171 114 "
            "C 167 120 159 122 153 118 "
            "C 140 109 130 102 124 100 "
            "L 125 135 "
            "L 148 180 "
            "C 152 188 145 195 137 195 "
            "L 112 195 "
            "C 107 195 104 190 102 185 "
            "L 100 150 "
            "L 98 185 "
            "C 96 190 93 195 88 195 "
            "L 63 195 "
            "C 55 195 48 188 52 180 "
            "L 75 135 "
            "L 76 100 "
            "C 70 102 60 109 47 118 "
            "C 41 122 33 120 29 114 "
            "C 25 108 28 100 35 98 "
            "C 55 92 75 78 87 72 "
            "C 80 67 75 59 75 50 "
            "C 75 36 86 25 100 25 Z")

def build_bg_svg():
    return """<svg class="bg" viewBox="0 0 2160 2160" fill="none">
  <defs>
    <pattern id="grid" width="120" height="120" patternUnits="userSpaceOnUse">
      <path d="M 120 0 L 0 0 0 120" fill="none" stroke="#E3EAF2" stroke-width="3"/>
      <circle cx="120" cy="120" r="5" fill="#D0DDEB"/>
    </pattern>
  </defs>
  <rect width="2160" height="2160" fill="#F4F7FB"/>
  <rect width="2160" height="2160" fill="url(#grid)"/>
  <circle cx="180" cy="1980" r="300" stroke="#3D7AE8" stroke-width="7" stroke-opacity="0.16" stroke-dasharray="24 24"/>
  <circle cx="1980" cy="280" r="260" stroke="#F59E0B" stroke-width="7" stroke-opacity="0.18" stroke-dasharray="20 20"/>
  <circle cx="1980" cy="1980" r="180" fill="#10B981" fill-opacity="0.08"/>
  <circle cx="160" cy="340" r="140" fill="#EC4899" fill-opacity="0.06"/>
</svg>"""

def build_cover_sticker():
    return f"""<svg class="sticker" viewBox="0 0 1000 800" width="1440" height="1150">
  <defs>
    <filter id="diecut" x="-20%" y="-20%" width="140%" height="140%">
      <feMorphology in="SourceAlpha" operator="dilate" radius="22" result="dilated"/>
      <feFlood flood-color="#FFFFFF" result="white"/>
      <feComposite in="white" in2="dilated" operator="in" result="stroke"/>
      <feDropShadow in="stroke" dx="0" dy="24" stdDeviation="28" flood-color="#182844" flood-opacity="0.22" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="stroke"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="cardGrad1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F43F5E"/>
      <stop offset="100%" stop-color="#BE123C"/>
    </linearGradient>
    <linearGradient id="cardGrad2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
  </defs>

  <g filter="url(#diecut)">
    <!-- Isometric Board Base -->
    <path d="M 500 240 L 860 440 L 500 640 L 140 440 Z" fill="#E2EBF5" stroke="#CBDCEE" stroke-width="8"/>
    <path d="M 140 440 L 500 640 L 500 680 L 140 480 Z" fill="#93B2D6"/>
    <path d="M 500 640 L 860 440 L 860 480 L 500 680 Z" fill="#B9D0E8"/>

    <!-- Track tiles on board -->
    <path d="M 280 440 L 500 320 L 720 440 L 500 560 Z" fill="none" stroke="#FFFFFF" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 280 440 L 500 320 L 720 440 L 500 560 Z" fill="none" stroke="#60A5FA" stroke-width="20" stroke-dasharray="45 25" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- Game Cards Fan Left -->
    <g transform="translate(240, 260) rotate(-18)">
      <rect x="0" y="0" width="160" height="230" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="4"/>
      <rect x="12" y="12" width="136" height="206" rx="12" fill="url(#cardGrad1)"/>
      <circle cx="80" cy="115" r="34" fill="#FFFFFF" opacity="0.9"/>
      <polygon points="80,95 90,115 80,135 70,115" fill="#BE123C"/>
    </g>

    <!-- Game Card Middle -->
    <g transform="translate(320, 230) rotate(6)">
      <rect x="0" y="0" width="160" height="230" rx="16" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="4"/>
      <rect x="12" y="12" width="136" height="206" rx="12" fill="url(#cardGrad2)"/>
      <circle cx="80" cy="115" r="34" fill="#FFFFFF" opacity="0.9"/>
      <polygon points="80,90 92,105 107,105 95,117 100,132 80,122 60,132 65,117 53,105 68,105" fill="#D97706"/>
    </g>

    <!-- Big Blue Meeple Center-Front -->
    <g transform="translate(410, 360) scale(1.65)">
      <path d="{MEEPLE_D}" fill="#2563EB"/>
      <path d="{MEEPLE_D}" fill="none" stroke="#60A5FA" stroke-width="6" opacity="0.6"/>
    </g>

    <!-- Small Yellow Meeple Right -->
    <g transform="translate(620, 390) scale(1.15)">
      <path d="{MEEPLE_D}" fill="#F59E0B"/>
    </g>

    <!-- Small Green Meeple Left -->
    <g transform="translate(260, 420) scale(1.15)">
      <path d="{MEEPLE_D}" fill="#10B981"/>
    </g>

    <!-- 3D White D6 Die (Right) -->
    <g transform="translate(660, 220) scale(1.1)">
      <polygon points="100,20 170,55 100,90 30,55" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="3"/>
      <polygon points="30,55 100,90 100,165 30,130" fill="#E2E8F0" stroke="#CBD5E1" stroke-width="3"/>
      <polygon points="100,90 170,55 170,130 100,165" fill="#CBD5E1" stroke="#94A3B8" stroke-width="3"/>
      <ellipse cx="65" cy="42" rx="6" ry="3" fill="#E11D48"/>
      <ellipse cx="100" cy="55" rx="6" ry="3" fill="#E11D48"/>
      <ellipse cx="135" cy="68" rx="6" ry="3" fill="#E11D48"/>
      <circle cx="50" cy="80" r="5" fill="#1E293B"/>
      <circle cx="80" cy="95" r="5" fill="#1E293B"/>
      <circle cx="65" cy="110" r="5" fill="#1E293B"/>
      <circle cx="50" cy="125" r="5" fill="#1E293B"/>
      <circle cx="80" cy="140" r="5" fill="#1E293B"/>
      <circle cx="120" cy="115" r="5" fill="#1E293B"/>
      <circle cx="150" cy="100" r="5" fill="#1E293B"/>
    </g>

    <!-- 3D Purple D6 Die (Left) -->
    <g transform="translate(180, 220) rotate(-22) scale(0.75)">
      <polygon points="100,20 170,55 100,90 30,55" fill="#A855F7"/>
      <polygon points="30,55 100,90 100,165 30,130" fill="#7E22CE"/>
      <polygon points="100,90 170,55 170,130 100,165" fill="#9333EA"/>
      <ellipse cx="100" cy="55" rx="10" ry="6" fill="#FFFFFF"/>
    </g>
  </g>
</svg>"""

def render_cover_html(title="แนะนำบอร์ดเกม", month="ประจำเดือน ตุลาคม 2569", location="งานบริการสื่อโสตทัศน์ ชั้น 4 สำนักวิทยบริการฯ (อาคาร 15)", logo_path=None):
    if logo_path is None:
        logo_path = DEFAULT_LOGO
    logo_uri = Path(logo_path).as_uri()

    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Mitr:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; }}
html, body {{
  margin: 0; width: 2160px; height: 2160px; overflow: hidden;
  background: #F4F7FB; font-family: 'Mitr', sans-serif; position: relative;
}}
.bg {{ position: absolute; inset: 0; z-index: 0; }}
.tab {{
  position: absolute; left: 918px; top: 0; width: 324px; height: 260px;
  background: #fff; border-radius: 0 0 24px 24px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 12px 30px rgba(30,45,75,0.08); z-index: 10;
}}
.tab img {{ width: 250px; }}
.content {{
  position: relative; z-index: 2; width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center;
}}
.header {{
  margin-top: 360px; text-align: center; display: flex; flex-direction: column; align-items: center;
}}
h1.title {{
  font-family: 'Mitr', sans-serif; font-weight: 700; font-size: 195px; line-height: 1.15;
  color: #1E3A8A; margin: 0;
  -webkit-text-stroke: 32px #FFFFFF; paint-order: stroke fill;
  filter: drop-shadow(0 18px 35px rgba(30,58,138,0.18));
}}
.chip {{
  margin-top: 35px;
  background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
  padding: 16px 85px; border-radius: 999px;
  font-family: 'Mitr', sans-serif; font-weight: 600; font-size: 78px; line-height: 1.3;
  color: #FFFFFF; white-space: nowrap;
  box-shadow: 0 16px 36px rgba(37,99,235,0.30);
  border: 6px solid #FFFFFF;
}}
.sticker-wrap {{
  margin-top: 50px;
  display: flex; align-items: center; justify-content: center;
}}
.footer-badge {{
  position: absolute; bottom: 85px;
  display: flex; align-items: center; gap: 16px;
  background: #FFFFFF; padding: 18px 56px; border-radius: 999px;
  border: 2px solid #E2E8F0;
  box-shadow: 0 10px 28px rgba(30,45,75,0.06);
  font-size: 46px; color: #475569; font-weight: 500;
}}
</style></head><body>
{build_bg_svg()}
<div class="tab"><img src="{logo_uri}"></div>
<div class="content">
  <div class="header">
    <h1 class="title">{title}</h1>
    <div class="chip">{month}</div>
  </div>
  <div class="sticker-wrap">
    {build_cover_sticker()}
  </div>
  <div class="footer-badge">
    {ICON_PIN}
    {location}
  </div>
</div>
</body></html>"""

def render_item_html(title, box_img_path, genre, players, code, location="งานบริการสื่อโสตทัศน์ ชั้น 4 สำนักวิทยบริการฯ (อาคาร 15)", logo_path=None):
    if logo_path is None:
        logo_path = DEFAULT_LOGO
    logo_uri = Path(logo_path).as_uri()
    box_uri = Path(box_img_path).as_uri()

    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Mitr:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; }}
html, body {{
  margin: 0; width: 2160px; height: 2160px; overflow: hidden;
  background: #F4F7FB; font-family: 'Mitr', sans-serif; position: relative;
}}
.bg {{ position: absolute; inset: 0; z-index: 0; }}
.tab {{
  position: absolute; left: 918px; top: 0; width: 324px; height: 260px;
  background: #fff; border-radius: 0 0 24px 24px;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 12px 30px rgba(30,45,75,0.08); z-index: 10;
}}
.tab img {{ width: 250px; }}
.content {{
  position: relative; z-index: 2; width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center;
}}
.header {{ margin-top: 320px; text-align: center; }}
.title {{
  font-family: 'Mitr', sans-serif; font-weight: 600; font-size: 96px; line-height: 1.2;
  color: #182844; margin: 0;
}}
.box-wrapper {{
  margin-top: 50px; height: 1100px; max-width: 1550px;
  display: flex; justify-content: center; align-items: center;
}}
.box-img {{
  max-height: 1100px; max-width: 1500px; height: 1050px; width: auto;
  border-radius: 28px; border: 8px solid #FFFFFF;
  box-shadow: 0 35px 70px rgba(25,40,65,0.22);
  object-fit: contain;
}}
.info-row {{
  margin-top: 60px; display: flex; gap: 28px;
  align-items: center; justify-content: center;
}}
.badge {{
  padding: 14px 44px; border-radius: 999px;
  font-size: 52px; font-weight: 500;
  display: flex; align-items: center; gap: 18px;
  box-shadow: 0 8px 20px rgba(30,45,75,0.06);
}}
.badge-genre {{ background: #EBF3FB; color: #18538A; border: 2px solid #D5E6F7; }}
.badge-players {{ background: #FEF3E8; color: #B04A05; border: 2px solid #FCDDC2; }}
.badge-code {{ background: #EDF6EE; color: #236B2B; border: 2px solid #D2EBD4; }}
.footer {{
  margin-top: 50px; font-size: 44px; color: #6B7C93; font-weight: 400;
  display: flex; align-items: center; gap: 12px;
}}
</style></head><body>
{build_bg_svg()}
<div class="tab"><img src="{logo_uri}"></div>
<div class="content">
  <div class="header">
    <h1 class="title">{title}</h1>
  </div>
  <div class="box-wrapper">
    <img class="box-img" src="{box_uri}">
  </div>
  <div class="info-row">
    <div class="badge badge-genre">
      {ICON_GENRE}
      {genre}
    </div>
    <div class="badge badge-players">
      {ICON_PLAYERS}
      {players}
    </div>
    <div class="badge badge-code">
      {ICON_CODE}
      {code}
    </div>
  </div>
  <div class="footer">
    {ICON_PIN}
    {location}
  </div>
</div>
</body></html>"""

def render_boardgame_set(games_data, month_text, out_dir, title="แนะนำบอร์ดเกม", location="งานบริการสื่อโสตทัศน์ ชั้น 4 สำนักวิทยบริการฯ (อาคาร 15)"):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = out_dir / "_tmp_html"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    pages = {}
    # 1. Cover
    cover_html = render_cover_html(title=title, month=month_text, location=location)
    pages["1.png"] = cover_html

    # 2. Item Cards
    for idx, g in enumerate(games_data, start=2):
        name = f"{idx}.png"
        item_html = render_item_html(
            title=g["title"],
            box_img_path=g["image"],
            genre=g["genre"],
            players=g["players"],
            code=g["code"],
            location=location
        )
        pages[name] = item_html

    for name, html in pages.items():
        src_html = tmp_dir / f"p_{name}.html"
        src_html.write_text(html, encoding="utf-8")
        out_png = out_dir / name
        cmd = [
            EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            "--window-size=2160,2160", "--virtual-time-budget=10000",
            rf"--user-data-dir={os.environ['TEMP']}\edgeshot",
            f"--screenshot={out_png}",
            src_html.as_uri()
        ]
        subprocess.run(cmd, check=True)
        wait_file(out_png)
        print(f"[OK] Generated: {out_png} ({out_png.stat().st_size:,} bytes)")

    # Cleanup tmp htmls
    for f in tmp_dir.glob("*.html"):
        try:
            f.unlink()
        except Exception:
            pass
    try:
        tmp_dir.rmdir()
    except Exception:
        pass
    print("All pages generated successfully!")

if __name__ == "__main__":
    # Test / Default Execution for October 2569
    OCT_DIR = Path(r"G:\Shared drives\งานแนะนำทรัพยากรสารสนเทศ\สื่อโสตทัศน์\2569 (New)\ตุลาคม NEW")
    games = [
        {
            "image": OCT_DIR / "BG-69-006.jpg",
            "title": "TAKE TIME อัจฉริยะข้ามเวลา",
            "genre": "กลยุทธ์ / การจัดการเวลา",
            "players": "2 – 4 คน",
            "code": "BG-69-006"
        },
        {
            "image": OCT_DIR / "BG-69-007.jpg",
            "title": "TIMELINE เจาะเวลาท้าพิสูจน์",
            "genre": "ความรู้ / การ์ดเชิงการศึกษา",
            "players": "2 – 8 คน",
            "code": "BG-69-007"
        },
        {
            "image": OCT_DIR / "BG-69-008.jpg",
            "title": "ไม่ล่ะ! ขอบคุณ NO THANKS",
            "genre": "ปาร์ตี้ / การ์ดเชิงกลยุทธ์เบา ๆ",
            "players": "3 – 7 คน",
            "code": "BG-69-008"
        },
        {
            "image": OCT_DIR / "BG-69-009.jpg",
            "title": "FOR SALE (TH) เกมบ้านนี้ขาย!",
            "genre": "ประมูล / การลงทุน",
            "players": "3 – 6 คน",
            "code": "BG-69-009"
        },
        {
            "image": OCT_DIR / "BG-69-010.jpg",
            "title": "SIDE EFFECT อาการข้างเคียง",
            "genre": "ปาร์ตี้ / การ์ดตีความสัญลักษณ์",
            "players": "2 – 10 คน",
            "code": "BG-69-010"
        }
    ]
    render_boardgame_set(
        games_data=games,
        month_text="ประจำเดือน ตุลาคม 2569",
        out_dir=OCT_DIR
    )
