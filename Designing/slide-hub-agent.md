# 🎮 Interactive Slide & Classroom Play Hub Suite

> **ใช้ร่วมกับ**: [textbook-structure-agent.md](textbook-structure-agent.md) (โครงเนื้อหาก่อนทำสไลด์) · [flowchart-diagram-agent.md](flowchart-diagram-agent.md) (ผังในสไลด์) · [../Writing/4-textbook-writer.md](../Writing/4-textbook-writer.md)

> **เอกสารคู่มือและ Agent ประจำชุดสำหรับการออกแบบสื่อการสอนเชิงปฏิสัมพันธ์ (Classroom Play Hub & Slides)**
> รวมทั้งส่วนของ **Engine โครงสร้างเนื้อหา/เกม** และ **Design System (Color Tokens, Typography, Layout)** ไว้ในที่เดียว

---

## 1. บทบาทและผลลัพธ์ (Deliverables)

Agent ประจำชุดนี้ทำหน้าที่สร้างและปรับแต่งหน้าเว็บสื่อการสอน HTML ไฟล์เดียว (`deck.html` หรือ `playhub.html`) ที่เปิดในเบราว์เซอร์และใช้งานได้ทันที ประกอบด้วย 4 ระบบหลัก:

| ระบบ | หน้าที่และการทำงาน |
| :--- | :--- |
| **🚀 สไลด์การสอน (Presentation)** | สไลด์ 16:9 ควบคุมด้วยแป้นลูกศร/Esc รองรับ Fullscreen และเชื่อมต่อไปยังโหมดเกม |
| **📺 กระดานเล่นเกม (Game Board)** | กระดานฉายโจทย์หน้าห้อง ปลดล็อกทีละด่าน (Level 1, 2 และ BOSS) รองรับการคลิกคัดลอกคำถาม |
| **🖨️ ใบความรู้ A4 (Printable Worksheets)** | ใบงานความรู้รายหัวข้อ จัดหน้า A4 อัตโนมัติเมื่อกดสั่งพิมพ์ (Ctrl+P / ปุ่ม Print) |
| **🧭 การนำทาง (Interactive Sidebar)** | เมนูเชื่อมโยงหัวข้อและสลับด่านกิจกรรมอัตโนมัติ |

---

## 2. โครงสร้าง Configuration Schema (`const HUB = {...}`)

ผู้ใช้และ AI สามารถสร้างฮับบทเรียนใหม่ได้โดยแก้ไขเพียงก้อน `HUB` Config นี้:

```javascript
const HUB = {
  brandEmoji: "✨",
  title: "ชื่อบทเรียน — หัวข้อหลัก",

  // ── 1. สไลด์นำเสนอ ──
  slides: [
    { 
      title: "🎯 หัวข้อสไลด์",
      content: `<p class="body">เนื้อหาสไลด์ที่ต้องการนำเสนอ...</p>`
    }
  ],

  // ── 2. หัวข้อบทเรียน + ด่านเกม + ใบงาน A4 ──
  topics: [
    {
      id: "topicA",
      emoji: "🌊",
      navLabel: "ชื่อหัวข้อย่อย 1",

      palette: {
        heroGradient: "linear-gradient(135deg,#0c4a6e 0%,#0369a1 60%,#164e63 100%)",
        heroLabel: "#7dd3fc",
        heroSub:   "#bae6fd",
        accent:    "#0ea5e9",
        accentDark:"#0c4a6e",
        accentMid: "#0369a1",
        badgeBg:   "#f0f9ff",
        badgeBorder:"#7dd3fc",
        badgeText: "#0369a1",
        wrapBorder:"#e0f2fe",
        divider:   "#bae6fd",
        body:      "#1e3a5f"
      },

      mission: "🌊 ภารกิจสืบค้นสารสนเทศ",
      challenges: [
        { level: "ด่านที่ 1", color: "#059669", title: "🃏 Flashcards Challenge", tool: "Flashcards",
          prompt: "จงสรุปความหมายของ ... จากใบความรู้", reward: "รับแต้มทีม +10" },
        { level: "ด่านที่ 2", color: "#d97706", title: "📊 Infographic Analysis", tool: "Infographic",
          prompt: "เปรียบเทียบข้อดีข้อเสียระหว่าง ...", reward: "รับแต้มทีม +20" },
        { level: "BOSS", boss: true, color: "#dc2626", title: "⚡ Ultimate Quest", tool: "Video + Quiz",
          prompt: "ออกแบบแนวทางประยุกต์ใช้ ... กับโจทย์ปัญหาจริง", reward: "รับรางวัลใหญ่ +50" }
      ],

      sheetKicker: "ใบความรู้ประกอบกิจกรรม · ชุดที่ 1",
      sheetTitle:  "🌊 ชื่อใบความรู้เรื่อง...",
      sheetSub:    "คำอธิบายสังเขปของใบงาน",
      sections: [
        { n: "01", title: "หลักการสำคัญ", html: `<p>เนื้อหาสาระสำคัญ...</p>` },
        { n: "02", title: "แนวทางการปฏิบัติ", html: `<p>รายละเอียดขั้นตอน...</p>` }
      ]
    }
  ]
};
```

---

## 3. Design Tokens & Styling Guide

### 3.1 Color System
* **Primary Accent:** `#d97706` (Amber — จุดเด่น, CTA, ไฮไลต์สำคัญ)
* **Stone Neutrals (โทนอุ่น):**
  * Dark Section Background: `#2e2b28`
  * Card Titles & Headers: `#3d3a37`
  * Body Text: `#6b6762`
  * Background: `#faf7f0` (Main), `#fffdfa` (Slide)
* **Semantic Status Colors:**
  * เขียว: `#059669` (สำเร็จ / Level 1)
  * ส้ม: `#d97706` (กำลังทำ / Level 2)
  * แดง: `#dc2626` (คำเตือน / BOSS Level)

### 3.2 Typography
* **Font-family:** `'Prompt'`, `'Sarabun'`, sans-serif
* **Header ขนาดใหญ่ (H1/Hero):** 48–72px ตัวหนา (Weight 700-800)
* **หัวข้อสไลด์ (H2):** 36–52px
* **เนื้อหา (Body):** 18–26px line-height 1.6–1.8
