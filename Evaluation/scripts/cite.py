# -*- coding: utf-8 -*-
"""เติมบรรทัดอ้างหลักฐานท้ายช่องคอลัมน์ ๓ ตาม house style
   เอกสารแนบ<ชื่อหมวด> ระดับที่ ๓: หมายเลข 【…】
   ช่องที่เจ้าของพิมพ์เลขไว้แล้ว = ข้าม ไม่แตะ"""
import sys, re; sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'.')
import docxkit as k
DOCX = r'C:\Users\Burt\OneDrive - Nakhon Sawan Rajabhat University\ไฟล์ของ romnalin taengnuanchan - สมรรถนะ3ปี\10-เล่มสมรรถนะ-รมย์นลิน-2569\สมรรถนะ [2569] - รมย์นลิน - ระดับชำนาญการ - ร่าง01.docx'
DRY = '--write' not in sys.argv

d = k.Doc(DOCX, 'เติมบรรทัดอ้างหลักฐาน-house-style')
cur = None
skipped = added = 0
report = []
for ti in (4, 5, 6, 7):
    tbl = re.findall(r'<w:tbl>.*?</w:tbl>', d.xml, re.S)[ti]
    new_tbl = tbl
    for tr in re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S):
        tcs = re.findall(r'<w:tc>.*?</w:tc>', tr, re.S)
        if len(tcs) != 3:
            continue
        c1, c2, c3 = (k.gettext(c).strip() for c in tcs)
        if c1.startswith('('):
            cur = re.sub(r'^\([ก-ฮ]\)\s*', '', c1)          # ชื่อหมวด ตัด (ก) ออก
        m = re.match(r'ระดับที่\s*([๑๒๓])', c2)
        if not m or cur is None or not c3.strip():
            continue
        lv = m.group(1)
        if 'เอกสารแนบ' in c3:                                # เจ้าของเติมแล้ว
            skipped += 1; report.append(('SKIP', cur, lv, c3[-60:])); continue
        line = 'เอกสารแนบ%s ระดับที่ %s: หมายเลข 【…】' % (cur, lv)
        ps = re.findall(r'<w:p\b.*?</w:p>', tcs[2], re.S)
        proto = next(q for q in ps if k.T_RE.search(q))
        newtc = tcs[2].replace(ps[-1], ps[-1] + k.puttext(proto, line), 1)
        new_tbl = new_tbl.replace(tr, tr.replace(tcs[2], newtc, 1), 1)
        added += 1; report.append(('ADD', cur, lv, line))
    d.xml = d.xml.replace(tbl, new_tbl, 1)

for tag, sec, lv, s in report:
    print(tag, '|', sec[:34], '| ระดับ', lv, '|', s[:70])
print('\nเติม %d ช่อง · ข้าม (เจ้าของเขียนแล้ว) %d ช่อง' % (added, skipped))
if DRY:
    print('\n[DRY RUN] ยังไม่เขียนไฟล์ — สั่ง python cite.py --write เพื่อเขียนจริง')
else:
    d.save()
