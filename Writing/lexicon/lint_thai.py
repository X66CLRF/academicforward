"""ตรวจภาษาไทยวิชาการจากคลังคำ thai-lexicon.tsv (ภาษาพูด · แปลตรง · วลีสำเร็จรูป · โครงอังกฤษ)

Usage: python lint_thai.py <file> [<file>...] [--level warn|info] [--syntax] [--strict]
รองรับ .pdf (รายงานเลขหน้า) · .docx · .md · .txt · .html · .js.part
ไม่แก้ไฟล์ แค่รายงานจุดที่เจอ + คำที่ควรใช้แทน ให้คนตัดสิน
--syntax  นับโครงประโยคอังกฤษ (ซึ่ง ของ ถูก…) ต่อย่อหน้า ใช้กับความเรียง ไม่ใช้กับสไลด์
--strict  exit 1 ถ้าเจอระดับ warn (ใช้ในสคริปต์ build)
"""
import re
import sys
import zipfile
from pathlib import Path

LEX = Path(__file__).with_name("thai-lexicon.tsv")


def load():
    rules = []
    for ln in LEX.read_text(encoding="utf-8").splitlines():
        if not ln.strip() or ln.startswith("#") or ln.startswith("pattern\t"):
            continue
        c = (ln.split("\t") + [""] * 6)[:6]
        rules.append(dict(pat=re.compile(c[0]), rep=c[1], type=c[2], level=c[3], exc=re.compile(c[4]) if c[4] else None, src=c[5]))
    return rules


def units(path):
    """คืน [(ตำแหน่ง, ข้อความ)] ตำแหน่ง = หน้า PDF หรือบรรทัด"""
    p = Path(path)
    ext = "".join(p.suffixes[-2:]) if p.name.endswith(".js.part") else p.suffix.lower()
    if ext == ".pdf":
        import pymupdf
        return [(f"หน้า {i + 1}", pg.get_text().replace("\n", " ")) for i, pg in enumerate(pymupdf.open(p))]
    if ext == ".docx":
        xml = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
        paras = [re.sub(r"<[^>]+>", "", x) for x in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)]
        return [(f"ย่อหน้า {i + 1}", t) for i, t in enumerate(paras) if t.strip()]
    txt = p.read_text(encoding="utf-8")
    out = []
    for i, ln in enumerate(txt.splitlines()):
        if ext in (".html", ".js.part", ".js"):
            if ln.lstrip().startswith(("/*", "//", "<style", "const ", "P.")):
                continue
            ln = re.sub(r"<[^>]+>|\$\{[^}]*\}|&nbsp;", " ", ln)
            ln = " ".join(re.findall(r"[฀-๿][^'`\"<>{}]*", ln))  # เก็บเฉพาะช่วงที่มีอักษรไทย
        if ln.strip():
            out.append((f"บรรทัด {i + 1}", ln))
    return out


def lint(path, rules, level="info", syntax=False):
    hits = []
    for loc, t in units(path):
        for r in rules:
            if r["type"] == "syntax":
                if not syntax:
                    continue
                n = len(r["pat"].findall(t))
                if n > int(r["rep"] or 99):
                    hits.append((loc, r, f"{r['pat'].pattern} = {n} ครั้ง (เพดาน {r['rep']})"))
                continue
            if level == "warn" and r["level"] != "warn":
                continue
            for m in r["pat"].finditer(t):
                a, b = m.span()
                win = t[max(0, a - 12): b + 12]
                if r["exc"] and any(e.start() <= a - max(0, a - 12) < e.end() or e.start() < b - max(0, a - 12) <= e.end()
                                    for e in r["exc"].finditer(win)):
                    continue
                ctx = t[max(0, a - 30): b + 30].strip()
                hits.append((loc, r, ctx))
    return hits


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    level = sys.argv[sys.argv.index("--level") + 1] if "--level" in sys.argv else "info"
    if level in args:
        args.remove(level)
    rules = load()
    nwarn = 0
    for f in args:
        hits = lint(f, rules, level, "--syntax" in sys.argv)
        print(f"\n== {Path(f).name}: {len(hits)} จุด")
        for loc, r, ctx in hits:
            tag = "แก้" if r["level"] == "warn" else "ดู"
            nwarn += r["level"] == "warn"
            print(f"[{tag}·{r['type']}] {loc} | {ctx}\n      → {r['rep']}  ({r['src']})")
    if "--strict" in sys.argv and nwarn:
        sys.exit(1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
