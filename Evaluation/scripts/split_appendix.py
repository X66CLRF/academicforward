# -*- coding: utf-8 -*-
"""แยกภาคผนวกออกเป็นไฟล์ทำงานต่างหาก — ลบทุกอย่างเหนือ 'ส่วนที่ 6 เอกสารแนบ...'"""
import sys, re, zipfile, shutil, os; sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'.')
import docxkit as k

SRC = r'C:\Users\Burt\OneDrive - Nakhon Sawan Rajabhat University\ไฟล์ของ romnalin taengnuanchan - สมรรถนะ3ปี\10-เล่มสมรรถนะ-รมย์นลิน-2569\สมรรถนะ [2569] - รมย์นลิน - ระดับชำนาญการ - ร่าง01.docx'
DST = r'C:\Users\Burt\OneDrive - Nakhon Sawan Rajabhat University\ไฟล์ของ romnalin taengnuanchan - สมรรถนะ3ปี\10-เล่มสมรรถนะ-รมย์นลิน-2569\ภาคผนวก-รมย์นลิน-ร่าง01.docx'

shutil.copy2(SRC, DST)
z = zipfile.ZipFile(DST); names = z.namelist(); blobs = {n: z.read(n) for n in names}; z.close()
doc = blobs['word/document.xml'].decode('utf8')

body_open = doc.index('<w:body>') + len('<w:body>')
body_close = doc.rindex('</w:body>')
body = doc[body_open:body_close]

blocks = re.findall(r'<w:tbl>.*?</w:tbl>|<w:p\b.*?</w:p>|<w:sectPr\b.*?</w:sectPr>|<w:bookmark\w+\b[^>]*/>', body, re.S)
texts = [k.gettext(b).strip() for b in blocks]
start = next(i for i, t in enumerate(texts) if t.startswith('ส่วนที่ 6') and 'เอกสารแนบ' in t)
print('ภาคผนวกเริ่มที่บล็อก', start, '| บล็อกทั้งหมด', len(blocks))

kept = blocks[start:]
img_before = sum(len(re.findall(r'<a:blip', b)) for b in blocks[:start])
img_after  = sum(len(re.findall(r'<a:blip', b)) for b in kept)
print('รูปในส่วนที่ตัดทิ้ง', img_before, '| รูปที่เก็บไว้', img_after)

# sectPr สุดท้ายของ body ต้องคงไว้ (คุมขนาดหน้า ขอบกระดาษ header/footer)
tail = re.search(r'<w:sectPr\b(?:(?!</w:sectPr>).)*</w:sectPr>\s*$', body, re.S)
newbody = ''.join(kept)
if tail and '<w:sectPr' not in newbody[-len(tail.group(0))-50:]:
    newbody += tail.group(0)
doc = doc[:body_open] + newbody + doc[body_close:]

tmp = DST + '.tmp'
zo = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
for n in names:
    zo.writestr(n, doc.encode('utf8') if n == 'word/document.xml' else blobs[n])
zo.close(); shutil.move(tmp, DST)
print('เขียน:', os.path.basename(DST), '|', os.path.getsize(DST)//1024//1024, 'MB')
