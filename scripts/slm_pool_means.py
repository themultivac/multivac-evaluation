#!/usr/bin/env python3
"""
SLM-pool respondent means, with genuine zero-scores INCLUDED (+ refusal rate per model).

The paper claims Qwen 3 8B (9.328) beats Phi-4 14B (8.924) and Gemma 3 27B (8.853) in the SLM
pool. Small models refuse more than frontier models, so the original scored-only means may
mis-rank them. This recomputes each SLM-pool respondent's mean composite score including the
zero-scores of refused/empty responses, alongside its refusal rate.

No API calls -- frozen data only.
"""

import json
import glob
import os
from collections import defaultdict

import numpy as np

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")


def main():
    rec = defaultdict(lambda: {"scored": [], "zero": 0})
    names = {}
    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        if ev.get("category") != "slm":
            continue
        for j in ev.get("judgments", []):
            if j.get("judge_key") == j.get("respondent_key") or j.get("error") is not None:
                continue
            rk, ws = j["respondent_key"], float(j.get("weighted_score") or 0.0)
            names[rk] = j.get("respondent_name", rk)
            if ws > 0:
                rec[rk]["scored"].append(ws)
            else:
                rec[rk]["zero"] += 1

    rows = []
    for m, d in rec.items():
        n1, n0 = len(d["scored"]), d["zero"]
        if n1 + n0 < 30:
            continue
        rows.append({"model": names[m], "excl": float(np.mean(d["scored"])) if n1 else 0.0,
                     "incl": sum(d["scored"]) / (n1 + n0), "refusal": n0 / (n1 + n0), "n": n1 + n0})

    print(f"{'model':22s} {'scored-only':>11s} {'incl-zeros':>11s} {'refusal%':>9s} {'n':>4s}")
    for r in sorted(rows, key=lambda x: -x["incl"]):
        print(f"{r['model']:22s} {r['excl']:>11.3f} {r['incl']:>11.3f} {100*r['refusal']:>8.1f}% {r['n']:>4d}")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "slm_pool_means.json")
    json.dump(rows, open(out, "w"), indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
