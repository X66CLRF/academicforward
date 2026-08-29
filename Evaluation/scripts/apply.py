# -*- coding: utf-8 -*-
"""Write the reviewed citations from a sheet back into the document.

    python apply.py "<path to .docx>" sheet.tsv [--dry-run] [--overwrite]

Only CELL rows with a non-empty `cite` column are touched.

Cells the user already filled in by hand (state DONE) are skipped and
reported, never rewritten - passing --overwrite is the only way past that,
and it still refuses a cell whose existing citation was written in the house
style, because replacing that safely means editing runs in the middle of the
cell rather than appending to the end.

A timestamped backup is written first, always.
"""
import io
import sys

import lib_docx as L


def read_sheet(path):
    rows = {}
    with io.open(path, encoding="utf-8") as fh:
        header = fh.readline()
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 5 or parts[0] != "CELL":
                continue
            cite = parts[3].strip()
            if not cite:
                continue
            nums = [int(x) for x in cite.replace(" ", "").split(",") if x]
            rows[parts[1]] = (nums, parts[4].strip())
    return rows


def main(path, sheet, dry, overwrite):
    doc = L.load(path)
    want = read_sheet(sheet)
    known = {n for _, _, n in L.captions(doc)}

    bad = sorted({n for nums, _ in want.values() for n in nums} - known)
    if bad:
        print("refusing: sheet cites attachments that do not exist: %s" % bad)
        return 1

    hits = 0
    skipped = []
    noprefix = []
    for ti, ri, cell in L.criteria_cells(doc):
        key = "t%d.r%d" % (ti, ri)
        if key not in want:
            continue
        nums, prefix = want[key]
        nums = sorted(set(nums))
        before = L.read_citation(cell)

        if before:
            if not overwrite or L.read_prefix(cell):
                skipped.append((key, before, nums))
                continue
        if before == nums:
            continue
        if not prefix:
            noprefix.append(key)
            continue

        print("%s  %s -> %s" % (key, before or "empty", nums))
        if not dry:
            L.write_citation(cell, nums, prefix)
        hits += 1

    for key, before, nums in skipped:
        print("skip (already written by hand): %s has %s, sheet says %s" % (key, before, nums))
    for key in noprefix:
        print("skip (no prefix in sheet, fill the prefix column): %s" % key)

    if dry:
        print("dry run: %d cell(s) would change" % hits)
        return 0
    if not hits:
        print("nothing to change")
        return 0

    dest = L.backup(path)
    print("backup: %s" % dest)
    doc.save(path)
    print("wrote %d cell(s)" % hits)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2],
                  "--dry-run" in sys.argv, "--overwrite" in sys.argv))
