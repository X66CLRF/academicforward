# 💻 Automation Suite — เครื่องมืออัตโนมัติสนับสนุนงานวิชาการ

> รวมเครื่องมือและสคริปต์อัตโนมัติที่ช่วยจัดการไฟล์และสิทธิ์เอกสารในสถาบันการศึกษา

---

## 📂 สารบัญเครื่องมือ
- 🔒 **[gdrive-permission-agent.md](gdrive-permission-agent.md)** — สคริปต์อัตโนมัติควบคุมและล็อกสิทธิ์ดาวน์โหลด/คัดลอกไฟล์ใน Google Drive แบบกลุ่ม (Batch) รวดเร็ว ปลอดภัย ผ่าน Windows Credential Manager
- 🧬 **[docx-safe-edit-agent.md](docx-safe-edit-agent.md)** — แก้ข้อความในไฟล์ `.docx` ที่จัดรูปแบบไว้แล้วโดยฟอร์แมตไม่พัง (แทนที่เฉพาะ `<w:t>` โคลนย่อหน้าเดิมเมื่อเพิ่มรายการ) + snapshot/restore อัตโนมัติ + แทนรูปโดยคงเฟรมและสัดส่วน + แนวทางยืมเล่มคนอื่นมาเป็นเทมเพลท

> สคริปต์อยู่ที่ [`Evaluation/scripts/`](../Evaluation/scripts/) — `docxkit.py` `slots.py` `split_appendix.py` `cite.py` `org.py`
