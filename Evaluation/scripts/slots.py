# -*- coding: utf-8 -*-
"""บัญชีสล็อตรูปในภาคผนวก — อ่านอย่างเดียว ไม่แก้ไฟล์"""
import sys, re, zipfile, csv, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0,'.')
import docxkit as k

DOCX = r'C:\Users\Burt\OneDrive - Nakhon Sawan Rajabhat University\ไฟล์ของ romnalin taengnuanchan - สมรรถนะ3ปี\10-เล่มสมรรถนะ-รมย์นลิน-2569\สมรรถนะ [2569] - รมย์นลิน - ระดับชำนาญการ - ร่าง01.docx'
OUT  = r'C:\Users\Burt\OneDrive - Nakhon Sawan Rajabhat University\ไฟล์ของ romnalin taengnuanchan - สมรรถนะ3ปี\10-เล่มสมรรถนะ-รมย์นลิน-2569\slots-เทมเพลทรูป.tsv'
EMU = 914400

z = zipfile.ZipFile(DOCX)
doc = z.read('word/document.xml').decode('utf8')
rels = z.read('word/_rels/document.xml.rels').decode('utf8')
rmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
sizes = {n: z.getinfo(n).file_size for n in z.namelist()}
z.close()

paras = re.findall(r'<w:p\b.*?</w:p>', doc, re.S)
txt = [k.gettext(p).strip() for p in paras]

blocks = []      # บล็อกรูปติดกัน = หนึ่งเอกสารแนบ
i = 0
while i < len(paras):
    if not re.search(r'<a:blip', paras[i]):
        i += 1; continue
    start = i
    imgs = []
    while i < len(paras) and (re.search(r'<a:blip', paras[i]) or (not txt[i] and i+1 < len(paras) and re.search(r'<a:blip', paras[i+1]))):
        for m in re.finditer(r'<wp:extent cx="(\d+)" cy="(\d+)"', paras[i]):
            imgs.append([round(int(m.group(1))/EMU, 2), round(int(m.group(2))/EMU, 2)])
        for r in re.findall(r'<a:blip[^>]*r:embed="(rId\d+)"', paras[i]):
            pass
        i += 1
    rids = [r for q in paras[start:i] for r in re.findall(r'<a:blip[^>]*r:embed="(rId\d+)"', q)]
    crops = sum(len(re.findall(r'<a:srcRect', q)) for q in paras[start:i])
    cap, capi = '', None
    j = i
    while j < min(i+3, len(paras)):
        if txt[j].startswith('เอกสารแนบที่'):
            cap, capi = txt[j], j; break
        j += 1
    blocks.append(dict(start=start, end=i-1, n=len(imgs), sizes=imgs, rids=rids,
                       crops=crops, cap=cap, capi=capi))

num_re = re.compile(r'เอกสารแนบที่\s*([0-9๐-๙]+)')
with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['slot_id','เลขเอกสารแนบเดิม','ย่อหน้าเริ่ม','ย่อหน้าจบ','จำนวนรูป',
                'ขนาดเฟรม(นิ้ว) กว้างxสูง','แนวรูป','ครอบตัด','ไฟล์ media','ขนาดไฟล์(KB)','คำบรรยายเดิม'])
    for n, b in enumerate(blocks, 1):
        media = [rmap.get(r, '?').replace('media/', '') for r in b['rids']]
        kb = [str(sizes.get('word/' + rmap.get(r, ''), 0)//1024) for r in b['rids']]
        orient = ['แนวนอน' if s[0] >= s[1] else 'แนวตั้ง' for s in b['sizes']]
        mm = num_re.search(b['cap'])
        w.writerow([f'S{n:03d}', mm.group(1) if mm else '', b['start'], b['end'], b['n'],
                    ' | '.join(f'{s[0]}x{s[1]}' for s in b['sizes']),
                    ' | '.join(orient), b['crops'], ' | '.join(media), ' | '.join(kb), b['cap']])

from collections import Counter
print('บล็อก(เอกสารแนบ) ทั้งหมด:', len(blocks), '| รูปรวม:', sum(b['n'] for b in blocks))
print('แพตเทิร์นจำนวนรูปต่อบล็อก:', dict(sorted(Counter(b['n'] for b in blocks).items())))
print('บล็อกที่มีคำบรรยาย:', sum(1 for b in blocks if b['cap']), '| ไม่มี:', sum(1 for b in blocks if not b['cap']))
print('บล็อกที่มีการครอบตัด:', sum(1 for b in blocks if b['crops']))
o = Counter()
for b in blocks:
    for s in b['sizes']: o['แนวนอน' if s[0] >= s[1] else 'แนวตั้ง'] += 1
print('แนวรูป:', dict(o))
print('เขียน:', OUT)
