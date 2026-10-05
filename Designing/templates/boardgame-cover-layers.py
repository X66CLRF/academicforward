# ใช้ตาม ../content-to-visual.md — ปกชุดบอร์ดเกม ต.ค. 69 ตามเทมเพลตนิยายเดิม (novel-set.py) → PNG พื้นใสทีละชิ้น + layers.json
import json, os, subprocess, time
from pathlib import Path
from PIL import Image

S = Path(__file__).parent / "layers_boardgame_cover"
S.mkdir(exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not Path(EDGE).exists():
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
LOGO = Path(__file__).with_name("aritc-logo.png").as_uri()

BG, LINE, NAVY, RED = "#E8F3F5", "#D3E6EA", "#15435B", "#C23B3B"


def wave(period=1080, gap=180, amp=70):
    rows = []
    for y in range(-gap, 2160 + gap * 2, gap):
        d = f"M{-period} {y} Q{-period * 3 // 4} {y - amp} {-period // 2} {y}"
        d += "".join(f" T{x} {y}" for x in range(0, 2160 + period * 2, period // 2))
        rows.append(f'<path d="{d}"/>')
    return "".join(rows)


BASE = """<!doctype html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Pattaya&display=block" rel="stylesheet">
<style>
html,body{margin:0;width:2160px;height:2160px;overflow:hidden;background:transparent;position:relative}
.bg{position:absolute;inset:0}
.tab{position:absolute;left:918px;top:0;width:324px;height:336px;background:#fff;border-radius:0 0 22px 22px;display:flex;align-items:center;justify-content:center}
.tab img{width:260px}
h1{position:absolute;top:400px;width:100%;text-align:center;margin:0;font-family:Pattaya;font-weight:400;font-size:270px;line-height:1.2;color:%NAVY%;-webkit-text-stroke:36px #fff;paint-order:stroke fill}
.chip{position:absolute;top:780px;left:50%;transform:translateX(-50%);background:#fff;padding:6px 52px;border-radius:999px;font-family:Pattaya;font-weight:400;font-size:112px;color:%RED%;white-space:nowrap}
</style></head><body>""".replace("%NAVY%", NAVY).replace("%RED%", RED)

layers = {
    "wave": f'<svg class="bg" viewBox="0 0 2160 2160"><g fill="none" stroke="{LINE}" stroke-width="10">{wave()}</g></svg>',
    "logo-tab": f'<div class="tab"><img src="{LOGO}"></div>',
    "title": "<h1>แนะนำบอร์ดเกม</h1>",
    "chip": '<div class="chip">ประจำเดือน ต.ค. 69</div>',
}


def wait_file(path, timeout=40):
    path, last, t0 = Path(path), -1, time.time()
    while time.time() - t0 < timeout:
        if path.exists() and path.stat().st_size == last > 0:
            return
        last = path.stat().st_size if path.exists() else -1
        time.sleep(0.5)
    raise SystemExit(f"Edge ไม่เขียน {path}")


pos = {}
for name, html in layers.items():
    src = S / f"{name}.html"
    src.write_text(BASE + html + "</body></html>", encoding="utf-8")
    png = S / f"{name}_full.png"
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", "--default-background-color=00000000", "--window-size=2160,2160",
                    "--virtual-time-budget=20000", rf"--user-data-dir={os.environ['TEMP']}\edgeshot2",
                    f"--screenshot={png}", src.as_uri()], check=True)
    wait_file(png)
    im = Image.open(png).convert("RGBA")
    box = im.getchannel("A").getbbox()
    im.crop(box).save(S / f"{name}.png")
    pos[name] = {"left": box[0], "top": box[1], "width": box[2] - box[0], "height": box[3] - box[1]}
    png.unlink()
(S / "layers.json").write_text(json.dumps(pos, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(pos, ensure_ascii=False))
