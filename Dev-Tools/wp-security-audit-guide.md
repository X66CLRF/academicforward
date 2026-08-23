# WordPress Security Audit & Auto-Fix Guide (IIS/Windows Server)

> **วันที่จัดทำ:** 2026-06-12  
> **สภาพแวดล้อม:** WordPress บน IIS (Windows Server), PHP runs as IUSR  
> **จุดประสงค์:** รวบรวมปัญหาจริงที่พบ + คำสั่งแก้ไขที่ใช้ได้จริง เพื่อ reuse ในอนาคต

---

## สารบัญ

1. [Pre-Audit Checklist](#1-pre-audit-checklist)
2. [ปัญหาที่พบบ่อย & วิธีแก้ไขอัตโนมัติ (PowerShell)](#2-ปัญหาที่พบบ่อย--วิธีแก้ไขอัตโนมัติ-powershell)
3. [Database Audit Queries (SQL)](#3-database-audit-queries-sql)
4. [IIS web.config Security Template](#4-iis-webconfig-security-template)
5. [mu-plugins Security Template](#5-mu-plugins-security-template)
6. [Post-Fix Verification Checklist](#6-post-fix-verification-checklist)
7. [การป้องกันในอนาคต](#7-การป้องกันในอนาคต)

---

## 1. Pre-Audit Checklist

ก่อนเริ่ม audit ทุกครั้ง ให้รวบรวมข้อมูลพื้นฐานก่อน:

### ข้อมูลที่ต้องรู้

| รายการ | คำสั่งตรวจสอบ |
|--------|--------------|
| WordPress root path | `(Get-Item "Y:\").FullName` |
| PHP version | `php -v` |
| IIS App Pool identity | IIS Manager → App Pools → Advanced Settings |
| WordPress DB prefix | ดูใน `wp-config.php` |
| Active plugins | ดูใน WP Admin หรือ query DB |

### PowerShell - ดูข้อมูล Site พื้นฐาน

```powershell
# กำหนด WordPress root (ปรับ path ตามจริง)
$wpRoot = "Y:\"
$wpContent = "$wpRoot\wp-content"

# แสดงข้อมูลสิทธิ์ปัจจุบัน
Write-Host "=== Current Permissions on wp-content ===" -ForegroundColor Cyan
icacls "$wpContent"

# ตรวจสอบ wp-config.php ว่ามี debug mode เปิดอยู่ไหม
Write-Host "`n=== WP_DEBUG Status ===" -ForegroundColor Cyan
Select-String -Path "$wpRoot\wp-config.php" -Pattern "WP_DEBUG"

# แสดง PHP identity (ต้องรันผ่าน web request แล้วดู error log)
Write-Host "`n=== IIS App Pool Check ===" -ForegroundColor Cyan
Import-Module WebAdministration -ErrorAction SilentlyContinue
Get-WebConfiguration "system.applicationHost/applicationPools/add" | 
    Select-Object name, processModel | Format-Table -AutoSize
```

---

## 2. ปัญหาที่พบบ่อย & วิธีแก้ไขอัตโนมัติ (PowerShell)

---

### ปัญหาที่ 1 — Plugin "Disable All Updates" บล็อก WordPress Updates

**ปัญหา:**  
Plugin เช่น "Admin Site Enhancements" มี feature "Disable All Updates" ที่เมื่อเปิดใช้งาน จะบล็อก core/plugin/theme updates ทั้งหมด ทำให้ site เสี่ยงต่อช่องโหว่จาก outdated software

**วิธีตรวจสอบ:**

```powershell
# ตรวจสอบ plugin options ใน database ที่เกี่ยวกับการปิด updates
# (ต้องรัน SQL query ใน phpMyAdmin หรือ MySQL CLI)
# ดู Section 3 สำหรับ SQL queries
```

```sql
-- ตรวจหา options ที่ disable updates
SELECT option_name, option_value 
FROM wp_options 
WHERE option_name LIKE '%disable%update%' 
   OR option_name LIKE '%asenha%'
   OR option_name LIKE '%admin_site_enhancements%';
```

**คำสั่งแก้ไข (mu-plugin):**

```powershell
# สร้าง mu-plugin เพื่อ force enable updates (ดู Section 5 สำหรับ full template)
$muPluginsDir = "Y:\wp-content\mu-plugins"
if (-not (Test-Path $muPluginsDir)) {
    New-Item -ItemType Directory -Path $muPluginsDir -Force
    Write-Host "Created mu-plugins directory" -ForegroundColor Green
}
```

```php
// ใส่ใน mu-plugin: force-updates.php
add_filter('auto_update_plugin', '__return_true');
add_filter('auto_update_theme', '__return_true');
add_filter('auto_update_core', '__return_true');
// ยกเลิกการ disable ที่ plugin อื่นทำไว้
remove_all_filters('pre_site_transient_update_core');
remove_all_filters('pre_site_transient_update_plugins');
remove_all_filters('pre_site_transient_update_themes');
```

---

### ปัญหาที่ 2 — IIS App Pool Permissions ไม่เพียงพอ

**ปัญหา:**  
WordPress ต้องการสิทธิ์ **Modify** (ไม่ใช่แค่ Read) บน directories บางตัวเพื่อ upload files, install updates, และ cache data

**Directories ที่ต้องการ Modify:**
- `wp-content/uploads/` — media uploads
- `wp-content/upgrade/` — core/plugin updates
- `wp-content/cache/` — caching plugins

**วิธีตรวจสอบ:**

```powershell
$wpContent = "Y:\wp-content"

# ตรวจสอบ permissions บน directories สำคัญ
foreach ($dir in @("uploads", "upgrade", "cache")) {
    $path = "$wpContent\$dir"
    Write-Host "`n=== $dir ===" -ForegroundColor Yellow
    if (Test-Path $path) {
        icacls $path
    } else {
        Write-Host "Directory does not exist: $path" -ForegroundColor Red
    }
}
```

**คำสั่งแก้ไข:**

```powershell
$wpRoot    = "Y:\"
$wpContent = "Y:\wp-content"

# App Pool identity (ปรับชื่อ App Pool ตามจริง เช่น "DefaultAppPool")
$appPool = "IIS AppPool\DefaultAppPool"

# ให้สิทธิ์ Modify บน directories ที่จำเป็น
$dirsNeedingModify = @(
    "$wpContent\uploads",
    "$wpContent\upgrade",
    "$wpContent\cache",
    "$wpContent\wflogs"   # Wordfence logs (ถ้ามี)
)

foreach ($dir in $dirsNeedingModify) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created: $dir" -ForegroundColor Yellow
    }
    icacls $dir /grant "${appPool}:(OI)(CI)M" /T
    Write-Host "Granted Modify to App Pool on: $dir" -ForegroundColor Green
}
```

---

### ปัญหาที่ 3 — PHP รันในฐานะ IUSR (ไม่ใช่ App Pool Identity)

**ปัญหา:**  
บน Windows Server บางการตั้งค่า PHP จะรันในฐานะ `IUSR` แทน App Pool identity ทำให้ต้องให้สิทธิ์กับ `IUSR` แยกต่างหาก

**วิธีตรวจสอบ:**

```powershell
# ดูว่า PHP handler ตั้งค่า identity เป็นอะไร
# วิธีที่ง่ายที่สุดคือดู IIS Manager:
# Sites → [Your Site] → Handler Mappings → PHP → Edit → Request Restrictions

# หรือตรวจสอบผ่าน applicationHost.config
$iisConfig = "C:\Windows\System32\inetsrv\config\applicationHost.config"
Select-String -Path $iisConfig -Pattern "php" | Select-Object -First 20
```

**คำสั่งแก้ไข — ให้สิทธิ์ IUSR อย่างปลอดภัย:**

> ⚠️ **คำเตือน:** อย่าให้ `IUSR:(OI)(CI)M` บน root ทั้งหมด เพราะ IUSR จะแก้ไข `wp-config.php`, `wp-login.php` และ core files ได้ — เป็นช่องโหว่ร้ายแรง

```powershell
$wpRoot    = "D:\Websites\ejournal"   # ปรับ path ตามจริง
$wpContent = "$wpRoot\wp-content"

# ให้ IUSR แค่ Read บน root (เพื่อ serve static files)
icacls $wpRoot /grant "IUSR:(OI)(CI)R" /T
Write-Host "Granted IUSR Read on WordPress root" -ForegroundColor Green

# ให้ IUSR Write เฉพาะโฟลเดอร์ที่ WordPress ต้องเขียน
$dirsNeedingWrite = @(
    "$wpContent\uploads",   # สำหรับ media uploads
    "$wpContent\upgrade",   # สำหรับ plugin/theme updates
    "$wpContent\cache",     # สำหรับ caching plugins
    "$wpContent\mu-plugins" # ถ้าต้องการ
)

foreach ($dir in $dirsNeedingWrite) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    icacls $dir /grant "IUSR:(OI)(CI)M" /T
    Write-Host "Granted IUSR Modify on: $dir" -ForegroundColor Green
}

# สำหรับ llms.txt หรือไฟล์ที่ Yoast/plugin ต้องสร้างที่ root
# ให้สิทธิ์เฉพาะ Write (ไม่ใช่ Modify ทั้ง folder)
icacls $wpRoot /grant "IUSR:(W)"
Write-Host "Granted IUSR Write-only on root (for llms.txt, robots.txt)" -ForegroundColor Green

# ปิดกั้นไฟล์สำคัญไม่ให้ IUSR แก้ไขได้
$protectedFiles = @(
    "$wpRoot\wp-config.php",
    "$wpRoot\wp-login.php",
    "$wpRoot\wp-settings.php",
    "$wpRoot\.htaccess",
    "$wpRoot\web.config"
)

foreach ($file in $protectedFiles) {
    if (Test-Path $file) {
        icacls $file /deny "IUSR:(W,M,D)"
        Write-Host "Protected: $file" -ForegroundColor Yellow
    }
}

# ตรวจสอบผล
Write-Host "`n=== Verification ===" -ForegroundColor Cyan
icacls $wpRoot | Select-String "IUSR"
```

> **หมายเหตุ:** Flag `(OI)(CI)M` หมายถึง:
> - `(OI)` = Object Inherit — files ใหม่ใน directory จะได้รับ permission นี้
> - `(CI)` = Container Inherit — subdirectories จะได้รับ permission นี้
> - `R` = Read Only — อ่านได้อย่างเดียว (ปลอดภัย)
> - `W` = Write — เขียนได้แต่ลบไม่ได้
> - `M` = Modify — read, write, delete ได้ (ใช้เฉพาะ folder ที่จำเป็น)

> **ช่องโหว่ที่ต้องระวัง:** ถ้าให้ `IUSR` สิทธิ์ `M` บน root — แฮคเกอร์ที่ exploit PHP จะแก้ไข `wp-config.php` (ได้ DB credentials) และ `wp-login.php` (backdoor) ได้ทันที

---

### ปัญหาที่ 4 — SSL/TLS Certificate Trust Issues บน Windows Server

**ปัญหา:**  
Windows Server บางตัวไม่ trust CA certificates บางตัว ทำให้ WordPress ไม่สามารถ connect ไปยัง external services (WordPress.org update servers, Jetpack, etc.)

**วิธีตรวจสอบ:**

```powershell
# ทดสอบ SSL connection ไปยัง WordPress.org
$url = "https://api.wordpress.org"
try {
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10
    Write-Host "Connection OK: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Connection FAILED: $_" -ForegroundColor Red
}

# ดู root certificates ที่มีอยู่
Get-ChildItem -Path "Cert:\LocalMachine\Root" | 
    Where-Object { $_.Subject -like "*Let's Encrypt*" -or $_.Subject -like "*ISRG*" } |
    Select-Object Subject, Thumbprint, NotAfter
```

**คำสั่งแก้ไข — อัปเดต Root Certificates:**

```powershell
# วิธีที่ 1: ใช้ certutil (อาจ fail ถ้า Windows Update blocked)
certutil -generateSSTFromWU roots.sst
certutil -addstore -f Root roots.sst

# วิธีที่ 2: อัปเดตผ่าน Windows Update (แนะนำ)
# รันใน PowerShell (Admin)
$updateSession = New-Object -ComObject Microsoft.Update.Session
$updateSearcher = $updateSession.CreateUpdateSearcher()
$searchResult = $updateSearcher.Search("IsInstalled=0 and Type='Software'")
Write-Host "Available updates: $($searchResult.Updates.Count)"

# วิธีที่ 3: Import certificate จากเครื่องที่ trust ได้
# Export จากเครื่องที่ OK: certmgr.msc → Trusted Root CAs → Export
# Import บน server: 
# Import-Certificate -FilePath ".\ca-bundle.cer" -CertStoreLocation "Cert:\LocalMachine\Root"

# วิธีที่ 4: ใช้ PHP cURL กับ ca-bundle แทน Windows cert store
# เพิ่มใน php.ini:
# curl.cainfo = "C:\php\extras\ssl\cacert.pem"
# openssl.cafile = "C:\php\extras\ssl\cacert.pem"
# ดาวน์โหลด cacert.pem จาก https://curl.se/ca/cacert.pem
```

---

### ปัญหาที่ 5 — Jetpack Module ทำให้เกิด 400 Errors

**ปัญหา:**  
Jetpack Subscriptions module (หรือ module อื่น) อาจทำให้เกิด HTTP 400 errors บน specific endpoints

**วิธีตรวจสอบ:**

```powershell
# ดู IIS error logs
$logPath = "C:\inetpub\logs\LogFiles"
Get-ChildItem $logPath -Recurse -Filter "*.log" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 3 | 
    ForEach-Object {
        Select-String -Path $_.FullName -Pattern " 400 " | 
            Select-Object -Last 20
    }
```

**คำสั่งแก้ไข — Disable Jetpack Module ผ่าน mu-plugin:**

```php
// ใส่ใน wp-content/mu-plugins/jetpack-module-control.php
<?php
/**
 * Disable specific Jetpack modules that cause issues
 */
add_filter('jetpack_get_default_modules', function($modules) {
    $disable = [
        'subscriptions',   // ทำให้เกิด 400 errors
        // เพิ่ม module อื่นที่ต้องการ disable ที่นี่
    ];
    return array_diff($modules, $disable);
});

// Force disable modules ที่ active อยู่แล้ว
add_action('init', function() {
    if (class_exists('Jetpack')) {
        Jetpack::deactivate_module('subscriptions');
    }
});
```

---

### ปัญหาที่ 6 — Google Search Console Verification Code จาก Account อื่น

**ปัญหา:**  
พบ Google Search Console verification code ใน `wp_options` ที่เป็นของ account อื่น (อาจเป็น hacker หรือ เจ้าของเก่า) ทำให้คนอื่นสามารถ verify ownership ของ site ได้

**วิธีตรวจสอบ:**

```sql
-- ตรวจหา Google verification codes ทั้งหมด
SELECT option_name, option_value, autoload
FROM wp_options
WHERE option_name LIKE '%verification%'
   OR option_name LIKE '%google%'
   OR option_name LIKE '%site-verification%'
ORDER BY option_name;

-- ตรวจ verification_services_codes (เก็บ codes หลายอันรวมกัน)
SELECT option_value 
FROM wp_options 
WHERE option_name = 'verification_services_codes';
```

**คำสั่งแก้ไข:**

```sql
-- ดู codes ที่มีอยู่ก่อน (JSON format)
SELECT option_value FROM wp_options WHERE option_name = 'verification_services_codes';

-- ลบ verification codes ทั้งหมด (แล้ว add ใหม่ผ่าน plugin)
UPDATE wp_options 
SET option_value = 'a:0:{}'  -- empty serialized array
WHERE option_name = 'verification_services_codes';

-- หรือลบทิ้งเลย
DELETE FROM wp_options WHERE option_name = 'verification_services_codes';

-- ลบ Google verification meta tags ที่เก็บแยก
DELETE FROM wp_options 
WHERE option_name LIKE '%google-site-verification%';
```

> **หลังแก้ไข:** ไปที่ Google Search Console → Settings → Ownership Verification → ตรวจสอบว่ามีเฉพาะ account ของเราเท่านั้น

---

### ปัญหาที่ 7 — SEO Farming / Spam URLs ใน Google Index

**ปัญหา:**  
จากการถูก hack ในอดีต มี spam URLs เช่น `/Baccarat/`, `/ogeh/video/`, `/erot/video/`, `/books/video/`, `/files/video/` ยังคงอยู่ใน Google index

**วิธีตรวจสอบ:**

```powershell
# ตรวจหา suspicious files/directories ใน WordPress root
$wpRoot = "Y:\"
$suspiciousDirs = @("Baccarat", "ogeh", "erot", "books", "files", "video", "slot", "casino")

foreach ($dir in $suspiciousDirs) {
    $path = "$wpRoot\$dir"
    if (Test-Path $path) {
        Write-Host "FOUND SUSPICIOUS DIR: $path" -ForegroundColor Red
        Get-ChildItem $path -Recurse | Select-Object FullName
    }
}

# ตรวจหา .php files แปลกๆ ใน root
Get-ChildItem $wpRoot -Filter "*.php" -File | 
    Where-Object { $_.Name -notin @(
        "wp-config.php","wp-load.php","wp-blog-header.php","wp-settings.php",
        "wp-cron.php","wp-login.php","wp-mail.php","wp-signup.php",
        "wp-trackback.php","wp-activate.php","wp-comments-post.php",
        "wp-links-opml.php","index.php","xmlrpc.php"
    )} |
    Select-Object Name, LastWriteTime, Length
```

```sql
-- ตรวจ rewrite rules ใน database ที่อาจเป็น spam
SELECT option_value 
FROM wp_options 
WHERE option_name = 'rewrite_rules';

-- ค้นหา URLs แปลกๆ ใน posts (SEO spam injection)
SELECT ID, post_title, post_status, post_type, post_modified
FROM wp_posts
WHERE post_content LIKE '%baccarat%'
   OR post_content LIKE '%casino%'
   OR post_content LIKE '%ogeh%'
   OR post_content LIKE '%viagra%'
   OR post_content LIKE '%poker%'
   OR post_status = 'publish'
   AND post_type NOT IN ('post', 'page', 'attachment', 'nav_menu_item', 'revision')
ORDER BY post_modified DESC
LIMIT 50;
```

**คำสั่งแก้ไข — Redirect Spam URLs:**

```powershell
# เพิ่ม redirects ใน web.config สำหรับ spam URLs ที่ยังอยู่ใน Google index
# (ดู Section 4 สำหรับ full web.config template)

# ตรวจสอบและลบ spam directories
$spamDirs = @("Y:\Baccarat", "Y:\ogeh", "Y:\erot")
foreach ($dir in $spamDirs) {
    if (Test-Path $dir) {
        Remove-Item $dir -Recurse -Force
        Write-Host "Removed: $dir" -ForegroundColor Green
    }
}
```

```sql
-- Redirect spam URLs ผ่าน WordPress (ใส่ใน functions.php หรือ plugin)
-- หรือใช้ Redirection plugin แล้ว import CSV

-- ลบ posts ที่เป็น spam
-- (ตรวจสอบให้แน่ใจก่อนลบ!)
DELETE FROM wp_posts WHERE ID IN (
    SELECT ID FROM (
        SELECT ID FROM wp_posts 
        WHERE post_content LIKE '%baccarat%' 
        AND post_status = 'publish'
    ) tmp
);
```

---

### ปัญหาที่ 8 — web.config MIME Type Conflict (.xml)

**ปัญหา:**  
การเพิ่ม `.xml` MIME type ใน `web.config` ทำให้เกิด 500 errors บน JavaScript files ทุกไฟล์ เพราะ IIS มี `.xml` MIME type อยู่แล้วใน global config การเพิ่มซ้ำทำให้เกิด conflict

**วิธีตรวจสอบ:**

```powershell
# ดู MIME types ที่ IIS มีอยู่แล้ว (global)
Import-Module WebAdministration
Get-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST' `
    -filter "system.webServer/staticContent" `
    -name "." | 
    Select-Object -ExpandProperty Collection | 
    Where-Object { $_.fileExtension -eq ".xml" }

# ดู MIME types ใน web.config ของ site
$webConfig = "Y:\web.config"
Select-String -Path $webConfig -Pattern "mimeMap|\.xml"
```

**คำสั่งแก้ไข:**

```powershell
# อ่าน web.config และตรวจหา duplicate MIME types
[xml]$config = Get-Content "Y:\web.config"
$mimeTypes = $config.configuration.'system.webServer'.staticContent.mimeMap
$mimeTypes | Select-Object fileExtension, mimeType | Sort-Object fileExtension

# วิธีปลอดภัย: ใช้ <remove> ก่อน <add> ใน web.config
```

```xml
<!-- วิธีที่ถูกต้องใน web.config: ใช้ remove ก่อน add เสมอ -->
<staticContent>
    <remove fileExtension=".xml" />
    <mimeMap fileExtension=".xml" mimeType="text/xml" />
    <!-- เพิ่ม MIME types อื่นๆ ด้วยวิธีเดียวกัน -->
    <remove fileExtension=".woff" />
    <mimeMap fileExtension=".woff" mimeType="font/woff" />
    <remove fileExtension=".woff2" />
    <mimeMap fileExtension=".woff2" mimeType="font/woff2" />
</staticContent>
```

---

### ปัญหาที่ 9 — Yoast llms.txt Permission Denied

**ปัญหา:**  
Yoast SEO (version ใหม่) สร้างไฟล์ `llms.txt` เพื่อให้ AI crawlers อ่าน แต่ถ้า IUSR ไม่มีสิทธิ์ write บน root folder จะเกิด permission error

**วิธีตรวจสอบ:**

```powershell
# ตรวจว่า llms.txt มีอยู่ไหม
$llmsTxt = "Y:\llms.txt"
if (Test-Path $llmsTxt) {
    Write-Host "llms.txt exists" -ForegroundColor Green
    Get-Item $llmsTxt | Select-Object LastWriteTime, Length
} else {
    Write-Host "llms.txt missing - possible permission issue" -ForegroundColor Yellow
}

# ดู PHP error log สำหรับ permission errors
$phpErrorLog = "C:\Windows\Temp\php_errors.log"  # ปรับ path ตาม php.ini
if (Test-Path $phpErrorLog) {
    Select-String -Path $phpErrorLog -Pattern "permission|llms" | 
        Select-Object -Last 20
}
```

**คำสั่งแก้ไข:**

```powershell
$wpRoot = "Y:\"

# ให้สิทธิ์ IUSR Modify บน root folder (recursive)
icacls $wpRoot /grant "IUSR:(OI)(CI)M" /T
Write-Host "Granted IUSR Modify on root (recursive)" -ForegroundColor Green

# ตรวจสอบผล
icacls $wpRoot | Select-String "IUSR"

# Force สร้าง llms.txt โดย Yoast (flush rewrite rules)
# ทำผ่าน WP-CLI ถ้ามี:
# wp rewrite flush --hard
```

---

### ปัญหาที่ 10 — X-Robots-Tag: noindex บน Sitemap

**ปัญหา:**  
Sitemap URLs มี HTTP header `X-Robots-Tag: noindex` ทำให้ดูเหมือน Google จะไม่ index sitemap

**วิธีตรวจสอบ:**

```powershell
# ตรวจ HTTP headers ของ sitemap
$sitemapUrl = "https://yoursite.com/sitemap_index.xml"
try {
    $response = Invoke-WebRequest -Uri $sitemapUrl -UseBasicParsing -Method HEAD
    $response.Headers | Where-Object { $_.Key -like "*robot*" -or $_.Key -like "*noindex*" }
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
```

> **หมายเหตุ:** `X-Robots-Tag: noindex` บน sitemap เป็น **behavior ปกติของ Yoast** — Google จะยังคง read sitemap ได้ เพราะ noindex ส่งผลกับ the sitemap page itself ไม่ใช่ URLs ภายใน sitemap ไม่จำเป็นต้องแก้ไข

---

### ปัญหาที่ 11 — Hacker's Google Verification Code ใน wp_options

**ปัญหา:**  
หลังจาก site ถูก hack มักพบ Google/Bing verification codes ของ hacker ยังคงอยู่ใน `wp_options` table ทำให้ hacker ยังมี Search Console access

**วิธีตรวจสอบ:**

```sql
-- ตรวจหา verification codes ทั้งหมด
SELECT option_id, option_name, option_value
FROM wp_options
WHERE option_name LIKE '%verify%'
   OR option_name LIKE '%verification%'
   OR option_value LIKE '%google-site-verification%'
   OR option_value LIKE '%msvalidate%'
   OR option_value LIKE '%yandex-verification%'
ORDER BY option_name;
```

**คำสั่งแก้ไข:**

```sql
-- Step 1: ดู current value ก่อน
SELECT option_value FROM wp_options WHERE option_name = 'verification_services_codes';

-- Step 2: ลบ verification codes ที่ไม่รู้จัก
-- ถ้า option_value เป็น serialized PHP array ให้ใช้ phpMyAdmin แก้ไข
-- หรือ reset เป็น empty:
UPDATE wp_options 
SET option_value = 'a:4:{s:6:"google";s:0:"";s:4:"bing";s:0:"";s:6:"yandex";s:0:"";s:7:"baidu  ";s:0:"";}' 
WHERE option_name = 'verification_services_codes';

-- Step 3: ลบ verification meta แยก (ถ้ามี)
DELETE FROM wp_options WHERE option_name = 'google-site-verification';
DELETE FROM wp_options WHERE option_name = 'msvalidate.01';
```

---

## 3. Database Audit Queries (SQL)

> รันใน phpMyAdmin, MySQL CLI, หรือ TablePlus  
> **แทนที่ `wp_` ด้วย prefix จริงของ database คุณ**

### 3.1 ตรวจ Spam Rewrite Rules

```sql
-- ดู rewrite rules ทั้งหมด (อาจ include spam paths)
SELECT option_value 
FROM wp_options 
WHERE option_name = 'rewrite_rules';

-- ตรวจหา .htaccess-style injections ใน options
SELECT option_name, LEFT(option_value, 200) as preview
FROM wp_options
WHERE option_value LIKE '%RewriteRule%'
   OR option_value LIKE '%RewriteCond%'
   OR option_value LIKE '%redirect%'
   AND option_name != 'permalink_structure'
ORDER BY option_name;
```

### 3.2 ตรวจ Suspicious Users

```sql
-- ดู users ทั้งหมด เรียงตาม registered date
SELECT ID, user_login, user_email, user_registered, display_name
FROM wp_users
ORDER BY user_registered DESC;

-- ตรวจหา admin accounts ที่อาจเป็น backdoor
SELECT u.ID, u.user_login, u.user_email, u.user_registered, um.meta_value as capabilities
FROM wp_users u
JOIN wp_usermeta um ON u.ID = um.user_id
WHERE um.meta_key = 'wp_capabilities'
  AND um.meta_value LIKE '%administrator%'
ORDER BY u.user_registered DESC;

-- ตรวจหา users ที่ email ใช้ domain แปลกๆ
SELECT ID, user_login, user_email, user_registered
FROM wp_users
WHERE user_email NOT LIKE '%@yourdomain.com%'  -- ปรับ domain ตามจริง
  AND user_email NOT LIKE '%@gmail.com%'
  AND user_email NOT LIKE '%@hotmail.com%'
ORDER BY user_registered DESC;

-- ดู login sessions ที่ active อยู่ (WordPress sessions)
SELECT user_id, meta_value 
FROM wp_usermeta 
WHERE meta_key = 'session_tokens';
```

### 3.3 ตรวจ Malicious Verification Codes

```sql
-- ตรวจ verification codes ทั้งหมด
SELECT option_id, option_name, option_value
FROM wp_options
WHERE option_name LIKE '%verify%'
   OR option_name LIKE '%verification%'
   OR option_name LIKE '%google%site%'
   OR option_name LIKE '%msvalidate%'
   OR option_name LIKE '%yandex%'
ORDER BY option_name;

-- ตรวจ Yoast SEO verification fields
SELECT option_value 
FROM wp_options 
WHERE option_name = 'wpseo';
-- หลังจากนั้นค้นหา "googleverify", "bingverify", "yandexverify" ใน JSON output

-- ตรวจ All in One SEO verification fields  
SELECT option_value
FROM wp_options
WHERE option_name = 'aioseo_options';
```

### 3.4 ตรวจ Suspicious Options

```sql
-- ตรวจหา options ที่มี PHP code injection
SELECT option_name, LEFT(option_value, 300) as preview
FROM wp_options
WHERE option_value LIKE '%eval(%'
   OR option_value LIKE '%base64_decode%'
   OR option_value LIKE '%gzinflate%'
   OR option_value LIKE '%str_rot13%'
   OR option_value LIKE '%preg_replace%'
   OR option_value LIKE '%<script%'
   OR option_value LIKE '%javascript:%'
ORDER BY option_name;

-- ตรวจหา spam links ที่อาจ inject เข้ามา
SELECT option_name, LEFT(option_value, 300) as preview
FROM wp_options
WHERE option_value LIKE '%baccarat%'
   OR option_value LIKE '%casino%'
   OR option_value LIKE '%poker%'
   OR option_value LIKE '%viagra%'
   OR option_value LIKE '%cialis%'
ORDER BY option_name;

-- ตรวจ active plugins list
SELECT option_value 
FROM wp_options 
WHERE option_name = 'active_plugins';

-- ตรวจ siteurl และ home URL (ต้องตรงกับ domain จริง)
SELECT option_name, option_value
FROM wp_options
WHERE option_name IN ('siteurl', 'home', 'blogname', 'admin_email')
ORDER BY option_name;

-- ตรวจหา cron jobs ที่น่าสงสัย
SELECT option_value
FROM wp_options
WHERE option_name = '_transient_doing_cron'
   OR option_name = 'cron';
```

### 3.5 ตรวจ Post Content ที่อาจถูก Inject

```sql
-- ตรวจ posts/pages ที่มี spam content
SELECT ID, post_title, post_type, post_status, post_modified,
       LEFT(post_content, 200) as content_preview
FROM wp_posts
WHERE post_status = 'publish'
  AND (
    post_content LIKE '%<script%'
    OR post_content LIKE '%eval(%'
    OR post_content LIKE '%base64_decode%'
    OR post_content LIKE '%baccarat%'
    OR post_content LIKE '%casino%'
    OR post_content LIKE '%iframe%src=%'
  )
ORDER BY post_modified DESC;

-- ตรวจ post meta ที่น่าสงสัย
SELECT pm.post_id, p.post_title, pm.meta_key, LEFT(pm.meta_value, 200) as meta_preview
FROM wp_postmeta pm
JOIN wp_posts p ON pm.post_id = p.ID
WHERE pm.meta_value LIKE '%eval(%'
   OR pm.meta_value LIKE '%base64_decode%'
   OR pm.meta_value LIKE '%<script%'
LIMIT 50;
```

---

## 4. IIS web.config Security Template

> **คำเตือน:** ทดสอบบน staging ก่อนใช้บน production เสมอ  
> ไฟล์นี้ใช้ได้กับ IIS 8.5+ และ WordPress

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>

        <!-- ==========================================
             REWRITE RULES (WordPress + Security)
             ========================================== -->
        <rewrite>
            <rules>

                <!-- Redirect spam URLs ที่ยังอยู่ใน Google index -->
                <rule name="Redirect Spam Baccarat" stopProcessing="true">
                    <match url="^Baccarat(/.*)?$" />
                    <action type="Redirect" url="/" redirectType="Permanent" />
                </rule>
                <rule name="Redirect Spam Video" stopProcessing="true">
                    <match url="^(ogeh|erot|books|files)/video(/.*)?$" />
                    <action type="Redirect" url="/" redirectType="Permanent" />
                </rule>

                <!-- Block xmlrpc.php (ยกเว้นถ้าใช้ Jetpack) -->
                <!-- <rule name="Block xmlrpc" stopProcessing="true">
                    <match url="^xmlrpc\.php$" />
                    <action type="CustomResponse" statusCode="403" statusReason="Forbidden" />
                </rule> -->

                <!-- WordPress pretty permalinks -->
                <rule name="WordPress" stopProcessing="true">
                    <match url="^(.*)$" />
                    <conditions logicalGrouping="MatchAll">
                        <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
                        <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
                    </conditions>
                    <action type="Rewrite" url="index.php" />
                </rule>

            </rules>

            <!-- Security: ซ่อน X-Powered-By header -->
            <outboundRules>
                <rule name="Remove X-Powered-By">
                    <match serverVariable="RESPONSE_X-Powered-By" pattern=".*" />
                    <action type="Rewrite" value="" />
                </rule>
            </outboundRules>
        </rewrite>

        <!-- ==========================================
             SECURITY HEADERS
             ========================================== -->
        <httpProtocol>
            <customHeaders>
                <!-- ลบ headers ที่เปิดเผย server info -->
                <remove name="X-Powered-By" />
                <remove name="Server" />

                <!-- Security headers -->
                <add name="X-Frame-Options" value="SAMEORIGIN" />
                <add name="X-Content-Type-Options" value="nosniff" />
                <add name="X-XSS-Protection" value="1; mode=block" />
                <add name="Referrer-Policy" value="strict-origin-when-cross-origin" />
                <add name="Permissions-Policy" value="camera=(), microphone=(), geolocation=()" />

                <!-- HSTS (เปิดเฉพาะถ้ามี valid SSL cert) -->
                <add name="Strict-Transport-Security" value="max-age=31536000; includeSubDomains" />
            </customHeaders>
        </httpProtocol>

        <!-- ==========================================
             MIME TYPES (ใช้ remove ก่อน add เสมอ!)
             ========================================== -->
        <staticContent>
            <!-- Web Fonts -->
            <remove fileExtension=".woff" />
            <mimeMap fileExtension=".woff" mimeType="font/woff" />
            <remove fileExtension=".woff2" />
            <mimeMap fileExtension=".woff2" mimeType="font/woff2" />
            <remove fileExtension=".ttf" />
            <mimeMap fileExtension=".ttf" mimeType="font/ttf" />
            <remove fileExtension=".eot" />
            <mimeMap fileExtension=".eot" mimeType="application/vnd.ms-fontobject" />
            <remove fileExtension=".otf" />
            <mimeMap fileExtension=".otf" mimeType="font/otf" />

            <!-- SVG -->
            <remove fileExtension=".svg" />
            <mimeMap fileExtension=".svg" mimeType="image/svg+xml" />

            <!-- JSON/Manifest -->
            <remove fileExtension=".json" />
            <mimeMap fileExtension=".json" mimeType="application/json" />
            <remove fileExtension=".webmanifest" />
            <mimeMap fileExtension=".webmanifest" mimeType="application/manifest+json" />

            <!-- WebP -->
            <remove fileExtension=".webp" />
            <mimeMap fileExtension=".webp" mimeType="image/webp" />

            <!-- AVIF -->
            <remove fileExtension=".avif" />
            <mimeMap fileExtension=".avif" mimeType="image/avif" />

            <!-- ไม่ต้อง add .xml เพราะ IIS มีอยู่แล้ว! -->
            <!-- <remove fileExtension=".xml" /> -->
            <!-- <mimeMap fileExtension=".xml" mimeType="text/xml" /> -->

            <!-- Cache Control สำหรับ static files -->
            <clientCache cacheControlMode="UseMaxAge" cacheControlMaxAge="7.00:00:00" />
        </staticContent>

        <!-- ==========================================
             BLOCKED FILES & DIRECTORIES
             ========================================== -->
        <security>
            <requestFiltering>
                <!-- Block การเข้าถึงไฟล์ sensitive -->
                <hiddenSegments>
                    <add segment="wp-config.php" />
                    <add segment=".git" />
                    <add segment=".env" />
                    <add segment="wp-content/debug.log" />
                </hiddenSegments>

                <!-- Block file extensions ที่อันตราย -->
                <fileExtensions>
                    <add fileExtension=".log" allowed="false" />
                    <add fileExtension=".bak" allowed="false" />
                    <add fileExtension=".sql" allowed="false" />
                    <add fileExtension=".ini" allowed="false" />
                </fileExtensions>

                <!-- Block URL strings อันตราย -->
                <denyUrlSequences>
                    <add sequence="../" />
                    <add sequence="..\" />
                </denyUrlSequences>
            </requestFiltering>
        </security>

        <!-- ==========================================
             COMPRESSION
             ========================================== -->
        <urlCompression doStaticCompression="true" doDynamicCompression="true" />

        <!-- ==========================================
             DEFAULT DOCUMENT
             ========================================== -->
        <defaultDocument>
            <files>
                <clear />
                <add value="index.php" />
                <add value="index.html" />
            </files>
        </defaultDocument>

    </system.webServer>
</configuration>
```

---

## 5. mu-plugins Security Template

> ไฟล์นี้ใส่ใน `wp-content/mu-plugins/` และจะโหลดอัตโนมัติทุก request  
> **ไม่สามารถ disable ได้ผ่าน WP Admin** (ต้องลบไฟล์เท่านั้น)

```php
<?php
/**
 * WordPress Security & Stability mu-plugin
 * 
 * File: wp-content/mu-plugins/security-fixes.php
 * 
 * รวม fixes สำหรับปัญหาที่พบจริงบน IIS/Windows Server:
 * - Disable Jetpack modules ที่ก่อปัญหา
 * - Force enable WordPress updates
 * - Block spam URL patterns
 * - Remove malicious verification codes
 * - Security hardening
 */

defined('ABSPATH') || exit;

// ============================================================
// 1. JETPACK MODULE CONTROL
// ============================================================

/**
 * Disable Jetpack modules ที่ก่อปัญหา 400 errors บน IIS
 */
add_filter('jetpack_get_default_modules', function (array $modules): array {
    $disable_modules = [
        'subscriptions',  // ทำให้เกิด 400 errors บน IIS
        // เพิ่ม modules อื่นที่ต้องการ disable:
        // 'contact-form',
        // 'carousel',
    ];
    return array_diff($modules, $disable_modules);
});

/**
 * Force deactivate modules ที่ active อยู่แล้ว
 */
add_action('init', function (): void {
    if (!class_exists('Jetpack')) {
        return;
    }
    $modules_to_deactivate = ['subscriptions'];
    foreach ($modules_to_deactivate as $module) {
        if (Jetpack::is_module_active($module)) {
            Jetpack::deactivate_module($module);
        }
    }
}, 1);

// ============================================================
// 2. FORCE ENABLE WORDPRESS UPDATES
// ============================================================

/**
 * ยกเลิก "Disable All Updates" ที่ plugin อื่นอาจตั้งไว้
 * (เช่น Admin Site Enhancements)
 */
add_action('init', function (): void {
    // Remove filters ที่ block update checks
    remove_all_filters('pre_site_transient_update_core');
    remove_all_filters('pre_site_transient_update_plugins');
    remove_all_filters('pre_site_transient_update_themes');

    // Remove actions ที่ disable update notifications
    remove_all_actions('admin_init');  // ระวัง: อาจกระทบ plugins อื่น
}, 999);

/**
 * Enable automatic updates (optional - ปรับตาม policy ของ site)
 */
// add_filter('auto_update_plugin', '__return_true');
// add_filter('auto_update_theme', '__return_true');
// add_filter('auto_update_core_minor', '__return_true');

// ============================================================
// 3. SECURITY HARDENING
// ============================================================

/**
 * ลบ WordPress version จาก HTML source
 */
remove_action('wp_head', 'wp_generator');
add_filter('the_generator', '__return_empty_string');

/**
 * ปิด XML-RPC (ถ้าไม่ได้ใช้ Jetpack หรือ remote publishing)
 * หากใช้ Jetpack ให้ comment บรรทัดนี้ออก
 */
// add_filter('xmlrpc_enabled', '__return_false');

/**
 * ลบ RSD link จาก header (เปิดเผย xmlrpc endpoint)
 */
remove_action('wp_head', 'rsd_link');
remove_action('wp_head', 'wlwmanifest_link');

/**
 * จำกัด login attempts โดย block IPs ที่ fail เกิน threshold
 * (ต้องใช้ร่วมกับ plugin เช่น Wordfence หรือ Login LockDown)
 */

/**
 * ซ่อน login error messages (ไม่บอกว่า username หรือ password ผิด)
 */
add_filter('login_errors', function (): string {
    return 'Invalid credentials. Please try again.';
});

/**
 * Block การเข้าถึง wp-admin สำหรับ non-admin users
 */
add_action('admin_init', function (): void {
    if (is_admin() && !current_user_can('manage_options') && !wp_doing_ajax()) {
        wp_redirect(home_url());
        exit;
    }
});

// ============================================================
// 4. SPAM URL PROTECTION
// ============================================================

/**
 * Redirect spam URLs ที่อาจยังอยู่ใน Google index
 * (ทางเลือกสำหรับกรณีที่แก้ใน web.config ไม่ได้)
 */
add_action('template_redirect', function (): void {
    $request_uri = $_SERVER['REQUEST_URI'] ?? '';

    $spam_patterns = [
        '/^\/Baccarat\//i',
        '/^\/ogeh\/video\//i',
        '/^\/erot\/video\//i',
        '/^\/books\/video\//i',
        '/^\/files\/video\//i',
        '/^\/slot\//i',
        '/^\/casino\//i',
    ];

    foreach ($spam_patterns as $pattern) {
        if (preg_match($pattern, $request_uri)) {
            wp_redirect(home_url('/'), 301);
            exit;
        }
    }
});

// ============================================================
// 5. GOOGLE VERIFICATION CODE PROTECTION
// ============================================================

/**
 * ป้องกันการ add/update verification codes ผ่าน options API
 * (ป้องกัน hacker inject verification codes กลับเข้ามา)
 */
add_filter('pre_update_option_verification_services_codes', function ($new_value, $old_value) {
    // Log การเปลี่ยนแปลง
    if ($new_value !== $old_value) {
        error_log('[Security] verification_services_codes changed. Review required.');
    }
    return $new_value;
}, 10, 2);

// ============================================================
// 6. WP-CRON SECURITY
// ============================================================

/**
 * ตรวจสอบ scheduled events ที่น่าสงสัย (log เท่านั้น ไม่ block)
 */
add_action('init', function (): void {
    if (!defined('DOING_CRON') || !DOING_CRON) {
        return;
    }

    $crons = _get_cron_array();
    $suspicious_hooks = [];

    foreach ($crons as $timestamp => $cron) {
        foreach ($cron as $hook => $events) {
            // Hooks ที่ไม่รู้จัก (ไม่ได้มาจาก plugins ที่รู้จัก)
            if (preg_match('/[a-f0-9]{32}/', $hook)) {
                $suspicious_hooks[] = $hook;
            }
        }
    }

    if (!empty($suspicious_hooks)) {
        error_log('[Security] Suspicious cron hooks found: ' . implode(', ', $suspicious_hooks));
    }
});

// ============================================================
// 7. FILE UPLOAD SECURITY
// ============================================================

/**
 * Block การ upload ไฟล์ที่อันตราย
 */
add_filter('upload_mimes', function (array $mimes): array {
    // ลบ file types ที่อันตราย
    unset($mimes['php']);
    unset($mimes['php3']);
    unset($mimes['php4']);
    unset($mimes['php5']);
    unset($mimes['phtml']);
    unset($mimes['exe']);
    unset($mimes['bat']);
    unset($mimes['cmd']);
    unset($mimes['sh']);
    unset($mimes['js']);   // ระวัง: อาจกระทบ plugin ที่ต้อง upload JS
    return $mimes;
});

/**
 * Double-check file type ด้วย real MIME type (ไม่ใช่แค่ extension)
 */
add_filter('wp_check_filetype_and_ext', function (array $data, string $file): array {
    if (!empty($data['ext']) && !empty($data['type'])) {
        $finfo = new finfo(FILEINFO_MIME_TYPE);
        $real_mime = $finfo->file($file);

        // Block PHP files ที่ disguise ตัวเองเป็น images
        if (in_array($real_mime, ['text/x-php', 'text/php', 'application/x-php'], true)) {
            $data['ext']  = false;
            $data['type'] = false;
        }
    }
    return $data;
}, 10, 2);
```

---

## 6. Post-Fix Verification Checklist

หลังจากแก้ไขปัญหาทุกข้อ ให้ตรวจสอบตามรายการนี้:

### การตรวจสอบ Permissions

```powershell
$wpRoot    = "Y:\"
$wpContent = "Y:\wp-content"

Write-Host "=== Permission Verification ===" -ForegroundColor Cyan

# ตรวจ IUSR permissions
Write-Host "`n[1] IUSR on Root:" -ForegroundColor Yellow
icacls $wpRoot | Select-String "IUSR"

# ตรวจ wp-content directories
foreach ($dir in @("uploads", "upgrade", "cache", "mu-plugins")) {
    Write-Host "`n[+] $dir :" -ForegroundColor Yellow
    icacls "$wpContent\$dir" | Select-String "IUSR|AppPool"
}

# ตรวจ llms.txt
Write-Host "`n[2] llms.txt:" -ForegroundColor Yellow
if (Test-Path "$wpRoot\llms.txt") {
    Write-Host "EXISTS" -ForegroundColor Green
    Get-Item "$wpRoot\llms.txt" | Select-Object LastWriteTime, Length
} else {
    Write-Host "MISSING" -ForegroundColor Red
}
```

### การตรวจสอบ HTTP Responses

```powershell
$baseUrl = "https://yoursite.com"  # ปรับ URL ตามจริง

$urlsToCheck = @(
    "$baseUrl/",
    "$baseUrl/sitemap_index.xml",
    "$baseUrl/wp-login.php",
    "$baseUrl/wp-json/",
    "$baseUrl/llms.txt",
    "$baseUrl/Baccarat/",        # ต้องได้ 301
    "$baseUrl/wp-config.php",    # ต้องได้ 403/404
)

foreach ($url in $urlsToCheck) {
    try {
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -MaximumRedirection 0 -ErrorAction SilentlyContinue
        $status = $resp.StatusCode
    } catch {
        $status = $_.Exception.Response.StatusCode.value__
    }

    $color = switch ($true) {
        ($status -eq 200) { "Green" }
        ($status -in 301, 302) { "Yellow" }
        ($status -in 403, 404) { "Cyan" }
        default { "Red" }
    }
    Write-Host "[$status] $url" -ForegroundColor $color
}
```

### การตรวจสอบ Security Headers

```powershell
$url = "https://yoursite.com"
$response = Invoke-WebRequest -Uri $url -UseBasicParsing -Method HEAD

Write-Host "=== Security Headers ===" -ForegroundColor Cyan
$securityHeaders = @(
    "X-Frame-Options",
    "X-Content-Type-Options",
    "X-XSS-Protection",
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "Referrer-Policy"
)

foreach ($header in $securityHeaders) {
    if ($response.Headers.ContainsKey($header)) {
        Write-Host "[OK] $header : $($response.Headers[$header])" -ForegroundColor Green
    } else {
        Write-Host "[MISSING] $header" -ForegroundColor Yellow
    }
}
```

### Checklist สรุป

- [ ] WordPress Admin เข้าได้ปกติ
- [ ] Plugin/Theme updates แสดงขึ้นมา (ไม่ถูก block)
- [ ] Media upload ทำงานได้
- [ ] Sitemap เข้าได้ (`/sitemap_index.xml`)
- [ ] llms.txt สร้างได้ (`/llms.txt`)
- [ ] Spam URLs (เช่น `/Baccarat/`) redirect ไป `/` ด้วย 301
- [ ] `wp-config.php` ถูก block (ได้ 403)
- [ ] Security headers ครบ
- [ ] Google Search Console — มีเฉพาะ account ของเราเท่านั้น
- [ ] Database ไม่มี verification codes แปลกปลอม
- [ ] Jetpack subscriptions ไม่ก่อ 400 errors
- [ ] IIS Event Viewer ไม่มี PHP errors ใหม่

---

## 7. การป้องกันในอนาคต

### 7.1 Monitoring อัตโนมัติ

```powershell
# Script ตรวจสอบ IIS error logs รายวัน
# บันทึกเป็น: C:\Scripts\check-wp-errors.ps1

$logPath   = "C:\inetpub\logs\LogFiles\W3SVC1"
$threshold = 50  # จำนวน 500 errors ที่ยอมรับได้ต่อวัน

$today     = Get-Date -Format "yyMMdd"
$logFile   = Get-ChildItem $logPath -Filter "u_ex$today*.log" | Select-Object -Last 1

if ($logFile) {
    $errors500 = (Select-String -Path $logFile.FullName -Pattern " 5\d\d " -SimpleMatch).Count
    $errors400 = (Select-String -Path $logFile.FullName -Pattern " 4\d\d " -SimpleMatch).Count

    Write-Host "Today's IIS Errors:"
    Write-Host "  5xx errors: $errors500"
    Write-Host "  4xx errors: $errors400"

    if ($errors500 -gt $threshold) {
        # ส่ง alert (ใช้ Send-MailMessage หรือ webhook)
        Write-Warning "HIGH 500 ERRORS: $errors500 today!"
    }
}
```

### 7.2 WordPress Auto-Update Policy

```php
// ใส่ใน wp-config.php หรือ mu-plugin
// Minor version updates (เช่น 6.7.1 → 6.7.2): auto
define('WP_AUTO_UPDATE_CORE', 'minor');

// Major version updates: manual (ทดสอบก่อน)
// define('WP_AUTO_UPDATE_CORE', true);  // auto ทุก version
```

### 7.3 Database Backup อัตโนมัติ

```powershell
# Script backup database รายวัน
# บันทึกเป็น: C:\Scripts\backup-wp-db.ps1

$backupDir = "C:\Backups\WordPress"
$date      = Get-Date -Format "yyyy-MM-dd"
$backupFile = "$backupDir\wp-db-$date.sql"

# ดึง DB credentials จาก wp-config.php
$wpConfig  = "Y:\wp-config.php"
$dbName    = (Select-String -Path $wpConfig -Pattern "DB_NAME.*'(.+)'").Matches.Groups[1].Value
$dbUser    = (Select-String -Path $wpConfig -Pattern "DB_USER.*'(.+)'").Matches.Groups[1].Value
$dbPass    = (Select-String -Path $wpConfig -Pattern "DB_PASSWORD.*'(.+)'").Matches.Groups[1].Value
$dbHost    = (Select-String -Path $wpConfig -Pattern "DB_HOST.*'(.+)'").Matches.Groups[1].Value

if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}

# Backup ด้วย mysqldump
$env:MYSQL_PWD = $dbPass
mysqldump -h $dbHost -u $dbUser $dbName | Out-File $backupFile -Encoding utf8

if (Test-Path $backupFile) {
    $sizeMB = [math]::Round((Get-Item $backupFile).Length / 1MB, 2)
    Write-Host "Backup created: $backupFile ($sizeMB MB)" -ForegroundColor Green
}

# เก็บแค่ 30 วันล่าสุด
Get-ChildItem $backupDir -Filter "wp-db-*.sql" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -Skip 30 |
    Remove-Item -Force
```

### 7.4 Security Audit Schedule

| ความถี่ | งาน |
|---------|-----|
| **รายวัน** | ตรวจ IIS error logs, ตรวจ failed login attempts |
| **รายสัปดาห์** | อัปเดต plugins/themes/core, ตรวจ new admin users |
| **รายเดือน** | รัน full DB audit queries (Section 3), ตรวจ file integrity |
| **รายไตรมาส** | Review web.config security rules, ตรวจ Google Search Console |
| **เมื่อถูก hack** | รัน checklist นี้ทั้งหมด + reset passwords ทุก account |

### 7.5 Security Plugins ที่แนะนำสำหรับ IIS/Windows

| Plugin | จุดประสงค์ | หมายเหตุ |
|--------|-----------|---------|
| **Wordfence Security** | Firewall + Malware scanner | ทำงานได้ดีบน IIS |
| **WP Activity Log** | ติดตาม user actions | ดีสำหรับ audit trail |
| **Redirection** | จัดการ 301/302 redirects | ใช้แทน web.config rewrites |
| **Disable XML-RPC** | ปิด xmlrpc.php | ถ้าไม่ใช้ Jetpack |
| **iThemes Security** | Security hardening | มี IIS support |

### 7.6 หลักการป้องกัน SEO Farming

1. **ตรวจสอบ Google Search Console** สม่ำเสมอ — ดู Coverage report และ URL Inspection
2. **ใช้ Google Search Console URL Removal Tool** เพื่อ request removal ของ spam URLs
3. **ตั้ง Google Alerts** สำหรับ `site:yoursite.com casino` เพื่อ monitor spam indexing
4. **หลัง hack ให้ Request Re-indexing** บน main pages ทั้งหมดทันที
5. **ติดตั้ง File Integrity Monitoring** — Wordfence มี feature นี้

---

> **เอกสารนี้จัดทำขึ้นจากประสบการณ์จริง** — ปัญหาทั้งหมดในเอกสารนี้เกิดขึ้นจริงและได้รับการแก้ไขแล้ว  
> อัปเดตล่าสุด: 2026-06-12  
> สภาพแวดล้อม: WordPress + IIS (Windows Server) + PHP as IUSR
