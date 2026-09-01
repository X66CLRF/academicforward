# -*- coding: utf-8 -*-
"""docxkit — แก้ .docx แบบแทนที่ข้อความล้วน + backup อัตโนมัติทุกครั้ง

ใช้:
    import docxkit as k
    d = k.Doc(path)          # โหลด + snapshot document.xml ลง _backup/
    d.para_replace({...})    # แทนที่ย่อหน้าตามข้อความเดิม
    d.save()                 # เขียนกลับ
    k.milestone(path, 'ร่าง02')   # ก๊อบเล่มเต็มเป็นเวอร์ชันใหม่
    k.restore(path, 'xxx.xml')    # กู้ document.xml จาก snapshot
"""
import zipfile, re, shutil, os, sys, datetime

T_RE = re.compile(r'<w:t(?:\s[^>]*)?>.*?</w:t>', re.S)
P_RE = re.compile(r'<w:p\b.*?</w:p>', re.S)
TR_RE = re.compile(r'<w:tr\b.*?</w:tr>', re.S)
TC_RE = re.compile(r'<w:tc>.*?</w:tc>', re.S)
TBL_RE = re.compile(r'<w:tbl>.*?</w:tbl>', re.S)

def gettext(x):
    return ''.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', x, re.S))

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def puttext(xml, text):
    """ข้อความใหม่ลง <w:t> ตัวแรก ล้าง <w:t> ที่เหลือ — ไม่แตะ run/prop/tab"""
    hits = list(T_RE.finditer(xml))
    if not hits:
        return xml
    out, prev, first = [], 0, True
    for m in hits:
        out.append(xml[prev:m.start()])
        out.append('<w:t xml:space="preserve">' + (esc(text) if first else '') + '</w:t>')
        first = False
        prev = m.end()
    out.append(xml[prev:])
    return ''.join(out)

def _bakdir(path):
    d = os.path.join(os.path.dirname(path), '_backup')
    os.makedirs(d, exist_ok=True)
    return d

class Doc:
    def __init__(self, path, note='edit'):
        self.path = path
        z = zipfile.ZipFile(path)
        self.names = z.namelist()
        self.blobs = {n: z.read(n) for n in self.names}
        z.close()
        self.xml = self.blobs['word/document.xml'].decode('utf8')
        ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        base = os.path.splitext(os.path.basename(path))[0]
        self.snap = os.path.join(_bakdir(path), f'{base}__{ts}__{note}.xml')
        open(self.snap, 'w', encoding='utf8').write(self.xml)
        print('snapshot:', os.path.basename(self.snap))

    # --- แทนที่ย่อหน้าทั้งไฟล์ตาม dict {ข้อความเดิม: ข้อความใหม่} ---
    def para_replace(self, mapping, scope=None):
        region = self.xml if scope is None else scope
        n = 0
        for p in P_RE.findall(region):
            t = gettext(p).strip()
            if t in mapping:
                self.xml = self.xml.replace(p, puttext(p, mapping[t]), 1)
                n += 1
        return n

    # --- แทนที่ย่อหน้าด้วยฟังก์ชันตัดสินใจเอง fn(text) -> str|None ---
    def para_map(self, fn, limit_before_tbl=False):
        region = self.xml[:self.xml.index('<w:tbl>')] if limit_before_tbl else self.xml
        n = 0
        for p in P_RE.findall(region):
            new = fn(gettext(p).strip())
            if new is not None:
                self.xml = self.xml.replace(p, puttext(p, new), 1)
                n += 1
        return n

    # --- แทนที่เซลล์ในตารางที่ index ด้วย fn(row_texts) -> list|None ---
    def table_map(self, idx, fn, ncols=4):
        tbls = TBL_RE.findall(self.xml)
        tbl = tbls[idx]
        new_tbl = tbl
        n = 0
        for tr in TR_RE.findall(tbl):
            tcs = TC_RE.findall(tr)
            if len(tcs) != ncols:
                continue
            vals = fn([gettext(c) for c in tcs])
            if vals is None:
                continue
            newtr = tr
            for i in range(ncols):
                if vals[i] is not None:
                    newtr = newtr.replace(tcs[i], puttext(tcs[i], vals[i]), 1)
            new_tbl = new_tbl.replace(tr, newtr, 1)
            n += 1
        self.xml = self.xml.replace(tbl, new_tbl, 1)
        return n

    # --- แทนแถวข้อมูลทั้งตารางด้วยชุดใหม่ (โคลนแถวต้นแบบ) ---
    def table_fill(self, idx, rows, keep_head=2, proto=2, ncols=4):
        tbl = TBL_RE.findall(self.xml)[idx]
        trs = TR_RE.findall(tbl)
        head = ''.join(trs[:keep_head])
        pr = trs[proto]
        ptcs = TC_RE.findall(pr)
        out = []
        for r in rows:
            tr = pr
            for i in range(ncols):
                tr = tr.replace(ptcs[i], puttext(ptcs[i], r[i]), 1)
            out.append(tr)
        new_tbl = tbl[:tbl.index('<w:tr')] + head + ''.join(out) + '</w:tbl>'
        self.xml = self.xml.replace(tbl, new_tbl, 1)
        return len(out)

    def save(self):
        tmp = self.path + '.tmp'
        zo = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
        for n in self.names:
            zo.writestr(n, self.xml.encode('utf8') if n == 'word/document.xml' else self.blobs[n])
        zo.close()
        shutil.move(tmp, self.path)
        print('saved:', os.path.basename(self.path))

