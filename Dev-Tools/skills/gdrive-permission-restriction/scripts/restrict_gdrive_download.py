import ctypes
from ctypes import wintypes
import os
import sys
import re
import glob
import json
import sqlite3
import urllib.request
import urllib.parse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

CLIENT_ID = "947318989803-6bn6qk8qdgf4n4g3pfee6491hc0brc4i.apps.googleusercontent.com"
CLIENT_SECRET = "gtDkCw7oR54acTIqay0eliAO"

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("TargetName", wintypes.LPWSTR),
        ("Comment", wintypes.LPWSTR),
        ("LastWritten", wintypes.FILETIME),
        ("CredentialBlobSize", wintypes.DWORD),
        ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)),
        ("Persist", wintypes.DWORD),
        ("AttributeCount", wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wintypes.LPWSTR),
        ("UserName", wintypes.LPWSTR),
    ]

def get_refresh_token_from_cred_manager():
    Advapi32 = ctypes.windll.Advapi32
    CredRead = Advapi32.CredReadW
    CredRead.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(CREDENTIAL))]
    CredRead.restype = wintypes.BOOL
    CredFree = Advapi32.CredFree

    for target in ["DriveFS_101873106784454803900", "DriveFS_111767459909400682616", "DriveFS_110254100452498592214"]:
        p_cred = ctypes.POINTER(CREDENTIAL)()
        if CredRead(target, 1, 0, ctypes.byref(p_cred)):
            cred = p_cred.contents
            blob = bytes([cred.CredentialBlob[i] for i in range(cred.CredentialBlobSize)])
            CredFree(p_cred)
            
            rf_matches = re.findall(rb'1//[a-zA-Z0-9_\-\*]+', blob)
            if rf_matches:
                clean_rf = rf_matches[0].decode('ascii').rstrip('*')
                return clean_rf
    return None

def get_access_token(refresh_token):
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }).encode('utf-8')

    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        return res.get("access_token")

def find_folder_id(folder_name_or_path):
    dbs = glob.glob(r'C:\Users\Burt\AppData\Local\Google\DriveFS\*\metadata_sqlite_db')
    target_basename = os.path.basename(os.path.normpath(folder_name_or_path))
    for db_path in dbs:
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            cursor = conn.cursor()
            res = cursor.execute("SELECT id FROM items WHERE local_title = ? AND is_folder = 1 AND trashed = 0 LIMIT 1", (target_basename,)).fetchone()
            if res:
                return res[0]
        except Exception:
            pass
    return None

def list_all_files(access_token, folder_id):
    files = []
    folders = []
    page_token = None
    
    while True:
        q = f"'{folder_id}' in parents and trashed = false"
        params = {
            "q": q,
            "fields": "nextPageToken, files(id, name, mimeType, copyRequiresWriterPermission, writersCanShare)",
            "pageSize": 1000
        }
        if page_token:
            params["pageToken"] = page_token
            
        url = "https://www.googleapis.com/drive/v3/files?" + urllib.parse.urlencode(params)
        req_list = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
        
        with urllib.request.urlopen(req_list) as r:
            res_data = json.loads(r.read().decode('utf-8'))
            items = res_data.get("files", [])
            for item in items:
                if item["mimeType"] == "application/vnd.google-apps.folder":
                    folders.append(item)
                else:
                    files.append(item)
            page_token = res_data.get("nextPageToken")
            if not page_token:
                break
                
    for sub in folders:
        sub_files, sub_folders = list_all_files(access_token, sub["id"])
        files.extend(sub_files)
        
    return files, folders

def update_permission(access_token, file_info):
    file_id = file_info["id"]
    file_name = file_info["name"]
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=id,copyRequiresWriterPermission,writersCanShare"
    payload = json.dumps({
        "copyRequiresWriterPermission": True,
        "writersCanShare": True
    }).encode('utf-8')
    
    req_patch = urllib.request.Request(url, data=payload, method="PATCH", headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    })
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req_patch) as r_patch:
                patch_res = json.loads(r_patch.read().decode('utf-8'))
                if patch_res.get("copyRequiresWriterPermission") is True:
                    return True, file_name, None
        except Exception as e:
            if attempt == 2:
                return False, file_name, str(e)
            time.sleep(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python restrict_gdrive_download.py <FOLDER_PATH_OR_NAME>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    print(f"Target path: {target_path}")
    
    rf = get_refresh_token_from_cred_manager()
    if not rf:
        print("Error: Could not retrieve Google Drive refresh token from Credential Manager.")
        sys.exit(1)
        
    access_token = get_access_token(rf)
    print("Access token successfully acquired.")
    
    folder_id = find_folder_id(target_path)
    if not folder_id:
        print(f"Error: Could not locate folder ID for '{target_path}'.")
        sys.exit(1)
        
    print(f"Found folder ID: {folder_id}")
    print("Scanning all files in directory tree...")
    all_files, all_folders = list_all_files(access_token, folder_id)
    print(f"Total files found: {len(all_files)}")
    
    files_to_update = [f for f in all_files if not f.get("copyRequiresWriterPermission")]
    print(f"Files to update: {len(files_to_update)}")
    
    if not files_to_update:
        print("All files are already restricted!")
        return
        
    success_count = 0
    fail_count = 0
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(update_permission, access_token, f): f for f in files_to_update}
        completed = 0
        for future in as_completed(futures):
            completed += 1
            success, name, err = future.result()
            if success:
                success_count += 1
            else:
                fail_count += 1
                print(f"Failed [{name}]: {err}")
                
            if completed % 100 == 0 or completed == len(files_to_update):
                print(f"Progress: {completed}/{len(files_to_update)} ({success_count} success, {fail_count} failed)")
                
    print(f"\nCOMPLETED: {success_count} updated, {fail_count} failed.")

if __name__ == '__main__':
    main()
