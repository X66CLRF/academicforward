#!/usr/bin/env python3
"""สร้างคลังแพทเทิร์นพื้นหลังเวกเตอร์ 100 แบบ (SVG ต้นฉบับ วาดด้วยโค้ด ไม่ได้ก๊อปงานใคร)

25 ตระกูล x 4 แบบ (ขนาดลาย/น้ำหนักเส้นต่างกัน + จานสีหมุนผ่านสไตล์ A-E ของ style-library.md)
ผลลัพธ์: svg/NN-<ตระกูล>-<สไตล์><ขนาด>.svg · index.json · sheet.html (แผ่นเทียบดูทั้ง 100)

ใช้: python build_patterns.py   (stdlib อย่างเดียว ไม่ต้องติดตั้งอะไร)
ทุกลายเป็น <pattern> ต่อกันเนียนทั้ง 4 ด้าน — ย่อ/ขยายได้ไม่แตก อัปขึ้น Canva เป็นพื้นหลังได้ทันที
"""
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "svg"
CANVAS = 1200  # ผืนตัวอย่าง (viewBox) — ลายเป็นเวกเตอร์ ใช้ขนาดไหนก็ได้

# จานสี = สไตล์ A-E ใน style-library.md (สีหน่วยงานจาก design-system/skins/aritc/social-cover.json)
# bg พื้น · fg สีลาย (จางโดยตั้งใจ — ลายต้องเป็นฉากหลัง ไม่แย่งภาพจริง) · acc สีเน้นจุดเล็ก
PALETTES = {
    "A": dict(name="ครีมบรรณาธิการ", bg="#FAF6EC", fg="#E4D7B4", acc="#E8B820"),
    "B": dict(name="กรมท่า-ทอง", bg="#001F5C", fg="#1C418F", acc="#EFC84C"),
    "C": dict(name="ไล่สีเข้ม", bg="#0B1B4D", bg2="#16409A", fg="#FFFFFF", fg_op=0.15, acc="#7EBAEE"),
    "D": dict(name="ครีมอุ่น", bg="#F8ECD8", fg="#EBCBA2", acc="#7A3E8E"),
    "E": dict(name="เทาอ่อน", bg="#EEF0F4", fg="#D3D8E3", acc="#003399"),
}
STYLE_ORDER = ["A", "B", "C", "D", "E"]
SIZES = [("s", 96), ("m", 128), ("l", 168), ("x", 224)]  # ขนาดกระเบื้อง 1 ชิ้น (หน่วย viewBox)


