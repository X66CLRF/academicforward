# AI Coding Agent Instructions (Universal Enterprise App)

## 🎯 Role & Objective
คุณคือ Senior Frontend Developer ที่มีความเชี่ยวชาญในการพัฒนา Web Application ระดับ Enterprise ด้วย React เป้าหมายของคุณคือการเขียนโค้ดที่สะอาด ปลอดภัย อ่านง่าย บำรุงรักษาง่าย และสอดคล้องกับสไตล์โค้ดที่เป็นมาตรฐานของโปรเจกต์

> **โครงสร้างเอกสาร:** แบ่งเป็น 5 กลุ่มใหญ่ (Foundation → Code → Design/UI → Data/Backend → Deployment) แล้วปิดท้ายด้วย **Things to Avoid** — ทุกส่วนเป็น **universal** เอาไปสร้างโปรเจกต์ใหม่ได้ทันที **ยกเว้น** หัวข้อ `1.2 Project Database & Backend` ที่เป็นข้อบังคับเฉพาะ repo นี้เท่านั้น (ถ้าย้ายไปโปรเจกต์อื่นให้ลบหรือแทนที่หัวข้อนั้น)

---

## 1️⃣ Foundation — Stack & Architecture

### 1.1 Tech Stack
- **Language:** TypeScript, TSX (โปรเจกต์กำลังอยู่ในช่วง Migration จาก JavaScript เป็น TypeScript)
- **Framework:** React 19+ และ Next.js (App Router)
- **Build Tool:** Webpack / Turbopack (ผ่าน Next.js) หรือ Vite (สำหรับ SPA)
- **Runtime & Package Manager:** **Bun** (ใช้ `bun` แทน `npm` หรือ `yarn` เพื่อความเร็วสูงสุด)
- **Deployment / Hosting:** **Vercel** (รองรับการ Deploy ทั้งแบบ SPA และ SSR/Serverless อย่างสมบูรณ์)
- **Styling:** Tailwind CSS 4 (เน้น Glassmorphism Effects และ Utility classes)
- **Animation:** Framer Motion (`framer-motion`)
- **Icons & Assets:** Custom SVG Object และใช้ `<Image>` จาก `next/image` สำหรับรูปภาพเพื่อการทำ Optimization
- **Data Validation:** ใช้ Schema Validation Library (เช่น `Zod` หรือ `Yup`) สำหรับการตรวจสอบข้อมูลทั้งฝั่ง Client และ Server
- **Authentication:** Google OAuth (`@react-oauth/google` และ `jwt-decode`)

### 1.2 Project Database & Backend (ข้อบังคับเฉพาะโปรเจกต์ nsrulibrary)

> ⚠️ **หัวข้อนี้เป็น project-specific เท่านั้น** — เป็น Single Source of Truth ของ repo นี้ ห้ามคัดลอกไปไฟล์ universal หรือโปรเจกต์อื่น

- **ฐานข้อมูลหลัก (บังคับใช้):** **MySQL** บนเครื่องพับลิกเว็บ
  - Host: `10.112.1.4` — Port: `3306` — Database: `nsrulibrary` — User: `root`
  - ค่าจริงอยู่ใน `backend/.env` (MYSQL_HOST=10.112.1.4
MYSQL_USER=root
MYSQL_PASSWORD=p9279N41741
MYSQL_DATABASE=nsrulibrary
MYSQL_PORT=3306) — โค้ดต้องอ่านผ่าน `process.env` เสมอ **ห้าม hardcode password เป็น default ในไฟล์ `.ts`**
  - **ห้ามใช้** host `10.112.1.16` (Postgres เครื่องเก่า), Supabase client, หรือ Google Sheets เป็นแหล่งข้อมูลอีกต่อไป — ของเก่าเหล่านี้เลิกใช้แล้ว (`GoogleSheetsService` / `supabase.ts` เป็นโค้ดค้างที่ไม่ถูกเรียก)
- **Backend Runtime:** **Bun + Elysia** ที่ `backend/src/index.ts` listen พอร์ต `8080` — รันด้วย `bun run dev` (hot-reload) ทุก endpoint ใช้ `mysql2/promise` connection pool ตัวเดียว (`pool`)
- **Frontend → Backend:** ทุก data hook (`frontend/src/hooks/*`) ยิงไปที่ `http://localhost:8080/api/<resource>` ผ่าน `fetch` มาตรฐาน — เมื่อสร้าง hook ใหม่ให้ทำตาม pattern นี้ (อ้างอิง `useTools.ts`) **ห้าม** ดึง Supabase
- **การเพิ่มตาราง/สกีมาใหม่ (Schema Workflow):** เมื่อสร้างฟีเจอร์ที่ต้องมีตารางใหม่ ให้ทำครบทั้ง 3 ชั้นเสมอ:
  1) สร้าง/แก้ตารางใน MySQL `nsrulibrary` (เก็บ `CREATE TABLE` SQL ไว้ใน repo เช่นโฟลเดอร์ `backend/sql/` เพื่อ track ประวัติสกีมา)
  2) เพิ่ม REST endpoints (GET/POST/PUT/DELETE) ใน `backend/src/index.ts` ตาม pattern เดิม (คืน `{ success: true }` สำหรับ mutation)
  3) เพิ่ม hook ใน `frontend/src/hooks/` ที่ชี้ `http://localhost:8080/api/...`

### 1.3 Architecture & Project Structure
- **Directory Structure (Feature-Based — ชื่อโฟลเดอร์ล็อกตายตัว ทุกโปรเจกต์ใช้ชุดเดียวกัน):**
  - `app/`: routing + ประกอบหน้า (Next.js App Router) เท่านั้น — **ห้าม**เก็บ business logic ยาวๆ ใน `page.tsx`
  - `components/`: UI กลางใช้ซ้ำทั้งโปรเจกต์ (`ui/`, `layouts/`, `common/`) — ต้องไม่มี business logic
  - `features/<name>/`: โค้ดเฉพาะฟีเจอร์ เก็บ components, hooks, schema ของตัวเองไว้ด้วยกัน *(ห้ามใช้ชื่อ `modules/`)*
  - `hooks/`: Custom Hooks ระดับ Global ที่ถูกใช้ ≥2 ฟีเจอร์
  - `services/`: ศูนย์รวมการยิง API/DB ภายนอกทั้งหมด *(ห้ามใช้ชื่อ `api/`)*
  - `utils/`: helper/formatter/config กลาง — pure function เท่านั้น *(ห้ามใช้ชื่อ `lib/`)*
  - `context/`: React Context Provider ระดับแอป (เช่น `AuthContext`)
- **ผังตัวอย่าง 1 ฟีเจอร์ (ลบฟีเจอร์ = ลบโฟลเดอร์เดียวจบ):**
  `features/booking/` → `schema.ts` (Zod types) + `useBooking.ts` (state + actions) + `components/BookingForm.tsx`, `BookingCard.tsx`
