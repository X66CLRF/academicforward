"""ตรวจด่าน Canva แยกชั้น (ข้อ 0) และดึงค่าหน้าที่เจ้าของแก้ใน Canva (✓ / v2) กลับเป็นแม่แบบโค้ด
กติกา: ../canva-handover.md ข้อ 0, 1.1 + ../owner-design-principles.md ข้อ 1, 2, 3, 5, 7, 8

ตัวอย่างที่ถูก:
  1) ตรวจด่านก่อนส่งลิงก์ให้ผู้ใช้:
     py -X utf8 Designing/scripts/canva_sync_template.py audit canva_pages.json --page-size 2160

  2) เทียบหน้าที่เจ้าของแก้ (v2 / ✓) กับหน้าร่างเดิม (v1) หรือ layers.json แล้วออกตาราง .md + โค้ด .py:
     py -X utf8 Designing/scripts/canva_sync_template.py sync canva_pages.json --before-layers layers.json --out-md owner-fixed.md
     py -X utf8 Designing/scripts/canva_sync_template.py sync canva_pages.json --before-page 0 --after-page 1
"""
import argparse
import json
import sys
from pathlib import Path


def fail_usage(msg: str) -> None:
    sys.stderr.write(
        f"[canva_sync_template.py:{sys._getframe(1).f_lineno}] {msg}\n"
        "ตัวอย่างที่ถูก: py -X utf8 Designing/scripts/canva_sync_template.py audit canva_pages.json --page-size 2160\n"
    )
    sys.exit(2)


