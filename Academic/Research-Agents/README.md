# 🔬 Research Agents Suite — ชุดผู้ช่วยวิจัย มรนว. 2568 (APA 7th)

> **เวอร์ชัน**: Suite v6.0 | **ปรับปรุงล่าสุด**: 23 สิงหาคม 2569  
> **มาตรฐาน**: มรนว. ฉบับปรับปรุง พ.ศ. 2568 + APA 7th Edition

ชุด AI Agent สำหรับช่วยนักศึกษาและนักวิจัยในการค้นคว้า สังเคราะห์วรรณกรรม (บทที่ 2) และเขียนเล่มวิจัยตามมาตรฐานมหาวิทยาลัยราชภัฏนครสวรรค์

---

## 📂 สารบัญไฟล์ในชุด Research Agents

| ไฟล์ | ประเภท | หน้าที่และกลุ่มผู้ใช้ |
| :--- | :---: | :--- |
| ⚡ **[core-rules-lite.md](core-rules-lite.md)** | `Prompt` | **(แนะนำ)** กฎเหล็ก 4 ข้อฉบับกระชับ (~800 Tokens) สำหรับโมเดลฟรี/System Prompt |
| 📌 **[core-rules-full.md](core-rules-full.md)** | `Reference` | กฎระเบียบและมาตรฐานกลางฉบับสมบูรณ์ (143 KB) สำหรับอ้างอิงละเอียด |
| 🎓 **[undergrad-research-agent.md](undergrad-research-agent.md)** | `Agent` | ผู้ช่วยสำหรับนักศึกษา ป.ตรี (เน้นสอนเป็นขั้นเป็นตอน รายงาน 5 บท) |
| 🔬 **[grad-research-agent.md](grad-research-agent.md)** | `Agent` | ผู้ช่วยบัณฑิตศึกษา ป.โท/เอก (เน้น Proposal, Thesis/IS, Methodology) |
| 🧪 **[researcher-manuscript-agent.md](researcher-manuscript-agent.md)** | `Agent` | ผู้ช่วยนักวิจัย ตรวจและวิเคราะห์ Manuscript สำหรับตีพิมพ์วารสาร |
| 📚 **[jit-apa7-formatter.md](jit-apa7-formatter.md)** | `JIT Tool` | คำสั่งจัดบรรณานุกรมท้ายบท (ป้อนเฉพาะตอนจบบท) |
| 🚀 **[quickstart-guide.md](quickstart-guide.md)** | `Guide` | คู่มือสอนใช้งานสำหรับผู้เริ่มต้น (อ่าน 5 นาที) |
| 📖 **[architecture-guide.md](architecture-guide.md)** | `Guide` | รายละเอียดสถาปัตยกรรมและกฎความปลอดภัยเบื้องหลัง |

---

## 💡 วิธีการนำไปใช้งาน
1. **คัดลอกไฟล์กฎ:** นำ `core-rules-lite.md` ไปใส่ใน System Prompt หรือ Custom Instructions
2. **คัดลอกไฟล์ Agent:** นำ Agent ตามระดับของคุณ (เช่น `grad-research-agent.md`) วางในช่องแชท
3. **ส่งวัตถุประสงค์:** ส่งหัวข้อวิจัยและวัตถุประสงค์บทที่ 1 เพื่อเริ่มวางโครงบทที่ 2