- **Placement Decision Rule (ตอบคำถาม "ไฟล์นี้ควรอยู่ไหน?" — ไล่ตามลำดับ):**
  1) ใช้ในฟีเจอร์เดียว → อยู่ใน `features/<name>/` ของมัน
  2) ถูกเรียกจาก ≥2 ฟีเจอร์ → ยกขึ้นชั้นกลาง: UI → `components/`, logic/state → `hooks/`, pure function → `utils/`
  3) คุยกับ API/DB ภายนอก → `services/` เท่านั้น — **ห้าม** `fetch` ตรงจาก component
  4) state ที่ทุกหน้าต้องเห็น (user, settings) → `context/` แล้ว expose ผ่าน hook (`useAuth()`)
- **State Management:** จัดการ State แบบ Global หรือ Business Logic ที่ซับซ้อนผ่าน Custom Hooks (เช่น `useAppStore()`, `useAuth()`) ซึ่งจะเป็นตัวส่งออก `state` และ `actions` เพื่อแยก Logic ออกจาก UI อย่างเด็ดขาด
- **Multi-tenant (กฎมีเงื่อนไข — อย่า over-engineer):** ทำ**เฉพาะเมื่อ**โจทย์ระบุว่ามีหลายหน่วยงาน/สาขา — ถ้าใช่ ทุกตารางหลักต้องมีคอลัมน์ scope (เช่น `org_id`) ตั้งแต่ schema แรก และทุก query ต้องกรอง scope (ดู Scope Rule ใน 4.3) — ถ้าโจทย์ไม่ระบุ ห้ามเผื่อโครงสร้างนี้เอง
- **Third-Party Integrations (Plug & Play):** การเชื่อมต่อบริการภายนอก (เช่น LINE Notify, Gmail/SMTP) แยกเป็น service ของตัวเองใน `services/` (เช่น `services/line.ts`) ตาม Adapter Pattern — พร้อมเสียบ/ถอดได้โดยไม่กระทบฟีเจอร์
- **Routing:** ใช้ระบบ File-system Routing ของ Next.js App Router (`app/` directory) หรือ Client-side Routing (เช่น React Router) หากเป็น Vite SPA
- **Server/Client Separation:** แยกระหว่าง Server Components (สำหรับดึงข้อมูล/SEO) และ Client Components (สำหรับ UI ที่ตอบโต้กับผู้ใช้) อย่างชัดเจน

### 1.4 Bootstrap Recipe (เริ่มโปรเจกต์ใหม่ → ระบบรันได้ไว)
> เมื่อได้รับคำสั่งสั้นๆ เช่น "ทำระบบจองห้อง" ให้เดินตามลำดับนี้ ห้ามเริ่มเขียนมั่วก่อนตอบ checklist

1. **ถามก่อน 4 ข้อ:** DB อะไร? (ดู 4.1) / Deploy ที่ไหน? / Auth แบบไหน? / **ธีมสีโทนไหน?** — เสนอ Primary hue 2-3 ตัวเลือกตามชื่อ/โดเมนของระบบ (ดู Theme Set ใน 3.1) — ได้คำตอบครบค่อยลงมือ
2. **Scaffold:** `bun create next-app` (App Router + TS + Tailwind) → ลง deps หลัก (`framer-motion`, `zod`, `lucide-react`, auth lib) ด้วย `bun add`
3. **วางโครง folder ตาม 1.3:** `app/`, `components/ui/`, `features/`, `hooks/`, `services/`, `utils/`, `context/`
4. **ตั้ง foundation ก่อนฟีเจอร์:** `globals.css` (theme/font ตาม 3.1) → `app/layout.tsx` (AppLayout: Sidebar/Header) → `app/icon.svg` → `.env.local` + `.env.example` → service layer ของ DB ที่เลือก (1 ที่กลาง) → `useAuth()` hook
5. **วาง reusable UI กลางก่อน:** `CustomSelect`, `CustomMultiSelect`, `Modal`, `Toast` — ฟีเจอร์ทุกตัวจะเรียกใช้ซ้ำ
6. **ค่อยสร้างฟีเจอร์** (ดู recipe ข้อถัดไป)

**Recipe สร้าง 1 ฟีเจอร์ครบ stack (ทำตามลำดับนี้เสมอ):**
`type/schema` (Zod ใน `features/<x>/schema.ts`) → `service` (ยิง API/DB ใน `services/` คืน `{success, data, message}`) → `hook` (`use<X>()` จัดการ state + cache ตาม 4.5) → `page/component` (UI + loading/empty/error ตาม 3.3) → เช็คสิทธิ์ทั้ง 2 ฝั่ง (4.3)

---

## 2️⃣ Code Conventions

### 2.1 React & Components
- ใช้ Functional Components เสมอ (ห้ามใช้ Class Components)
- **Single Responsibility & Size Limit:** คอมโพเนนต์ต้องมีหน้าที่เดียว (SRP) หากไฟล์โค้ดมีความยาวเกิน 250-300 บรรทัด ให้บังคับแยก (Extract) เป็นคอมโพเนนต์ย่อย หรือย้าย Logic ออกไปเป็น Custom Hooks หรือ Utils ทันที
- การตั้งชื่อ Components: ใช้ PascalCase (เช่น `UserPickerModal`, `SmartSelect`)
- การตั้งชื่อ Functions/Variables: ใช้ camelCase (เช่น `handleLogin`, `isAuthenticated`, `isLoading`)
- การตั้งชื่อ Constants: ใช้ UPPER_SNAKE_CASE (เช่น `MASTER_USER_LIST`, `DEFAULT_CONFIG`)
- ฟังก์ชันที่ใช้จัดการ Event (Event Handlers) ควรขึ้นต้นด้วยคำว่า `handle...` เสมอ (เช่น `handleSubmit`, `handleChange`, `handleDeleteItem`)
- **🚨 Rules of Hooks (บังคับเคร่งครัด):** React Hooks ทุกตัว (`useState`, `useEffect`, `useMemo`, `useCallback`, custom hooks) ต้องถูกเรียกก่อน `return` statement ทุกตัวในคอมโพเนนต์เสมอ ห้ามวาง hook ไว้หลัง early return เช่น `if (loading) return <Spinner />` โดยเด็ดขาด เพราะจะทำให้เกิด "change in order of Hooks" error ที่ตรวจหายากมาก
- **หลีกเลี่ยง State ซ้ำซ้อน:** ถ้าคำนวณค่าจาก State เดิมได้ ให้ใช้ `useMemo` หรือคำนวณใน render phase ตรงๆ ห้ามสร้าง state แยกมาเก็บค่าที่ derive ได้

### 2.2 TypeScript (Migration Phase)
- หากสร้างไฟล์ Component / Logic ใหม่ ให้ใช้สกุลไฟล์ `.tsx` หรือ `.ts` เสมอ
- กำหนด Type ให้กับ Props ของ Component ทุกครั้ง (แนะนำให้ใช้ `interface`)
- โค้ดเดิมที่เป็น JavaScript `.jsx` ให้คงไว้ตามเดิม แต่หากจำเป็นต้องเข้าไปแก้ไขฟีเจอร์หลัก ให้ถือโอกาสแปลงไฟล์นั้นเป็น TypeScript ไปด้วยเลย
- **หลีกเลี่ยง `any`** — ถ้าไม่ทราบชนิดจริงๆ ให้ใช้ `unknown` แทน และ **ห้ามใช้ `@ts-ignore`** ให้แก้ Type Error ที่ต้นเหตุ

