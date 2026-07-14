#!/usr/bin/env python3
"""
Per-JUDGE leniency statistics (backs the themultivac.com/judges page).

The judges page cites per-individual-judge numbers (e.g. "GPT-5.4 strictest at 7.19,
Mistral Small most lenient at 9.70", a "2.5-point spread", "GPT-5.4 SD 2.22", "Granite 0.49").
Those were previously in no committed script. This computes them from the frozen dataset so
they are traceable (or corrected).

For each judge model: mean weighted_score GIVEN, SD of scores given, n valid non-self judgments.

No API calls -- pure re-analysis of the frozen dataset.
"""

import json
import glob
import os
from collections import defaultdict

import numpy as np

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")


def main():
    by_judge = defaultdict(list)
    names = {}
    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        for j in ev.get("judgments", []):
            if (j.get("error") is None and j.get("weighted_score") and j["weighted_score"] > 0
                    and j.get("judge_key") != j.get("respondent_key")):
                by_judge[j["judge_key"]].append(j["weighted_score"])
                if j.get("judge_name"):
                    names[j["judge_key"]] = j["judge_name"]

    rows = []
    for jk, sc in by_judge.items():
        if len(sc) >= 30:                      # stable per-judge stats only
            rows.append((names.get(jk, jk), float(np.mean(sc)), float(np.std(sc, ddof=1)), len(sc)))
    rows.sort(key=lambda x: x[1])

    print(f"{'judge':32s} {'mean given':>10s} {'SD':>7s} {'n':>6s}")
    for name, mu, sd, n in rows:
        print(f"{name:32s} {mu:>10.3f} {sd:>7.3f} {n:>6d}")

    means = [r[1] for r in rows]
    print(f"\njudges with n>=30: {len(rows)}")
    print(f"strictest: {rows[0][0]} = {rows[0][1]:.2f}   most lenient: {rows[-1][0]} = {rows[-1][1]:.2f}")
    print(f"leniency spread (max-min mean): {max(means)-min(means):.2f} points")
    sds = sorted(rows, key=lambda x: x[2])
    print(f"lowest SD (most compressed): {sds[0][0]} = {sds[0][2]:.2f}")
    print(f"highest SD (most variable):  {sds[-1][0]} = {sds[-1][2]:.2f}")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "judge_leniency_stats.json")
    json.dump({"judges": [{"name": n, "mean_given": m, "sd": s, "n": c} for n, m, s, c in rows],
               "leniency_spread": max(means) - min(means)}, open(out, "w"), indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
