# ย้อมลายจากคลังเป็นโทนพื้นของเทมเพลต + แผ่นเทียบ 6 ลายบนปกจริง (ดู ../content-to-visual.md ข้อ 1 ลำดับ 5)
import importlib.util, random, os, subprocess
from pathlib import Path
from PIL import Image

import sys
S = Path(__file__).parent / "tryout"
S.mkdir(exist_ok=True)
COVER = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "templates" / "layers_boardgame_cover"  # โฟลเดอร์ที่มี layers.json + logo-tab/title/chip.png
spec = importlib.util.spec_from_file_location("bp", str(Path(__file__).with_name("build_patterns.py")))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

# จานสีเทมเพลตฟ้า (พื้น #E8F3F5) — ลายโปร่งใส ไม่มีพื้น
PAL = dict(bg="#E8F3F5", fg="#C9DEE4", fg_op=1.0, acc="#E8913A", acc_op=0.55)
CAND = [("maze", 168, 1), ("memphis", 168, 2), ("cubes", 224, 1), ("bauhaus", 224, 0), ("pixels", 168, 1), ("truchet", 224, 0)]
fam = {slug: fn for slug, _, fn, _ in bp.FAMILIES}
idx = {slug: i for i, (slug, *_r) in enumerate(bp.FAMILIES, 1)}


def svg_for(slug, t, p, fg=None):
    pal = dict(PAL)
    if fg:
        pal["fg"] = fg
    w, h, inner = fam[slug](t, pal, random.Random(idx[slug] * 10 + p), p)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2160 2160" width="2160" height="2160">'
            f'<defs><pattern id="p" width="{bp.f2(w * 2160 / 1200)}" height="{bp.f2(h * 2160 / 1200)}" patternUnits="userSpaceOnUse" '
            f'patternTransform="scale({2160 / 1200 / (2160 / 1200)})">'
            f'<g transform="scale({2160 / 1200})">{inner}</g></pattern></defs><rect width="100%" height="100%" fill="url(#p)"/></svg>')


if __name__ == "__main__":
    EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    out = []
    for slug, t, p in CAND:
        f = S / f"pat_{slug}.svg"
        f.write_text(svg_for(slug, t, p), encoding="utf-8")
        html = S / f"pat_{slug}.html"
        html.write_text(f'<html><body style="margin:0;background:transparent"><img src="{f.name}" width=2160 height=2160></body></html>', encoding="utf-8")
        png = S / f"pat_{slug}.png"
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--allow-file-access-from-files", "--default-background-color=00000000", "--window-size=2160,2160",
                        "--virtual-time-budget=8000", rf"--user-data-dir={os.environ['TEMP']}\edgeshot3", f"--screenshot={png}", html.as_uri()], check=True)
        import time
        time.sleep(1)
        out.append(slug)
    sheet = Image.new("RGB", (1500, 1000), "white")
    import json
    pos = json.load(open(COVER / "layers.json"))
    for i, slug in enumerate(out):
        base = Image.new("RGBA", (2160, 2160), "#E8F3F5")
        base.alpha_composite(Image.open(S / f"pat_{slug}.png").convert("RGBA"))
        for n in ["logo-tab", "title", "chip"]:
            base.alpha_composite(Image.open(COVER / f"{n}.png"), (pos[n]["left"], pos[n]["top"]))
        sheet.paste(base.convert("RGB").resize((500, 500)), ((i % 3) * 500, (i // 3) * 500))
    sheet.save(S / "pattern_sheet.png")
    print(out)
