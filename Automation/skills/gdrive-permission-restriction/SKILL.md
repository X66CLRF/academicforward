---
name: gdrive-permission-restriction
description: >-
  Automate batch setting Google Drive file permissions to restrict download, copy, and print (copyRequiresWriterPermission=True)
  for all files within a specified Google Drive folder or directory on Windows (G:\My Drive\...).
---

# Google Drive Download Permission Restriction Skill

This skill provides an automated workflow to restrict downloading, copying, and printing of files inside a Google Drive folder tree using the Google Drive API v3.

## Overview

When files are hosted on Google Drive (mounted on Windows via Google Drive for Desktop at `G:\My Drive\...`), changing permissions individually for thousands of files via the UI can be slow. This skill extracts the authenticated OAuth refresh token from Windows Credential Manager (`DriveFS_*`), obtains a fresh Google Drive API access token, and batch-updates files concurrently via Python (`ThreadPoolExecutor`).

## When to Use

Use this skill when:
- The user requests to disable download, copy, or print permissions for files in a Google Drive folder (`G:\My Drive\...`).
- The user wants to change Google Drive file sharing permissions in bulk for hundreds or thousands of files.

## Workflow & Step-by-Step Guide

### 1. Execute the Automation Script

Run the provided helper script with the target Google Drive folder path or name:

```powershell
python "scripts/restrict_gdrive_download.py" "G:\My Drive\<Folder_Path>"
```

### 2. Script Actions Overview

The script performs the following steps automatically:
1. Reads the `DriveFS` credential from Windows Credential Manager (`DriveFS_*`).
2. Obtains a fresh access token from `https://oauth2.googleapis.com/token` using client ID `947318989803-6bn6qk8qdgf4n4g3pfee6491hc0brc4i.apps.googleusercontent.com`.
3. Locates the folder ID from the Google Drive Desktop SQLite DB (`metadata_sqlite_db`).
4. Recursively lists all non-trashed files within the target folder and its subdirectories via Google Drive API v3.
5. Executes parallel `PATCH` HTTP requests setting:
   ```json
   {
     "copyRequiresWriterPermission": true,
     "writersCanShare": true
   }
   ```

### 3. Verification

Verify the updated permissions by running a quick count query against Google Drive API:
- `copyRequiresWriterPermission: true` confirms viewers and commenters cannot download, copy, or print.