def load_pages(path: Path) -> list[dict]:
    if not path.exists():
        fail_usage(f"ไม่พบไฟล์ JSON: {path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "pages" in data and isinstance(data["pages"], list):
            return data["pages"]
        if "design" in data and isinstance(data["design"], dict) and "pages" in data["design"]:
            return data["design"]["pages"]
    fail_usage(f"รูปแบบ JSON ใน {path} ไม่มีคีย์ 'pages' ที่เป็นรายการหน้า")
    return []


def norm_el(el: dict, idx: int) -> dict:
    """แปลง element จาก Canva transaction JSON ให้มีคีย์มาตรฐาน"""
    pos = el.get("position") or el.get("bounds") or {}
    left = round(el.get("left", pos.get("left", pos.get("x", 0))))
    top = round(el.get("top", pos.get("top", pos.get("y", 0))))
    width = round(el.get("width", pos.get("width", pos.get("w", 0))))
    height = round(el.get("height", pos.get("height", pos.get("h", 0))))
    etype = str(el.get("type", el.get("kind", "element"))).lower()
    text = el.get("text", el.get("richtext", ""))
    if isinstance(text, dict):
        text = text.get("text", "")
    fmt = el.get("format") or el.get("style") or {}
    return {
        "id": el.get("id", el.get("element_id", f"el_{idx}")),
        "label": el.get("label") or el.get("name") or (str(text).strip()[:20] if text else f"{etype}_{idx}"),
        "type": etype,
        "left": left,
        "top": top,
        "width": width,
        "height": height,
        "opacity": el.get("opacity", fmt.get("opacity", 1.0)),
        "text": str(text).strip() if text else "",
        "font_size": el.get("font_size", fmt.get("font_size", fmt.get("fontSize"))),
        "font_weight": el.get("font_weight", fmt.get("font_weight", fmt.get("fontWeight"))),
        "color": el.get("color", fmt.get("color")),
    }


def cmd_audit(pages: list[dict], page_size: int, require_text: bool) -> int:
    problems = 0
    for p_idx, p in enumerate(pages):
        title = p.get("title") or p.get("name") or f"หน้า {p_idx + 1}"
        raw_els = p.get("elements") or p.get("children") or []
        els = [norm_el(e, i) for i, e in enumerate(raw_els)]

        # 1. กฎเหล็กข้อ 0: ห้ามส่งภาพแบนรูปเดียวทั้งหน้า
        if len(els) <= 1:
            print(
                f"[canva_sync_template.py:81] ภาพแบน ({title}): มีเพียง {len(els)} ชิ้นในหน้า "
                f"(กฎข้อ 0 ต้องแยกชั้น พื้น/ลาย/กรอบ/รูป/ข้อความ · ตัวอย่างแก้: รันสคริปต์แยกชั้นแล้ว insert_fill ทีละชิ้น)"
            )
            problems += 1
            continue

        # 2. ตรวจชั้นเต็มหน้า (ลายพื้นหลังต้อง opacity 0.18-0.25 ตามหลักการข้อ 2)
        full_bleeds = [
            e for e in els
            if e["width"] >= page_size * 0.95 and e["height"] >= page_size * 0.95 and e["type"] not in ("background", "shape_bg")
        ]
        for fb in full_bleeds:
            op = float(fb["opacity"]) if fb["opacity"] is not None else 1.0
            if op > 0.28:
                print(
                    f"[canva_sync_template.py:96] ลายทึบเกิน ({title} -> {fb['label']}): opacity={op:.2f} "
                    f"(หลักการข้อ 2 ฉากหลังต้องจาง opacity 0.18–0.25 · ตัวอย่างแก้: ตั้ง opacity=0.22 ตอน insert_fill)"
                )
                problems += 1

        # 3. ตรวจขนาดภาพพระเอก (หลักการข้อ 5: กว้างหรือสูง ≥ 55% ของหน้า)
        non_bg = [
            e for e in els
            if not (e["width"] >= page_size * 0.95 and e["height"] >= page_size * 0.95)
            and e["type"] not in ("text", "richtext")
        ]
        if non_bg:
            hero = max(non_bg, key=lambda e: max(e["width"], e["height"]))
            span = max(hero["width"], hero["height"])
            min_span = round(page_size * 0.55)
            if span < min_span:
                print(
                    f"[canva_sync_template.py:113] พระเอกเล็ก ({title} -> {hero['label']}): {hero['width']}x{hero['height']}px "
                    f"(< {min_span}px หรือ 55% ของหน้า · ตัวอย่างแก้: ขยายเป็น ≥ {min_span}px ตามเทมเพลต v2)"
                )
                problems += 1

        # 4. ตรวจข้อความจริงและขนาดฟอนต์ (กฎข้อ 0 + หลักการข้อ 3: ข้อความอ่าน ≥ 54px)
        text_els = [e for e in els if e["text"] or e["type"] in ("text", "richtext")]
        if require_text and not text_els:
            print(
                f"[canva_sync_template.py:123] ไม่มีข้อความจริง ({title}): ไม่พบ text element ที่แก้ไขได้ "
                f"(กฎข้อ 0 ข้อมูล/ชิปต้องเป็น text element · ตัวอย่างแก้: ใช้ add_text + format_text)"
            )
            problems += 1
        for te in text_els:
            fs = te.get("font_size")
            if fs is not None and float(fs) < 54 and page_size >= 2000:
                print(
                    f"[canva_sync_template.py:131] ฟอนต์เล็ก ({title} -> '{te['text'][:18]}'): font_size={fs}px "
                    f"(หลักการข้อ 3 บนหน้า 2160 ต้อง ≥ 54px ตัวหนา · ตัวอย่างแก้: format_text font_size=54, font_weight='bold')"
                )
                problems += 1

        print(f"ok   ตรวจหน้า '{title}': {len(els)} ชิ้น ({len(text_els)} ข้อความจริง)")

    print("ผ่านด่าน Canva ครบทุกข้อ" if not problems else f"พบ {problems} จุด — แก้ก่อนส่งลิงก์ให้ผู้ใช้")
    return 1 if problems else 0


def cmd_sync(pages: list[dict], before_layers: str, before_page: int | None, after_page: int | None, out_md: str) -> int:
    # เลือกหน้าต้นแบบที่เจ้าของแก้ (มี ✓ หรือ v2 ในชื่อหน้า หรือระบุ --after-page)
    target_idx = after_page
    if target_idx is None:
        for i, p in enumerate(pages):
            t = str(p.get("title") or p.get("name") or "")
            if "✓" in t or "v2" in t.lower():
                target_idx = i
                break
    if target_idx is None:
        target_idx = len(pages) - 1

    if target_idx < 0 or target_idx >= len(pages):
        fail_usage(f"ไม่พบหน้าลำดับ {target_idx} (มีทั้งหมด {len(pages)} หน้า)")

    after_p = pages[target_idx]
    after_title = after_p.get("title") or after_p.get("name") or f"หน้า {target_idx + 1}"
    after_els = [norm_el(e, i) for i, e in enumerate(after_p.get("elements") or after_p.get("children") or [])]

    before_map: dict[str, dict] = {}
    if before_layers:
        lp = Path(before_layers)
        if not lp.exists():
            fail_usage(f"ไม่พบไฟล์ --before-layers: {lp}")
        raw_pos = json.loads(lp.read_text(encoding="utf-8-sig"))
        for k, v in raw_pos.items():
            before_map[k] = {
                "left": v.get("left", 0),
                "top": v.get("top", 0),
                "width": v.get("width", 0),
                "height": v.get("height", 0),
                "opacity": v.get("opacity", 1.0),
            }
    elif before_page is not None and 0 <= before_page < len(pages):
        bp = pages[before_page]
        for i, e in enumerate(bp.get("elements") or bp.get("children") or []):
            ne = norm_el(e, i)
            before_map[ne["label"]] = ne

    lines = [
        f"# แม่แบบจากหน้าที่เจ้าของแก้: {after_title}",
        "",
        "| ชั้น / ชิ้น | ค่าที่เจ้าของตั้ง (x, y, w×h) | ค่าเดิมของเอเจนต์ | การเปลี่ยนแปลง |",
        "| :--- | :--- | :--- | :--- |",
    ]
    py_dict = {}

    for e in after_els:
        lbl = e["label"]
        cur_str = f"`({e['left']}, {e['top']})` ขนาด `{e['width']}×{e['height']}`"
        if e.get("opacity") not in (None, 1, 1.0):
            cur_str += f" opacity `{e['opacity']}`"
        if e.get("font_size"):
            cur_str += f" ฟอนต์ `{e['font_size']}px`"

        old = before_map.get(lbl)
        if old:
            old_str = f"`({old['left']}, {old['top']})` ขนาด `{old['width']}×{old['height']}`"
            diffs = []
            if abs(e["left"] - old["left"]) > 2 or abs(e["top"] - old["top"]) > 2:
                diffs.append(f"ย้าย Δ({e['left'] - old['left']:+d}, {e['top'] - old['top']:+d})")
            if abs(e["width"] - old["width"]) > 2 or abs(e["height"] - old["height"]) > 2:
                diffs.append(f"ปรับขนาด Δ({e['width'] - old['width']:+d}×{e['height'] - old['height']:+d})")
            if e.get("opacity") != old.get("opacity") and e.get("opacity") is not None:
                diffs.append(f"opacity → {e['opacity']}")
            diff_str = " · ".join(diffs) if diffs else "คงเดิม"
        else:
            old_str = "— (ไม่มี/ไม่ตรงชื่อ)"
            diff_str = "ชิ้นใหม่/เปลี่ยนชื่อ"

        lines.append(f"| {lbl} | {cur_str} | {old_str} | {diff_str} |")
        py_dict[lbl] = {
            "left": e["left"],
            "top": e["top"],
            "width": e["width"],
            "height": e["height"],
            **({"opacity": e["opacity"]} if e.get("opacity") not in (None, 1, 1.0) else {}),
            **({"font_size": e["font_size"]} if e.get("font_size") else {}),
        }

    lines.extend([
        "",
        "## โค้ดพิกัดสำหรับวางใน `templates/*.py`",
        "",
        "```python",
        f"OWNER_FIXED_POS = {json.dumps(py_dict, ensure_ascii=False, indent=4)}",
        "```",
    ])
    report = "\n".join(lines) + "\n"
    print(report)
    if out_md:
        Path(out_md).write_text(report, encoding="utf-8")
        print(f"บันทึกตารางแม่แบบลง {out_md} เรียบร้อย")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_audit = sub.add_parser("audit", help="ตรวจด่าน Canva แยกชั้น + opacity + ขนาดพระเอก + ฟอนต์")
    p_audit.add_argument("json_file")
    p_audit.add_argument("--page-size", type=int, default=2160)
    p_audit.add_argument("--no-require-text", action="store_true")

    p_sync = sub.add_parser("sync", help="ดึงค่าหน้าที่เจ้าของแก้ (✓ / v2) เทียบกับค่าเดิมออกเป็นตาราง .md + โค้ด .py")
    p_sync.add_argument("json_file")
    p_sync.add_argument("--before-layers", default="")
    p_sync.add_argument("--before-page", type=int, default=None)
    p_sync.add_argument("--after-page", type=int, default=None)
    p_sync.add_argument("--out-md", default="")

    a = ap.parse_args()
    pages = load_pages(Path(a.json_file))
    if a.cmd == "audit":
        sys.exit(cmd_audit(pages, a.page_size, not a.no_require_text))
    elif a.cmd == "sync":
        sys.exit(cmd_sync(pages, a.before_layers, a.before_page, a.after_page, a.out_md))


if __name__ == "__main__":
    main()