def f2(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- ตระกูลลาย
# แต่ละฟังก์ชันคืน (กว้าง, สูง, svg ข้างใน) ในพิกัดกระเบื้อง · ชิ้นที่ล้นขอบวาดซ้ำที่มุมให้ต่อกันเนียน
# arg: t=ขนาดกระเบื้อง · c=จานสี · r=random ตั้ง seed · p=ดัชนีแบบ 0-3 (ปรับน้ำหนักเส้น)


def dots(t, c, r, p):
    rad = t * (0.05 + 0.012 * p)
    pts = [(0, 0), (t, 0), (0, t), (t, t), (t / 2, t / 2)]
    s = "".join(f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(rad)}" fill="{c["fg"]}" fill-opacity="{c["fg_op"]}"/>' for x, y in pts[:4])
    s += f'<circle cx="{f2(t/2)}" cy="{f2(t/2)}" r="{f2(rad*.8)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/>'
    return t, t, s


def halftone(t, c, r, p):
    n = 4
    cell = t / n
    s = ""
    for i in range(n):
        for j in range(n):
            k = (i + j) % n
            rad = cell * (0.08 + 0.13 * (k / (n - 1))) * (1 + 0.1 * p)
            s += f'<circle cx="{f2(cell*(i+.5))}" cy="{f2(cell*(j+.5))}" r="{f2(rad)}" fill="{c["fg"]}" fill-opacity="{c["fg_op"]}"/>'
    return t, t, s


def plus(t, c, r, p):
    a = t * (0.13 + 0.015 * p)
    w = t * 0.035
    def cross(x, y, col, op):
        return (f'<path d="M{f2(x-a)} {f2(y)}H{f2(x+a)}M{f2(x)} {f2(y-a)}V{f2(y+a)}" stroke="{col}" stroke-opacity="{op}" '
                f'stroke-width="{f2(w)}" stroke-linecap="round" fill="none"/>')
    s = "".join(cross(x, y, c["fg"], c["fg_op"]) for x, y in [(0, 0), (t, 0), (0, t), (t, t)])
    s += cross(t / 2, t / 2, c["fg"], c["fg_op"])
    s += f'<circle cx="{f2(t/2)}" cy="{f2(0)}" r="{f2(w*.8)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/>'
    s += f'<circle cx="{f2(t/2)}" cy="{f2(t)}" r="{f2(w*.8)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/>'
    return t, t, s


def diag(t, c, r, p):
    w = t * (0.03 + 0.012 * p)
    segs = [(-t / 2, t / 2, t / 2, -t / 2), (0, t, t, 0), (t / 2, 3 * t / 2, 3 * t / 2, t / 2)]
    s = ""
    for i, (x1, y1, x2, y2) in enumerate(segs):
        col, op = (c["acc"], c["acc_op"]) if i == 1 and p % 2 else (c["fg"], c["fg_op"])
        s += f'<line x1="{f2(x1)}" y1="{f2(y1)}" x2="{f2(x2)}" y2="{f2(y2)}" stroke="{col}" stroke-opacity="{op}" stroke-width="{f2(w)}"/>'
    return t, t, s


def zigzag(t, c, r, p):
    w = t * (0.04 + 0.01 * p)
    def row(y, col, op):
        pts = " ".join(f"{f2(i*t/4)},{f2(y + (t*.14 if i % 2 else -t*.14))}" for i in range(5))
        return f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{f2(w)}" stroke-linejoin="round"/>'
    return t, t, row(t * .3, c["fg"], c["fg_op"]) + row(t * .78, c["acc"], c["acc_op"])


def _hexverts(cx, cy, s, rot=-90):
    return [(cx + s * math.cos(math.radians(rot + 60 * k)), cy + s * math.sin(math.radians(rot + 60 * k))) for k in range(6)]


def _hexcenters(s):
    w, h = math.sqrt(3) * s, 3 * s
    return w, h, [(0, 0), (w, 0), (0, h), (w, h), (w / 2, h / 2)]


def hexline(t, c, r, p):
    s0 = t * 0.5
    w, h, cs = _hexcenters(s0)
    sw = t * (0.025 + 0.008 * p)
    s = ""
    for cx, cy in cs:
        pts = " ".join(f"{f2(x)},{f2(y)}" for x, y in _hexverts(cx, cy, s0))
        s += f'<polygon points="{pts}" fill="none" stroke="{c["fg"]}" stroke-opacity="{c["fg_op"]}" stroke-width="{f2(sw)}" stroke-linejoin="round"/>'
    s += f'<circle cx="{f2(w/2)}" cy="{f2(h/2)}" r="{f2(sw*1.4)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/>'
    return w, h, s


def cubes(t, c, r, p):
    s0 = t * 0.5
    w, h, cs = _hexcenters(s0)
    s = ""
    for cx, cy in cs:
        v = _hexverts(cx, cy, s0 * .96)
        faces = [([(cx, cy), v[5], v[0], v[1]], .55), ([(cx, cy), v[1], v[2], v[3]], .85), ([(cx, cy), v[3], v[4], v[5]], 1.0)]
        for pts, k in faces:
            ps = " ".join(f"{f2(x)},{f2(y)}" for x, y in pts)
            s += f'<polygon points="{ps}" fill="{c["fg"]}" fill-opacity="{f2(c["fg_op"]*k)}"/>'
    return w, h, s


def seigaiha(t, c, r, p):
    s = ""
    rows = [(0, [0, t]), (t / 2, [t / 2]), (t, [0, t])]
    sw = t * (0.018 + 0.006 * p)
    for y, xs in rows:
        for x in xs:
            for k, rad in enumerate([t * .5, t * .38, t * .26, t * .14]):
                if k == 3:
                    s += f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(rad)}" fill="{c["bg"]}"/>'
                fill = c["bg"] if k < 3 else c["acc"]
                fo = 1 if k < 3 else f2(c["acc_op"] * .4)
                s += (f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(rad)}" fill="{fill}" fill-opacity="{fo}" stroke="{c["fg"]}" stroke-opacity="{c["fg_op"]}" '
                      f'stroke-width="{f2(sw)}"/>')
    return t, t, s


