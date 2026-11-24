"""Generate an editable 1-page A4 Portrait infographic (.pptx) for Canva import.

Usage:
    py -X utf8 a4-article-pptx.py --spec article.json --out out.pptx --theme navy-amber
    py -X utf8 a4-article-pptx.py --demo --out demo-a4.pptx --theme editorial-warm
"""
import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

THEMES = {
    "navy-amber": {
        "bg": RGBColor(0xFB, 0xF8, 0xF3),
        "primary": RGBColor(0x16, 0x2B, 0x49),
        "secondary": RGBColor(0x0D, 0x94, 0x88),
        "accent": RGBColor(0xD9, 0x77, 0x06),
        "accent2": RGBColor(0x25, 0x63, 0xEB),
        "pill_bg": RGBColor(0xE6, 0xF4, 0xF1),
        "card_bg": RGBColor(0xFF, 0xFF, 0xFF),
        "border": RGBColor(0xCB, 0xD5, 0xE1),
        "text": RGBColor(0x33, 0x41, 0x55),
        "muted": RGBColor(0x64, 0x74, 0x8B),
        "row_alt": RGBColor(0xF8, 0xFA, 0xFC),
        "warn_bg": RGBColor(0xFE, 0xF2, 0xF2),
        "warn_border": RGBColor(0xFE, 0xCA, 0xCA),
        "warn_text": RGBColor(0x99, 0x1B, 0x1B),
    },
    "editorial-warm": {
        "bg": RGBColor(0xFA, 0xF6, 0xF0),
        "primary": RGBColor(0x6D, 0x3B, 0x2E),
        "secondary": RGBColor(0x58, 0x59, 0x37),
        "accent": RGBColor(0xB4, 0x53, 0x09),
        "accent2": RGBColor(0x8B, 0x5E, 0x3C),
        "pill_bg": RGBColor(0xEF, 0xE9, 0xE4),
        "card_bg": RGBColor(0xFF, 0xFF, 0xFF),
        "border": RGBColor(0xE2, 0xD9, 0xD0),
        "text": RGBColor(0x3F, 0x3A, 0x36),
        "muted": RGBColor(0x78, 0x71, 0x6C),
        "row_alt": RGBColor(0xF7, 0xF3, 0xEE),
        "warn_bg": RGBColor(0xFE, 0xF2, 0xF2),
        "warn_border": RGBColor(0xFE, 0xCA, 0xCA),
        "warn_text": RGBColor(0x99, 0x1B, 0x1B),
    },
    "sage-minimal": {
        "bg": RGBColor(0xF6, 0xF9, 0xF6),
        "primary": RGBColor(0x1E, 0x3A, 0x2F),
        "secondary": RGBColor(0x2F, 0x6B, 0x55),
        "accent": RGBColor(0xCA, 0x8A, 0x04),
        "accent2": RGBColor(0x0F, 0x76, 0x6E),
        "pill_bg": RGBColor(0xE3, 0xF1, 0xE8),
        "card_bg": RGBColor(0xFF, 0xFF, 0xFF),
        "border": RGBColor(0xCC, 0xDC, 0xD2),
        "text": RGBColor(0x2D, 0x3A, 0x34),
        "muted": RGBColor(0x5F, 0x72, 0x69),
        "row_alt": RGBColor(0xF2, 0xF7, 0xF4),
        "warn_bg": RGBColor(0xFF, 0xF7, 0xED),
        "warn_border": RGBColor(0xFE, 0xD7, 0xAA),
        "warn_text": RGBColor(0x9A, 0x34, 0x12),
    },
    "coral-modern": {
        "bg": RGBColor(0xFD, 0xF8, 0xF6),
        "primary": RGBColor(0x2D, 0x2A, 0x4A),
        "secondary": RGBColor(0xE1, 0x61, 0x62),
        "accent": RGBColor(0xD9, 0x77, 0x06),
        "accent2": RGBColor(0x4F, 0x46, 0xE5),
        "pill_bg": RGBColor(0xFD, 0xEA, 0xE8),
        "card_bg": RGBColor(0xFF, 0xFF, 0xFF),
        "border": RGBColor(0xE5, 0xDC, 0xDA),
        "text": RGBColor(0x36, 0x33, 0x47),
        "muted": RGBColor(0x6E, 0x6A, 0x80),
        "row_alt": RGBColor(0xFA, 0xF5, 0xF4),
        "warn_bg": RGBColor(0xFE, 0xF2, 0xF2),
        "warn_border": RGBColor(0xFE, 0xCA, 0xCA),
        "warn_text": RGBColor(0x99, 0x1B, 0x1B),
    },
}

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT_HEAD = "Kanit"
FONT_BODY = "Sarabun"


