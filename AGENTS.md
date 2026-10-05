# กติกาสำหรับ AI agent ทุกตัว (Antigravity / Claude Code / อื่น ๆ)

ผู้ใช้สลับใช้ทั้ง Antigravity (Gemini) และ Claude Code และสลับเครื่องบ่อย ไฟล์นี้คือจุดนัดพบร่วมกัน

## สิ่งที่ใช้ร่วมกัน และสิ่งที่ไม่ใช้ร่วมกัน

- **ร่วมกัน:** คู่มือสกิลใน repo นี้ (แหล่งจริงเดียว) + ไฟล์งานในเครื่อง/Drive
- **ไม่ร่วมกัน:** ประวัติแชท และ memory ของแต่ละ agent (Claude = `~/.claude/...`, Antigravity = `~/.gemini/antigravity/brain`) — agent อีกตัวมองไม่เห็น และไม่ย้ายตามไปเครื่องใหม่
- ดังนั้น **อย่าเก็บกฎหรือความคืบหน้าไว้ใน memory ของตัวเอง** — เขียนลงไฟล์ใน repo เสมอ

## ส่งงานต่อข้าม agent / ข้ามเครื่อง

1. กฎใหม่ที่ผู้ใช้ตั้ง → แก้คู่มือสกิลที่เกี่ยวข้อง หรือไฟล์นี้
2. งานค้าง → เขียนโน้ตสั้น ๆ ในโฟลเดอร์งานนั้น (ทำอะไรไปแล้ว / เหลืออะไร / ไฟล์อยู่ไหน)
3. ก่อนจบงานที่แก้ repo → commit + push (repo นี้ และ `claude-config` ถ้าแตะ) เพราะผู้ใช้อาจเปิดเครื่องอื่นต่อทันที
4. เริ่มงานบนเครื่องใดก็ตาม → `git pull` ก่อน
5. ไฟล์ที่ไม่อยู่ใน git (`.env`, `~/Documents/slides/`) ต้องคัดลอกเอง — ดู [SETUP.md](SETUP.md)

## คำสั่ง `/academicforward`

- คำสั่งเดียวครอบทุกสกิล เลือกคู่มือให้เองตามงาน ใช้ได้ทั้ง Antigravity และ Claude Code
- สร้างจาก `.claude/commands/*.md` ด้วย `python gen-antigravity.py` (สำเนาเดียวกับ `claude-config/gen-antigravity.py`)
  - Antigravity: `~/.gemini/config/skills/academicforward/SKILL.md` — อยู่นอก git ต้องรันใหม่ทุกเครื่อง
  - Claude Code: `~/.claude/commands/academicforward.md` (= `claude-config/commands/`, อยู่ใน git)
- **ห้ามแก้ไฟล์ที่สร้างอัตโนมัติด้วยมือ** — แก้คู่มือต้นทางหรือ `.claude/commands/` แล้วรันสคริปต์ใหม่
- เพิ่มสกิลใหม่ → เพิ่มคู่มือ + ไฟล์ใน `.claude/commands/` → รัน `gen-antigravity.py` และ `claude-config/gen-commands.py` → commit + push ทั้ง 2 repo

## ระบบนิเวศข้าม repo (อ่านก่อนเรียกข้าม repo)

ทุก repo อยู่ใน `~/Documents/GitHub/` และเรียกหากันได้ด้วยพาธนี้:

| repo | ใช้ทำอะไร | จุดเข้า |
|---|---|---|
| `academicforward` | สกิลวิชาการ/เอกสาร/โพสต์ (`/academicforward`) | `README.md`, `AGENTS.md` |
| `desk-utils` | เครื่องมือ Python: `photo_post`, `file_organizer`, `cutdesk`, `premierekit`, `paper_tiler`, `format_converter`, `watcher` | `tools/<ชื่อ>/SKILL.md` |
| `design-system` | มาตรฐานดีไซน์ ARITC/NSRU (กฎเหล็ก 17 ข้อ, tokens, skins) — ใช้ทุกครั้งที่ทำ/แก้ UI | `SKILL.md` (`/design-system`) |
| `libdesk`, `noteboard`, `aritc-duty`, `aritc-audit` | เว็บแอป — ต้องทำตาม design-system | `CLAUDE.md` ในแต่ละ repo |
| `lab-setup` | ตั้งค่า/ติดตั้งเครื่องแล็บ Windows 11 ของ มรนว. (ทำลายข้อมูลได้ — ห้ามรันเองถ้าผู้ใช้ไม่สั่ง) | `AGENTS.md` |

- งานคัดรูป/ล้างไฟล์ซ้ำ/ตัดต่อวิดีโอ → อ่าน `desk-utils/tools/<ชื่อ>/SKILL.md` แล้วรัน `py -X utf8 -m <module>` ได้จากทุกโฟลเดอร์ (ตั้ง `desk_utils.pth` ไว้แล้วโดย `claude-config/sync-claude.ps1`)
- งานกราฟิก/สไลด์/หน้าเว็บ → อ่าน `design-system` ก่อน อย่าเดาสี/ฟอนต์
- repo ไหนหาย → `git clone https://github.com/X66CLRF/<ชื่อ>.git` ใน `~/Documents/GitHub`
- ใช้พาธแบบ `~/...` เสมอ ห้ามฝังชื่อผู้ใช้เครื่อง