def waves(t, c, r, p):
    a = t * 0.14
    w = t * (0.035 + 0.008 * p)
    def wave(y, col, op):
        return (f'<path d="M0 {f2(y)}Q{f2(t/4)} {f2(y-a*2)} {f2(t/2)} {f2(y)}T{f2(t)} {f2(y)}" fill="none" stroke="{col}" '
                f'stroke-opacity="{op}" stroke-width="{f2(w)}" stroke-linecap="round"/>')
    return t, t, wave(t * .3, c["fg"], c["fg_op"]) + wave(t * .8, c["acc"], c["acc_op"])


def circlelattice(t, c, r, p):
    sw = t * (0.02 + 0.007 * p)
    rad = t / 2
    s = "".join(f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(rad)}" fill="none" stroke="{c["fg"]}" stroke-opacity="{c["fg_op"]}" stroke-width="{f2(sw)}"/>'
                for x, y in [(0, 0), (t, 0), (0, t), (t, t), (t / 2, t / 2)])
    s += f'<circle cx="{f2(t/2)}" cy="{f2(t/2)}" r="{f2(t*.06)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/>'
    return t, t, s


def prajam(t, c, r, p):
    """ตาข่ายขนมเปียกปูนแบบประจำยาม: เส้นทแยงตัดกัน + ดอกสี่กลีบที่จุดตัด"""
    sw = t * (0.018 + 0.006 * p)
    s = (f'<path d="M0 0L{t} {t}M{t} 0L0 {t}" stroke="{c["fg"]}" stroke-opacity="{c["fg_op"]}" stroke-width="{f2(sw)}" fill="none"/>')
    pr, d = t * .05, t * .085
    def flower(x, y):
        o = "".join(f'<circle cx="{f2(x+dx)}" cy="{f2(y+dy)}" r="{f2(pr)}" fill="{c["fg"]}" fill-opacity="{c["fg_op"]}"/>'
                    for dx, dy in [(d, 0), (-d, 0), (0, d), (0, -d)])
        return o + f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(pr*.8)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/>'
    s += "".join(flower(x, y) for x, y in [(t / 2, t / 2), (0, 0), (t, 0), (0, t), (t, t)])
    return t, t, s


def octagons(t, c, r, p):
    sw = t * (0.02 + 0.007 * p)
    R = (t / 2) / math.cos(math.radians(22.5))
    def octo(cx, cy):
        pts = " ".join(f"{f2(cx + R*math.cos(math.radians(22.5+45*k)))},{f2(cy + R*math.sin(math.radians(22.5+45*k)))}" for k in range(8))
        return f'<polygon points="{pts}" fill="none" stroke="{c["fg"]}" stroke-opacity="{c["fg_op"]}" stroke-width="{f2(sw)}" stroke-linejoin="round"/>'
    s = "".join(octo(x, y) for x, y in [(0, 0), (t, 0), (0, t), (t, t)])
    half = t * 0.2929
    cx = cy = t / 2
    s += (f'<polygon points="{f2(cx)},{f2(cy-half)} {f2(cx+half)},{f2(cy)} {f2(cx)},{f2(cy+half)} {f2(cx-half)},{f2(cy)}" '
          f'fill="{c["acc"]}" fill-opacity="{f2(c["acc_op"]*.22)}" stroke="{c["fg"]}" stroke-opacity="{c["fg_op"]}" stroke-width="{f2(sw)}" stroke-linejoin="round"/>')
    return t, t, s


