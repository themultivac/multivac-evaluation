#!/usr/bin/env python3
"""
Head-to-head (H2H) batch results: per-batch win/loss/tie counts and totals.

The paper reports five H2H batches (180 questions total) with a single external judge, the
largest being Qwen 3.6 Plus vs DeepSeek V3.2 (150 questions), which it states Qwen won 107--11
with 25 ties. H2H is pairwise (each question yields a winner or a tie), so the zero-score issue
that affects means does not apply -- a refused response simply loses. This recomputes the actual
W/L/T from the frozen H2H data.

No API calls -- frozen data only.
"""

import json
import glob
import os
from collections import defaultdict, Counter

H2H_ROOT = os.path.join(os.path.dirname(__file__), "..", "data", "head_to_head")


def main():
    batches = sorted(d for d in glob.glob(os.path.join(H2H_ROOT, "*")) if os.path.isdir(d))
    total_q = 0
    summary = {}
    for b in batches:
        files = glob.glob(os.path.join(b, "*.json"))
        wins = Counter()
        ties = 0
        names = set()
        for f in files:
            d = json.load(open(f))
            contestants = d.get("contestants", {})
            for c in contestants.values():
                names.add(c.get("display_name", ""))
            w = d.get("winner")
            if not w or str(w).lower() in ("tie", "draw", "none") or d.get("margin") == 0:
                ties += 1
            else:
                wins[w] += 1
        n = len(files)
        total_q += n
        summary[os.path.basename(b)] = {"n": n, "wins": dict(wins), "ties": ties,
                                        "contestants": sorted(names)}
        record = " / ".join(f"{k} {v}" for k, v in wins.most_common()) + f" / ties {ties}"
        print(f"{os.path.basename(b):26s} n={n:3d}  {record}")

    print(f"\nTotal H2H questions across {len(batches)} batches: {total_q}")
    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "h2h_results.json")
    json.dump({"batches": summary, "total_questions": total_q, "n_batches": len(batches)},
              open(out, "w"), indent=2)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