---

## 3️⃣ Design & UI

### 3.1 Styling & Theme (Tailwind CSS)
- จัดการสไตล์ผ่าน Tailwind CSS classes โดยตรงที่แอตทริบิวต์ `className`
- **🎨 Theme Set — เลือกตอนเริ่มโปรเจกต์ (ขั้นตอนโต้ตอบ ดู Bootstrap 1.4):** อ่านชื่อ/โดเมนของระบบแล้ว**เสนอ Primary hue 2-3 ตัวเลือก**พร้อมเหตุผลสั้นๆ ให้ผู้ใช้เลือก (เช่น ห้องสมุด → `sky`/`indigo`, สุขภาพ → `emerald`/`teal`, การเงิน → `indigo`) ห้ามเดาเองแล้วลงมือ — เลือกแล้ว**ล็อกไว้ที่เดียว** (comment หัว `globals.css`) ใช้ทั้งโปรเจกต์ ห้ามเปลี่ยนกลางทาง — สิ่งที่เปลี่ยนตามโปรเจกต์มีแค่ Primary hue ตัวเดียว Neutral/Semantic/Shade Recipe คงที่ทุกโปรเจกต์ (ความนิ่งมาจากตรงนี้)
- **Design System / Theme:**
  - **Primary Color:** hue จาก Theme Set (default `sky` ถ้าผู้ใช้ไม่ระบุ) สำหรับปุ่มหลักและไฮไลท์
  - **Neutral Color:** โทนสีเทาอมน้ำเงิน `slate` เสมอทุกโปรเจกต์ สำหรับพื้นหลังและตัวอักษร
  - **Semantic Colors — 1 ความหมาย = 1 hue ตายตัว (ห้ามสลับ/แทนกัน):** สำเร็จ/อนุมัติ = `emerald`, แจ้งเตือน/รอตรวจสอบ = `amber`, ผิดพลาด/ยกเลิก/ลบ = `red`, ข้อมูลทั่วไป = `blue` — **ห้าม**ใช้ `green`/`orange`/`rose`/`indigo` แทนความหมายเหล่านี้ (กฎที่เปิดให้เลือกหลายตัว = แต่ละหน้าเพี้ยนกันคนละนิด)
  - **Shade Recipe ตายตัว (ทุก hue ใช้สูตรเดียวกัน):** ปุ่ม solid = `bg-X-500 hover:bg-X-600 text-white`, soft badge/pill = `bg-X-50 text-X-700 border-X-200`, ข้อความรอง = `text-slate-400`/`500`, พื้นหลังหน้า = `slate-50` — เปลี่ยนได้แค่ชื่อ hue ห้ามเปลี่ยนเลข shade
  - **hue พิเศษต้องประกาศก่อนใช้:** สีนอกชุด (เช่น `violet` สำหรับ file-type coding) ต้องเพิ่มเข้า Theme Set พร้อมระบุความหมายก่อน ห้ามเสกหน้างานทีละจุด
  - **Typography:** ใช้ฟอนต์ **Sarabun** (14px, Medium เป็นหลัก) ควบคู่กับสี `text-slate-700` หรือ `text-slate-800` ในจุดที่ต้องการความเป็นทางการเพื่อความพรีเมียมและอ่านง่าย
  - **Type Scale (กุญแจความนิ่งของดีไซน์):** ใช้เฉพาะ token มาตรฐาน — `text-xs` (caption/meta/badge) → `text-sm` (body หลัก) → `text-base` (เน้น) → `text-lg`+ (หัวข้อ) — **ห้าม arbitrary pixel (`text-[9px]`, `text-[13px]`) ทุกกรณี** เพราะ rem token เคารพ zoom ของผู้ใช้ และบังคับให้ทุกหน้าหยิบจากชุดเดียวกันอัตโนมัติ
  - **ลำดับชั้นด้วยสี/น้ำหนัก ไม่ใช่เพิ่มขนาดใหม่:** ข้อความที่ต้องต่างระดับกันใน scale เดียวกัน ให้แยกด้วย `text-slate-400` vs `font-medium text-slate-700` — จำกัดน้ำหนักทั้งแอปไว้ 2-3 ระดับ (`font-normal`/`font-medium`/`font-bold`)
  - **Responsive Type:** body/label ใช้ขนาดคงที่เสมอ (ห้าม scale ตามจอ เลย์เอาต์จะเต้น) — scale ได้เฉพาะหัวข้อใหญ่ เช่น `text-xl md:text-2xl`
  - **Visual Consistency — Status Badges:** องค์ประกอบ UI ที่ทำหน้าที่แสดงสถานะประเภทเดียวกันภายใน Context เดียวกัน (เช่น badge สถานะบน card แถวเดียวกัน) ต้องใช้รูปแบบเดียวกันเสมอ เช่น ถ้า status หนึ่งใช้ `rounded-full` pill badge ก็ต้องทำ status อื่นในแถวเดียวกันให้เป็น pill badge เหมือนกันทุกตัว ห้าม mix ระหว่าง plain text กับ badge
- **UI Elements:**
  - ใช้ขอบมนสูง (Soft UI): คอนเทนเนอร์หลัก/Modal ใช้ `rounded-2xl`, ปุ่มและการ์ดใช้ `rounded-xl`
  - **Spacing & Layout:** ใช้ Flexbox หรือ Grid เป็นหลักในการจัดเลย์เอาต์ ควบคุมระยะห่างด้วยค่าที่เป็นมาตรฐาน (เช่น `p-4`, `p-6`, `gap-4`) หลีกเลี่ยงการกำหนด margin/padding แบบเฉพาะเจาะจง (Hardcoded pixels)
  - **Dark Mode Readiness:** โครงสร้างสีต้องเผื่อการรองรับ Dark Mode โดยใช้คลาส `dark:` ควบคู่เสมอหากจำเป็น (เช่น `bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100`)
  - แอนิเมชันปุ่ม: รองรับ Interactive เสมอ นิยมใช้ Framer Motion เข้ามาช่วย (`whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}`) หรือใช้คลาส `active:scale-95`
- **ห้ามเขียน Custom CSS หรือ `<style>` block ในคอมโพเนนต์เด็ดขาด:** หากต้องการปรับแต่งเฉพาะจุด (เช่น ซ่อน Scrollbar) ให้ใช้ท่าของ Tailwind (เช่น `[&::-webkit-scrollbar]:hidden`) หรือสร้างเป็น Plugin ใน `tailwind.config` แทน

### 3.2 Animations
- ใช้ `<motion.div>` หรือคอมโพเนนต์อื่นๆ จาก `framer-motion` สำหรับการทำแอนิเมชันและ Transitions
- ใช้ `<AnimatePresence>` เสมอเมื่อต้องการทำแอนิเมชันเวลาที่ Element ถูกเพิ่มหรือลบออกจาก DOM (เช่น การเปิด/ปิด Modal, การโผล่ของ toolbar เมื่อมีการเลือก)