def memphis(t, c, r, p):
    n = 3
    cell = t / n
    s = ""
    kinds = ["squiggle", "ring", "tri", "plus", "dot", "ring", "squiggle", "dot", "tri"]
    r.shuffle(kinds)
    for idx, kind in enumerate(kinds):
        i, j = idx % n, idx // n
        x, y = cell * (i + .5) + r.uniform(-cell * .08, cell * .08), cell * (j + .5) + r.uniform(-cell * .08, cell * .08)
        acc = idx % 4 == 0
        col, op = (c["acc"], c["acc_op"]) if acc else (c["fg"], c["fg_op"])
        w, a = cell * .09, cell * .36
        if kind == "squiggle":
            d = f"M{f2(x-a)} {f2(y)}q{f2(a/2)} {f2(-a)} {f2(a)} 0t{f2(a)} 0"
            s += f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{f2(w)}" stroke-linecap="round"/>'
        elif kind == "ring":
            s += f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(a*.7)}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{f2(w)}"/>'
        elif kind == "tri":
            s += f'<polygon points="{f2(x)},{f2(y-a*.7)} {f2(x+a*.7)},{f2(y+a*.55)} {f2(x-a*.7)},{f2(y+a*.55)}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{f2(w)}" stroke-linejoin="round"/>'
        elif kind == "plus":
            s += f'<path d="M{f2(x-a*.6)} {f2(y)}H{f2(x+a*.6)}M{f2(x)} {f2(y-a*.6)}V{f2(y+a*.6)}" stroke="{col}" stroke-opacity="{op}" stroke-width="{f2(w)}" stroke-linecap="round"/>'
        else:
            s += f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(a*.28)}" fill="{col}" fill-opacity="{op}"/>'
    return t, t, s


def truchet_arcs(t, c, r, p):
    n = 3
    cell = t / n
    sw = cell * (0.2 + 0.03 * p)
    s = ""
    for i in range(n):
        for j in range(n):
            x, y, h = i * cell, j * cell, cell / 2
            if r.random() < .5:
                d = f"M{f2(x+h)} {f2(y)}A{f2(h)} {f2(h)} 0 0 1 {f2(x)} {f2(y+h)}M{f2(x+cell)} {f2(y+h)}A{f2(h)} {f2(h)} 0 0 1 {f2(x+h)} {f2(y+cell)}"
            else:
                d = f"M{f2(x+h)} {f2(y)}A{f2(h)} {f2(h)} 0 0 0 {f2(x+cell)} {f2(y+h)}M{f2(x)} {f2(y+h)}A{f2(h)} {f2(h)} 0 0 0 {f2(x+h)} {f2(y+cell)}"
            s += f'<path d="{d}" fill="none" stroke="{c["fg"]}" stroke-opacity="{c["fg_op"]}" stroke-width="{f2(sw)}" stroke-linecap="butt"/>'
    return t, t, s


def truchet_diag(t, c, r, p):
    n = 4
    cell = t / n
    sw = cell * (0.16 + 0.03 * p)
    s = ""
    for i in range(n):
        for j in range(n):
            x, y = i * cell, j * cell
            a, b = ((x, y), (x + cell, y + cell)) if r.random() < .5 else ((x + cell, y), (x, y + cell))
            col, op = (c["acc"], c["acc_op"]) if r.random() < .12 else (c["fg"], c["fg_op"])
            s += (f'<line x1="{f2(a[0])}" y1="{f2(a[1])}" x2="{f2(b[0])}" y2="{f2(b[1])}" stroke="{col}" stroke-opacity="{op}" '
                  f'stroke-width="{f2(sw)}" stroke-linecap="square"/>')
    return t, t, s


