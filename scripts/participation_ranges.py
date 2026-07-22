#!/usr/bin/env python3
"""
Per-model participation counts and the core / extended / focused tier ranges.

The paper states core-pool models appear in 116--230 evaluations, extended-pool in 30--99, and
focused-batch models in 1--29. Participation is the number of peer-matrix evaluations a model
takes part in; it is independent of scores (a refused response still counts as participation), so
zeros do not change it -- this script simply verifies the ranges against the frozen data.

No API calls -- frozen data only.
"""

import json
import glob
import os
from collections import defaultdict

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")


def main():
    count = defaultdict(int)
    names = {}
    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        for m in set(ev.get("models_used", [])):
            count[m] += 1
        for j in ev.get("judgments", []):
            if j.get("respondent_name"):
                names[j["respondent_key"]] = j["respondent_name"]

    rows = sorted(count.items(), key=lambda x: -x[1])
    print(f"{len(rows)} models participate. Distribution of evaluation counts:")
    print(f"  {'model':26s} {'evals':>6s}")
    for m, c in rows:
        print(f"  {names.get(m, m):26s} {c:>6d}")

    core = [c for _, c in rows if c >= 100]
    ext = [c for _, c in rows if 30 <= c < 100]
    foc = [c for _, c in rows if c < 30]
    print(f"\ncore pool (>=100 evals): {len(core)} models, range {min(core)}--{max(core)}")
    print(f"extended (30--99):       {len(ext)} models, range {min(ext)}--{max(ext)}")
    print(f"focused batch (<30):     {len(foc)} models, range {min(foc)}--{max(foc)}")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "participation_ranges.json")
    json.dump({"core": [min(core), max(core), len(core)], "extended": [min(ext), max(ext), len(ext)],
               "focused": [min(foc), max(foc), len(foc)],
               "per_model": {names.get(m, m): c for m, c in rows}}, open(out, "w"), indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
