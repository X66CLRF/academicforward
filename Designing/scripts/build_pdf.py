"""Build a deck/worksheet HTML into PDF with the shared assets embedded.

Usage:
    python build_pdf.py <deck.html> <out.pdf> [--room "รหัสห้อง NoteBoard: ABC123"] [--sheet]

The HTML keeps placeholders so the source stays small and editable:
    __LOGO__  -> slides/assets/aritc-logo.png (base64)
    __PHOTO__ -> slides/assets/speaker.jpg    (base64)
    __ROOM__  -> --room text (empty when omitted, e.g. offline venues)
Also prints a contact-sheet PNG next to the PDF (<out>.sheet.png) for review,
and the fonts found in the PDF so a Prompt/fallback leak is caught.
"""
import base64, subprocess, sys, tempfile
from pathlib import Path

ASSETS = Path(r"C:\Users\Burt\Documents\slides\assets")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    room = sys.argv[sys.argv.index("--room") + 1] if "--room" in sys.argv else ""
    html = (src.read_text(encoding="utf-8")
            .replace("__LOGO__", b64(ASSETS / "aritc-logo.png", "image/png"))
            .replace("__PHOTO__", b64(ASSETS / "speaker.jpg", "image/jpeg"))
            .replace("__ROOM__", room))
    tmp = Path(tempfile.gettempdir()) / f"build_{src.stem}.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=15000", rf"--user-data-dir={tempfile.gettempdir()}\edgepdf",
                    f"--print-to-pdf={out}", tmp.as_uri()], check=True)

    import pymupdf
    from PIL import Image
    doc = pymupdf.open(out)
    fonts = sorted({f[3].split("+")[-1] for p in doc for f in p.get_fonts() if f[3]})
    print(f"{out.name}: {doc.page_count} pages · fonts: {', '.join(fonts)}")
    if any("Prompt" in f for f in fonts):
        print("!! Prompt font found — must be Sarabun only")
    dpi = 30 if "--sheet" not in sys.argv else 40
    ims = []
    for p in doc:
        px = p.get_pixmap(dpi=dpi)
        ims.append(Image.frombytes("RGB", [px.width, px.height], px.samples))
    cols = 4 if "--sheet" not in sys.argv else 2
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(out.with_suffix(".sheet.png"))


if __name__ == "__main__":
    main()