def graph_grid(t, c, r, p):
    w, w2 = t * (0.02 + 0.004 * p), t * 0.01
    s = (f'<path d="M0 0H{t}M0 0V{t}" stroke="{c["fg"]}" stroke-opacity="{c["fg_op"]}" stroke-width="{f2(w)}" fill="none"/>'
         f'<path d="M{f2(t/2)} 0V{t}M0 {f2(t/2)}H{t}" stroke="{c["fg"]}" stroke-opacity="{f2(c["fg_op"]*.55)}" stroke-width="{f2(w2)}" fill="none"/>')
    s += f'<circle cx="0" cy="0" r="{f2(t*.035)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/><circle cx="{t}" cy="{t}" r="{f2(t*.035)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/>'
    return t, t, s


def pixels(t, c, r, p):
    n = 8
    cell = t / n
    g = cell * .12
    s = ""
    for i in range(n):
        for j in range(n):
            v = r.random()
            if v < .42:
                continue
            acc = v > .95
            col, op = (c["acc"], c["acc_op"]) if acc else (c["fg"], c["fg_op"] * (0.5 + 0.5 * r.random()))
            s += f'<rect x="{f2(i*cell+g)}" y="{f2(j*cell+g)}" width="{f2(cell-2*g)}" height="{f2(cell-2*g)}" rx="{f2(cell*.1)}" fill="{col}" fill-opacity="{f2(op)}"/>'
    return t, t, s


def bauhaus(t, c, r, p):
    n = 2
    cell = t / n
    s = ""
    kinds = ["quarter", "half", "circle", "ring"]
    for i in range(n):
        for j in range(n):
            x, y, k = i * cell, j * cell, r.choice(kinds)
            col, op = (c["acc"], c["acc_op"] * .7) if (i, j) == (0, 1) else (c["fg"], c["fg_op"] * (1 if (i + j) % 2 else .6))
            rot = r.choice([0, 90, 180, 270])
            cx, cy = x + cell / 2, y + cell / 2
            g = f'<g transform="rotate({rot} {f2(cx)} {f2(cy)})" fill="{col}" fill-opacity="{op}">'
            h = cell / 2 * .86
            if k == "quarter":
                g += f'<path d="M{f2(cx-h)} {f2(cy+h)}V{f2(cy-h)}A{f2(2*h)} {f2(2*h)} 0 0 1 {f2(cx+h)} {f2(cy+h)}Z"/>'
            elif k == "half":
                g += f'<path d="M{f2(cx-h)} {f2(cy)}A{f2(h)} {f2(h)} 0 0 1 {f2(cx+h)} {f2(cy)}Z"/>'
            elif k == "circle":
                g += f'<circle cx="{f2(cx)}" cy="{f2(cy)}" r="{f2(h*.8)}"/>'
            else:
                g += f'<circle cx="{f2(cx)}" cy="{f2(cy)}" r="{f2(h*.75)}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{f2(h*.3)}"/>'
            s += g + "</g>"
    return t, t, s


def spines(t, c, r, p):
    n = 6
    w = t / n
    s = ""
    for i in range(n):
        hgt = t * r.uniform(.42, .8)
        x = i * w
        acc = i == 2 + p % 2
        col, op = (c["acc"], c["acc_op"] * .7) if acc else (c["fg"], c["fg_op"] * r.uniform(.55, 1))
        s += f'<rect x="{f2(x+w*.08)}" y="{f2(t*.9-hgt)}" width="{f2(w*.84)}" height="{f2(hgt)}" rx="{f2(w*.08)}" fill="{col}" fill-opacity="{f2(op)}"/>'
        s += f'<rect x="{f2(x+w*.08)}" y="{f2(t*.9-hgt+hgt*.12)}" width="{f2(w*.84)}" height="{f2(hgt*.05)}" fill="{c["bg"]}" fill-opacity=".55"/>'
    s += f'<rect x="0" y="{f2(t*.9)}" width="{t}" height="{f2(t*.045)}" fill="{c["fg"]}" fill-opacity="{c["fg_op"]}"/>'
    return t, t, s


