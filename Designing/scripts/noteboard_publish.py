"""Publish a lesson to NoteBoard: create a column board, post notes, pin, attach files.

Auth: server-to-server key read from ~/.noteboard-skill-key (never printed).
Usage:
    python noteboard_publish.py lesson.json [--api http://localhost:8090]

lesson.json:
{
  "title": "...", "desc": "...", "location": "...",
  "joinMode": "email" | "profile",
  "columns": [{"id": "c1", "title": "เนื้อหา"}, ...],
  "notes": [{"column": "c1", "text": "...", "link": "https://...", "file": "path.pdf",
             "color": "blue", "pin": true}, ...]
}
Prints board id + join code. Files are uploaded to the API's /api/upload,
so --api must be the server that serves them (production), not a dev box.
"""
import json, sys, time, random, mimetypes, urllib.request, urllib.parse, uuid
from pathlib import Path

KEY = (Path.home() / ".noteboard-skill-key").read_text().strip()


def rpc(api, payload):
    req = urllib.request.Request(f"{api}/api/rpc", data=json.dumps({**payload, "token": KEY}).encode(),
                                 headers={"Content-Type": "application/json"})
    res = json.load(urllib.request.urlopen(req, timeout=30))
    if res.get("status") != "success":
        raise SystemExit(f"{payload['action']} failed: {res.get('message')}")
    return res


def upload(api, path):
    p = Path(path)
    boundary = uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{p.name}\"\r\n"
            f"Content-Type: {mimetypes.guess_type(p.name)[0] or 'application/octet-stream'}\r\n\r\n").encode() \
        + p.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(f"{api}/api/upload", data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}", "Authorization": f"Bearer {KEY}"})
    res = json.load(urllib.request.urlopen(req, timeout=120))
    if res.get("status") != "success":
        raise SystemExit(f"upload {p.name} failed: {res.get('message')}")
    return f"{api}{res['url']}#{urllib.parse.quote(p.name)}"


def main():
    lesson = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    api = sys.argv[sys.argv.index("--api") + 1] if "--api" in sys.argv else "https://noteboard.nsru.ac.th"

    board = rpc(api, {
        "action": "createBoard", "title": lesson["title"], "desc": lesson.get("desc", ""),
        "location": lesson.get("location", ""), "mode": "columns", "columns": lesson["columns"],
        "joinMode": lesson.get("joinMode", "email"),
        "authorId": lesson.get("ownerId", ""), "authorName": lesson.get("author", ""),
    })["board"]
    print(f"board {board['id']} code {board['code']}")

    for i, n in enumerate(lesson["notes"]):
        sid = f"{int(time.time() * 1000)}{i:02d}{random.randint(100, 999)}"
        file_url = upload(api, n["file"]) if n.get("file") else ""
        rpc(api, {
            "action": "submitWork", "id": sid, "boardId": board["id"], "name": lesson.get("author", "วิทยากร"),
            "text": n.get("text", ""), "link": n.get("link", ""), "color": n.get("color", "blue"),
            "fileUrl": file_url, "fileType": "file" if file_url else "text",
            "rotation": "rotate-0", "columnId": n.get("column", ""), "authorId": lesson.get("ownerId", ""),
        })
        if n.get("pin"):
            rpc(api, {"action": "pinWork", "id": sid, "pinned": True})
        print(f"  note {i + 1}: {n.get('text', '')[:40]!r}{' [pinned]' if n.get('pin') else ''}")


if __name__ == "__main__":
    main()
