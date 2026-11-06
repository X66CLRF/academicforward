"""ตรวจระยะห่าง สมมาตร และขนาดพระเอกของชั้นงานก่อนส่งขึ้น Canva
กติกา: ../canva-handover.md ข้อ 4 + ../owner-design-principles.md ข้อ 5, 8

ตัวอย่างที่ถูก:
    py -X utf8 Designing/scripts/check_layers.py <โฟลเดอร์ layers> --page 2160 --unit 24 ^
        --pages "title,chip,sticker|frame2,photo2,num2" ^
        --center "title,chip,frame2,photo2" ^
        --hero "photo2,frame2" ^
        --equal-width "logo_row=title" ^
        --row "chip1,chip2,chip3"

อ่าน layers.json ({ชื่อ: {left, top, width, height}}) ที่สคริปต์แยกชั้นเขียนไว้
ตรวจ 6 ด่าน:
1. ขอบปลอดภัย (6 หน่วย = 144px บนหน้า 2160)
2. การซ้อนทับและระยะห่างแนวตั้ง (≥ 2 หน่วย ในกลุ่ม)
3. ขนาดภาพพระเอก (--hero กว้างหรือสูง ≥ 55% ของหน้า ตามหลักการข้อ 5)
4. ความสมมาตรซ้าย-ขวา (--center ขอบซ้ายและขวาต่างกัน ≤ 8px ตามหลักการข้อ 8)
5. ความกว้างคู่ขนาน (--equal-width "a=b") และแถวแนวนอน (--row "c1,c2,c3" เส้นฐานตรงกัน + ช่องไฟเท่ากัน)
6. ขอบใสแฝงในไฟล์ PNG (เทียบขนาดไฟล์ .png จริงกับกรอบ alpha)
exit 1 เมื่อมีปัญหา
"""
import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None