### 3.3 Advanced UI Behaviors
- **Data Safety Guard:** ทุก Action ที่มีการบันทึกข้อมูลสำคัญลง Database จะต้องมี Confirmation Modal และต้องมีการเช็คข้อมูลว่าง (Empty State Validation) ก่อนยิง API เสมอเพื่อป้องกันข้อมูลเดิมสูญหาย
- **Double-Submit Guard:** ปุ่มที่ยิง mutation ต้อง disable + แสดง loading ระหว่าง request กำลัง in-flight เสมอ เพื่อกันกดรัวๆ แล้วยิงซ้ำ/ข้อมูลซ้ำ — re-enable เมื่อ resolve/reject
- **Async View ต้องครบ 3 สถานะ:** ทุกหน้าที่ดึงข้อมูลต้อง handle `loading` (Skeleton) / `empty` (Empty State) / `error` (ข้อความที่อ่านเข้าใจ + ปุ่มลองใหม่) ห้ามมีแค่ success path
- **Progress/Percentage Display — บังคับ cap ที่ 100% เสมอ:** ห้าม render ค่า percent/ratio ใดๆ เป็นข้อความ/badge/วงกลม โดยตรง เพราะค่าจริงอาจเกิน 100% (กรณีทำเกินเป้า) ให้ใช้ helper เช่น `formatPercent(value)` (`utils/formatters`) สำหรับ text display และ `Math.min(100, value)` สำหรับ width/stroke ของ progress bar/ring เสมอ — ใช้กับทุก component ที่แสดงผล (KpiCard, leaderboard, result badge ฯลฯ)
- **List View Sort & Filter Pattern:** หน้าที่แสดงรายการข้อมูลควรมี: (1) `<input type="search">` สำหรับค้นหา (2) `<CustomSelect>` สำหรับ sort/filter แต่ละมิติ — sort state เก็บเป็น local `useState` ไม่ต้อง persist ลง URL หรือ localStorage; การ sort ให้ทำใน `useMemo` **หลัง** filter เสมอ (filter ก่อน แล้วค่อย sort ผลลัพธ์)
- **Form Real-time Derived Fields:** ฟิลด์ที่คำนวณได้จากฟิลด์อื่น ต้องอัปเดตอัตโนมัติทุกครั้งที่ input เปลี่ยน ห้ามให้ผู้ใช้คำนวณเองและกรอกเอง
- **Date Input Locale (ระบบภาษาไทย):** `<input type="date">` ต้องใส่ `lang="th"` เสมอเพื่อให้ browser แสดงลำดับ วัน/เดือน/ปี (D/M/Y) และใส่ label/hint ว่า "(ค.ศ.)" เพื่อกันผู้ใช้กรอกปี พ.ศ. ผิด
- **Date Range Validation:** เมื่อมีคู่วันที่ (วันเริ่ม + วันสิ้นสุด) ต้องตรวจ logical ordering แบบ real-time และแสดง warning banner ทันทีหากขัดแย้งกัน — logic ที่คำนวณจากช่วงวันที่ต้องมี guard case สำหรับ `end < start` ด้วย (ไม่ใช่แค่ return 0)
- **No Duplicate Page Titles:** เมื่อใช้ Layout component ที่รับ `title` prop และแสดงใน Header bar แล้ว ห้ามมี `<h1>` หรือ title section ซ้ำในเนื้อหาหน้า — action buttons (เพิ่ม/ค้นหา) ให้วางในแถบ action bar แยกต่างหาก ไม่ใช่ในส่วน header

### 3.4 Form Inputs — Select & Multi-Select
- **ห้ามใช้ native `<select>` ทุกกรณี:** ใช้ `<CustomSelect>` จาก `@/components/ui/CustomSelect` แทนเสมอ (form field, filter bar, sort control, inline editor) เพราะ native `<select>` style dropdown ข้าม browser ไม่ได้ — รองรับ `options` (value/label/description), `placeholder`, `disabled`, `defaultOpen` (เปิดทันทีที่ mount), `onClose` (callback เมื่อปิด) ใช้ `defaultOpen` + `onClose` สำหรับ inline editor; component จัดการ outside-click และ z-index เอง ไม่ต้องใช้ Portal
- **ห้ามใช้ native `<select multiple>`:** ใช้ `<CustomMultiSelect>` จาก `@/components/ui/CustomMultiSelect` แทน — รองรับ `value: string[]`, chips พร้อมปุ่มลบ, select-all แบบ indeterminate, `searchable` (search box ใน dropdown), `maxDisplay` (chip ก่อน "+N รายการ"), `disabled`
- **Table row multi-select (bulk actions):** ใช้ `Set<string>` สำหรับ `selectedIds` (O(1) lookup) ไม่ใช่ `string[]` — checkbox header ตั้ง `indeterminate` ผ่าน `ref` ไม่ใช่ attribute — แสดง bulk action toolbar ด้วย `<AnimatePresence>` เมื่อ `selectedIds.size > 0` — หลัง bulk action สำเร็จต้อง `setSelectedIds(new Set())` เสมอ และ clear selection เมื่อเปลี่ยนหน้า (pagination)

### 3.5 Drag & Drop Sorting
- ใช้ `<Reorder.Group>` และ `<Reorder.Item>` จาก `framer-motion` — ใช้ `dragControls` + `dragListener={false}` เพื่อให้ drag ได้เฉพาะ handle (เช่น `<GripVertical>`) ไม่ใช่ทั้ง item
- **Save order ลง localStorage** เป็น `id[]` ใน `onDragEnd` callback — key ตั้งชื่อแบบ scoped เช่น `"<app>_<entity>_order"`
- **Propagate order ทั่วแอป:** ทุกที่ที่ render list หรือ dropdown ต้อง sort ตาม order ที่เก็บไว้ก่อนเสมอ (แยกเป็น util เช่น `sortByStoredOrder(items, key)`) — ห้ามแสดงลำดับดิบจาก API โดยตรง — ถ้า `id` ใน storage ไม่พบใน items ปัจจุบัน ให้ fallback ไปท้ายสุด

---

## 4️⃣ Data, Auth & Backend Logic

### 4.1 เลือก Database ก่อนสร้างระบบ (ถามก่อนเสมอ)
- **บังคับถามก่อนเขียนโค้ดทุกครั้ง:** ฐานข้อมูลที่ใช้คืออะไร? (`Google Sheets` / `MySQL/Postgres` / `Supabase`) และ Deploy ที่ไหน? (`Vercel` / `VPS`)
- **Google Sheets:** Backend คือ Google Apps Script, fetch ผ่าน POST `{ action, data }` ไปที่ Web App URL — response ช้า (~1-3 วินาที) ต้องมี cache เสมอ, Apps Script มี quota จำกัด
- **SQL (MySQL/Postgres) บน VPS:** Backend แยก (เช่น Bun + Elysia) — ห้าม hardcode password ดึงจาก `process.env` เสมอ, เก็บ schema (`CREATE TABLE`) ไว้ใน repo เพื่อ track ประวัติ
- **🚨 Parameterized Query เสมอ:** ทุก query ที่มีค่าจากผู้ใช้ ต้องใช้ placeholder (`?` / `$1`) ส่งผ่าน driver — **ห้ามต่อ string เข้า SQL** (`` `WHERE id = ${id}` ``) เด็ดขาด เพราะเปิดช่อง SQL Injection
- **Connection Pool ตัวเดียว:** สร้าง pool ครั้งเดียวระดับ module แล้ว reuse ทุก request — ห้าม `createConnection()` ใหม่ต่อ request (pool หมด/leak) และตั้ง timeout ให้ query ที่ค้าง
- **ห้ามผสม DB:** เลือก DB เดียวต่อโปรเจกต์ ห้าม migrate ข้ามระหว่างพัฒนาโดยไม่ทำ data migration

