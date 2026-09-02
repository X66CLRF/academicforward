# 💻 Automation Suite — เครื่องมืออัตโนมัติสนับสนุนงานวิชาการ

> รวมเครื่องมือและสคริปต์อัตโนมัติที่ช่วยผลิตไฟล์ จัดการไฟล์ และควบคุมสิทธิ์เอกสารในสถาบันการศึกษา

---

## 📂 สารบัญเครื่องมือ
- 🔒 **[gdrive-permission-agent.md](gdrive-permission-agent.md)** — สคริปต์อัตโนมัติควบคุมและล็อกสิทธิ์ดาวน์โหลด/คัดลอกไฟล์ใน Google Drive แบบกลุ่ม (Batch) รวดเร็ว ปลอดภัย ผ่าน Windows Credential Manager
- 🧱 **[docx-builder.md](docx-builder.md)** — **สร้าง** ไฟล์ `.docx` ขึ้นใหม่จากศูนย์ ผูกทุกค่าไว้ที่ Word Styles แทนการจัดรูปแบบโดยตรง แก้บั๊กอักษรเชิงซ้อนของ `python-docx` ที่ทำให้ Word ตัดคำภาษาไทยผิด มาตรฐานตารางและคำบรรยาย พร้อมด่านตรวจ 10 ข้อก่อนส่งมอบ
- 🧬 **[docx-safe-edit-agent.md](docx-safe-edit-agent.md)** — แก้ข้อความในไฟล์ `.docx` ที่จัดรูปแบบไว้แล้วโดยฟอร์แมตไม่พัง (แทนที่เฉพาะ `<w:t>` โคลนย่อหน้าเดิมเมื่อเพิ่มรายการ) + snapshot/restore อัตโนมัติ + แทนรูปโดยคงเฟรมและสัดส่วน + แนวทางยืมเล่มคนอื่นมาเป็นเทมเพลท

> 🐍 **ไลบรารีกลาง** [`Automation/scripts/`](scripts/) — `docx_core.py` (ตัวสร้าง) · `check_docx.py` (ด่านตรวจ) · `example_report.py` (ตัวอย่างพร้อมก๊อป)
> ใช้ร่วมกันได้ทุกงานเอกสาร ไม่ผูกกับวิชาหรือสถาบันใด

> **เลือกให้ถูกตัว** — สร้างไฟล์ใหม่ใช้ `docx-builder` · แก้ไฟล์ที่มีอยู่แล้วใช้ `docx-safe-edit-agent`

> สคริปต์อยู่ที่ [`Evaluation/scripts/`](../Evaluation/scripts/) — `docxkit.py` `slots.py` `split_appendix.py` `cite.py` `org.py`