def sprigs(t, c, r, p):
    def sprig(cx, cy, ang, ln, col, op):
        g = f'<g transform="translate({f2(cx)} {f2(cy)}) rotate({ang})" fill="{col}" fill-opacity="{op}">'
        g += f'<line x1="0" y1="{f2(-ln/2)}" x2="0" y2="{f2(ln/2)}" stroke="{col}" stroke-opacity="{op}" stroke-width="{f2(ln*.03)}" stroke-linecap="round"/>'
        for k in range(4):
            y = -ln / 2 + ln * (.2 + .2 * k)
            for side in (-1, 1):
                g += f'<ellipse cx="{f2(side*ln*.09)}" cy="{f2(y)}" rx="{f2(ln*.045)}" ry="{f2(ln*.095)}" transform="rotate({side*35} {f2(side*ln*.09)} {f2(y)})"/>'
        return g + "</g>"
    s = sprig(t / 2, t / 2, 35 + p * 5, t * .85, c["fg"], c["fg_op"])
    s += "".join(sprig(x, y, -40, t * .7, c["fg"], c["fg_op"]) for x, y in [(0, 0), (t, 0), (0, t), (t, t)])
    s += f'<circle cx="{f2(t*.5)}" cy="{f2(t*.06)}" r="{f2(t*.03)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/><circle cx="{f2(t*.5)}" cy="{f2(t*.94)}" r="{f2(t*.03)}" fill="{c["acc"]}" fill-opacity="{c["acc_op"]}"/>'
    return t, t, s


def _star(x, y, d, col, op):
    return (f'<path d="M{f2(x)} {f2(y-d)}Q{f2(x)} {f2(y)} {f2(x+d)} {f2(y)}Q{f2(x)} {f2(y)} {f2(x)} {f2(y+d)}'
            f'Q{f2(x)} {f2(y)} {f2(x-d)} {f2(y)}Q{f2(x)} {f2(y)} {f2(x)} {f2(y-d)}Z" fill="{col}" fill-opacity="{op}"/>')


def sparkle(t, c, r, p):
    s = _star(t / 2, t / 2, t * (.2 + .02 * p), c["fg"], c["fg_op"])
    s += "".join(_star(x, y, t * .1, c["fg"], c["fg_op"]) for x, y in [(0, 0), (t, 0), (0, t), (t, t)])
    s += _star(t * .22, t * .72, t * .06, c["acc"], c["acc_op"]) + _star(t * .78, t * .28, t * .06, c["acc"], c["acc_op"])
    return t, t, s


def rings(t, c, r, p):
    sw = t * (0.025 + 0.007 * p)
    s = ""
    for x, y, k in [(t / 2, t / 2, 1), (0, 0, .6), (t, 0, .6), (0, t, .6), (t, t, .6)]:
        for i, rad in enumerate([.34, .25, .16]):
            col, op = (c["acc"], c["acc_op"]) if i == 2 else (c["fg"], c["fg_op"])
            s += f'<circle cx="{f2(x)}" cy="{f2(y)}" r="{f2(t*rad*k)}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{f2(sw)}"/>'
    return t, t, s


def bricks(t, c, r, p):
    h = t / 4
    g = t * (0.02 + 0.006 * p)
    s = ""
    for row, xs in enumerate([[0, t / 2], [-t / 4, t / 4, 3 * t / 4]]):
        y = row * h
        for k, x in enumerate(xs):
            acc = row == 1 and k == 1
            col, op = (c["acc"], c["acc_op"] * .8) if acc else (c["fg"], c["fg_op"] * (.6 + .4 * ((k + row) % 2)))
            s += f'<rect x="{f2(x+g)}" y="{f2(y+g)}" width="{f2(t/2-2*g)}" height="{f2(h-2*g)}" rx="{f2(h*.18)}" fill="{col}" fill-opacity="{f2(op)}"/>'
    return t, t / 2, s


