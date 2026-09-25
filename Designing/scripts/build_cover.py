r"""ปกห้อง NoteBoard 16:9 — ออกแบบให้อ่านออกทั้งการ์ด (~300px) และรูปย่อ (64px)

    python build_cover.py --title "มือถือเรา ใครคุม?" --kicker "อบรมความรู้ดิจิทัล" \
        --theme soft-blue --icon shield --out <งาน>\cover.jpg

กติกาปก: หัวเรื่องใหญ่ 1 บรรทัด (ไม่เกิน 2) · กราฟิกเรขาคณิต 1 ชุดฝั่งขวา · ไม่มีเลขหน้า/ข้อความเล็ก
มุมล่างซ้ายเว้นว่าง (NoteBoard วางป้าย Active ทับ) · ธีมเดียวกับสไลด์ชุดนั้น
ได้ JPEG 1280×720 ขนาด < 150KB (ฐานข้อมูลเก็บเป็น data URL)
"""
import argparse, base64, io, subprocess, tempfile
from pathlib import Path

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
LOGO = Path.home() / "Documents" / "slides" / "assets" / "aritc-logo.png"

THEMES = {  # พื้น, ลาย, สีเน้นหลัก, สีเน้นรอง, พื้นแผงอ่อน
    "soft-blue":    ("#f7f9fc", "#d6dee9", "#1e88c8", "#7cc0ea", "#e3f1fb"),
    "library-warm": ("#faf7f0", "#e4dccb", "#5f7f67", "#d0694a", "#e8efe6"),
    "craft-paper":  ("#f8f5ee", "#e3d9c8", "#8b6b52", "#c9a27e", "#efe6da"),
    "graphite":     ("#f8f8f6", "#d4d4d8", "#18181b", "#71717a", "#ececec"),
}

# lucide (MIT) — path ของไอคอนที่ใช้บ่อยในงานอบรม
ICONS = {
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "book": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    "sparkles": '<path d="M9.94 14.06 5 19"/><path d="M12 3l1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z"/>',
    "library": '<path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/>',
    "smartphone": '<rect width="14" height="20" x="5" y="2" rx="2"/><path d="M12 18h.01"/>',
    "graduation": '<path d="M21.42 10.92a1 1 0 0 0-.02-1.84L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.83l8.57 3.91a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "presentation": '<path d="M2 3h20"/><path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/><path d="m7 21 5-5 5 5"/>',
}

HTML = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@500;700;800&display=swap" rel="stylesheet">
<style>
@page{{size:1280px 720px;margin:0}}
*{{box-sizing:border-box;margin:0}}
html,body{{width:1280px;height:720px;overflow:hidden}}
body{{font-family:'Sarabun','Leelawadee UI',Tahoma,sans-serif;background:{bg};
  background-image:radial-gradient({dot} 1.6px,transparent 1.6px);background-size:28px 28px;position:relative;color:#18181b}}
.left{{position:absolute;left:84px;top:0;bottom:0;width:640px;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}}
.logo{{height:58px;width:auto;margin-bottom:34px;align-self:flex-start}}
.kicker{{display:inline-block;align-self:flex-start;font-size:30px;font-weight:700;line-height:1.6;color:{a1};
  background:#fff;border:1px solid #e4e4e7;border-radius:999px;padding:4px 26px;margin-bottom:22px}}
h1{{font-size:{size}px;font-weight:800;line-height:1.35;letter-spacing:-.5px;text-wrap:balance}}
h1 mark{{background:linear-gradient(transparent 62%,{a2}55 62%);color:inherit}}
.art{{position:absolute;right:-40px;top:50%;transform:translateY(-50%);width:560px;height:560px}}
.ring{{position:absolute;border-radius:50%}}
.r1{{inset:0;background:{panel}}}
.r2{{inset:70px;border:2px solid {a2}66}}
.r3{{inset:140px;background:#fff;box-shadow:0 30px 60px -20px rgba(0,0,0,.12)}}
.dot{{position:absolute;width:64px;height:64px;border-radius:50%;background:{a2}}}
.icon{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}}
.icon svg{{width:170px;height:170px;stroke:{a1};stroke-width:1.8;fill:none;stroke-linecap:round;stroke-linejoin:round}}
</style></head><body>
<div class="art"><div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div>
<div class="dot" style="left:92px;top:78px"></div><div class="dot" style="left:470px;top:410px;width:34px;height:34px;background:{a1}"></div>
<div class="icon"><svg viewBox="0 0 24 24">{icon}</svg></div></div>
<div class="left">{logo}<span class="kicker">{kicker}</span><h1>{title}</h1></div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True, help="*คำ* = ขีดเน้น · | = ขึ้นบรรทัดใหม่ (ไม่เกิน 2 บรรทัด)")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--theme", default="soft-blue", choices=THEMES)
    ap.add_argument("--icon", default="presentation", choices=ICONS)
    ap.add_argument("--no-logo", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    bg, dot, a1, a2, panel = THEMES[a.theme]
    import re
    lines = [ln.strip() for ln in a.title.split("|")]
    title = "<br>".join(
        '<span style="white-space:nowrap">' + re.sub(r"\*(.+?)\*", r"<mark>\1</mark>", ln) + "</span>"
        for ln in lines)
    longest = max(len(ln.replace("*", "")) for ln in lines)
    size = 104 if longest <= 12 else 88 if longest <= 16 else 76 if longest <= 20 else 64
    logo = ""
    if not a.no_logo and LOGO.exists():
        logo = f'<img class="logo" src="data:image/png;base64,{base64.b64encode(LOGO.read_bytes()).decode()}">'
    html = HTML.format(bg=bg, dot=dot, a1=a1, a2=a2, panel=panel, size=size, title=title,
                       kicker=a.kicker or "&nbsp;", icon=ICONS[a.icon], logo=logo)

    out = Path(a.out).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "cover.html"
        src.write_text(html, encoding="utf-8")
        png = Path(tmp) / "cover.png"
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--window-size=1280,720", "--virtual-time-budget=8000", f"--user-data-dir={tmp}\\edge",
                        f"--screenshot={png}", src.as_uri()], check=True, capture_output=True)
        from PIL import Image
        img = Image.open(png).convert("RGB").crop((0, 0, 1280, 720))
        for q in (88, 80, 72, 64):
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
            if buf.tell() < 150_000:
                break
        out.write_bytes(buf.getvalue())
    print(f"{out}  {out.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
