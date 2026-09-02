# -*- coding: utf-8 -*-
"""ด่านตรวจไฟล์ .docx ภาษาไทย — รันก่อนส่งมอบทุกครั้ง

วิธีใช้
    python check_docx.py file.docx              ตรวจไฟล์เดียว
    python check_docx.py folder/                ตรวจทุกไฟล์ในโฟลเดอร์
    python check_docx.py file.docx --lang lo-LA ระบุภาษาอักษรเชิงซ้อนอื่น

คืนค่า exit code 0 เมื่อผ่านทั้งหมด · 1 เมื่อมีไฟล์ไม่ผ่าน
ถ้าไม่ผ่าน ห้ามส่งมอบไฟล์ ให้แก้แล้วตรวจใหม่
"""

import sys
import os
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_core import verify  # noqa: E402


def collect(target):
    if os.path.isdir(target):
        return sorted(glob.glob(os.path.join(target, "*.docx")))
    return [target]


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    lang = "th-TH"
    for a in argv:
        if a.startswith("--lang"):
            lang = a.split("=", 1)[1] if "=" in a else argv[argv.index(a) + 1]

    targets = args or ["."]
    files = []
    for t in targets:
        files += collect(t)
    files = [f for f in files if not os.path.basename(f).startswith("~$")]

    if not files:
        print("ไม่พบไฟล์ .docx")
        return 1

    all_ok = True
    for f in files:
        ok, items = verify(f, lang)
        all_ok = all_ok and ok
        print("\n=== %s ===" % os.path.basename(f))
        for name, passed, val in items:
            print("  %-4s %-32s %s" % ("PASS" if passed else "FAIL", name, val))

    print("\n%s (%d ไฟล์)" % (
        "ผ่านทั้งหมด" if all_ok else "มีไฟล์ไม่ผ่าน ห้ามส่งมอบ", len(files)))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
