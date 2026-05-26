# AI Prompt Templates — NotebookLM Classroom Play Hub
**วิธีใช้:** copy บล็อก `CONTEXT` ไปวางก่อน prompt ทุกครั้ง แล้วต่อด้วย Recipe ที่ต้องการ

---

## CONTEXT BLOCK
> **Copy ส่วนนี้ไปวางท้าย prompt ทุกครั้งเพื่อให้ AI รู้จักไฟล์**

```
ไฟล์นี้คือ Single-HTML-File classroom tool ชื่อ "เทคโนโลยีและนวัตกรรม AI.html"
เป็น Vanilla JS + Tailwind CSS inline + html2canvas + jsPDF ไม่มี server
โครงสร้างหลัก:
  - #tab-intro     → slideDeck[] array (JS) เรนเดอร์สไลด์สอน
  - #tab-gameboard → challenge cards ล็อก/ปลดล็อกได้ แยก 3 หัวข้อ
  - #tab-marian / #tab-mars / #tab-tutan → ใบความรู้ A4 พิมพ์/export ได้

Design tokens:
  Font: 'Sarabun', sans-serif
  Primary: #d97706 (amber-600), #b45309 (amber-700), #1c1917 (stone-900)
  Background: #faf7f0 (page), #fffdfa (slide deck)
  Border: #ede7db
  Radius: rounded-2xl = 16px, rounded-xl = 12px, rounded-lg = 8px

หัวข้อปัจจุบัน: marian (🌊 ใต้ทะเลมาเรียนา) / mars (🚀 ดาวอังคาร) / tutan (👑 ตุตันคาเมน)
```

---

## RECIPE 1 — เพิ่มสไลด์ใหม่

**Prompt สั่ง AI:**
```
[CONTEXT BLOCK]

เพิ่มสไลด์ใหม่เข้าใน slideDeck[] array ในไฟล์ HTML
หัวข้อสไลด์: "[ชื่อสไลด์]"
เนื้อหา: [อธิบายสิ่งที่อยากสอน]
ใช้สไตล์เดียวกับสไลด์อื่น — Tailwind utility classes, ฟอนต์ Sarabun, โทนสี amber/stone
ใส่เป็น object ต่อท้าย array และแสดง code ที่แก้ไขแล้ว
```

**HTML Template สไลด์ — copy ไปใส่ใน slideDeck[]:**
```javascript
{
    title: "📌 ชื่อสไลด์",
    content: `<div class="space-y-5">
        <p class="text-lg text-stone-700 leading-relaxed">เนื้อหาหลัก...</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div class="bg-[#fdf9f2] border-2 border-[#ebdcb9] p-6 rounded-2xl">
                <div class="text-4xl mb-3">📝</div>
                <h4 class="font-bold text-lg text-stone-800 mb-2">หัวข้อย่อย</h4>
                <p class="text-stone-600 text-base leading-relaxed">รายละเอียด...</p>
            </div>
            <!-- เพิ่ม card ได้อีก -->
        </div>
        <div class="bg-[#fffbeb] border border-[#fde68a] p-4 rounded-xl text-center text-base text-amber-800 font-semibold">
            🔑 สรุป: ข้อความสรุป
        </div>
    </div>`
},
```

**ตำแหน่งแก้ไข:** `const slideDeck = [` → เพิ่ม object ต่อท้าย array ก่อน `];`

---

## RECIPE 2 — เปลี่ยนชุดหัวข้อทั้งหมด (ทำ theme ใหม่แทน marian/mars/tutan)

**Prompt สั่ง AI:**
```
[CONTEXT BLOCK]

เปลี่ยนชุดหัวข้อ 3 หัวข้อในไฟล์ HTML จาก [หัวข้อเดิม] เป็น:
  หัวข้อ 1: [emoji] [ชื่อ] — key: "[id1]"
  หัวข้อ 2: [emoji] [ชื่อ] — key: "[id2]"
  หัวข้อ 3: [emoji] [ชื่อ] — key: "[id3]"

สิ่งที่ต้องแก้ทั้งหมด:
1. custom dropdown — ตัวเลือก 3 ข้อ + label ค่า default
2. data-value ใน .topic-dd-opt
3. updatePresentationTopic() — เงื่อนไข switch case
4. challenge card groups — id "challenges-[id1/2/3]"
5. tab IDs — "tab-[id1/2/3]"
6. localStorage keys — "reward-[id]-1", "reward-[id]-2", "reward-[id]-boss"
7. ใบความรู้ hero gradient + เนื้อหา
8. sidebar navigation items
แสดง diff ที่แก้ทุกจุด
```

---

## RECIPE 3 — เพิ่มใบความรู้ชุดใหม่ (knowledge sheet)

