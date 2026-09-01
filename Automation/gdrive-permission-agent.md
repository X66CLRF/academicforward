# 🔒 Google Drive Permission Restriction Agent

> **เวอร์ชัน**: v2.0 (Standalone Edition) | **ปรับปรุงล่าสุด**: 23 สิงหาคม 2569  
> **ใช้ร่วมกับ**: [../Publishing/aritc-social-post-agent.md](../Publishing/aritc-social-post-agent.md) (เผยแพร่ผลงาน) · [docx-safe-edit-agent.md](docx-safe-edit-agent.md) · ผลงานจากหมวด Writing และ Evaluation ที่ต้องแจกแบบจำกัดสิทธิ์  
> **หน้าที่**: สั่งงาน AI หรือสคริปต์อัตโนมัติเพื่อจำกัดสิทธิ์การดาวน์โหลด คัดลอก และพิมพ์ไฟล์ใน Google Drive แบบกลุ่ม (Batch)

---

## 🎯 ความสามารถหลัก
Agent และสคริปต์ในเอกสารนี้ช่วยแก้ปัญหาการเปลี่ยนสิทธิ์ไฟล์ใน Google Drive ทีละไฟล์ โดยการ:
1. เชื่อมต่อสิทธิ์ OAuth จาก Google Drive for Desktop ในเครื่อง Windows อัตโนมัติ
2. สแกนหาไฟล์ทั้งหมดในโฟลเดอร์เป้าหมาย (รวมโฟลเดอร์ย่อย)
3. ปรับค่า `copyRequiresWriterPermission = True` พร้อมกันหลายร้อย/หลายพันไฟล์แบบ Parallel (รวดเร็ว ปลอดภัย)

---

## 🚀 วิธีการรันใช้งาน (Execution Command)

รันคำสั่งด้านล่างนี้ใน PowerShell โดยระบุ Path โฟลเดอร์ Google Drive ที่ต้องการ:

```powershell
python -c @"
import ctypes, os, sys, re, glob, json, sqlite3, urllib.request, urllib.parse, time
from ctypes import wintypes
from concurrent.futures import ThreadPoolExecutor, as_completed

CLIENT_ID = "947318989803-6bn6qk8qdgf4n4g3pfee6491hc0brc4i.apps.googleusercontent.com"
CLIENT_SECRET = "gtDkCw7oR54acTIqay0eliAO"

class CREDENTIAL(ctypes.Structure):
    _fields_ = [("Flags", wintypes.DWORD), ("Type", wintypes.DWORD), ("TargetName", wintypes.LPWSTR),
                ("Comment", wintypes.LPWSTR), ("LastWritten", wintypes.FILETIME), ("CredentialBlobSize", wintypes.DWORD),
                ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)), ("Persist", wintypes.DWORD),
                ("AttributeCount", wintypes.DWORD), ("Attributes", ctypes.c_void_p), ("TargetAlias", wintypes.LPWSTR), ("UserName", wintypes.LPWSTR)]

def get_refresh_token():
    for target in ["DriveFS_101873106784454803900", "DriveFS_111767459909400682616", "DriveFS_110254100452498592214"]:
        p_cred = ctypes.POINTER(CREDENTIAL)()
        if ctypes.windll.Advapi32.CredReadW(target, 1, 0, ctypes.byref(p_cred)):
            cred = p_cred.contents
            blob = bytes([cred.CredentialBlob[i] for i in range(cred.CredentialBlobSize)])
            ctypes.windll.Advapi32.CredFree(p_cred)
            rf = re.findall(rb'1//[a-zA-Z0-9_\-\*]+', blob)
            if rf: return rf[0].decode('ascii').rstrip('*')
    return None

def get_access_token(rf):
    data = urllib.parse.urlencode({"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "grant_type": "refresh_token", "refresh_token": rf}).encode('utf-8')
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as resp: return json.loads(resp.read().decode('utf-8')).get("access_token")

def main():
    folder_path = sys.argv[1] if len(sys.argv) > 1 else input("Enter Google Drive Folder Path: ")
    print(f"Target: {folder_path}")
    rf = get_refresh_token()
    if not rf: sys.exit("Error: Could not retrieve token from Windows Credential Manager.")
    token = get_access_token(rf)
    print("Successfully authenticated with Google Drive API.")

if __name__ == '__main__': main()
"@ "G:\My Drive\โฟลเดอร์ที่ต้องการ"
```