def fail_usage(msg: str) -> None:
    sys.stderr.write(
        f"[check_layers.py:{sys._getframe(1).f_lineno}] {msg}\n"
        "ตัวอย่างที่ถูก: py -X utf8 Designing/scripts/check_layers.py %TEMP%\\w\\layers --page 2160 --pages \"title,chip|frame2,photo2\"\n"
    )
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--page", type=int, default=2160)
    ap.add_argument("--unit", type=int, default=24)
    ap.add_argument("--skip", default="topo,ring,dots,shadow,logo-tab,pattern")
    ap.add_argument("--pages", default="")
    ap.add_argument("--center", default="title,chip,frame,cover,photo",
                    help="คำนำหน้าชื่อชิ้นที่ต้องอยู่กึ่งกลางแนวนอน (คั่นด้วย ,)")
    ap.add_argument("--hero", default="cover,photo,frame,hero",
                    help="คำนำหน้าชื่อชิ้นพระเอกที่ต้องใหญ่ ≥ 55%% ของหน้า")
    ap.add_argument("--hero-min", type=float, default=0.55,
                    help="สัดส่วนต่ำสุดของชิ้นพระเอกเทียบกับหน้า (ค่าเริ่มต้น 0.55)")
    ap.add_argument("--equal-width", default="",
                    help="คู่ชิ้นที่ต้องกว้างเท่ากัน เช่น logo_row=title,th_name=en_name")
    ap.add_argument("--row", action="append", default=[],
                    help="กลุ่มชิ้นที่เรียงแนวนอนแถวเดียวกัน เช่น --row chip1,chip2,chip3")
    a = ap.parse_args()

    folder = Path(a.folder)
    json_path = folder / "layers.json"
    if not json_path.exists():
        alt = folder / "layers_games.json"
        if alt.exists():
            json_path = alt
        else:
            fail_usage(f"ไม่พบไฟล์ {json_path} หรือ {alt}")

    pos = json.loads(json_path.read_text(encoding="utf-8-sig"))
    skip = [s for s in a.skip.split(",") if s]
    center_prefixes = [s for s in a.center.split(",") if s]
    hero_prefixes = [s for s in a.hero.split(",") if s]
    safe, min_gap = 6 * a.unit, 2 * a.unit
    row_members = {x.strip() for r in a.row for x in r.split(",") if x.strip()}
    pages = [p.split(",") for p in a.pages.split("|")] if a.pages else [list(pos)]
    problems = 0

    for page_idx, names in enumerate(pages, 1):
        items = {n: pos[n] for n in names if n in pos and not any(n.startswith(s) for s in skip)}
        if not items:
            continue

        # 1. ขอบปลอดภัย
        for n, b in items.items():
            r, btm = b["left"] + b["width"], b["top"] + b["height"]
            if b["left"] < safe or b["top"] < safe or r > a.page - safe or btm > a.page - safe:
                print(
                    f"[check_layers.py:86] ขอบ  (หน้า {page_idx}) {n}: "
                    f"ซ้าย={b['left']} บน={b['top']} ขวา={a.page - r} ล่าง={a.page - btm} "
                    f"(ต้อง ≥ {safe}px · ตัวอย่างแก้: left={max(safe, min(b['left'], a.page - safe - b['width']))})"
                )
                problems += 1

        # 2. ซ้อนทับและระยะห่างแนวตั้ง
        ordered = sorted(items.items(), key=lambda kv: kv[1]["top"])
        for i, (n1, b1) in enumerate(ordered):
            for n2, b2 in ordered[i + 1:]:
                x_overlap = min(b1["left"] + b1["width"], b2["left"] + b2["width"]) - max(b1["left"], b2["left"])
                if x_overlap <= 0:
                    continue
                gap = b2["top"] - (b1["top"] + b1["height"])
                if gap < 0:
                    print(
                        f"[check_layers.py:102] ซ้อน (หน้า {page_idx}) {n1} ↔ {n2}: "
                        f"ทับกัน {-gap}px (ถ้าตั้งใจซ้อนให้เพิ่มใน --skip · ถ้าไม่ตั้งใจให้ขยับ {n2}.top เป็น {b1['top'] + b1['height'] + min_gap})"
                    )
                    problems += 1
                elif gap < min_gap:
                    print(
                        f"[check_layers.py:108] เบียด (หน้า {page_idx}) {n1} ↔ {n2}: "
                        f"ห่าง {gap}px (ต้อง ≥ {min_gap}px ในกลุ่ม · ตัวอย่างแก้: {n2}.top={b1['top'] + b1['height'] + min_gap})"
                    )
                    problems += 1
                else:
                    print(f"ok   (หน้า {page_idx}) {n1} ↔ {n2}: ห่าง {gap}px")
                break

        # 3. ขนาดพระเอก (owner-design-principles ข้อ 5: ภาพหลัก ≥ 55% ของหน้า)
        heroes = {n: b for n, b in items.items() if any(n.startswith(p) for p in hero_prefixes)}
        if heroes:
            biggest_name, biggest_box = max(heroes.items(), key=lambda kv: max(kv[1]["width"], kv[1]["height"]))
            span = max(biggest_box["width"], biggest_box["height"])
            min_span = round(a.page * a.hero_min)
            if span < min_span:
                print(
                    f"[check_layers.py:124] เล็ก (หน้า {page_idx}) พระเอก '{biggest_name}' ขนาด {biggest_box['width']}x{biggest_box['height']}px "
                    f"(ด้านยาวสุด {span}px < {min_span}px หรือ {int(a.hero_min * 100)}% ของหน้า · ตัวอย่างแก้: ขยายกรอบ/ภาพเป็น ≥ {min_span}px)"
                )
                problems += 1
            else:
                print(f"ok   (หน้า {page_idx}) พระเอก '{biggest_name}': {biggest_box['width']}x{biggest_box['height']}px ({span * 100 // a.page}% ของหน้า)")

        # 4. สมมาตรซ้าย-ขวา (owner-design-principles ข้อ 8: ระยะซ้าย=ขวา · ยกเว้นชิ้นที่อยู่ใน --row ซึ่งตรวจกึ่งกลางทั้งแถวแทน)
        for n, b in items.items():
            if n not in row_members and any(n.startswith(p) for p in center_prefixes):
                left_margin = b["left"]
                right_margin = a.page - (b["left"] + b["width"])
                diff = abs(left_margin - right_margin)
                if diff > 8:
                    ideal_left = (a.page - b["width"]) // 2
                    print(
                        f"[check_layers.py:140] เอียง (หน้า {page_idx}) {n}: "
                        f"ขอบซ้าย={left_margin}px ขอบขวา={right_margin}px (ต่างกัน {diff}px > 8px · ตัวอย่างแก้: left={ideal_left})"
                    )
                    problems += 1

    # 5A. ความกว้างคู่ขนาน (--equal-width "logo_row=title")
    if a.equal_width:
        for pair in a.equal_width.split(","):
            if "=" not in pair:
                continue
            k1, k2 = [x.strip() for x in pair.split("=", 1)]
            if k1 in pos and k2 in pos:
                w1, w2 = pos[k1]["width"], pos[k2]["width"]
                if abs(w1 - w2) > 8:
                    print(
                        f"[check_layers.py:155] กว้างไม่เท่า {k1} ({w1}px) ≠ {k2} ({w2}px): "
                        f"ต่างกัน {abs(w1 - w2)}px (หลักการข้อ 8 ต้องกว้างเท่ากัน ±8px · ตัวอย่างแก้: ปรับขนาด {k2} คูณ {w1 / max(1, w2):.3f})"
                    )
                    problems += 1
                else:
                    print(f"ok   กว้างเท่ากัน {k1} ({w1}px) ≈ {k2} ({w2}px)")

    # 5B. แถวแนวนอน (--row "chip1,chip2,chip3")
    for row_spec in a.row:
        rnames = [x.strip() for x in row_spec.split(",") if x.strip() in pos]
        if len(rnames) < 2:
            continue
        rboxes = [pos[n] for n in rnames]
        tops = [b["top"] for b in rboxes]
        heights = [b["height"] for b in rboxes]
        if max(tops) - min(tops) > 4 or max(heights) - min(heights) > 4:
            print(
                f"[check_layers.py:172] เส้นฐานแถว {rnames}: top={tops} height={heights} "
                f"(ต่างกันเกิน 4px · ตัวอย่างแก้: ตั้ง top={tops[0]}, height={heights[0]} ทุกชิ้นในแถว)"
            )
            problems += 1
        gaps = [rboxes[i + 1]["left"] - (rboxes[i]["left"] + rboxes[i]["width"]) for i in range(len(rboxes) - 1)]
        if len(gaps) > 1 and max(gaps) - min(gaps) > 4:
            print(
                f"[check_layers.py:179] ช่องไฟแถว {rnames}: ห่าง {gaps}px ไม่เท่ากัน "
                f"(ตัวอย่างแก้: ใช้ช่องไฟ {a.unit}px เท่ากันทุกคู่)"
            )
            problems += 1
        row_left = rboxes[0]["left"]
        row_right = a.page - (rboxes[-1]["left"] + rboxes[-1]["width"])
        if abs(row_left - row_right) > 8:
            total_w = (rboxes[-1]["left"] + rboxes[-1]["width"]) - rboxes[0]["left"]
            ideal_start = (a.page - total_w) // 2
            print(
                f"[check_layers.py:189] แถวไม่อยู่กลาง {rnames}: ซ้าย={row_left}px ขวา={row_right}px "
                f"(ตัวอย่างแก้: เริ่มชิ้นแรกที่ left={ideal_start})"
            )
            problems += 1

    # 6. ตรวจขอบใสแฝงในไฟล์ PNG (หลักการข้อ 8: PNG โลโก้/ข้อความมีขอบแฝง)
    if Image is not None:
        for n, b in pos.items():
            if any(n.startswith(s) for s in skip):
                continue
            png_file = folder / f"{n}.png"
            if not png_file.exists():
                continue
            im = Image.open(png_file).convert("RGBA")
            alpha_bb = im.getchannel("A").getbbox()
            if not alpha_bb:
                continue
            vis_w, vis_h = alpha_bb[2] - alpha_bb[0], alpha_bb[3] - alpha_bb[1]
            pad_w, pad_h = im.width - vis_w, im.height - vis_h
            if pad_w > 8 or pad_h > 8:
                print(
                    f"[check_layers.py:210] ขอบใสแฝง {png_file.name}: ขนาดไฟล์ {im.width}x{im.height}px "
                    f"แต่เนื้อภาพจริง {vis_w}x{vis_h}px (มีขอบใสเกิน {pad_w}x{pad_h}px · ตัวอย่างแก้: im.crop(im.getchannel('A').getbbox()))"
                )
                problems += 1

    print("ผ่านครบทุกด่าน" if not problems else f"พบ {problems} จุด — แก้ก่อน commit ลง Canva")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()