def argyle(t, c, r, p):
    h = t / 2
    def dia(cx, cy, col, op):
        return f'<polygon points="{f2(cx)},{f2(cy-h)} {f2(cx+h)},{f2(cy)} {f2(cx)},{f2(cy+h)} {f2(cx-h)},{f2(cy)}" fill="{col}" fill-opacity="{op}"/>'
    s = dia(t / 2, t / 2, c["fg"], f2(c["fg_op"] * .55))
    s += "".join(dia(x, y, c["acc"], f2(c["acc_op"] * .22)) for x, y in [(0, 0), (t, 0), (0, t), (t, t)])
    s += f'<path d="M0 0L{t} {t}M{t} 0L0 {t}" stroke="{c["bg"]}" stroke-opacity=".7" stroke-width="{f2(t*(.012+.004*p))}" stroke-dasharray="{f2(t*.04)} {f2(t*.05)}" fill="none"/>'
    return t, t, s


def barcode(t, c, r, p):
    x, s = 0.0, ""
    bars = []
    while x < t - 2:
        wv = r.choice([1, 1, 2, 3]) * t * .018
        gap = r.choice([1, 2, 2]) * t * .018
        if x + wv > t:
            break
        bars.append((x, wv))
        x += wv + gap
    for i, (bx, bw) in enumerate(bars):
        acc = i == len(bars) // 2
        col, op = (c["acc"], c["acc_op"]) if acc else (c["fg"], c["fg_op"])
        s += f'<rect x="{f2(bx)}" y="0" width="{f2(bw)}" height="{t}" fill="{col}" fill-opacity="{op}"/>'
    return t, t, s


# ลำดับ = เลขลาย 01-25 (ห้ามสลับ เพราะเลขอยู่ในชื่อไฟล์)
FAMILIES = [
    ("dots", "จุดตาราง", dots, "เรียบสุด ใช้ได้ทุกงาน"),
    ("halftone", "ฮาล์ฟโทนไล่ขนาด", halftone, "แนวดิจิทัล/เทคโนโลยี หัวข้อฐานข้อมูล"),
    ("plus", "เครื่องหมายบวก", plus, "แนวเทคนิค ตารางข้อมูล"),
    ("diag", "เส้นทแยง", diag, "แถบหัวข้อ ปกสไลด์เรียบ"),
    ("zigzag", "ซิกแซก", zigzag, "กิจกรรม ความเคลื่อนไหว"),
    ("hexline", "รังผึ้งเส้น", hexline, "วิทยาศาสตร์ เครือข่าย"),
    ("cubes", "ลูกบาศก์ไอโซเมตริก", cubes, "ปกชุดวิชา ปกสไลด์อบรมเชิงโครงสร้าง"),
    ("seigaiha", "คลื่นเซกายฮะ", seigaiha, "ปกวารสาร/นิยาย เนื้อสัมผัสนุ่ม"),
    ("waves", "คลื่นเส้นคู่", waves, "นิยาย วรรณกรรม ความอ่อนโยน"),
    ("circlelattice", "วงกลมซ้อนทับ", circlelattice, "ปกชุดเล่ม ฐานข้อมูลรวม"),
    ("prajam", "ตาข่ายประจำยาม", prajam, "งานไทย เกียรติบัตร พิธีการ"),
    ("octagons", "แปดเหลี่ยม-สี่เหลี่ยม", octagons, "หรูเป็นทางการ ประกาศ รางวัล"),
    ("memphis", "เมมฟิส", memphis, "กิจกรรมเด็ก/นักศึกษา โพสต์สนุก"),
    ("truchet", "ทรูเชต์โค้ง (เส้นหนา)", truchet_arcs, "ลายไหลแบบออร์แกนิก ปกสไลด์ทันสมัย"),
    ("maze", "ทรูเชต์ทแยง (เขาวงกต)", truchet_diag, "เกม ปริศนา กิจกรรมค้นหา"),
    ("grid", "กระดาษกราฟ", graph_grid, "สไลด์วิชาการ ตำรา แบบฝึกหัด"),
    ("pixels", "พิกเซลสุ่ม", pixels, "ดิจิทัล AI การรู้เท่าทันสื่อ"),
    ("bauhaus", "เบาเฮาส์", bauhaus, "ปกหนังสือ งานออกแบบ"),
    ("spines", "สันหนังสือ", spines, "ห้องสมุดโดยตรง แนะนำหนังสือ"),
    ("sprigs", "กิ่งใบ", sprigs, "นิยาย ธรรมชาติ สุขภาพ"),
    ("sparkle", "ประกายดาว", sparkle, "ประกาศข่าวดี เปิดบริการใหม่"),
    ("rings", "วงแหวนซ้อน", rings, "เสียง วิทยุ ชุมชน เป้านิ่ง"),
    ("bricks", "อิฐเหลื่อม", bricks, "โครงสร้าง ขั้นตอน เป็นระบบ"),
    ("argyle", "ขนมเปียกปูนอาร์ไกล์", argyle, "คลาสสิก วารสารวิชาการ"),
    ("barcode", "บาร์โค้ด", barcode, "ยืม-คืน เลขเรียกหนังสือ บริการ"),
]


