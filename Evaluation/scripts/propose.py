# -*- coding: utf-8 -*-
"""Dump the review sheet: one row per criteria cell, one row per attachment.

    python propose.py "<path to .docx>" > sheet.tsv

The sheet is TSV so it opens in Excel and diffs in git. Claude fills the
`cite` column, the user corrects it, then apply.py writes it back.

Columns:
    kind    CELL or ATTACH
    id      t<table>.r<row>  for cells, the number for attachments
    state   DONE  = the user already wrote a citation here, leave it alone
            EMPTY = nothing cited yet, this is what the skill fills in
    cite    numbers, comma separated - blank means "not decided yet"
    prefix  the house-style prefix to write, e.g.
            "เอกสารแนบการใช้คอมพิวเตอร์ ระดับที่ ๓"
    text    the existing text, tabs and newlines flattened
"""
import sys

import lib_docx as L


def flat(s, limit=600):
    s = " ".join(s.split())
    return s[:limit]


def guess_prefix(doc, ti, ri, cell, learned):
    """Reuse the prefix this cell already has, else borrow from a sibling row.

    Sibling = a row in the same table under the same competency heading
    (column 1). Only the level number is swapped in.
    """
    own = L.read_prefix(cell)
    if own:
        return own
    row = doc.tables[ti].rows[ri]
    key = (ti, flat(row.cells[0].text, 80))
    base = learned.get(key)
    if not base:
        return ""
    level = L.read_level(row)
    if not level:
        return ""
    return L.LEVEL_RE.sub("ระดับที่ " + level, base, count=1)


def main(path):
    doc = L.load(path)
    cells = L.criteria_cells(doc)

    # First pass: learn one prefix per (table, competency heading).
    learned = {}
    for ti, ri, cell in cells:
        pre = L.read_prefix(cell)
        if not pre:
            continue
        head = flat(doc.tables[ti].rows[ri].cells[0].text, 80)
        learned.setdefault((ti, head), pre)

    out = sys.stdout
    out.write("kind\tid\tstate\tcite\tprefix\ttext\n")

    for _, p, n in L.captions(doc):
        out.write("ATTACH\t%d\t\t\t\t%s\n" % (n, flat(p.text)))

    for ti, ri, cell in cells:
        got = L.read_citation(cell) or []
        row = doc.tables[ti].rows[ri]
        crit = flat(row.cells[0].text, 60) + " / " + flat(row.cells[1].text, 80)
        # A row whose column 2 carries no "ระดับที่" is a header row, not a
        # criteria row - nothing is ever cited there.
        if L.read_level(row):
            state = "DONE" if got else "EMPTY"
        else:
            state = "HEAD"
        out.write("CELL\tt%d.r%d\t%s\t%s\t%s\t%s || %s\n" % (
            ti, ri,
            state,
            ",".join(str(x) for x in got),
            guess_prefix(doc, ti, ri, cell, learned),
            crit,
            flat(cell.text),
        ))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
