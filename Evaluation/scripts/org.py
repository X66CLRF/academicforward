# -*- coding: utf-8 -*-
"""เติมคอลัมน์หน่วยงานในตารางฝึกอบรม จากการจับคู่ชื่อหลักสูตรกับแพลตฟอร์มผู้จัด"""
import sys, re, csv; sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'.')
import docxkit as k
DOCX = r'C:\Users\Burt\OneDrive - Nakhon Sawan Rajabhat University\ไฟล์ของ romnalin taengnuanchan - สมรรถนะ3ปี\10-เล่มสมรรถนะ-รมย์นลิน-2569\สมรรถนะ [2569] - รมย์นลิน - ระดับชำนาญการ - ร่าง01.docx'
REPORT = r'C:\Users\Burt\OneDrive - Nakhon Sawan Rajabhat University\ไฟล์ของ romnalin taengnuanchan - สมรรถนะ3ปี\10-เล่มสมรรถนะ-รมย์นลิน-2569\หน่วยงานจัดอบรม-ที่จับคู่ได้.tsv'
WRITE = '--write' in sys.argv

OCSC  = 'สำนักงาน ก.พ. (การอบรมออนไลน์)'
TDGA  = 'สถาบันพัฒนาบุคลากรภาครัฐด้านดิจิทัล (TDGA) สำนักงานพัฒนารัฐบาลดิจิทัล (องค์การมหาชน) (การอบรมออนไลน์)'
MOOC  = 'โครงการมหาวิทยาลัยไซเบอร์ไทย (Thai MOOC) กระทรวงการอุดมศึกษา วิทยาศาสตร์ วิจัยและนวัตกรรม (การอบรมออนไลน์)'
GREEN = 'ชมรมห้องสมุดสีเขียว สมาคมห้องสมุดแห่งประเทศไทยฯ'
NSRU  = 'สำนักวิทยบริการและเทคโนโลยีสารสนเทศ มหาวิทยาลัยราชภัฏนครสวรรค์'
GOOG  = 'Google for Education ร่วมกับสำนักวิทยบริการและเทคโนโลยีสารสนเทศ มหาวิทยาลัยราชภัฏนครสวรรค์'

RULES = [   # (คีย์เวิร์ดในชื่อหลักสูตร, หน่วยงาน, ระดับความมั่นใจ)
 (['หนังสือราชการ','สมรรถนะหลักสำหรับข้าราชการ','วินัยและจรรยาข้าราชการ','ภาษาอังกฤษเพื่อการทำงาน',
   'การให้บริการที่เป็นเลิศ','จริยธรรมในการทำงาน','การบริหารจัดการเวลาและตนเอง','ภาวะผู้นำในตนเอง',
   'การพัฒนาตนเองและผู้อื่น','การสื่อสารในภาวะวิกฤติ','ปัญญาประดิษฐ์กับการทำงาน','การจัดซื้อจัดจ้างและการบริหารพัสดุ',
   'กระบวนการยุติธรรมทางอาญา','Micro Learning','data literacy','ดิจิทับกับชีวิต','ดิจิทัลกับชีวิต',
   'Microsoft Office','Microsoft Excel','การบริหารงบประมาณและการเงิน','ทักษะการคิด','Effective Thinking',
   'เทคนิคการนำเสนอ','การบริหารอย่างมืออาชีพ','นวัตกรรมในหน่วยงาน','ทางก้าวหน้าในสายอาชีพ',
   'ความเป็นมืออาชีพ','Post New Normal'], OCSC, 'สูง'),
 (['ธรรมาภิบาลข้อมูล','blackchain','blockchain','digital techonlogy','digital technology','digital Literacy',
   'hadoop','UX UI','รัฐบาลดิจิทัล','การให้บริการภาครัฐผ่านระบบดิจิทัล','องค์กรดิจิทัล'], TDGA, 'สูง'),
 (['ThaiMOOC','Thaimooc'], MOOC, 'สูง'),
 (['green','Green','ห้องสมุดสีเขียว','GreenOffice'], GREEN, 'ปานกลาง'),
 (['google','Google'], GOOG, 'ปานกลาง'),
 (['Canva','AI ปลดล็อก','ai ปลด'], NSRU, 'ต่ำ'),
]

def guess(name):
    for keys, org, conf in RULES:
        for kw in keys:
            if kw.lower() in name.lower():
                return org, conf, kw
    return None, None, None

d = k.Doc(DOCX, 'เติมหน่วยงานจัดอบรม')
tbl = re.findall(r'<w:tbl>.*?</w:tbl>', d.xml, re.S)[0]
new_tbl = tbl
rows_out, filled, left = [], 0, 0
for i, tr in enumerate(re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S)):
    tcs = re.findall(r'<w:tc>.*?</w:tc>', tr, re.S)
    if len(tcs) != 4 or i < 2:
        continue
    date, dur, name, org = (k.gettext(c).strip() for c in tcs)
    if not org.startswith('⚠'):
        continue
    new, conf, kw = guess(name)
    if new is None:
        # ThaiMOOC ที่คอลัมน์เดิมเขียนไว้แล้วจะไม่เข้าเงื่อนไขนี้
        rows_out.append([date, name, org, '', 'ไม่พบ', '']); left += 1; continue
    ps = re.findall(r'<w:p\b.*?</w:p>', tcs[3], re.S)
    proto = next(q for q in ps if k.T_RE.search(q))
    newtc = tcs[3].replace(''.join(ps), k.puttext(proto, new), 1)
    new_tbl = new_tbl.replace(tr, tr.replace(tcs[3], newtc, 1), 1)
    rows_out.append([date, name, org, new, conf, kw]); filled += 1

# แถวที่คอลัมน์หน่วยงานเขียนว่า ThaiMOOC เฉย ๆ ให้ขยายเป็นชื่อเต็ม
for i, tr in enumerate(re.findall(r'<w:tr\b.*?</w:tr>', new_tbl, re.S)):
    tcs = re.findall(r'<w:tc>.*?</w:tc>', tr, re.S)
    if len(tcs) != 4 or i < 2:
        continue
    date, dur, name, org = (k.gettext(c).strip() for c in tcs)
    if org.strip().lower() not in ('thaimooc', 'thai mooc'):
        continue
    ps = re.findall(r'<w:p\b.*?</w:p>', tcs[3], re.S)
    proto = next(q for q in ps if k.T_RE.search(q))
    newtc = tcs[3].replace(''.join(ps), k.puttext(proto, MOOC), 1)
    new_tbl = new_tbl.replace(tr, tr.replace(tcs[3], newtc, 1), 1)
    rows_out.append([date, name, org, MOOC, 'สูง', 'ThaiMOOC']); filled += 1

d.xml = d.xml.replace(tbl, new_tbl, 1)
with open(REPORT, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['วันที่','ชื่อหลักสูตร','ค่าเดิม','หน่วยงานที่จับคู่ได้','ความมั่นใจ','คีย์เวิร์ดที่ใช้ตัดสิน'])
    w.writerows(rows_out)
print('เติมได้ %d แถว | ยังไม่พบ %d แถว' % (filled, left))
print('รายงาน:', REPORT)
if WRITE:
    d.save()
else:
    print('[DRY RUN] ยังไม่เขียน .docx — สั่ง --write เพื่อเขียนจริง')
