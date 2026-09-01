# -*- coding: utf-8 -*-
"""ลบย่อหน้าโน้ตทำงานที่หลุดลงเล่ม (ขึ้นต้นด้วย * และมี ⚠)"""
import sys, re; sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'.')
import docxkit as k
DOCX = r'C:\Users\Burt\OneDrive - Nakhon Sawan Rajabhat University\ไฟล์ของ romnalin taengnuanchan - สมรรถนะ3ปี\10-เล่มสมรรถนะ-รมย์นลิน-2569\สมรรถนะ [2569] - รมย์นลิน - ระดับชำนาญการ - ร่าง01.docx'
WRITE = '--write' in sys.argv

def is_note(t):
    t = t.strip()
    return t.startswith('*') and ('⚠' in t or 'เรโป' in t)

d = k.Doc(DOCX, 'ลบโน้ตทำงานที่หลุดลงเล่ม')
n = 0
for q in re.findall(r'<w:p\b.*?</w:p>', d.xml, re.S):
    t = k.gettext(q).strip()
    if is_note(t):
        d.xml = d.xml.replace(q, '', 1); n += 1
        print('ลบ:', t[:110])
print('\nลบ %d ย่อหน้า' % n)
if WRITE: d.save()
else: print('[DRY RUN] สั่ง --write เพื่อเขียนจริง')
