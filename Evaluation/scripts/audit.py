# -*- coding: utf-8 -*-
"""Read-only report on the state of the evaluation document.

    python audit.py "<path to .docx>"

Writes nothing. Answers four questions:
  1. are the caption numbers a clean 1..N run?
  2. which attachments are never cited by any criteria cell?
  3. do any cells cite a number that does not exist?
  4. which captions cannot be rewritten safely (mixed run formatting)?
"""
import sys

import lib_docx as L


def main(path):
    doc = L.load(path)
    caps = L.captions(doc)
    cells = L.criteria_cells(doc)

    nums = [n for _, _, n in caps]
    print("captions: %d" % len(caps))
    print("numbers: %s -> %s" % (nums[0] if nums else "-", nums[-1] if nums else "-"))

    dupes = sorted({n for n in nums if nums.count(n) > 1})
    expected = list(range(1, len(nums) + 1))
    print("sequential 1..N: %s" % (nums == expected))
    if dupes:
        print("duplicate numbers: %s" % dupes)
    missing = sorted(set(expected) - set(nums))
    if missing:
        print("gaps: %s" % missing)

    unsafe = [n for _, p, n in caps if not L.is_uniform(p)]
    print("captions with mixed run formatting (edit by hand): %s" % (unsafe or "none"))

    cited = {}
    phantom = []
    for ti, ri, cell in cells:
        got = L.read_citation(cell)
        if not got:
            continue
        for n in got:
            cited.setdefault(n, []).append("t%d.r%d" % (ti, ri))
            if n not in nums:
                phantom.append((n, ti, ri))

    print("")
    print("criteria cells with text: %d" % len(cells))
    print("cells carrying a citation: %d" % len({c for v in cited.values() for c in v}))

    unused = [n for n in nums if n not in cited]
    print("attachments never cited: %d" % len(unused))
    if unused:
        print("  %s" % ", ".join(str(n) for n in unused))
    if phantom:
        print("citations pointing at nothing:")
        for n, ti, ri in phantom:
            print("  table %d row %d cites %d" % (ti, ri, n))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
