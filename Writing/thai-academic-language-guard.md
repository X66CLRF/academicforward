# 🧬 thai-academic-language-guard — คู่มือภาษาไทยวิชาการต้นฉบับ & ด่านกันติดเครื่องตรวจ

> **สำหรับ**: ใช้คู่กับไฟล์ชุดเขียนทุกเล่ม (1-undergrad / 2-grad / 3-manuscript / 4-textbook / 5-prose-cleaner / 6-argument-auditor) และงานเขียนไทยวิชาการทุกชิ้น
> **เวอร์ชัน**: Language Integrity v1.3 | **สถานะ**: เอกสารอ้างอิงเปิดอ่าน (ไฟล์ชุดเขียนแต่ละเล่มมีฉบับย่อฝังอยู่แล้ว จึงทำงานเดี่ยวได้ — 1-undergrad ข้อ 5.5 · 2-grad ข้อ 5.5 · 3-manuscript ข้อ 6.5 · 4-textbook ข้อ 3.5 · **ถ้าฉบับย่อขัดกับคู่มือนี้ ให้ถือคู่มือนี้ แล้วแก้ฉบับย่อให้ตรงทันที**)
> **จุดประสงค์**: ทำให้เนื้อความเป็นภาษาไทยวิชาการที่ผู้เขียนคิดเองจริง ศัพท์เฉพาะถูกบริบท ไม่ทิ้งร่องรอยงานแปลด้วยเครื่อง และการใช้ AI ที่เกิดขึ้นจริงตรงตามนโยบายของสำนักพิมพ์ปลายทาง
> **สองด่านที่ต่างกัน**: ข้อ 0–7 คือด่านภาษาและความซ้ำ · [ข้อ 8](thai-academic-language-guard/08-publisher-ai-policy.md) คือด่านนโยบายและการเปิดเผยของสำนักพิมพ์ ผ่านด่านแรกแล้วยังตกด่านหลังได้
> **ภาษาแปลถูกจับสามชั้น** เพราะปัญหาอยู่คนละระดับกัน — [ข้อ 2](thai-academic-language-guard/02-terminology-gate.md) จับที่ **คำ** · [ข้อ 12](thai-academic-language-guard/12-syntax-calque-gate.md) จับที่ **โครงประโยค** · [ข้อ 3](thai-academic-language-guard/03-thai-ai-tells.md) จับที่ **ย่อหน้า** และเมื่อจะเขียนขึ้นใหม่ ให้หยิบรูปประโยคจาก [ข้อ 13](thai-academic-language-guard/13-thai-pattern-bank.md) ไม่ใช่แปลจากอังกฤษ

---

## 📑 ดัชนีส่วน — อ่านไฟล์นี้ก่อน แล้วอ่านส่วนที่งานต้องใช้ให้ครบทั้งไฟล์

> คู่มือนี้แยกเป็นไฟล์ส่วนย่อย (2026-10-08) เพราะไฟล์เดียวยาวเกินที่เครื่องมืออ่านไฟล์อ่านได้ในครั้งเดียว agent จึงอ่านไม่ครบและพลาดกฎ — **เนื้อกฎทุกข้ออยู่ครบในไฟล์ส่วน ไม่มีการตัดหรือย่อ**
> วิธีอ่าน: เปิดส่วนที่ติด **ทุกครั้ง** เสมอ แล้วเปิดส่วนอื่นตามคอลัมน์ "อ่านเมื่อ" · ถ้าไม่แน่ใจว่าเกี่ยวไหม ให้เปิดอ่าน อย่าเดา
> เลขข้อ N ในคู่มือนี้ (เช่น ข้อ 2.2 กฎ 5, ข้อ 12.5) ตรงกับไฟล์ `NN-*.md` ในโฟลเดอร์ `thai-academic-language-guard/` (ข้อ 2.2 → `02-*.md`)

