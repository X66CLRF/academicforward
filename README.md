# 🤖 AcademicForward — AI Agent & Knowledge Framework Hub

ศูนย์รวมสถาปัตยกรรม AI Agent, กฎมาตรฐานวิจัย (มรนว. 2568 + APA 7th Edition), ชุดผลิตตำราเรียน, และเครื่องมือสนับสนุนการศึกษายุคใหม่

[![Version](https://img.shields.io/badge/Version-v6.0_Zero--Bloat-blue.svg)](Academic/zero-bloat-workflow.md)
[![Standard](https://img.shields.io/badge/Standard-NSRU_2568_%7C_APA_7th-success.svg)](Academic/Research-Agents/core-rules-full.md)
[![Updated](https://img.shields.io/badge/Updated-August_2026-orange.svg)](#-ตารางเวอร์ชันและประวัติการปรับปรุง-master-release-matrix)

---

## 🧭 แผนผังเส้นทางการใช้งาน (3 Main Tracks)

```text
academicforward/
├── 🎓 Academic/              # สำหรับงานวิจัย วิทยานิพนธ์ ตำราเรียน และฐานข้อมูล
├── 🎮 Classroom/             # สำหรับอาจารย์ สื่อการสอน สไลด์ และโพสต์โซเชียลหอสมุด
└── 🛠️ Dev-Tools/              # สำหรับนักพัฒนา โค้ด สถาปัตยกรรม โปรไฟล์ และความปลอดภัย
```

---

## 📊 ตารางเวอร์ชันและประวัติการปรับปรุง (Master Release Matrix)

| หมวดหมู่ | ไฟล์ / ชุดเครื่องมือ | เวอร์ชัน | ปรับปรุงล่าสุด | สถานะความพร้อม |
| :--- | :--- | :---: | :---: | :---: |
| 🎓 **Academic** | [zero-bloat-workflow.md](Academic/zero-bloat-workflow.md) | `v1.0` | 23 ส.ค. 2569 | 🟢 พร้อมใช้งาน (สายฟรี) |
| 🎓 **Academic** | [Research-Agents/core-rules-lite.md](Academic/Research-Agents/core-rules-lite.md) | `v1.0` | 23 ส.ค. 2569 | 🟢 พร้อมใช้งาน (~800 Tokens) |
| 🎓 **Academic** | [Research-Agents/core-rules-full.md](Academic/Research-Agents/core-rules-full.md) | `v5.6` | 26 ก.ค. 2569 | 🟢 พร้อมใช้งาน (ฉบับเต็ม) |
| 🎓 **Academic** | [Research-Agents/undergrad-research-agent.md](Academic/Research-Agents/undergrad-research-agent.md) | `v5.6` | 26 ก.ค. 2569 | 🟢 พร้อมใช้งาน (ป.ตรี) |
| 🎓 **Academic** | [Research-Agents/grad-research-agent.md](Academic/Research-Agents/grad-research-agent.md) | `v5.6` | 26 ก.ค. 2569 | 🟢 พร้อมใช้งาน (ป.โท/เอก) |
| 🎓 **Academic** | [Research-Agents/researcher-manuscript-agent.md](Academic/Research-Agents/researcher-manuscript-agent.md) | `v5.6` | 26 ก.ค. 2569 | 🟢 พร้อมใช้งาน (นักวิจัย) |
| 🎓 **Academic** | [Research-Agents/jit-apa7-formatter.md](Academic/Research-Agents/jit-apa7-formatter.md) | `v1.0` | 23 ส.ค. 2569 | 🟢 พร้อมใช้งาน (จบบท) |
| 📚 **Textbook** | [Textbook-Agent/textbook-structure-agent.md](Academic/Textbook-Agent/textbook-structure-agent.md) | `v1.6` | 26 ก.ค. 2569 | 🟢 พร้อมใช้งาน (ขั้น 0) |
| 📚 **Textbook** | [Textbook-Agent/textbook-writer-agent.md](Academic/Textbook-Agent/textbook-writer-agent.md) | `v5.8` | 26 ก.ค. 2569 | 🟢 พร้อมใช้งาน (ขั้น 3) |
| 🌐 **Database** | [Database-Guides/academic-search-keywords.md](Academic/Database-Guides/academic-search-keywords.md) | `v2.0` | 23 ส.ค. 2569 | 🟢 พร้อมใช้งาน |
| 🌐 **Database** | [Database-Guides/academic-database-prompts.md](Academic/Database-Guides/academic-database-prompts.md) | `v2.0` | 23 ส.ค. 2569 | 🟢 พร้อมใช้งาน |
| 🎮 **Classroom** | [Classroom/slide-hub-agent.md](Classroom/slide-hub-agent.md) | `v2.0` | 23 ส.ค. 2569 | 🟢 พร้อมใช้งาน |
| 📱 **Classroom** | [Classroom/arit-social-post-agent.md](Classroom/arit-social-post-agent.md) | `v2.0` | 23 ส.ค. 2569 | 🟢 พร้อมใช้งาน (เพจ ARIT) |
| 🛠️ **Dev-Tools** | [Dev-Tools/user-master-profile.md](Dev-Tools/user-master-profile.md) | `v2.0` | 23 ส.ค. 2569 | 🟢 พร้อมใช้งาน |
| 🛠️ **Dev-Tools** | [Dev-Tools/code-developer-agent.md](Dev-Tools/code-developer-agent.md) | `v1.0` | 12 มิ.ย. 2569 | 🟢 พร้อมใช้งาน |
| 🛠️ **Dev-Tools** | [Dev-Tools/flowchart-diagram-agent.md](Dev-Tools/flowchart-diagram-agent.md) | `v1.0` | 7 มิ.ย. 2569 | 🟢 พร้อมใช้งาน |
| 🔒 **Dev-Tools** | [Dev-Tools/skills/gdrive-permission-restriction](Dev-Tools/skills/gdrive-permission-restriction) | `v1.0` | 8 ส.ค. 2569 | 🟢 พร้อมใช้งาน (Skill) |

---

## 📂 สารบัญแยกตามหมวดหมู่ (Folder Tracks)

### 1. 🎓 [Academic Track (งานวิจัย & ตำราเรียน)](Academic/)
* ⚡ **[zero-bloat-workflow.md](Academic/zero-bloat-workflow.md)** — คู่มือการทำงานวิจัยสายฟรี 100% ไม่ให้ Context บวม
* 🔬 **[Research-Agents/](Academic/Research-Agents/)** — ชุดเอเจนต์เขียนงานวิจัย 5 บท / Thesis / IS / Manuscript พร้อมกฎ มรนว. 2568
* 📚 **[Textbook-Agent/](Academic/Textbook-Agent/)** — ชุดกระบวนการผลิตตำราเรียนและเอกสารประกอบการสอน 4 ขั้นตอน
* 🌐 **[Database-Guides/](Academic/Database-Guides/)** — คลังสะพานคำค้นไทย-อังกฤษ และพรอมท์สืบค้นฐานข้อมูลวิชาการ

### 2. 🎮 [Classroom Track (สื่อการสอน & สื่อสารองค์กร)](Classroom/)
* 🚀 **[slide-hub-agent.md](Classroom/slide-hub-agent.md)** — Suite รวมระบบสไลด์ 16:9 + กระดานเล่นเกมแบบปลดล็อกด่าน + ใบงาน A4 Print-ready
* 📱 **[arit-social-post-agent.md](Classroom/arit-social-post-agent.md)** — เอเจนต์ร่างโพสต์ Facebook/Social Media ของสำนักวิทยบริการฯ (ARIT NSRU)

### 3. 🛠️ [Dev & Utility Track (เครื่องมือระบบ & โปรไฟล์)](Dev-Tools/)
* 👤 **[user-master-profile.md](Dev-Tools/user-master-profile.md)** — แม่แบบบันทึกโปรไฟล์ ความชอบ และสมองสำรองคุมโครงการส่วนตัว
* 💻 **[code-developer-agent.md](Dev-Tools/code-developer-agent.md)** — ผู้เชี่ยวชาญการเขียนโค้ด วิเคราะห์ระบบ และแก้ไขบั๊ก
* 📊 **[flowchart-diagram-agent.md](Dev-Tools/flowchart-diagram-agent.md)** — ออกแบบ Diagram, Flowchart และ Architecture
* 🛡️ **[wp-security-audit-guide.md](Dev-Tools/wp-security-audit-guide.md)** — คู่มือตรวจสอบความปลอดภัย WordPress
* 🔒 **[skills/gdrive-permission-restriction](Dev-Tools/skills/gdrive-permission-restriction)** — Antigravity Skill ควบคุมสิทธิ์การดาวน์โหลดไฟล์ใน Google Drive

### 4. 📜 [Framework Rules](Framework-Rules/)
* 📄 **[Framework-Rules/README.md](Framework-Rules/README.md)** — พื้นที่สำรองสำหรับ Global System Rules ในอนาคต

---

> *ปรับปรุงล่าสุด: 23 สิงหาคม 2569 | มาตรฐาน: Kebab-Case Standard + Zero-Bloat Edition*
