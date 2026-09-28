# ย้ายเครื่อง / เครื่องใหม่ — เช็กลิสต์ให้สกิลทำงานครบ

สกิลทั้งหมดอ้าง path แบบ `~` (โฟลเดอร์ผู้ใช้ของเครื่องนั้น) จึงใช้ได้ทุกเครื่องที่วาง repo ตามนี้

## 1. Clone repo ไว้ใต้ `~\Documents\GitHub\`

| repo | ใช้ทำอะไร |
|---|---|
| `academicforward` | คู่มือสกิลฉบับเต็ม (แหล่งจริงเดียว) |
| `claude-config` | ลิงก์ `~\.claude\commands` + settings → รัน `sync-claude.ps1` |
| `aritc-audit` | สคริปต์รายงาน KPI `scripts/kpi-report.mjs` |
| `noteboard` | สคริปต์ขึ้นห้อง `backend/scripts/publish-lesson.ts` |
| `design-system` | CSS อ้างอิงของสไลด์ |
| `desk-utils` | สกิล **photo-post** (คัดรูปกิจกรรม → โพสต์ → หลักฐาน) — รัน `python bootstrap.py --yes` ลงไลบรารี + ลงทะเบียนสกิล + ทางลัดคลิกขวา |
| `dev-tools` (= โฟลเดอร์ `GitHub` เอง) | `dev-start` + `dev-tunnel-watch.ps1 -Install` (tunnel DB ต่อเองตอน login แบบเงียบ) + `CLAUDE.md` กฎหลักฐานทุกงาน |

เพิ่ม/แก้สกิลใน academicforward แล้ว → `python ~\Documents\GitHub\claude-config\gen-commands.py` → commit ทั้ง 2 repo

## 2. ติดตั้งโปรแกรม

* Node.js ≥ 20.12 · Python 3.12 + `pip install python-docx pymupdf pillow opencv-python`
* Microsoft Edge (ออก PDF) · `npm i -g @mermaid-js/mermaid-cli` (`mmdc` สำหรับผัง)
* Google Drive for desktop — map เป็นไดรฟ์ `G:` (`G:\My Drive\อบรม` = ที่เก็บไฟนอล)
* แต่ละ repo เว็บ: `npm install` / `bun install`

## 3. คัดลอกเอง (ไม่อยู่ใน git)

* `aritc-audit\.env.local` — `DATABASE_URL` (DB จริงบน server สำนัก ผ่าน tunnel ของ dev-start)
* `noteboard\backend\.env`
* `~\Documents\slides\` ทั้งโฟลเดอร์ — โดยเฉพาะ `assets\speaker.jpg` `assets\aritc-logo.png` และงานเก่าที่ใช้เป็นแม่แบบ
* memory ของ Claude **ไม่ต้องคัดลอก** — กฎที่เจ้าของตั้งย้ายเข้า repo แล้ว (CLAUDE.md / AGENTS.md / SKILL.md) เพิ่มกฎใหม่ที่ repo เสมอ
* API keys ตั้งเป็น environment variable ของเครื่อง (ดู claude-config/README)

## 4. เครือข่าย

รายงาน KPI และขึ้น NoteBoard ต้องเข้าถึง server สำนัก (ดู IP ใน dev-start) — อยู่ใน LAN สำนักหรือต่อ VPN แล้วเปิด dev-start ให้ tunnel `127.0.0.1:3306` ทำงาน

## 5. ตรวจความพร้อม

```powershell
node -v; python --version; mmdc -V
Test-Path "$HOME\Documents\slides\assets\speaker.jpg"
Test-Path "G:\My Drive\อบรม"
cd $HOME\Documents\GitHub\aritc-audit; node scripts/kpi-report.mjs list   # เห็น KPI 4 ตัว = DB ต่อได้
```