def add_rounded_box(slide, left, top, width, height, fill_color, border_color=None, radius=0.06):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.adjustments[0] = radius
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.2)
    else:
        shape.line.fill.background()
    return shape


def add_text_box(slide, left, top, width, height, text, font_name=FONT_BODY, font_size=11,
                 bold=False, color=None, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(4)
    tf.margin_right = Pt(4)
    tf.margin_top = Pt(2)
    tf.margin_bottom = Pt(2)
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    return tb


def build_a4_infographic(spec: dict, out_path: Path, theme_name: str = "navy-amber") -> None:
    if theme_name not in THEMES:
        raise ValueError(f"Unknown theme '{theme_name}'. Choose from: {', '.join(THEMES)}")
    t = THEMES[theme_name]

    prs = Presentation()
    prs.slide_width = Inches(8.268)   # A4 Portrait 210mm
    prs.slide_height = Inches(11.693) # A4 Portrait 297mm
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = t["bg"]

    margin = Inches(0.55)
    content_w = prs.slide_width - (margin * 2)

    # Top pill badge
    pill = add_rounded_box(slide, margin, Inches(0.48), Inches(3.1), Inches(0.34), t["pill_bg"], t["secondary"], radius=0.5)
    ptf = pill.text_frame
    ptf.vertical_anchor = MSO_ANCHOR.MIDDLE
    pp = ptf.paragraphs[0]
    pp.alignment = PP_ALIGN.CENTER
    pr = pp.add_run()
    pr.text = spec.get("badge", "คู่มือผู้ใช้บริการห้องสมุด")
    pr.font.name = FONT_HEAD
    pr.font.size = Pt(10.5)
    pr.font.bold = True
    pr.font.color.rgb = t["secondary"]

    # Optional ARITC logo
    logo_path = Path(__file__).parent / "aritc-logo-transparent.png"
    if logo_path.exists():
        slide.shapes.add_picture(str(logo_path), prs.slide_width - margin - Inches(1.45), Inches(0.44), width=Inches(1.45))

    # Title & Subtitle
    add_text_box(slide, margin, Inches(0.88), Inches(5.6), Inches(0.95),
                 spec["title"], font_name=FONT_HEAD, font_size=25, bold=True, color=t["primary"])
    add_text_box(slide, margin, Inches(1.88), content_w, Inches(0.38),
                 spec.get("subtitle", ""), font_name=FONT_BODY, font_size=11.5, color=t["muted"])

    # Pre-check / Intro callout banner
    precheck = spec.get("callout")
    if precheck:
        add_rounded_box(slide, margin, Inches(2.38), content_w, Inches(0.95), t["card_bg"], t["border"], radius=0.14)
        add_rounded_box(slide, margin, Inches(2.38), Inches(0.1), Inches(0.95), t["secondary"], None, radius=0.0)
        add_text_box(slide, margin + Inches(0.24), Inches(2.46), content_w - Inches(0.4), Inches(0.28),
                     precheck["heading"], font_name=FONT_HEAD, font_size=12, bold=True, color=t["secondary"])
        add_text_box(slide, margin + Inches(0.24), Inches(2.74), content_w - Inches(0.4), Inches(0.52),
                     precheck["body"], font_name=FONT_BODY, font_size=10.5, color=t["text"])

    # 2x2 Step Cards
    steps = spec.get("steps", [])[:4]
    step_colors = [t["primary"], t["secondary"], t["accent"], t["accent2"]]
    gap = Inches(0.22)
    card_w = (content_w - gap) / 2
    card_h = Inches(1.62)
    grid_top = Inches(3.52)

    for idx, step in enumerate(steps):
        col, row = idx % 2, idx // 2
        x = margin + col * (card_w + gap)
        y = grid_top + row * (card_h + gap)
        accent_col = step_colors[idx % len(step_colors)]

        add_rounded_box(slide, x, y, card_w, card_h, t["card_bg"], t["border"], radius=0.12)
        badge = add_rounded_box(slide, x + Inches(0.18), y + Inches(0.16), Inches(1.15), Inches(0.28), accent_col, None, radius=0.5)
        btf = badge.text_frame
        btf.vertical_anchor = MSO_ANCHOR.MIDDLE
        bp = btf.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        br = bp.add_run()
        br.text = step.get("label", f"ขั้นตอนที่ {idx + 1}")
        br.font.name = FONT_HEAD
        br.font.size = Pt(9.5)
        br.font.bold = True
        br.font.color.rgb = WHITE

        add_text_box(slide, x + Inches(0.18), y + Inches(0.50), card_w - Inches(0.36), Inches(0.34),
                     step["heading"], font_name=FONT_HEAD, font_size=12.5, bold=True, color=t["primary"])
        add_text_box(slide, x + Inches(0.18), y + Inches(0.86), card_w - Inches(0.36), Inches(0.66),
                     step["body"], font_name=FONT_BODY, font_size=10.5, color=t["text"])

    # Native Table Section
    tbl_spec = spec.get("table")
    if tbl_spec and tbl_spec.get("rows"):
        add_text_box(slide, margin, Inches(7.08), content_w, Inches(0.34),
                     tbl_spec.get("title", "ตารางสรุปข้อมูล"), font_name=FONT_HEAD, font_size=13, bold=True, color=t["primary"])
        rows_data = tbl_spec["rows"]
        n_rows = len(rows_data)
        n_cols = len(rows_data[0])
        tbl_shape = slide.shapes.add_table(n_rows, n_cols, margin, Inches(7.46), content_w, Inches(2.55))
        table = tbl_shape.table
        col_widths = tbl_spec.get("col_widths_in")
        if col_widths and len(col_widths) == n_cols:
            for c_i, w_in in enumerate(col_widths):
                table.columns[c_i].width = Inches(w_in)

        for r_idx, row_vals in enumerate(rows_data):
            for c_idx, val in enumerate(row_vals):
                cell = table.cell(r_idx, c_idx)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                cell.margin_left = Inches(0.1)
                cell.margin_right = Inches(0.1)
                cell.margin_top = Inches(0.06)
                cell.margin_bottom = Inches(0.06)
                cell.fill.solid()
                cell.fill.fore_color.rgb = t["primary"] if r_idx == 0 else (t["row_alt"] if r_idx % 2 == 0 else WHITE)

                p = cell.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.LEFT
                run = p.add_run()
                run.text = val
                run.font.name = FONT_HEAD if (r_idx == 0 or c_idx == 1) else FONT_BODY
                run.font.size = Pt(10.5 if r_idx == 0 else 10)
                run.font.bold = (r_idx == 0 or c_idx == 1)
                run.font.color.rgb = WHITE if r_idx == 0 else (t["accent"] if c_idx == 1 else t["text"])

    # Footer Warning + CTA
    footer = spec.get("footer")
    if footer:
        footer_top = Inches(10.28)
        add_rounded_box(slide, margin, footer_top, content_w, Inches(0.92), t["warn_bg"], t["warn_border"], radius=0.14)
        add_text_box(slide, margin + Inches(0.18), footer_top + Inches(0.10), Inches(4.85), Inches(0.74),
                     footer["warning"], font_name=FONT_BODY, font_size=10, bold=True, color=t["warn_text"])
        if footer.get("cta"):
            cta = add_rounded_box(slide, margin + Inches(5.15), footer_top + Inches(0.24), Inches(1.82), Inches(0.42), t["primary"], None, radius=0.5)
            ctf = cta.text_frame
            ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
            cp = ctf.paragraphs[0]
            cp.alignment = PP_ALIGN.CENTER
            cr = cp.add_run()
            cr.text = footer["cta"]
            cr.font.name = FONT_HEAD
            cr.font.size = Pt(10)
            cr.font.bold = True
            cr.font.color.rgb = WHITE

    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    print(f"SAVED: {out_path} (theme={theme_name})")


DEMO_SPEC = {
    "badge": "คู่มือผู้ใช้บริการห้องสมุด · ระบบ ALIST",
    "title": "หนังสือหาย อย่าตกใจ!\nแก้ไขได้ ง่ายนิดเดียว",
    "subtitle": "แนวปฏิบัติการแจ้งและชดใช้ทรัพยากรสารสนเทศสูญหาย · ประกาศ มรนว. พ.ศ. 2565 ข้อ 8 (3)",
    "callout": {
        "heading": "ก่อนแจ้งหาย: เช็กให้ชัวร์ก่อน",
        "body": "ทบทวนจุดอ่านหนังสือ โต๊ะทำงาน หอพัก รถยนต์ส่วนตัว ถามเพื่อนร่วมชั้น และตรวจสอบสถานะบาร์โค้ด/วันกำหนดคืนใน Web OPAC",
    },
    "steps": [
        {"label": "ขั้นตอนที่ 1", "heading": "แจ้งเคาน์เตอร์ยืม-คืนทันที",
         "body": "ติดต่อเจ้าหน้าที่เพื่อบันทึก \"รับแจ้งทรัพยากรหาย\" ในระบบ ALIST ช่วยระงับการสะสมค่าปรับเกินกำหนดได้ทันที"},
        {"label": "ขั้นตอนที่ 2", "heading": "ตรวจสอบเกณฑ์ชดใช้ พ.ศ. 2565",
         "body": "ชำระตามราคาปก/ราคาตลาด + ค่าเทคนิค 50 บาท (กรณีไม่มีราคา: คิดหน้าละ 1 บาท + ค่าเทคนิค 50 บาท)"},
        {"label": "ขั้นตอนที่ 3", "heading": "ชำระค่าปรับเกินกำหนด (ถ้ามี)",
         "body": "หากแจ้งหลังเลยกำหนดคืน ชำระวันละ 5 บาท/เล่ม นับถึงวันที่แจ้งหาย (สูงสุดไม่เกินราคาปก)"},
        {"label": "ขั้นตอนที่ 4", "heading": "เคลียร์รายการและคืนสิทธิ",
         "body": "เมื่อชำระครบ เจ้าหน้าที่จะตัดรายการออกจากระบบ ALIST และคืนสถานะสมาชิกกลับมาเป็นปกติ"},
    ],
    "table": {
        "title": "อัตราค่าธรรมเนียมและค่าปรับ (ประกาศ มรนว. พ.ศ. 2565 ข้อ 8 (3))",
        "col_widths_in": [2.35, 2.15, 2.668],
        "rows": [
            ["ประเภทรายการ / กรณี", "อัตราค่าปรับ / ชดใช้", "รายละเอียดและเงื่อนไขเพิ่มเติม"],
            ["ส่งคืนหนังสือเกินกำหนด", "5 บาท / วัน / เล่ม", "สูงสุดไม่เกินราคาปกหนังสือ"],
            ["ทำหนังสือสูญหาย (จ่ายชดใช้)", "ราคาปก + 50 บาท", "ราคาปก หรือราคาตลาดปัจจุบัน + ค่าเทคนิค"],
            ["หนังสือไม่มีราคา", "หน้าละ 1 บาท + 50 บาท", "คำนวณจากจำนวนหน้าทั้งหมด + ค่าเทคนิค"],
            ["นำออกไม่ผ่านการยืม (RFID)", "ปรับ 2 เท่าของมูลค่า", "กรณีตรวจพบที่ประตูสัญญาณ RFID"],
        ],
    },
    "footer": {
        "warning": "ผลกระทบหากนิ่งเฉย: ถูกระงับสิทธิยืมใน ALIST · ค่าปรับวิ่งต่อทุกวันจนชนราคาปก · นักศึกษาปีสุดท้ายไม่ผ่านอนุมัติจบการศึกษา",
        "cta": "ยืมต่อผ่าน Web OPAC",
    },
}


def main():
    parser = argparse.ArgumentParser(description="Build 1-page A4 Portrait infographic PPTX for Canva import")
    parser.add_argument("--spec", type=Path, help="Path to JSON content spec")
    parser.add_argument("--out", type=Path, required=True, help="Output .pptx path")
    parser.add_argument("--theme", default="navy-amber", choices=list(THEMES.keys()), help="Color theme")
    parser.add_argument("--demo", action="store_true", help="Use built-in demo content")
    args = parser.parse_args()

    if args.demo:
        spec = DEMO_SPEC
    elif args.spec:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
    else:
        raise SystemExit("Provide --spec <file.json> or --demo")

    build_a4_infographic(spec, args.out, args.theme)


if __name__ == "__main__":
    main()
