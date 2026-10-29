# cover-set-v2.py — ชั้นภาพชุดปกจริง (เทมเพลต v2 ที่เจ้าของแก้): ลายคลัง ย้อมสีปก · แถบโลโก้ · เงา · ปกขยายสูง 1560 · หัวเรื่อง/ป้ายเดือน Pattaya (หน้าชุด)
# ใช้: คัดลอกไป %TEMP%\w\ วางปกเป็น j.jpg / n1.jpg ... แก้ตารางสี `cols` + ข้อความหัวเรื่อง แล้ว `py -X utf8 cover-set-v2.py` → layers\*.png + sizes.json
# ขึ้น Canva: อัปแต่ละไฟล์ → insert_fill ลำดับ ลาย(opacity 0.18) → แถบโลโก้ (918,0 324x336) → เงา (x-140, 292) → ปก (กลางหน้า, top 432)
# ชั้นภาพ v2: พื้นขาว · ลายจาก pattern-library (ย้อมสีตามปก) · แถบโลโก้ · เงา · ปกจริง · (หน้าชุด) ชื่อ+ป้ายเดือน
import json, os, re, subprocess, time, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

W = Path(os.environ["TEMP"]) / "w"
L = W / "layers"; L.mkdir(exist_ok=True)
LIB = Path.home() / "Documents/GitHub/academicforward/Designing"
LOGO = LIB / "templates/aritc-logo.png"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not Path(EDGE).exists():
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
TILE = 144  # 2160/144 = 15 → ต่อกันได้ตอน Facebook เรียง 2x2


def wait_file(p, t=40):
    p, last, t0 = Path(p), -1, time.time()
    while time.time() - t0 < t:
        if p.exists() and p.stat().st_size == last > 0:
            return
        last = p.stat().st_size if p.exists() else -1
        time.sleep(0.5)
    raise SystemExit(f"Edge ไม่เขียน {p}")


def shot(html, out, w=2160, h=2160):
    src = Path(str(out) + ".html")
    src.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", "--default-background-color=00000000", f"--window-size={w},{h}",
                    "--virtual-time-budget=20000", rf"--user-data-dir={os.environ['TEMP']}\edgeshot3",
                    f"--screenshot={out}", src.as_uri()], check=True)
    wait_file(out)


def pattern_svg(family, base_tile, repl):
    s = (LIB / f"patterns/svg/{family}.svg").read_text(encoding="utf-8")
    for a, b in repl.items():
        s = s.replace(a, b)
    s = re.sub(r'<rect width="100%" height="100%" fill="#[0-9A-Fa-f]{6}"/>', "", s, count=1)  # ตัดพื้น เหลือแต่ลาย
    k = TILE / base_tile
    s = s.replace('<pattern id="p"', f'<pattern id="p" patternTransform="scale({k})"')
    return s.replace('viewBox="0 0 1200 1200" width="1200" height="1200"', 'viewBox="0 0 2160 2160" width="2160" height="2160"')


def pattern_png(name, svg):
    (L / f"{name}.svg").write_text(svg, encoding="utf-8")
    html = f'<!doctype html><html><body style="margin:0;background:transparent">{svg}</body></html>'
    shot(html, L / f"{name}.png")


def tab_png():
    im = Image.new("RGBA", (324, 336), (255, 255, 255, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, -40, 323, 335), 22, fill="white")
    d.rectangle((0, 0, 323, 40), fill="white")
    logo = Image.open(LOGO).convert("RGBA"); r = 260 / logo.width
    logo = logo.resize((260, int(logo.height * r)), Image.LANCZOS)
    im.alpha_composite(logo, (32, (336 - logo.height) // 2))
    im.save(L / "tab.png")


def cover(src, name, H=1560):
    im = Image.open(src).convert("RGB")
    w = round(im.width * H / im.height)
    im = im.resize((w, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 3))
    im.save(L / f"{name}.jpg", quality=95)
    return w, H


def shadow(name, w, h, pad=140, dy=26, blur=36, alpha=80):
    cv = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new("L", cv.size, 0)
    ImageDraw.Draw(sh).rectangle((pad, pad + dy, pad + w, pad + h + dy), fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    ImageDraw.Draw(sh).rectangle((pad, pad, pad + w - 1, pad + h - 1), fill=0)  # เจาะกลางออก
    cv.putalpha(sh); cv.save(L / f"{name}.png")
    return w + pad * 2, h + pad * 2, pad


def title_png(text, name, kind):
    css = ("font-family:Pattaya;font-weight:400;position:absolute;left:0;top:0;white-space:nowrap;")
    if kind == "title":
        body = f'<div style="{css}font-size:270px;line-height:1.2;color:#15435B;-webkit-text-stroke:36px #fff;paint-order:stroke fill;padding:30px 60px">{text}</div>'
    else:
        body = f'<div style="{css}background:#fff;padding:6px 52px;border-radius:999px;font-size:112px;color:#C23B3B">{text}</div>'
    html = ('<!doctype html><html lang="th"><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Pattaya&display=block" rel="stylesheet">'
            f'<style>html,body{{margin:0;width:2160px;height:2160px;background:transparent;position:relative}}</style></head><body>{body}</body></html>')
    out = L / f"{name}_full.png"
    shot(html, out)
    im = Image.open(out).convert("RGBA"); bb = im.getchannel("A").getbbox()
    im.crop(bb).save(L / f"{name}.png"); out.unlink()
    return bb[2] - bb[0], bb[3] - bb[1]


pos = {}
tab_png()
# --- วารสาร: อาร์ไกล์ น้ำเงิน+แดงจากปก ---
j = pattern_svg("24-argyle-Bl", 168, {"#1C418F": "#1A6FC2", "#EFC84C": "#F2284B", "#001F5C": "#F2284B"})
pattern_png("j_pattern", j)
pos["j_cover"] = cover(W / "j.jpg", "j_cover")
pos["j_shadow"] = shadow("j_shadow", *pos["j_cover"])
# --- นิยาย: กิ่งใบ ย้อมสีตามปกแต่ละเล่ม ---
cols = {"set": ("#F28C1E", "#3FA66B"), "n1": ("#F28C1E", "#3FA66B"), "n2": ("#4B4F8A", "#F2B705"), "n3": ("#E0577F", "#F2B705")}
for k, (a, b) in cols.items():
    s = pattern_svg("20-sprigs-Bm", 128, {"#1C418F": a, "#EFC84C": b, "#001F5C": a})
    pattern_png(f"{k}_pattern", s)
for k in ("n1", "n2", "n3"):
    pos[f"{k}_cover"] = cover(W / f"{k}.jpg", f"{k}_cover")
    pos[f"{k}_shadow"] = shadow(f"{k}_shadow", *pos[f"{k}_cover"])
pos["title"] = title_png("แนะนำนวนิยาย", "title", "title")
pos["chip"] = title_png("ประจำเดือน ต.ค. 69", "chip", "chip")
(L / "sizes.json").write_text(json.dumps(pos, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(pos, ensure_ascii=False))