**Prompt สั่ง AI:**
```
[CONTEXT BLOCK]

เพิ่มใบความรู้ชุดใหม่ในไฟล์ HTML
หัวข้อ: "[ชื่อหัวข้อ]"  ID: "tab-[id]"
สี theme: [เลือก: ฟ้า (#0c4a6e) / ม่วง (#1e1b4b) / น้ำตาล (#78350f) / หรือระบุเอง]
เนื้อหา 3 section:
  01: [หัวข้อ] — [รายละเอียด]
  02: [หัวข้อ] — [รายละเอียด]
  03: [หัวข้อ] — [รายละเอียด]

ใช้โครงสร้างเดียวกับ #tab-marian (hero banner + content-wrap + 3 content-section + print-footer)
เพิ่ม tab button ใน sidebar ด้วย
```

**HTML Template ใบความรู้ — โครงสร้างหลัก:**
```html
<div id="tab-[id]" class="tab-content w-full hidden">
  <!-- toolbar no-print -->
  <div class="no-print flex flex-wrap justify-between items-center bg-white rounded-xl px-5 py-3 border border-[#ede7db] mb-4 shadow-sm gap-3">
    <span class="font-semibold text-stone-700">[emoji] ใบความรู้ — [ชื่อ]</span>
    <div class="flex gap-2">
      <!-- ปุ่ม print + zoom — copy จาก tab-marian -->
    </div>
  </div>
  <!-- hero -->
  <div class="print-hero relative rounded-2xl mb-4 overflow-hidden" style="background:linear-gradient(135deg,[COLOR1] 0%,[COLOR2] 60%,[COLOR3] 100%);min-height:140px">
    <div class="hero-main relative z-10 p-6 md:p-8">
      <div class="hero-label" style="font-size:14px;font-weight:700;color:[ACCENT];text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px">ใบความรู้ประกอบกิจกรรม · ชุดที่ N</div>
      <h2 style="font-size:clamp(26px,4vw,40px);font-weight:700;color:white;line-height:1.2;margin-bottom:8px">[emoji] [ชื่อหัวข้อ]</h2>
      <p class="hero-sub" style="font-size:16px;color:[ACCENT];font-weight:500">[คำบรรยาย]</p>
    </div>
  </div>
  <!-- content -->
  <div class="print-content pb-8">
    <div class="content-wrap" style="background:white;border:1.5px solid [BORDER];border-radius:16px;box-shadow:0 2px 16px rgba([RGB],.07);overflow:hidden">
      <!-- section 01 -->
      <div class="content-section" style="padding:28px 32px">
        <div style="display:flex;gap:16px;align-items:flex-start">
          <span class="sec-badge" style="background:[BG50];border:2px solid [BORDER300];color:[TEXT700];font-size:16px;font-weight:800;padding:6px 14px;border-radius:8px;white-space:nowrap;flex-shrink:0;line-height:1.4">01</span>
          <div style="flex:1">
            <h3 style="font-size:20px;font-weight:700;color:[TEXT900];margin-bottom:12px">[ชื่อ section]</h3>
            <p style="font-size:17px;color:[TEXT700];line-height:1.85">[เนื้อหา]</p>
          </div>
        </div>
      </div>
      <div style="border-top:1px dashed [BORDER200];margin:0 32px"></div>
      <!-- section 02, 03 — ทำซ้ำแบบเดียวกัน -->
    </div>
  </div>
  <div class="print-footer">* สแกนด้วยแอป Google Drive แล้วอัปโหลดไปไขปมเกมใน NotebookLM ได้เลย! *</div>
</div>
```

---

## RECIPE 4 — เพิ่ม / แก้ด่านใหม่ใน Gameboard

**Prompt สั่ง AI:**
```
[CONTEXT BLOCK]

เพิ่มด่านใหม่ในกลุ่ม challenges-[topic] ของ #tab-gameboard
ด่าน: [ด่านที่ 1 🟢 / ด่านที่ 2 🟡 / BOSS 🔴]
ชื่อด่าน: "[ชื่อ]"
โจทย์ที่ให้นักเรียนทำใน NotebookLM: "[โจทย์]"
เงื่อนไขรับรางวัล: "[เงื่อนไข]"
reward-key: "[topic]-[tier]"

ใช้โครงสร้าง .chal-card เดิม สีตามด่าน:
  ด่าน 1 = #059669 (emerald) / ด่าน 2 = #d97706 (amber) / BOSS = #dc2626 (red)
```

