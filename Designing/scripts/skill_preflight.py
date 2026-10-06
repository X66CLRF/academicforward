"""skill_preflight — ให้ Jev (TypeSafe System One) ตัดสินว่างานนี้ต้องอ่านคู่มือไฟล์ไหนก่อนลงมือ

ใช้ก่อนเริ่มงานกราฟิก/เอกสารทุกครั้ง: ส่ง "งาน" + หัวไฟล์คู่มือแต่ละไฟล์ → ได้ความน่าจะเป็นว่าต้องอ่าน
แล้วเทียบกับไฟล์ที่เอเจนต์อ่านแล้ว (--read) → แสดงรายการ "ต้องอ่านแต่ยังไม่ได้อ่าน"

    py -X utf8 skill_preflight.py --task "ทำภาพโพสต์แนะนำหนังสือบริจาค 2160 ส่ง Canva" \
        --dir .. --read social-graphic-agent.md style-library.md

คีย์: ตัวแปรสภาพแวดล้อม TYPESAFE_API_KEY เท่านั้น ห้ามเขียนลงไฟล์/คอมมิต
"""
import argparse, json, os, sys, urllib.request, urllib.error
from pathlib import Path

URL = "https://api.typesafe.ai/v1/systemone"
HEAD_CHARS = 600
MUST = 0.6      # ≥ นี้ = ต้องอ่านก่อนลงมือ
MAYBE = 0.35    # ≥ นี้ = ควรอ่านถ้ามีเวลา


def head(p: Path) -> str:
    """ส่งออกเฉพาะบรรทัดหัวเรื่อง + คำอธิบายสั้น ไม่ส่งเนื้อไฟล์ทั้งไฟล์"""
    lines = [l for l in p.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
    return "\n".join(lines[:3])[:HEAD_CHARS]


def ask(task: str, files: list[Path]) -> dict:
    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        sys.exit("ไม่พบ TYPESAFE_API_KEY ในตัวแปรสภาพแวดล้อม")
    questions = {}
    for f in files:
        questions[f.name] = {
            "type": "noul",
            "instructions": {
                "guide_file": f.name,
                "guide_head": head(f),
                "question": "ก่อนลงมือทำ `task` ให้ถูกกฎของผู้ใช้ ผู้ทำงานต้องอ่านคู่มือ `guide_file` (ดูจาก `guide_head`) ก่อนหรือไม่",
            },
            "criteria": {
                "true": "คู่มือนี้กำหนดกฎ/ขั้นตอน/คลังตัวเลือกที่ต้องใช้โดยตรงกับงานนี้ หรือเป็นขั้นบังคับก่อนหน้า/ถัดไปของงานนี้",
                "false": "คู่มือนี้เป็นของงานชนิดอื่นที่ไม่เกี่ยวกับงานนี้",
            },
        }
    body = {"state": {"task": task}, "model": "jev-latest", "questions": questions}
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--dir", default=".", help="โฟลเดอร์คู่มือ (*.md ชั้นเดียว)")
    ap.add_argument("--read", nargs="*", default=[], help="ชื่อไฟล์ที่อ่านแล้ว")
    a = ap.parse_args()
    files = sorted(Path(a.dir).glob("*.md"))
    res = ask(a.task, files)
    read = {Path(x).name for x in a.read}
    rows = sorted(((v["noul"], k) for k, v in res["answers"].items()), reverse=True)
    print(f"งาน: {a.task}\nโมเดล: {res['model']}  โทเคน: {res['usage']}\n")
    gaps = []
    for p, name in rows:
        tag = "ต้องอ่าน" if p >= MUST else "ควรอ่าน" if p >= MAYBE else "ข้าม"
        done = "อ่านแล้ว" if name in read else "ยังไม่อ่าน"
        if tag != "ข้าม" and name not in read:
            gaps.append((p, name, tag))
        print(f"{p:5.2f}  {tag:8} {done:10} {name}")
    print("\nผลกระทบ — ต้อง/ควรอ่านแต่ยังไม่ได้อ่าน:")
    if not gaps:
        print("  ไม่มี")
    for p, name, tag in gaps:
        print(f"  [{tag}] {name} ({p:.2f})")


if __name__ == "__main__":
    main()
