# -*- coding: utf-8 -*-
"""Renumber attachment captions 1..N in document order, and follow the
citations in the criteria tables so they keep pointing at the same evidence.

    python renumber.py "<path to .docx>" [--dry-run]

Run this after inserting or deleting an attachment. The caption's number is
the only thing rewritten; its wording and formatting are untouched.

A caption whose runs carry mixed formatting is reported and skipped rather
than rewritten, because rewriting it would flatten that formatting.
"""
import sys

import lib_docx as L


def main(path, dry):
    doc = L.load(path)
    caps = L.captions(doc)
    if not caps:
        print("no captions found")
        return 1

    remap = {}
    moves = []
    skipped = []
    for new, (_, par, old) in enumerate(caps, start=1):
        if old == new:
            remap[old] = new
            continue
        if not L.is_uniform(par):
            skipped.append((old, new))
            continue
        remap[old] = new
        moves.append((old, new, par))

    for old, new in skipped:
        print("skip (mixed formatting, fix by hand): %d -> %d" % (old, new))

    for old, new, par in moves:
        text = par.text.strip()
        new_text = L.CAPTION_RE.sub(L.ATTACH + " " + str(new), text, count=1)
        print("caption %d -> %d" % (old, new))
        if not dry:
            L.set_paragraph_text(par, new_text)

    cell_hits = 0
    for ti, ri, cell in L.criteria_cells(doc):
        got = L.read_citation(cell)
        if not got:
            continue
        moved = sorted({remap.get(n, n) for n in got})
        if moved == sorted(got):
            continue
        print("t%d.r%d cites %s -> %s" % (ti, ri, got, moved))
        if not dry:
            L.write_citation(cell, moved)
        cell_hits += 1

    if dry:
        print("dry run: %d caption(s), %d cell(s) would change" % (len(moves), cell_hits))
        return 0
    if not moves and not cell_hits:
        print("already sequential, nothing to do")
        return 0

    dest = L.backup(path)
    print("backup: %s" % dest)
    doc.save(path)
    print("wrote %d caption(s), %d cell(s)" % (len(moves), cell_hits))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], "--dry-run" in sys.argv))
