# -*- coding: utf-8 -*-
"""ทำวลีนำหน้าย่อหน้าเป็นตัวหนา (ขึ้นต้นด้วย กรณี / ด้าน) ส่วนที่เหลือคงตัวปกติ"""
import sys, re; sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'.')
import docxkit as k
import os
# ไฟล์เล่มสมรรถนะ: ตั้งตัวแปร PROMOTE_DOCX=<path .docx> ก่อนรัน (ไม่ผูกเครื่อง/เจ้าของเล่ม)
DOCX = os.environ.get('PROMOTE_DOCX') or sys.exit('ตั้ง PROMOTE_DOCX=<path เล่ม .docx> ก่อนรัน')
BOOK_DIR = os.path.dirname(DOCX)
WRITE = '--write' in sys.argv

d = k.Doc(DOCX, 'ทำวลีนำเป็นตัวหนา')
n = 0
for q in re.findall(r'<w:p\b.*?</w:p>', d.xml, re.S):
    t = k.gettext(q).strip()
    if not t.startswith(('กรณี', 'ด้านการเงิน', 'ด้านสื่อ')):
        continue
    if ' ' not in t:
        continue
    head, rest = t.split(' ', 1)
    if len(head) > 60:            # วลีนำยาวผิดปกติ = ไม่ใช่วลีนำ ข้าม
        continue
    new = k.puttext_rich(q, [(head, True), (' ' + rest, False)])
    if new != q:
        d.xml = d.xml.replace(q, new, 1); n += 1
        print('หนา: %-42s | ปกติ: %s…' % (head, rest[:46]))
print('\nปรับ %d ย่อหน้า' % n)
if WRITE: d.save()
else: print('[DRY RUN] สั่ง --write เพื่อเขียนจริง')
