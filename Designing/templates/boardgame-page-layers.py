# ใช้ตาม ../content-to-visual.md — หน้าเกม (2-6) ตามเทมเพลตปก: ชื่อเรื่อง Pattaya ขอบขาว · กรอบรูปขาว+เงา · เลขหน้าวงกลม → PNG พื้นใส + layers_games.json
import json, os, subprocess, time
from pathlib import Path
from PIL import Image

S = Path(__file__).parent / "layers_boardgame_pages"
S.mkdir(exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
NAVY = "#15435B"
GAMES = [
    # no, title, photo size (w,h) fit 900x840, accent
    (2, "TAKE TIME อัจฉริยะข้ามเวลา", (827, 840), "#2F6F6B"),
    (3, "TIMELINE เจาะเวลาท้าพิสูจน์", (900, 828), "#D9791A"),
    (4, "ไม่ล่ะ! ขอบคุณ NO THANKS", (692, 840), "#C0392B"),
    (5, "FOR SALE (TH) เกมบ้านนี้ขาย!", (900, 697), "#3F8F6B"),
    (6, "SIDE EFFECT อาการข้างเคียง", (900, 774), "#B8862B"),
]
CX, CY = 1080, 1100

BASE = """<!doctype html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Pattaya&display=block" rel="stylesheet">
<style>
html,body{margin:0;width:2160px;height:2160px;overflow:hidden;background:transparent;position:relative}
.title{position:absolute;top:392px;width:100%;text-align:center;margin:0;font-family:Pattaya;font-weight:400;line-height:1.25;color:%NAVY%;-webkit-text-stroke:.14em #fff;paint-order:stroke fill;white-space:nowrap}
.frame{position:absolute;background:#fff;border-radius:36px;box-shadow:0 30px 60px rgba(30,60,80,.28)}
.num{position:absolute;left:1750px;top:1810px;width:230px;height:230px;border-radius:50%;background:#fff;box-shadow:0 14px 34px rgba(30,60,80,.22);display:flex;align-items:center;justify-content:center;font-family:Pattaya;font-size:120px;color:var(--c)}
</style></head><body>""".replace("%NAVY%", NAVY)


def wait_file(path, timeout=40):
    path, last, t0 = Path(path), -1, time.time()
    while time.time() - t0 < timeout:
        if path.exists() and path.stat().st_size == last > 0:
            return
        last = path.stat().st_size if path.exists() else -1
        time.sleep(0.5)
    raise SystemExit(f"Edge ไม่เขียน {path}")


pos = {}
for no, title, (w, h), acc in GAMES:
    # ขนาดตัวอักษรชื่อเรื่อง: ยาวมาก = ลดลงให้กว้างไม่เกิน ~1700px (ประมาณ 0.50 em ต่ออักษร)
    fs = min(170, int(1700 / (len(title) * 0.50)))
    left, top = CX - w // 2, CY - h // 2
    layers = {
        f"title{no}": f'<h1 class="title" style="font-size:{fs}px">{title}</h1>',
        f"frame{no}": f'<div class="frame" style="left:{left - 24}px;top:{top - 24}px;width:{w + 48}px;height:{h + 48}px"></div>',
        f"num{no}": f'<div class="num" style="--c:{acc}"><span>0{no - 1}</span></div>',
    }
    pos[f"photo{no}"] = {"left": left, "top": top, "width": w, "height": h}
    for name, html in layers.items():
        src = S / f"{name}.html"
        src.write_text(BASE + html + "</body></html>", encoding="utf-8")
        png = S / f"{name}_full.png"
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--allow-file-access-from-files", "--default-background-color=00000000", "--window-size=2160,2160",
                        "--virtual-time-budget=20000", rf"--user-data-dir={os.environ['TEMP']}\edgeshot4", f"--screenshot={png}", src.as_uri()], check=True)
        wait_file(png)
        im = Image.open(png).convert("RGBA")
        box = im.getchannel("A").getbbox()
        im.crop(box).save(S / f"{name}.png")
        pos[name] = {"left": box[0], "top": box[1], "width": box[2] - box[0], "height": box[3] - box[1]}
        png.unlink()
(S / "layers_games.json").write_text(json.dumps(pos, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in pos.items() if k.startswith("title")}, ensure_ascii=False))