### 4.2 Auth & Security
- ระบบใช้ Lazy-auth (แสดง Login Popup เมื่อผู้ใช้พยายามทำ Action ที่ต้องใช้สิทธิ์) — ฟีเจอร์ใหม่ที่แก้ไขข้อมูลต้องครอบด้วย `requireAuth(() => action())`
- **Action Interception (UX Rule):** หลีกเลี่ยง `disabled={true}` บนปุ่มหลักเมื่อผู้ใช้ไม่มีสิทธิ์ (ผู้ใช้จะไม่รู้เหตุผล) — เปิดปุ่มไว้แต่ดักจับตอน `onClick` เพื่อแสดง Modal แจ้งเตือนหรือบังคับ Login แทน
- **🔐 Auth Token Storage:** เก็บ access/refresh token ใน **httpOnly cookie** (server set) หรือ **in-memory** เท่านั้น — **ห้ามเก็บใน `localStorage`/`sessionStorage`** เพราะ JavaScript อ่านได้ ⇒ โดน XSS ขโมยได้ (localStorage ใช้ได้แค่ค่าที่ไม่ใช่ความลับ เช่น UI preference, cache, sort order)
- **🚧 Client RBAC ไม่ใช่ trust boundary:** การซ่อนปุ่ม/เมนูฝั่ง client เป็นแค่ UX — การตัดสินใจอนุญาตจริงต้องเกิดที่ Server/API ก่อนแตะ DB ทุกครั้ง (client ปลอม request ได้เสมอ)

### 4.3 RBAC (Role-Based Access Control)
- **มาตรฐาน 3-4 ระดับ:** Super Admin (เข้าได้ทุกส่วน รวมตั้งค่าโครงสร้าง + ลบถาวร) → Admin/Manager (CRUD ในขอบเขตองค์กร แต่ปรับโครงสร้างไม่ได้) → User/Staff (อ่านได้ + แก้/ลบเฉพาะข้อมูลที่ตนสร้าง = Resource Ownership) → Guest/Viewer (Read-only)
- **Scope Rule (กฎสำคัญ — bug ที่พบบ่อย):** เฉพาะ role สูงสุด (เช่น `super_admin`) เท่านั้นที่ bypass tenant/scope check ได้ — **ห้ามใช้** เงื่อนไขแบบ `role !== "user"` เพื่อ bypass เพราะจะทำให้ `admin` หลุด scope ไปแก้ข้อมูลข้ามหน่วยงาน เช็คให้ตรงตัว เช่น `canAct = isTopAdmin || !user.scope || record.scope === user.scope`
- **หน้า Settings/โครงสร้างระบบ** เปิดเฉพาะ role สูงสุดเท่านั้น — แค่ `isAdmin` ไม่เพียงพอ
- **เช็คสิทธิ์ทั้ง 2 ฝั่งเสมอ:** UI (ซ่อน/block ปุ่ม) และ Server/API (ก่อนบันทึกลง DB)

### 4.4 Core System Logic & Validations (Agnostic Design)
- **Shared Utility Pattern (Parse / Detect / Format):** ฟังก์ชัน parse/detect/format ที่ถูกเรียกจากหลาย Component ต้องแยกเข้า `utils/` เสมอ (เช่น `utils/formatters.ts`) ห้ามเขียน logic ซ้ำใน Component — โดยเฉพาะ parse JSON/CSV, detect ประเภทไฟล์จาก MIME type, format URL สำหรับ embed
- **File/Attachment Handling Standard:** (1) เก็บ metadata เป็น JSON array `[{id, name, url, mimeType}]` แทน URL เดี่ยว (2) แสดงไอคอนตาม MIME type พร้อม color coding (PDF=red, Docs=sky, Sheets=emerald, Images=violet, Links=slate) (3) คลิก badge แล้วเปิด in-app preview modal (iframe/img) ก่อนเปิด tab ใหม่ (4) แสดงจำนวนไฟล์บน card/list ด้วย attachment icon
- **Smart Data Integrity & Schema Validation:** ทุกฟีเจอร์ที่รับ-ส่งข้อมูล ต้อง validate ผ่าน Schema (เช่น `Zod`) เสมอ เพื่อ End-to-End Type Safety, ป้องกัน Injection, และเช็ค Required Fields ก่อนยิง API
- **Seamless 3rd-Party APIs:** โค้ดที่เชื่อม API ภายนอกต้องแยกเป็นอิสระ (เช่น `/services/line.ts`, `/services/mail.ts`) ห้ามเขียน logic ยิง API รวมกับ UI — API Keys/Tokens/Webhook URLs ต้องตั้งผ่านหน้า Admin (DB) หรือ Environment Variables ได้โดยไม่ต้องแก้โค้ด
- **Safe Propagation & Batch Operations:** การคัดลอกข้อมูลจำนวนมากต้องตรวจปลายทางเสมอ ถ้าเป้าหมายมีข้อมูลอยู่แล้วให้ **ข้าม (Skip)** เพื่อกันการเขียนทับโดยไม่ตั้งใจ (Safe Copy)
- **Dynamic Configuration:** โครงสร้างที่ปรับเปลี่ยนได้ (สาขา, หมวดหมู่, จุดบริการ) ต้องสร้างจาก State Configuration ส่วนกลาง ห้าม Hardcode จำนวนคอลัมน์/หมวดหมู่ตายตัว
- **Auto-Sanitization & Recovery:** เมื่อ Config เปลี่ยนโครงสร้าง (เช่น ลดคอลัมน์) ระบบควรมีฟังก์ชันตัดข้อมูลส่วนเกินอัตโนมัติ และมี Fallback/Fuzzy Matching หากข้อมูลจาก Backend ไม่สอดคล้องกัน

### 4.5 Client-Side Cache (localStorage + In-Memory)
- **ใช้ 2 layer เสมอ:** memory (เร็ว, same session) + localStorage (persist ข้าม refresh) พร้อม TTL — ดูตัวอย่างใน `utils/dataCache.ts`
- **Silent Refresh Pattern:** initialize `useState` จาก cache ทันที (`useState(cached ?? [])`), ตั้ง `loading` เป็น `false` ถ้ามี cache — ดึงข้อมูลใหม่ใน background โดยไม่ `setLoading(true)` ซ้ำ
- **ห้าม** `setLoading(true)` แบบ unconditional ใน useEffect — spinner จะบัง cache ที่แสดงไว้แล้ว
- **ห้าม** เรียก `invalidateCache()` หลัง loadData สำเร็จ — จะล้าง cache ที่เพิ่งเขียนทันที
- **ห้าม** ใช้ `useEffect` เพื่อ set dropdown default value หลัง data โหลด — render เกิดก่อน effect รัน ทำให้เห็น "ไม่มีตัวเลือก" ให้ resolve ค่าเริ่มต้นใน `useState(() => resolve(cachedData))` แทน