| ไฟล์ส่วน | หัวข้อ | อ่านเมื่อ |
| :--- | :--- | :--- |
| [00-detection-basics.md](thai-academic-language-guard/00-detection-basics.md) | 🎯 0. เข้าใจก่อนว่า "ติด" มีกี่แบบ | **ทุกครั้ง** · ผู้ใช้ถามเรื่องติด AI / ติดความซ้ำ / เครื่องตรวจ และเพื่อรู้ขอบเขตของคู่มือนี้ |
| [01-native-thai-draft.md](thai-academic-language-guard/01-native-thai-draft.md) | ✍️ 1. กฎเขียนไทยจากศูนย์ (Native Thai Draft Rule) | **ทุกครั้ง** · เขียนไทยจากต้นฉบับอังกฤษ หรือร่างไทยฟังเหมือนแปล |
| [02-terminology-gate.md](thai-academic-language-guard/02-terminology-gate.md) | 🔤 2. ด่านศัพท์เฉพาะ (Terminology Gate) — จุดที่พังบ่อยที่สุด | **ทุกครั้ง** · เลือกคำแปลศัพท์เฉพาะ วงเล็บอังกฤษ (Title Case) GLOSSARY-LOCK กับดักคำแปล ทับศัพท์ อักษรย่อ หน่วยวัด |
| [03-thai-ai-tells.md](thai-academic-language-guard/03-thai-ai-tells.md) | 🧯 3. ลายนิ้วมือภาษาเครื่องในภาษาไทย (Thai AI-Tells) | **ทุกครั้ง** · ตรวจวลีต้องห้าม ลายนิ้วมือเชิงโครงสร้าง และกฎความแปรผันของประโยค/ย่อหน้า |
| [04-similarity-control.md](thai-academic-language-guard/04-similarity-control.md) | 🔒 4. ด่านคุมความซ้ำ (Similarity Control) — ความเสี่ยงจริงของเนื้อไทย | คุมความซ้ำ (Turnitin / อักขราวิสุทธิ์) นิยามศัพท์ บทที่ 3 และ 5 |
| [05-english-sections.md](thai-academic-language-guard/05-english-sections.md) | 🌐 5. ส่วนภาษาอังกฤษ — จุดเดียวที่ถูกให้คะแนน AI จริง | เขียน/ตรวจบทคัดย่อ ชื่อเรื่อง หรือ manuscript ภาษาอังกฤษ |
| [06-pre-delivery-audit.md](thai-academic-language-guard/06-pre-delivery-audit.md) | ✅ 6. ด่านตรวจก่อนส่งทุกหัวข้อย่อย (Pre-Delivery Language Audit) | **ทุกครั้ง** · ก่อนส่งทุกบล็อก — บัตร [LANGUAGE-AUDIT] 8 ข้อ |
| [07-make-it-pass-ai.md](thai-academic-language-guard/07-make-it-pass-ai.md) | 🧭 7. เมื่อผู้ใช้ขอให้ "ทำให้ไม่ติด AI" | ผู้ใช้ขอ "ทำให้ไม่ติด AI" หรือถูกธงทั้งที่เขียนเอง |
| [08-publisher-ai-policy.md](thai-academic-language-guard/08-publisher-ai-policy.md) | 📜 8. นโยบายการใช้ AI ของสำนักพิมพ์ — ใช้ได้แค่ไหน ต้องแจ้งตรงไหน | ใช้ AI ได้แค่ไหน นโยบายสำนักพิมพ์/วารสาร/TCI ข้อความเปิดเผย (Disclosure) Policy Gate |
| [09-textbook-voice.md](thai-academic-language-guard/09-textbook-voice.md) | 📕 9. น้ำเสียงตำราไทย (Thai Textbook Voice) — ใช้กับงานประเภทตำรา เอกสารประกอบการสอน และหนังสือวิชาการ | งานตำรา เอกสารประกอบการสอน หนังสือวิชาการ — น้ำเสียง คำเรียกผู้อ่าน คำภาษาพูดต้องห้าม |
| [10-royal-references.md](thai-academic-language-guard/10-royal-references.md) | 👑 10. การอ้างอิงพระราชดำรัส พระราชดำริ และเอกสารที่เกี่ยวกับสถาบัน | อ้างพระราชดำรัส พระราชดำริ ราชาศัพท์ เอกสารเกี่ยวกับสถาบัน |
| [11-table-figure-integrity.md](thai-academic-language-guard/11-table-figure-integrity.md) | 📊 11. ความซื่อตรงของตารางและภาพที่ประมวลเอง | ตาราง/ภาพที่ประมวลเอง และการเขียนที่มาใต้ตาราง/ภาพ |
| [12-syntax-calque-gate.md](thai-academic-language-guard/12-syntax-calque-gate.md) | 🧱 12. ด่านโครงสร้างประโยค (Syntax Calque Gate) — ชั้นที่หายไประหว่างคำกับย่อหน้า | **ทุกครั้ง** · ประโยคคำถูกหมดแต่ยังอ่านเหมือนแปล — เพดาน การ/ความ ของ ซึ่ง ถูก ข้อยกเว้นผลบวกลวง regex ไทย |
| [13-thai-pattern-bank.md](thai-academic-language-guard/13-thai-pattern-bank.md) | 🗂️ 13. คลังรูปประโยคไทยวิชาการ (Thai-First Pattern Bank) | ต้องเขียนประโยคใหม่ — เลือกรูปประโยคไทยตามหน้าที่ย่อหน้า |
| [14-foreign-handbook-rule.md](thai-academic-language-guard/14-foreign-handbook-rule.md) | 📗 14. กฎใช้คู่มือการเขียนภาษาอังกฤษ (Foreign Handbook Rule) | หยิบเนื้อหาจากตำรา/คู่มือการเขียนภาษาอังกฤษ |
| [15-thai-corpus-intake.md](thai-academic-language-guard/15-thai-corpus-intake.md) | 📥 15. ข้อกำหนดคลังต้นแบบภาษาไทย (Thai Corpus Intake Spec) | ผู้ใช้ส่งเอกสารไทยต้นแบบเข้าคลัง |
| [16-cross-medium-term-lock.md](thai-academic-language-guard/16-cross-medium-term-lock.md) | 🔠 16. ด่านศัพท์ข้ามสื่อ (Cross-Medium Term Lock) | ศัพท์ในเนื้อความ ภาพ ตาราง สเปกภาพ ต้องตรงกัน (ส่งสเปกให้ figure-agent) |
| [17-collocation-gate.md](thai-academic-language-guard/17-collocation-gate.md) | 🔗 17. ด่านคำเข้าคู่ (Collocation Gate) — ชั้นสุดท้ายที่ด่านอื่นจับไม่ได้ | คู่คำที่อังกฤษเข้าคู่แต่ไทยไม่เข้าคู่ ลักษณนาม คำแจกแจง |