def milestone(path, tag):
    """ก๊อบเล่มเต็มเป็นเวอร์ชันใหม่ เช่น ร่าง02"""
    d, b = os.path.dirname(path), os.path.basename(path)
    new = os.path.join(d, re.sub(r'ร่าง\d+', tag, b))
    shutil.copy2(path, new)
    print('milestone:', os.path.basename(new))
    return new

def restore(path, snap_name):
    """กู้ document.xml จาก snapshot กลับเข้าเล่ม"""
    snap = os.path.join(_bakdir(path), snap_name)
    xml = open(snap, encoding='utf8').read()
    z = zipfile.ZipFile(path); names = z.namelist(); blobs = {n: z.read(n) for n in names}; z.close()
    tmp = path + '.tmp'
    zo = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
    for n in names:
        zo.writestr(n, xml.encode('utf8') if n == 'word/document.xml' else blobs[n])
    zo.close(); shutil.move(tmp, path)
    print('restored from:', snap_name)

def snaps(path):
    d = _bakdir(path)
    for f in sorted(os.listdir(d)):
        print(f, os.path.getsize(os.path.join(d, f)) // 1024, 'KB')

def replace_range(xml, start_text, end_text, items, protos):
    """แทนช่วงย่อหน้า [start_text .. end_text) ด้วย items = [(kind, text), ...]
    protos = {kind: paragraph_xml ต้นแบบ} (โคลนแล้วแทนข้อความ)
    end_text=None = ถึงย่อหน้าสุดท้ายของช่วงที่ให้มา"""
    paras = P_RE.findall(xml)
    texts = [gettext(p).strip() for p in paras]
    i = texts.index(start_text)
    j = texts.index(end_text) if end_text else len(paras)
    old = ''.join(paras[i:j])
    new = ''.join(puttext(protos[k], t) for k, t in items)
    return xml.replace(old, new, 1), j - i, len(items)


def puttext_rich(xml, segments):
    """วางข้อความหลายช่วงในย่อหน้าเดียว โดยคุมตัวหนารายช่วง
    segments = [(ข้อความ, bold True/False), ...]
    โคลน run แรกของย่อหน้าเป็นต้นแบบทุกช่วง ฟอนต์/ขนาด/ภาษาจึงเหมือนเดิมทุกประการ"""
    runs = re.findall(r'<w:r\b(?![a-zA-Z])(?:(?!</w:r>).)*</w:r>', xml, re.S)
    proto = next((r for r in runs if T_RE.search(r)), None)
    if proto is None:
        return xml

    def make(text, bold):
        r = proto
        rpr = re.search(r'<w:rPr>.*?</w:rPr>', r, re.S)
        if rpr:
            body = rpr.group(0)[len('<w:rPr>'):-len('</w:rPr>')]
            body = re.sub(r'<w:b/>|<w:bCs/>|<w:b\s[^>]*/>|<w:bCs\s[^>]*/>', '', body)
            if bold:
                body = '<w:b/><w:bCs/>' + body
            r = r.replace(rpr.group(0), '<w:rPr>' + body + '</w:rPr>', 1)
        elif bold:
            r = r.replace('<w:r>', '<w:r><w:rPr><w:b/><w:bCs/></w:rPr>', 1)
        # เขียนข้อความลง <w:t> ตัวแรกของ run ล้างที่เหลือ
        return puttext(r, text)

    new_runs = ''.join(make(t, b) for t, b in segments if t)
    first = xml.index(runs[0])
    last = xml.index(runs[-1]) + len(runs[-1])
    return xml[:first] + new_runs + xml[last:]