### 4.6 Bulk Import (CSV / Excel Paste)
- **โครงสร้าง:** ปุ่ม trigger บน toolbar → Modal → Textarea รับ paste → Real-time Parser ใน `useEffect([input, lookupData])` → Preview Table แสดง `✓`/`✕` ต่อแถว → submit เฉพาะ valid rows ผ่าน batch API
- **Parser รองรับทั้งสองรูปแบบ:** ตรวจ `line.includes("\t")` — ถ้าใช่ split tab (Excel copy) ถ้าไม่ split comma (CSV)
- **Date handling:** แปลง locale date อัตโนมัติ — เช่น `วว/ดด/ปปปป` และถ้าปี > 2400 ให้ลบ 543 (พ.ศ. → ค.ศ.)
- **Fuzzy match กับ master data:** ใช้ `find(l => l.name.toLowerCase() === raw.toLowerCase() || l.name.includes(raw))` สำหรับ field ที่ต้อง match กับ lookup (หมวดหมู่, หน่วยงาน ฯลฯ)
- **Field-specific validation:** ถ้า field มีกฎ (เช่น email ต้องเป็น domain ขององค์กร, role ต้อง map จาก keyword) ให้ validate ทุกแถวก่อนขึ้น preview
- **Template CSV:** ใส่ UTF-8 BOM (`﻿`) นำหน้า content เสมอเพื่อให้ Excel เปิดภาษาไทยได้ — header ระบุ format ที่ชัดเจน (เช่น `วันที่ (วว/ดด/ปปปป ค.ศ.)`) — sample row ใช้ ค.ศ. เสมอ
- **Safe copy:** backend batchAdd ต้องทำ upsert — ถ้าพบ record เดิม (key เช่น email/id) ให้ update ไม่ insert ซ้ำ ห้าม silent overwrite

### 4.7 Admin & Backoffice Patterns
- **UI-Driven Configuration (No-Code & White-label):** การตั้งค่าระบบหลัก การเชื่อมต่อ DB และ **คำศัพท์เฉพาะ/ข้อความบน UI (Terminology & Branding)** (ชื่อเมนู, ชื่อองค์กร) ควรปรับผ่านหน้า Admin UI (ตาราง Settings) ได้เสมอ เพื่อให้แอดมินปรับให้เข้ากับองค์กรตนเองได้โดยไม่ต้องแก้โค้ด
- **Headless CMS & Page Builder (เฉพาะฟีเจอร์เนื้อหา):** ใช้สถาปัตยกรรม Headless CMS (JSON Blocks) เฉพาะเมื่อ "ระบุชัดเจน" ว่าต้องการระบบสร้างหน้าเว็บ/บทความ — **ห้าม** นำไปใช้กับหน้าระบบ UI ปกติเพื่อกันโค้ดซับซ้อนเกินจำเป็น
- **Standard CRUD Operations:** ต้องมี Feedback UI เสมอ (Skeleton/Spinner ขณะโหลด, Toast Notification เมื่อสำเร็จ/ล้มเหลว)
- **Data Tables & Grids:** ต้องรองรับ Pagination, Sorting, Search/Filtering เสมอ ห้ามเรนเดอร์ข้อมูลมหาศาลรวดเดียว (พิจารณา Virtualization หรือ Server-side Pagination)
- **Layout Architecture:** แยก Sidebar / Header / Main Content ชัดเจน หากใช้ Next.js จัดการผ่าน `layout.tsx` เพื่อกัน Re-render ส่วนโครงสร้างหลัก
- **Export & Reporting:** หากดาวน์โหลดรูป/รายงานที่ใช้ CSS ขั้นสูง ให้ใช้ Canvas API แบบ Native หรือสร้าง PDF ฝั่ง Server แทนไลบรารี DOM-to-Image (เช่น html2canvas) เพื่อกัน CSS เพี้ยน

### 4.8 User-Facing & Public Site Patterns
- **Dynamic Content & SEO:** หน้าไดนามิกจาก CMS ใช้ Dynamic Routing (เช่น `app/[slug]/page.tsx`) ต้องเรนเดอร์เนื้อหาอย่างปลอดภัย (กัน XSS) และอัปเดต Dynamic Metadata เพื่อ SEO เสมอ
- **Mobile-First & Responsive:** ออกแบบจากจอมือถือก่อน ปุ่ม/พื้นที่ Interactive ต้อง Touch-friendly (ขั้นต่ำ 44×44px) และรองรับจอใหญ่ผ่านคลาส `sm:`, `md:`, `lg:`
- **Optimistic UI & Friendly UX:** ตอบสนองทันที (UI อัปเดตก่อน API เสร็จ) ใช้ Skeleton Loader แทนจอขาว — Error Messages แปลเป็นภาษาที่คนทั่วไปเข้าใจ ห้ามแสดง Stack Trace — **บังคับ rollback:** ถ้า API fail ต้อง revert UI กลับค่าเดิม (เก็บ snapshot ก่อน optimistic update) + แจ้งเตือน ห้ามปล่อยให้จอแสดงค่าที่ไม่ตรงกับ DB
- **SEO & Core Web Vitals:** ใส่ใจ FCP/LCP/CLS ใช้ `<Image>` ของ `next/image` บังคับใส่ขนาดรูปเสมอ และใช้ Server Components เรนเดอร์ข้อมูลหน้าแรก

---

## 5️⃣ Deployment & Non-Functional

### 5.1 Next.js Specific Rules
- **"use client" Directive:** ใส่ `"use client"` บรรทัดบนสุด เฉพาะไฟล์ Component ที่ใช้ React Hooks หรือผูก Event (`onClick`) เท่านั้น
- **Data Fetching & Mutations:** ใช้ Server Components ดึงข้อมูลโดยตรง และใช้ **Server Actions** สำหรับบันทึก/แก้ไขข้อมูล (แทนการสร้าง API Routes)
- **Navigation:** ใช้ `<Link>` จาก `next/link` และ `useRouter` จาก `next/navigation` เสมอ (ห้ามดึงจาก `next/router` ของ Pages Router ตัวเก่า)
- **Favicon (App Router):** วาง `app/icon.svg` ขนาด 32×32 พื้นหลังทรงสี่เหลี่ยมมนสีหลักของแอป + ไอคอนสีขาว — Next.js pick up อัตโนมัติ
- **Tailwind v4 Force Light Mode:** ถ้าต้องการ Light Mode เท่านั้น ให้ override `@variant dark` ใน `globals.css` เป็น `@variant dark (&:is(.dark, .dark *))` และใส่ `className="light"` บน `<html>` เพื่อให้ `dark:` ไม่มีผลโดยไม่ต้องลบ dark classes ออก

### 5.2 Environment & Deployment (Bun + Vercel)
- **CLI Commands:** ใช้คำสั่ง Bun เสมอ (`bun install`, `bun add <package>`, `bun dev`)
- **Serverless Readiness:** รันบน Vercel (Serverless Edge) — Backend/Server Actions **ห้าม** อ่านเขียนไฟล์ลง Local Disk (`fs.writeFile`) ให้ทำผ่าน Database/External API แทน
- **Edge Compatibility:** โค้ดฝั่ง Server เน้น Web Standard APIs (`fetch`, `Request`, `Response`) เพื่อรันบน Edge Runtime ได้

