# 🤖 AcademicForward — AI Agent & Knowledge Framework Hub

ศูนย์รวมสถาปัตยกรรม AI Agent และเครื่องมือวิชาการ มรนว. 2568 (APA 7th Edition) จัดระเบียบตาม **Action (สิ่งที่ต้องการทำ)**

[![Version](https://img.shields.io/badge/Version-v6.0_Action--Driven-blue.svg)](Writing/core-rules-lite.md)
[![Standard](https://img.shields.io/badge/Standard-NSRU_2568_%7C_APA_7th-success.svg)](Writing/core-rules-full.md)
[![Updated](https://img.shields.io/badge/Updated-August_2026-orange.svg)](#-ตารางเวอร์ชันและประวัติการปรับปรุง-master-release-matrix)

---

## 🧭 เลือกใช้งานตาม Action ที่คุณต้องการทำ:

```text
academicforward/
├── ✍️ Writing/       # สกิลสำหรับ "เขียน" (วิจัย 5 บท, วิทยานิพนธ์, Manuscript, ตำรา, บรรณานุกรม)
├── 🎨 Designing/     # สกิลสำหรับ "ออกแบบ" (สไลด์การสอน, โครงสร้างตำรา, ไดอะแกรม Flowchart)
├── 🔍 Searching/     # สกิลสำหรับ "สืบค้น" (คลังคำค้นหาฐานข้อมูลไทย-เทศ, พรอมท์สืบค้น)
├── 📢 Publishing/    # สกิลสำหรับ "เผยแพร่ & โพสต์" (แต่งโพสต์ Facebook/Social ARITC NSRU)
└── 💻 Automation/    # สกิลสำหรับ "พัฒนาโค้ด & จัดการระบบ" (เขียนโค้ด, สคริปต์ GDrive, โปรไฟล์ผู้ใช้)
```

---

## 📊 ตารางเวอร์ชันและประวัติการปรับปรุง (Master Release Matrix)

| Action | ไฟล์ / ชุดเครื่องมือ | เวอร์ชัน | หน้าที่หลัก |
| :--- | :--- | :---: | :--- |
| ✍️ **Writing** | [Writing/core-rules-lite.md](Writing/core-rules-lite.md) | `v1.0` | ⚡ กฎเหล็กฉบับเบาหวิว (~800 Tokens) สำหรับใส่แชทฟรี |
| ✍️ **Writing** | [Writing/core-rules-full.md](Writing/core-rules-full.md) | `v5.6` | 📌 กฎมาตรฐานกลางฉบับเต็ม มรนว. 2568 (APA 7th) |
| ✍️ **Writing** | [Writing/undergrad-research-agent.md](Writing/undergrad-research-agent.md) | `v5.6` | 🎓 เขียนรายงานวิจัย ป.ตรี (5 บท) |
| ✍️ **Writing** | [Writing/grad-research-agent.md](Writing/grad-research-agent.md) | `v5.6` | 🔬 เขียนวิทยานิพนธ์ / IS / Proposal ป.โท-เอก |
| ✍️ **Writing** | [Writing/researcher-manuscript-agent.md](Writing/researcher-manuscript-agent.md) | `v5.6` | 🧪 ตรวจและเขียน Manuscript ตีพิมพ์วารสาร |
| ✍️ **Writing** | [Writing/textbook-writer-agent.md](Writing/textbook-writer-agent.md) | `v5.8` | ✍️ เขียนเนื้อหาตำราเรียนแบบร้อยแก้วต่อเนื่อง |
| ✍️ **Writing** | [Writing/jit-apa7-formatter.md](Writing/jit-apa7-formatter.md) | `v1.0` | 📚 คำสั่งจัดฟอร์แมตบรรณานุกรมอัตโนมัติ (Just-In-Time) |
| 🎨 **Designing** | [Designing/slide-hub-agent.md](Designing/slide-hub-agent.md) | `v2.0` | 🚀 ออกแบบสไลด์ 16:9 + บอร์ดเกม + ใบงาน A4 |
| 🎨 **Designing** | [Designing/textbook-structure-agent.md](Designing/textbook-structure-agent.md) | `v1.6` | 🗂️ ออกแบบโครงสร้างเล่มตำรา & CLO & คีย์เวิร์ด |
| 🎨 **Designing** | [Designing/flowchart-diagram-agent.md](Designing/flowchart-diagram-agent.md) | `v1.0` | 📊 ออกแบบ Flowchart, Diagram และ Mermaid Architecture |
| 🔍 **Searching** | [Searching/academic-search-keywords.md](Searching/academic-search-keywords.md) | `v2.0` | 🔍 คลังสะพานคำค้นภาษาไทย ↔ อังกฤษรายฐานข้อมูล |
| 🔍 **Searching** | [Searching/academic-database-prompts.md](Searching/academic-database-prompts.md) | `v2.0` | 💡 ชุดคำสั่ง Prompt สำหรับสืบค้นฐานข้อมูลวิชาการ |
| 📢 **Publishing** | [Publishing/aritc-social-post-agent.md](Publishing/aritc-social-post-agent.md) | `v2.0` | 📱 แต่งโพสต์ Facebook/Social Media ของ ARITC NSRU |
| 💻 **Automation** | [Automation/user-master-profile.md](Automation/user-master-profile.md) | `v2.0` | 👤 แม่แบบโปรไฟล์ & สมองสำรองคุมโครงการส่วนตัว |
| 💻 **Automation** | [Automation/code-developer-agent.md](Automation/code-developer-agent.md) | `v1.0` | 💻 ผู้เชี่ยวชาญการเขียนโค้ด วิเคราะห์ระบบ และแก้บั๊ก |
| 🔒 **Automation** | [Automation/gdrive-permission-agent.md](Automation/gdrive-permission-agent.md) | `v2.0` | 🔒 เอเจนต์และสคริปต์ควบคุมสิทธิ์ดาวน์โหลดไฟล์ Google Drive |

---

> *อัปเดตล่าสุด: 23 สิงหาคม 2569 | มาตรฐาน: Flat Action-Oriented Architecture (`.md` Standard)*