**HTML Template card:**
```html
<div class="chal-card rounded-2xl overflow-hidden shadow mb-4" data-locked="true">
  <!-- header -->
  <div style="background:[TIER_COLOR];padding:16px 22px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
    <span style="font-size:22px">[emoji]</span>
    <div style="flex:1">
      <div style="font-size:11px;font-weight:700;color:rgba(255,255,255,.75);text-transform:uppercase;letter-spacing:.08em">[TIER LABEL]</div>
      <div style="font-size:18px;font-weight:700;color:white">[ชื่อด่าน]</div>
    </div>
    <span style="background:rgba(255,255,255,.22);color:white;font-size:12px;font-weight:700;padding:4px 14px;border-radius:20px">[ด่านที่ N]</span>
    <button onclick="toggleLock(this.closest('.chal-card'))" class="btn-lock-open" style="background:rgba(255,255,255,.95);color:[TIER_COLOR];border:none;padding:8px 18px;border-radius:8px;font-weight:700;cursor:pointer;font-size:14px">เปิดด่านนี้</button>
  </div>
  <!-- locked state -->
  <div class="chal-locked" style="background:#f5f5f4;padding:28px;display:flex;align-items:center;justify-content:center;gap:12px">
    <span style="font-size:32px">🔒</span>
    <span style="font-size:16px;font-weight:700;color:#78716c">ด่านนี้ยังล็อกอยู่</span>
  </div>
  <!-- body -->
  <div class="chal-body" style="background:#fafaf9;padding:18px 22px;border-left:5px solid [TIER_COLOR];border-right:1px solid #e7e5e4;border-bottom:1px solid #e7e5e4">
    <p style="font-size:14px;font-weight:700;color:#57534e;margin-bottom:10px">โจทย์ — ให้นักเรียนทำใน NotebookLM:</p>
    <div class="prompt-box" onclick="copyPromptText(this)" style="background:white;border:2px solid #e7e5e4;border-radius:12px;padding:16px 20px;font-size:17px;font-weight:600;color:#1c1917;cursor:pointer;line-height:1.7">[โจทย์]</div>
    <div style="margin-top:14px;background:[TIER_LIGHT];border:1px solid [TIER_BORDER];border-radius:10px;padding:14px 18px">
      <div style="font-size:11px;font-weight:700;color:[TIER_TEXT_DARK];text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">🎁 เงื่อนไขรับรางวัล:</div>
      <p contenteditable="true" data-reward-key="[topic]-[tier]" oninput="saveRewardText(this)" style="font-size:15px;font-weight:600;color:#292524;line-height:1.7;margin:0">[เงื่อนไข]</p>
    </div>
  </div>
</div>
```

---

## RECIPE 5 — เปลี่ยนเนื้อหาสไลด์ทั้งชุด (ไม่แตะ design)

**Prompt สั่ง AI:**
```
[CONTEXT BLOCK]

เขียน slideDeck[] array ใหม่ทั้งหมด (แทนที่ของเดิม)
หัวข้อการสอน: "[ชื่อเรื่อง]"
จำนวนสไลด์: [N] สไลด์
เนื้อหา:
  สไลด์ 1 — [บอกสิ่งที่สอน]
  สไลด์ 2 — [...]
  ...

ข้อกำหนด:
- ใช้ Tailwind utility classes + inline style เดิม ห้ามเพิ่ม class ใหม่
- สี: amber (#d97706 / #b45309), stone, white เท่านั้น
- ฟอนต์: Sarabun — ตัวหนา font-bold, body text-stone-700
- แต่ละสไลด์มี content ที่ readable บนหน้าจอ 16:9 และพิมพ์ได้เป็น A4 landscape
- ห้ามใช้ animation หรือ transition ใน content
```

---

## RECIPE 6 — Debug / แก้ปัญหา layout

**Prompt สั่ง AI:**
```
[CONTEXT BLOCK]

ปัญหาที่พบ: [อธิบายอาการ เช่น "ปุ่มถัดไปหายเมื่อสไลด์เนื้อหาเยอะ"]
ส่วนที่น่าจะเกี่ยวข้อง: [ระบุ element / CSS class ถ้าทราบ]

ช่วย:
1. วิเคราะห์สาเหตุ
2. แสดง CSS/JS ที่ต้องแก้ระบุ line หรือ selector ชัดเจน
3. อธิบายว่าทำไมถึงแก้ได้
```

---

## Design Tokens (Reference สำหรับแนบกับ Prompt)

```
สี:
  amber-600  #d97706  — ปุ่ม active, hover, focus ring
  amber-700  #b45309  — text header, section heading
  stone-900  #1c1917  — heading หลัก, ปุ่ม "ถัดไป"
  stone-800  #292524  — body text
  bg-page    #faf7f0  — พื้นหลังหน้า
  bg-slide   #fffdfa  — slide deck container
  border     #ede7db  — card border ทั่วไป

  theme มาเรียนา : #0c4a6e → #0369a1 → #164e63
  theme ดาวอังคาร: #1e1b4b → #4338ca → #312e81
  theme ตุตัน    : #78350f → #b45309 → #451a03

ด่าน:
  ด่าน 1 (Flashcard)   #059669 emerald
  ด่าน 2 (Infographic) #d97706 amber
  BOSS   (Video)        #dc2626 red

Typography:
  font-family: 'Sarabun', sans-serif
  body ใบความรู้ : 17px / line-height 1.85
  heading section: 20px / font-weight 700
  reward text    : 15px / font-weight 600 / line-height 1.7

Radius:
  16px = rounded-2xl  (slide deck, hero, challenge card, content-wrap)
  12px = rounded-xl   (sidebar, toolbar, dropdown list)
   8px = rounded-lg   (button, badge, prompt-box)
```