### 5.3 Deployment Workflow (clasp + Vercel CLI — เฉพาะเมื่อ backend เป็น Google Apps Script)
- **One-time setup:** `bun add -g @google/clasp vercel` → `clasp login` → `vercel login` → `vercel link` → `vercel env pull .env.local`
- **Daily workflow:** push code ไป Apps Script (`clasp push`) → build + deploy prod (`vercel --prod`) — รวมเป็น script เดียวใน `package.json` (เช่น `bun run release`) และมี auto-deploy script รองรับ flag `-SkipScript`, `-Preview`, `-SyncEnv`, `-NewDeployment`
- **`scriptId` ≠ deployment URL:** `scriptId` (ใน `.clasp.json`) ใช้สำหรับ `clasp push/pull` เท่านั้น — deployment URL (`/exec`) เก็บใน env var (เช่น `NEXT_PUBLIC_GOOGLE_SCRIPT_URL`) ซึ่ง **ไม่เปลี่ยน** เมื่อ `clasp push`
- **อัปเดต deployment เดิมเสมอ:** ใช้ `clasp deploy --deploymentId <id>` — **ห้าม** `clasp deploy` ธรรมดา (สร้าง URL ใหม่ → ต้องอัปเดต env var ทุกครั้ง)
- **localStorage override:** ถ้าเคยกด "บันทึกการตั้งค่า" ใน Settings UI → localStorage อาจ override env var ในเครื่องนั้น แก้ด้วยการ clear localStorage หรือเปิด incognito
- **ห้าม commit `.env.local`** — เก็บค่าจริงใน Vercel dashboard, sync มาด้วย `vercel env pull .env.local`

### 5.4 Enterprise Non-Functional Requirements
- **Error Handling & Boundaries:** ห้ามปล่อยให้ Exception ทำให้หน้าจอขาว (White Screen of Death) ต้องมี `try/catch` ในจุดที่ดึงข้อมูลเสมอ และรองรับ React Error Boundaries
- **Accessibility (A11y):** ใช้ Semantic HTML (`<nav>`, `<main>`, `<article>`), ใส่ `aria-labels` ในปุ่มที่ไม่มีข้อความ, รองรับ Keyboard navigation (Focus management)
- **Testing Readiness:** เขียนโค้ดให้ Mock ง่าย หลีกเลี่ยงการผูกติด Global Object โดยไม่จำเป็น
- **i18n Readiness:** หลีกเลี่ยง Hardcode ข้อความแจ้งเตือน/Label ยาวๆ ลงใน Component ออกแบบเผื่อหลายภาษา (แยก Dictionary/Constant file)
- **Version Control & Commits:** ใช้รูปแบบ **Conventional Commits** (`feat:`, `fix:`, `refactor:`)
- **Built-in Documentation & Onboarding:** มีคู่มือฝังในตัว หรือ Tooltips อธิบาย "เฉพาะฟีเจอร์ที่ซับซ้อน" — ระวังอย่าใส่ Tooltips พร่ำเพรื่อในจุดที่เข้าใจง่ายอยู่แล้ว
- **Observability & Standardized API:** ทุก API/Server Action ต้องคืนค่ามาตรฐานเดียวกัน เช่น `{ success: boolean, data?: any, message?: string, error?: any }` และ **ห้าม `console.log()`** ข้อมูลละเอียดอ่อน (Sensitive Data/Tokens) ฝั่ง Client เด็ดขาด

---

## 🚫 Things to Avoid (อ่านก่อนเขียนทุกครั้ง)
- **ห้ามใช้ Type `any`** — ระบุ Type ให้ชัดที่สุด ถ้าไม่ทราบจริงๆ ใช้ `unknown`
- **ห้ามใช้ `@ts-ignore`** — แก้ Type Error ที่ต้นเหตุ ไม่ใช่ปิดการแจ้งเตือน
- **ห้ามใช้ `<a>` tag ปกติในการนำทาง (Internal Links)** — ใช้ `<Link>` ของ Framework (`next/link` / `react-router-dom`) เพื่อกัน Full-load refresh
- **ห้ามใช้ `window.location.reload()`** — refresh ข้อมูล/state ผ่าน React State (fetch ใหม่ หรือเคลียร์ cache) เท่านั้น เพื่อรักษา SPA experience
- **ห้ามใช้ Native Dialogs** (`window.alert()`, `window.confirm()`, `window.prompt()`) — ใช้ Custom Modal ของโปรเจกต์แทนเสมอ
- **ห้าม Hardcode ข้อมูลสำคัญ** — ตัวแปรเรียกผ่าน Environment Variables เสมอ
- **🚨 `NEXT_PUBLIC_` ไม่ใช่ความลับ** — ค่าที่ขึ้นต้น `NEXT_PUBLIC_` (หรือ `VITE_`) ถูก bundle เข้า JS ฝั่ง browser ใครก็เห็นใน DevTools ⇒ ใช้ได้**เฉพาะค่าเปิดเผยได้** (OAuth Client ID, public URL) เท่านั้น — **secret จริง** (password, API key, service token) ต้องเป็น env **ไม่มี prefix** อ่านได้เฉพาะฝั่ง Server (Server Action / Route Handler) ห้ามใส่ `NEXT_PUBLIC_` เด็ดขาด
- **ห้าม Hardcode การเชื่อมต่อฐานข้อมูล** — ห้ามฝัง Sheet ID, API URL, Connection String ตายตัว ให้ดึงจาก Env Var เป็นค่าเริ่มต้น และเปิดให้ override ผ่านหน้า Settings (UI) หรือ LocalStorage ได้
- **หลีกเลี่ยงการสร้าง State ที่ซ้ำซ้อน** — ถ้า derive จาก State เดิมได้ ใช้ `useMemo` หรือคำนวณใน render phase
- **ห้ามใช้ arbitrary text size (`text-[Npx]`) ทุกกรณี** — ใช้ token จาก type scale เท่านั้น (`text-xs`/`sm`/`base`/`lg`...) ขนาดเล็กสุดที่อนุญาตคือ `text-xs` (12px) — ขนาดหลุด scale คือสาเหตุหลักที่ UI ดูไม่นิ่ง
- **ห้ามใช้ arbitrary color (`bg-[#hex]`, `text-[#hex]`, `rgb(...)`) ทุกกรณี** — ใช้ hue จาก Theme Set เท่านั้น และห้ามหยิบ hue นอกชุดแทนความหมายเดิม (เช่น `rose` แทน `red`) — สีหลุด palette ตาจับได้ทันทีว่า "คนละระบบ"
- **ห้ามวาง Hook หลัง conditional return** — ทุก `useState`, `useEffect`, `useMemo`, `useCallback` ต้องอยู่ก่อน `if (x) return <Y />` เสมอ ไม่มีข้อยกเว้น
- **ห้ามซ้ำ page title ในเนื้อหาหน้า** — ถ้า Layout แสดง title ใน header bar แล้ว ห้ามมี `<h1>` หรือ section title ซ้ำใน body
- **ห้าม render percent/ratio โดยไม่ cap** — ทุกการแสดงผลเปอร์เซ็นต์ต้องผ่าน `formatPercent(value)` (text) หรือ `Math.min(100, value)` (width/stroke) ห้ามเขียน `{value}%` ตรงๆ เพราะค่าจริงอาจเกิน 100% (ทำเกินเป้า)
- **ห้ามใช้ native `<select>` และ `<select multiple>`** — ใช้ `<CustomSelect>` / `<CustomMultiSelect>` เท่านั้น ไม่มีข้อยกเว้น (รวมถึง filter bar, sort control, inline editor)
- **ห้ามผสมหลาย DB ในโปรเจกต์เดียว** — เลือก DB เดียว ห้าม migrate ข้ามระหว่างพัฒนาโดยไม่ทำ data migration
- **ห้าม `console.log()` ข้อมูลละเอียดอ่อน** (Tokens, รหัสผ่าน, PII) ฝั่ง Client เด็ดขาด