def build():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    index = []
    for fi, (slug, th, fn, use) in enumerate(FAMILIES, start=1):
        for p, (sz, t) in enumerate(SIZES):
            style = STYLE_ORDER[(fi + p) % 5]
            pal = dict(PALETTES[style])
            pal.setdefault("fg_op", 1.0)
            pal["acc_op"] = 0.7 if style != "C" else 0.5
            if style == "C":
                pal["fg_op"] = PALETTES["C"]["fg_op"]
            r = random.Random(fi * 10 + p)
            w, h, inner = fn(t, pal, r, p)
            if style == "C":
                bg_def = (f'<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{pal["bg"]}"/>'
                          f'<stop offset="1" stop-color="{pal["bg2"]}"/></linearGradient>')
                bg = '<rect width="100%" height="100%" fill="url(#g)"/>'
            else:
                bg_def, bg = "", f'<rect width="100%" height="100%" fill="{pal["bg"]}"/>'
            name = f"{fi:02d}-{slug}-{style}{sz}"
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}" width="{CANVAS}" height="{CANVAS}">'
                   f'<defs>{bg_def}<pattern id="p" width="{f2(w)}" height="{f2(h)}" patternUnits="userSpaceOnUse">{inner}</pattern></defs>'
                   f'{bg}<rect width="100%" height="100%" fill="url(#p)"/></svg>')
            (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
            index.append(dict(id=name, no=(fi - 1) * 4 + p + 1, family=slug, thai=th, style=style, style_name=PALETTES[style]["name"],
                              size=sz, tile=t, bg=pal["bg"], fg=pal["fg"], accent=pal["acc"], use=use))
    (HERE / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    cards = "".join(
        f'<figure><img src="svg/{i["id"]}.svg" loading="lazy"><figcaption><b>{i["no"]:03d}</b> {i["thai"]}<br>'
        f'<small>สไตล์ {i["style"]} · {i["size"]} · {i["id"]}</small></figcaption></figure>' for i in index)
    (HERE / "sheet.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>คลังแพทเทิร์น 100 แบบ</title>'
        '<style>body{font:14px Mitr,Tahoma,sans-serif;margin:24px;background:#f4f4f6;color:#1f2430}'
        'main{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px}'
        'figure{margin:0;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px #0002}'
        'img{display:block;width:100%;aspect-ratio:1;object-fit:cover}figcaption{padding:8px 10px;line-height:1.35}small{color:#6b6f78}</style>'
        f'<h2>คลังแพทเทิร์นพื้นหลัง 100 แบบ ({len(index)})</h2><main>{cards}</main>', encoding="utf-8")
    print(f"built {len(index)} patterns -> {OUT}")


if __name__ == "__main__":
    build()
