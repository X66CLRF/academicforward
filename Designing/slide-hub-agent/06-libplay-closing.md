> ส่วนหนึ่งของ [slide-hub-agent.md](../slide-hub-agent.md) (ไฟล์ดัชนี: บอกว่าส่วนไหนอ่านเมื่อไร) · เลขข้อ N ในคู่มือนี้ตรงกับไฟล์ `NN-*.md` ในโฟลเดอร์ `slide-hub-agent/` (ข้อ 0–2 รวมใน `00`, ข้อ 3 แยกเป็น `03a`–`03c`)

## 6. ชุดบทเรียนสำหรับ LibPlay (เก็บทุกงาน — ย้ายเข้าเมื่อ LibPlay เสร็จ)

> LibPlay แบ่ง 2 ส่วน **บทเรียน** (สไลด์ + ใบงาน) และ **เกม** — ทุกชิ้น **จับคู่กัน** เหมือน HTML hub ดั้งเดิมของผู้ใช้ (ถอดแบบไว้แล้วใน `libplay/frontend/src/features/notebooklm/`: SlideDeck · Handouts · GameBoard)
> NoteBoard = ห้องให้ผู้เรียนเข้าเห็นสไลด์ + โพสต์ · เกมและใบงานไม่ขึ้น NoteBoard

**ทุกโฟลเดอร์งานต้องมีครบ 3 ชิ้นที่จับคู่กัน**

| ไฟล์ | ส่วนใน LibPlay | ตรงกับ (ถอดแบบ) |
|---|---|---|
| `deck.html` | บทเรียน → สไลด์ | `SlideDeck` / `data/slides.ts` |
| `worksheet.html` | บทเรียน → ใบงาน | `Handouts` / `topics.ts handout` |
| `game.json` | เกม | `GameBoard` / `topics.ts challenges` |
| `lesson.json` | ห้อง NoteBoard (+ `board.code` หลังสร้าง) | activity ขั้น `noteboard` |

**game.json**
```json
{
  "status": "draft | empty | approved",
  "mission": "ชื่อภารกิจ",
  "pairsWith": {"deck": "deck.html", "worksheet": "worksheet.html"},
  "challenges": [
    {"stage": "ด่านที่ 1", "title": "...", "tool": "...", "slides": [3,4], "prompt": "...", "win": "+10"},
    {"stage": "BOSS", "boss": true, "title": "...", "slides": [9], "prompt": "...", "win": "+50"}
  ]
}
```
* `slides` = เลขหน้าสไลด์ที่ด่านนั้นใช้ (จับคู่บทเรียน ↔ เกม)
* source มีโจทย์เกม → ยกตรงตัว `status: approved`
* source ไม่มี → `status: empty` แล้ว **ถามผู้ใช้** ว่าจะให้ร่างไหม · ร่างเอง = `draft` และแจ้งในรายงานขั้น 9
* ใบงานกับเกมต้องอ้างเนื้อหาในสไลด์ชุดเดียวกันเท่านั้น

---

## ขั้นปิดงาน: ส่งไฟนอล + รายงาน KPI (บังคับ งานของกษิดิศ)

งานออกแบบเสร็จเป็นไฟนอลแล้ว ต้องทำต่อทุกครั้ง ตาม [Automation/kpi-report.md](../../Automation/kpi-report.md):
1. คัดลอกไฟล์ไฟนอลเข้า `G:\My Drive\อบรม\<ปี-เดือน ชื่องาน (สถานที่)>\` → หาลิงก์ Drive เป็นหลักฐาน
2. `node scripts/kpi-report.mjs add --kpi <design | wp05 | wp06 | …> ...` เลือกที่ลงจากตารางใน kpi-report.md — งานเดียวหลายบทบาท = หลายรายการ · โพสต์แนะนำที่คนอื่นส่งเนื้อหา = `wp05` ไม่ใช่ `design` ใน repo `aritc-audit` (dry run ก่อน → ผู้ใช้ยืนยัน → `--commit`)
3. รายงาน path ไฟล์ · ลิงก์หลักฐาน · id รายการ KPI · ตรงเวลาไหม