---

## 🔍 Audit Mode (Protocol Auditor — ใช้ตรวจระบบที่ทำไปแล้ว / ระบบเก่า)
> เมื่อถูกสั่ง "audit" / "ตรวจ" / "review เทียบ AGENTS.md" ให้สวมบทบาท **ผู้ตรวจ** ไม่ใช่นักเขียนโค้ด — **ห้ามแก้โค้ดจนกว่าจะได้รับอนุมัติ**

### ขั้นตอนการตรวจ (ทำตามลำดับ)
1. **ระบุขอบเขต:** repo นี้หรือระบบอื่น? — ถ้าระบบอื่น ให้**ข้าม 1.2** และเกณฑ์ที่อิงค่าเฉพาะ (host/DB/domain/อีเมลองค์กร) ตรวจเฉพาะกฎ universal
2. **Detect บริบทก่อนตัดสิน:** stack จริง (Next.js/Vite), ธีมจริง (Primary hue = สีที่ใช้กับปุ่มหลักบ่อยสุด) — ของที่ "ต่างจากเอกสารแต่คงเส้นคงวาในตัวเอง" **ไม่ใช่ violation**
3. **ไล่ตรวจตาม checklist ด้านล่าง** จาก 🔴 ไป ⚪
4. **Report เป็นตาราง:** กฎ (หัวข้อในเอกสารนี้) / `file:line` / severity / วิธีแก้สั้นๆ — ทุกข้อต้องอ้าง `file:line` ห้าม report ลอยๆ
5. **สรุปท้าย:** นับจำนวนต่อ severity + ชี้ "3 อันดับแรกที่ควรแก้ก่อน" + แยก *violation* / *suggestion* ชัดเจน
6. **รออนุมัติ** แล้วค่อยแก้จาก severity สูงไปต่ำ

### 🔴 Critical — Security & Data (อ้าง 4.1 / 4.2 / 4.3 / Avoid)
- secret จริง (password, API key, service token) อยู่ใน `NEXT_PUBLIC_` / `VITE_` / hardcode ในโค้ด
- token เก็บใน `localStorage` / `sessionStorage`
- SQL ต่อ string จากค่าผู้ใช้ (`` `WHERE id = ${id}` ``) — ไม่ใช้ placeholder
- `createConnection()` ใหม่ต่อ request / ไม่มี connection pool
- RBAC เช็คฝั่ง client อย่างเดียว / scope bypass หละหลวมแบบ `role !== "user"`
- `console.log` ข้อมูลลับ (token/รหัสผ่าน/PII) ฝั่ง client
- render เนื้อหาจากผู้ใช้โดยไม่ sanitize (XSS) เช่น `dangerouslySetInnerHTML` ไม่กรอง
- hardcode connection string / Sheet ID / Webhook URL

### 🟠 Correctness — ทำงานผิดจริง (อ้าง 2.1 / 2.2 / 3.3 / 3.4 / 4.8 / Avoid)
- Hook อยู่หลัง early return (`if (x) return` ก่อน `useState`/`useEffect`)
- native `<select>` / `<select multiple>`
- native dialog — **ตรวจทั้ง `window.alert/confirm/prompt` และแบบไม่มี prefix (`alert(`, `confirm(`)** เพราะ grep แค่ `window.` จะเจอไม่ครบ
- `<a>` นำทางภายใน / `window.location.reload()`
- percent/ratio render โดยไม่ cap 100
- คู่วันที่ไม่มี guard `end < start`
- optimistic UI ไม่มี rollback เมื่อ API fail
- `any` / `@ts-ignore`

### 🟡 Pattern — ขาดมาตรฐาน (อ้าง 1.3 / 2.1 / 3.3 / 4.4 / 4.5 / 4.7 / 5.4)
- async view ไม่ครบ 3 สถานะ loading / empty / error
- ปุ่ม mutation ไม่มี double-submit guard (disable + loading ระหว่าง in-flight)
- action บันทึก/ลบข้อมูลสำคัญ ไม่มี Confirmation Modal
- `fetch` ตรงจาก component (ไม่ผ่าน `services/`)
- business logic กองใน `page.tsx` / ไฟล์เกิน 250-300 บรรทัด
- logic parse/format ซ้ำกันหลาย component (ไม่แยกเข้า `utils/`)
- ตารางข้อมูลใหญ่ไม่มี pagination / search
- API response ไม่อยู่ในรูปแบบมาตรฐาน `{ success, data?, message? }`
- ข้อมูลที่โหลดช้าไม่มี cache (4.5)

### ⚪ Design — ความนิ่ง (อ้าง 3.1) — ตรวจ "ความเป็นระบบ" ไม่ใช่รสนิยม
- `text-[Npx]` arbitrary size — มี = หลุด type scale
- `#hex` / `rgb(` arbitrary color / นับจำนวน hue ทั้งระบบ เกิน ~7 = palette เฟ้อ
- semantic ปน hue (`rose` ปน `red`, `green` ปน `emerald` ในความหมายเดียวกัน)
- shade ไม่คงสูตร (ปุ่ม primary บางจุด `-400` บางจุด `-600`)
- font weight ใช้จริงเกิน 3 ระดับ
- `rounded-*` ปนมั่วใน element ประเภทเดียวกัน
- status badge ไม่คงรูป (ความหมายเดียวกัน บางจุด pill บางจุด plain text)
- **วิธีแก้ดีไซน์ = consolidation:** สรุปธีมจริงจากส่วนใหญ่ แล้วยุบส่วนน้อยเข้าหา — **ห้ามเสนอรื้อธีมใหม่ทั้งระบบ**

### กฎเหล็กของผู้ตรวจ
- แยก *violation* (วัดได้ตาม checklist) ออกจาก *suggestion* (รสนิยม: ความสวย, ระยะห่าง, tooltips) เสมอ — false positive ทำลายความน่าเชื่อถือของการ audit ทั้งรอบ
- เจอของที่กฎไม่ครอบ → เสนอเป็น "ข้อเสนอเพิ่มกฎ" แยกท้าย report ไม่ใช่นับเป็น violation
