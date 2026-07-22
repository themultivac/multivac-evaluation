#!/usr/bin/env python3
"""
Per-dimension means and per-model clarity-depth gaps, with genuine zero-scores INCLUDED.

The paper reports depth as the lowest dimension (8.45), clarity the highest (9.40), and the
largest clarity-depth gap at GPT-5.2-Codex (1.438) -- all computed on the scored-only set. The
1,104 zero-scores have all five dimensions equal to 0, so including them lowers every dimension
mean and changes per-model gaps. This recomputes both with zeros included.

No API calls -- frozen data only.
"""

import json
import glob
import os
from collections import defaultdict

import numpy as np

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")
DIMS = ["correctness", "completeness", "clarity", "depth", "usefulness"]


def main():
    dim_all = defaultdict(list)                       # dimension -> all values (zeros incl.)
    per_model = defaultdict(lambda: defaultdict(list))  # model -> dim -> values
    names = {}
    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        for j in ev.get("judgments", []):
            if j.get("judge_key") == j.get("respondent_key") or j.get("error") is not None:
                continue
            rk = j["respondent_key"]
            names[rk] = j.get("respondent_name", rk)
            for dim in DIMS:                          # zero-score judgments contribute 0 to each dim
                v = float(j.get(dim) or 0.0)
                dim_all[dim].append(v)
                per_model[rk][dim].append(v)

    print("=== Overall per-dimension means (zeros included) ===")
    means = {d: float(np.mean(dim_all[d])) for d in DIMS}
    for d in sorted(DIMS, key=lambda x: -means[x]):
        print(f"  {d:14s} {means[d]:.3f}  (n={len(dim_all[d]):,})")
    print(f"  highest: {max(means, key=means.get)} ({max(means.values()):.3f}); "
          f"lowest: {min(means, key=means.get)} ({min(means.values()):.3f})")

    print("\n=== Largest clarity-depth gaps (zeros included, models with n>=100) ===")
    gaps = []
    for m, dd in per_model.items():
        if len(dd["clarity"]) >= 100:
            gaps.append((names[m], float(np.mean(dd["clarity"])) - float(np.mean(dd["depth"])),
                         float(np.mean(dd["clarity"])), float(np.mean(dd["depth"])), len(dd["clarity"])))
    gaps.sort(key=lambda x: -x[1])
    print(f"  {'model':22s} {'gap':>7s} {'clarity':>8s} {'depth':>7s} {'n':>5s}")
    for nm, g, c, dp, n in gaps[:6]:
        print(f"  {nm:22s} {g:>+7.3f} {c:>8.3f} {dp:>7.3f} {n:>5d}")
    n_gap_08 = sum(1 for _, g, *_ in gaps if g > 0.8)
    print(f"  models (n>=100) with clarity-depth gap > 0.8: {n_gap_08} of {len(gaps)}")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "dimension_means.json")
    json.dump({"overall_means": means,
               "top_gaps": [{"model": nm, "gap": g, "clarity": c, "depth": d} for nm, g, c, d, _ in gaps[:10]],
               "n_gap_over_0.8": n_gap_08, "n_models_ge100": len(gaps)}, open(out, "w"), indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
