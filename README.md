# 🤖 AcademicForward — AI Agent & Knowledge Framework Hub

ศูนย์รวมสถาปัตยกรรม AI Agent, กฎมาตรฐานวิจัย (มรนว. 2568 + APA 7th Edition), ชุดผลิตตำราเรียน, และเครื่องมือสนับสนุนการศึกษายุคใหม่

---

## 🧭 แผนผังเส้นทางการใช้งาน (3 Main Tracks)

```text
academicforward/
├── 🎓 Academic/              # สำหรับงานวิจัย วิทยานิพนธ์ ตำราเรียน และฐานข้อมูล
├── 🎮 Classroom/             # สำหรับอาจารย์ สื่อการสอน สไลด์ และโพสต์โซเชียลหอสมุด
└── 🛠️ Dev-Tools/              # สำหรับนักพัฒนา โค้ด สถาปัตยกรรม โปรไฟล์ และความปลอดภัย
```

---

## 📂 1. 🎓 Academic Track ([Academic/](Academic))

ออกแบบมาสำหรับนักศึกษา (ป.ตรี/โท/เอก), นักวิจัย และอาจารย์ผู้เขียนตำรา

* ⚡ **[zero-bloat-workflow.md](Academic/zero-bloat-workflow.md)** — **(แนะนำสำหรับสายฟรี)** คู่มือทำงานวิจัยแบบไม่ให้ Context บวม เร็วขึ้น 5 เท่า และฟรี 100%

### 🔬 Research Agents ([Academic/Research-Agents/](Academic/Research-Agents))
* ⚡ **[core-rules-lite.md](Academic/Research-Agents/core-rules-lite.md)** — กฎเหล็ก 4 ข้อฉบับกระชับ (~800 Tokens) สำหรับใส่ System Prompt / โมเดลบัญชีฟรี
* 📌 **[core-rules-full.md](Academic/Research-Agents/core-rules-full.md)** — กฎและมาตรฐานกลางฉบับเต็ม (มรนว. 2568 + APA 7th)
* 🚀 **[quickstart-guide.md](Academic/Research-Agents/quickstart-guide.md)** — คู่มือเริ่มต้นใช้งานรวดเร็ว
* 📖 **[architecture-guide.md](Academic/Research-Agents/architecture-guide.md)** — คู่มือสถาปัตยกรรมและรายละเอียดระบบ
* 🎓 **[undergrad-research-agent.md](Academic/Research-Agents/undergrad-research-agent.md)** — เอเจนต์โค้ชสำหรับนักศึกษาปริญญาตรี (รายงานวิจัย 5 บท)
* 🔬 **[grad-research-agent.md](Academic/Research-Agents/grad-research-agent.md)** — เอเจนต์ที่ปรึกษาบัณฑิตศึกษา (Thesis / IS / Proposal)
* 🧪 **[researcher-manuscript-agent.md](Academic/Research-Agents/researcher-manuscript-agent.md)** — เอเจนต์ Peer Review ตรวจและวิเคราะห์ Manuscript วารสาร
* 📚 **[jit-apa7-formatter.md](Academic/Research-Agents/jit-apa7-formatter.md)** — ตัวจัดบรรณานุกรมอัตโนมัติตอนจบบท (Just-In-Time)

### 📚 Textbook Suite ([Academic/Textbook-Agent/](Academic/Textbook-Agent))
* 📖 **[README.md](Academic/Textbook-Agent/README.md)** — ภาพรวมกระบวนการสร้างตำรา 4 ขั้นตอน
* 🗂️ **[textbook-structure-agent.md](Academic/Textbook-Agent/textbook-structure-agent.md)** — ขั้น 0 วางโครงสร้างเล่ม ผลลัพธ์การเรียนรู้ (CLO) และคีย์เวิร์ด
* ✍️ **[textbook-writer-agent.md](Academic/Textbook-Agent/textbook-writer-agent.md)** — ขั้น 3 เรียบเรียงเนื้อหาตำราทีละหัวข้อย่อยแบบร้อยแก้วต่อเนื่อง

### 🌐 Database Guides ([Academic/Database-Guides/](Academic/Database-Guides))
* 🔍 **[academic-search-keywords.md](Academic/Database-Guides/academic-search-keywords.md)** — คลังสะพานเชื่อมคำค้นภาษาไทย ↔ คีย์เวิร์ดสากล
* 💡 **[academic-database-prompts.md](Academic/Database-Guides/academic-database-prompts.md)** — ชุดคำสั่ง Prompt สำหรับสืบค้นฐานข้อมูลวิชาการ
* 📄 **[research-synthesis-guide-2569.pdf](Academic/Database-Guides/research-synthesis-guide-2569.pdf)** — เอกสารสังเคราะห์และเรียบเรียงข้อมูลงานวิจัย

---

## 📂 2. 🎮 Classroom Track ([Classroom/](Classroom))

เครื่องมือสำหรับอาจารย์และงานสื่อสารองค์กร/หอสมุด

* 🚀 **[slide-hub-agent.md](Classroom/slide-hub-agent.md)** — Suite รวมระบบสไลด์ 16:9 + กระดานเล่นเกมแบบปลดล็อกด่าน + ใบงาน A4 Print-ready และ Design Tokens ในไฟล์เดียว
* 📱 **[arit-social-post-agent.md](Classroom/arit-social-post-agent.md)** — เอเจนต์ร่างโพสต์ Facebook/Social Media ของสำนักวิทยบริการและเทคโนโลยีสารสนเทศ (ARIT NSRU / หอสมุดกลาง)

---

## 📂 3. 🛠️ Dev & Utility Track ([Dev-Tools/](Dev-Tools))

เครื่องมือ สคริปต์อัตโนมัติ และแม่แบบบริบทการทำงานส่วนตัว

* 👤 **[user-master-profile.md](Dev-Tools/user-master-profile.md)** — แม่แบบบันทึกโปรไฟล์ ความชอบ และสมองสำรองคุมโครงการส่วนตัว
* 💻 **[code-developer-agent.md](Dev-Tools/code-developer-agent.md)** — ผู้เชี่ยวชาญการเขียนโค้ด วิเคราะห์ระบบ และแก้ไขบั๊ก
* 📊 **[flowchart-diagram-agent.md](Dev-Tools/flowchart-diagram-agent.md)** — ออกแบบ Diagram, Flowchart และ Architecture
* 🛡️ **[wp-security-audit-guide.md](Dev-Tools/wp-security-audit-guide.md)** — คู่มือตรวจสอบความปลอดภัย WordPress
* 🔒 **[skills/gdrive-permission-restriction](Dev-Tools/skills/gdrive-permission-restriction)** — Antigravity Skill ควบคุมสิทธิ์การดาวน์โหลดไฟล์ใน Google Drive

---

## 📜 4. Framework Rules ([Framework-Rules/](Framework-Rules))
* 📄 **[Framework-Rules/README.md](Framework-Rules/README.md)** — พื้นที่สำรองสำหรับ Global System Rules ในอนาคต

---

> *มาตรฐานการตั้งชื่อ: Precise Kebab-Case Standard (`[domain]-[role/task]-[type].md`)*
