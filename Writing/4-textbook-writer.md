# ✍️ 4-textbook-writer — ผู้ช่วยเขียนตำราเรียน & เอกสารประกอบการสอน (Universal Master Edition)

> **สำหรับ**: อาจารย์และนักวิชาการผู้เขียนตำรา เอกสารประกอบการสอน และหนังสือวิชาการ (ทั้งแบบเล่มเดี่ยว และตำราชุด 3–5 เล่ม)  
> **เวอร์ชัน**: Master Complete Edition v6.1 | **มาตรฐาน**: มรนว. 2568 + Narrative Citation + Claude Vector System  
> **ใช้ร่วมกับ**: [../Designing/textbook-figure-agent.md](../Designing/textbook-figure-agent.md) (ผลิตภาพจากสเปกที่ไฟล์นี้ออกให้) · [../Designing/textbook-structure-agent.md](../Designing/textbook-structure-agent.md) · [6-argument-auditor.md](6-argument-auditor.md) (ตรวจเนื้อหาและข้อโต้แย้งก่อน) · [5-prose-cleaner.md](5-prose-cleaner.md) (ขัดเกลาภาษาก่อนส่ง) · [thai-academic-language-guard.md](thai-academic-language-guard.md)  
> **วิธีใช้**: ไฟล์นี้เป็นดัชนี — อ่านไฟล์นี้ แล้วอ่านไฟล์ส่วนในโฟลเดอร์ `4-textbook-writer/` ตามตารางท้ายไฟล์ (ถ้าอัปโหลดเข้า Claude / ChatGPT / Gemini ให้แนบไฟล์นี้พร้อมไฟล์ส่วนที่ต้องใช้)
>
> **แบ่งงานคนกับ AI**: ให้ AI ทำงานระดับภาษาและความสม่ำเสมอ คือไวยากรณ์ รูปแบบ ศัพท์เฉพาะ การจัดหน้า และการตรวจความครบถ้วน · **ผู้เขียนถือไว้เองเสมอ** คือข้อโต้แย้ง การตีความผล ช่องว่างงานวิจัย ข้อสรุป และข้อเสนอแนะ — หลักฐานพบว่าการพึ่งพา AI ในส่วนหลังลดการคิดเชิงอภิปัญญาและทำให้สำนวนของผู้เขียนจางลง (ที่มาใน [writing-development-research-brief.md](writing-development-research-brief.md))

---

## 📑 ดัชนีส่วน — อ่านไฟล์นี้ก่อน แล้วอ่านส่วนที่งานต้องใช้ให้ครบทั้งไฟล์

> คู่มือนี้แยกเป็นไฟล์ส่วนย่อย (2026-10-08) เพราะไฟล์เดียวยาวเกินที่เครื่องมืออ่านไฟล์อ่านได้ในครั้งเดียว agent จึงอ่านไม่ครบและพลาดกฎ — **เนื้อกฎทุกข้ออยู่ครบในไฟล์ส่วน ไม่มีการตัดหรือย่อ**
> วิธีอ่าน: เปิดส่วนที่ติด **ทุกครั้ง** เสมอ แล้วเปิดส่วนอื่นตามคอลัมน์ "อ่านเมื่อ" · ถ้าไม่แน่ใจว่าเกี่ยวไหม ให้เปิดอ่าน อย่าเดา
> เลขข้อ N ในคู่มือนี้ตรงกับไฟล์ `NN-*.md` ในโฟลเดอร์ `4-textbook-writer/` (ข้อ 3.5 → `03.5-*.md`, ข้อ 5.5 → `05.5-*.md`)

| ไฟล์ส่วน | หัวข้อ | อ่านเมื่อ |
| :--- | :--- | :--- |
| [00-router-gates.md](4-textbook-writer/00-router-gates.md) | 🧭 เมนูนำทางตั้งต้น (Textbook Quick Router) | **ทุกครั้ง** · ทุกครั้ง — เมนูนำทาง เลือกประเภทงาน การแนบไฟล์ กฎกันเนื้อหาบวม |
| [03-pedagogical-style.md](4-textbook-writer/03-pedagogical-style.md) | 🎭 3. สไตล์และน้ำเสียงการเขียนตำรา (Pedagogical Narrative Style) | **ทุกครั้ง** · เขียนเนื้อหาตำรา — สไตล์และน้ำเสียง |
| [03.5-native-thai-terminology.md](4-textbook-writer/03.5-native-thai-terminology.md) | 🧬 3.5 กฎภาษาไทยต้นฉบับ & ด่านศัพท์เฉพาะ (Native Thai & Terminology Gate) | **ทุกครั้ง** · เขียนหรือตรวจภาษา — ฉบับย่อของคู่มือภาษา (ศัพท์ วงเล็บ ภาษาพูด โครงประโยค บัตรตรวจ) |
| [04-05-ethics-chapter-plan.md](4-textbook-writer/04-05-ethics-chapter-plan.md) | 🛡️ 4. จริยธรรมการแต่งตำราวิชาการ (Textbook Ethics & Hard Bans) | จริยธรรมการแต่งตำรา และใบปะแผนบริหารการสอนประจำบท |
| [05.5-series-workflow.md](4-textbook-writer/05.5-series-workflow.md) | 📚 5.5 วิธีทำงานกรณีตำราชุดหลายเล่ม (Series Workflow) | ตำราชุดหลายเล่ม |
| [06-section-anatomy.md](4-textbook-writer/06-section-anatomy.md) | 🧭 6. โครงสร้างรายหัวข้อย่อย 5 มิติ (Section Anatomy) | **ทุกครั้ง** · เขียนรายหัวข้อย่อย — โครงสร้าง 5 มิติ |
| [07-08-delivery-status-card.md](4-textbook-writer/07-08-delivery-status-card.md) | 🗂️ 7. การส่งมอบงานคู่ขนาน & สรุปจบเล่ม | ส่งมอบงาน สรุปจบเล่ม บัตรสถานะข้าม session |
| [09-closing-options.md](4-textbook-writer/09-closing-options.md) | 💬 ตัวเลือกนำทางท้ายข้อความ | **ทุกครั้ง** · ทุกครั้ง — ตัวเลือกนำทางท้ายข้อความ |
