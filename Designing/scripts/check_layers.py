"""ตรวจระยะห่างชั้นงานก่อนส่งขึ้น Canva — กติกา ../canva-handover.md ข้อ 4

    python check_layers.py <โฟลเดอร์ layers> [--page 2160] [--unit 24] [--skip topo,ring,dots,shadow,logo-tab]
                           [--pages "title,chip,sticker|shadow1,cover1,num1"]

อ่าน layers.json ({ชื่อ: {left, top, width, height}}) ที่สคริปต์แยกชั้นเขียนไว้ (กรอบ = ขอบที่มองเห็นจริง เพราะครอปตาม alpha แล้ว)
--pages แบ่งชิ้นเป็นหน้า (คั่นหน้าด้วย |) — ไม่ใส่ = ถือว่าทุกชิ้นอยู่หน้าเดียวกัน
ชิ้นใน --skip (ขึ้นต้นด้วยคำนี้) เป็นของตกแต่ง ล้นขอบได้ ไม่ตรวจ
แจ้ง: ชิ้นที่ล้ำขอบปลอดภัย (6 หน่วย) · คู่ที่ซ้อนกันโดยไม่ได้ตั้งใจ · คู่ที่อยู่แนวเดียวกันแต่ห่างน้อยกว่า 2 หน่วย
exit 1 เมื่อมีปัญหา
"""
import argparse
import json
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--page", type=int, default=2160)
    ap.add_argument("--unit", type=int, default=24)
    ap.add_argument("--skip", default="topo,ring,dots,shadow,logo-tab")
    ap.add_argument("--pages", default="")
    a = ap.parse_args()

    pos = json.loads((Path(a.folder) / "layers.json").read_text(encoding="utf-8"))
    skip = [s for s in a.skip.split(",") if s]
    safe, min_gap = 6 * a.unit, 2 * a.unit
    pages = [p.split(",") for p in a.pages.split("|")] if a.pages else [list(pos)]
    problems = 0

    for names in pages:
        items = {n: pos[n] for n in names if n in pos and not any(n.startswith(s) for s in skip)}
        for n, b in items.items():
            r, btm = b["left"] + b["width"], b["top"] + b["height"]
            if b["left"] < safe or b["top"] < safe or r > a.page - safe or btm > a.page - safe:
                print(f"ขอบ  {n}: ห่างขอบ ซ้าย {b['left']} บน {b['top']} ขวา {a.page - r} ล่าง {a.page - btm} (ต้อง ≥ {safe})")
                problems += 1
        ordered = sorted(items.items(), key=lambda kv: kv[1]["top"])
        for i, (n1, b1) in enumerate(ordered):
            for n2, b2 in ordered[i + 1:]:
                x_overlap = min(b1["left"] + b1["width"], b2["left"] + b2["width"]) - max(b1["left"], b2["left"])
                if x_overlap <= 0:
                    continue
                gap = b2["top"] - (b1["top"] + b1["height"])
                if gap < 0:
                    print(f"ซ้อน {n1} ↔ {n2}: ทับกัน {-gap}px (ตั้งใจ = ใส่ชิ้นล่างใน --skip)")
                    problems += 1
                elif gap < min_gap:
                    print(f"เบียด {n1} ↔ {n2}: ห่าง {gap}px (ต้อง ≥ {min_gap} ในกลุ่ม · ≥ {4 * a.unit} ระหว่างกลุ่ม)")
                    problems += 1
                else:
                    print(f"ok   {n1} ↔ {n2}: {gap}px")
                break  # วัดเฉพาะชิ้นถัดไปที่อยู่ใต้กันจริง
    print("ผ่าน" if not problems else f"พบ {problems} จุด — แก้ก่อน commit ลง Canva")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
