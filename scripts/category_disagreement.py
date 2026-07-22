#!/usr/bin/env python3
"""
Inter-judge disagreement by category (paper finding 3).

For each response (one model's answer in one eval), compute the standard deviation of the
scores its multiple judges gave it; average that within-response SD per category. This is the
inter-judge disagreement. Reproduces the abstract's claim that code evaluation produces
disproportionate disagreement relative to meta-alignment.

No API calls -- pure re-analysis of the frozen dataset.
"""

import json
import glob
import os
from collections import defaultdict

import numpy as np

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")


def main():
    by_resp = defaultdict(list)
    cat_of = {}
    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        cat, eid = ev.get("category"), ev.get("evaluation_id")
        for j in ev.get("judgments", []):
            if j.get("error") is None and j.get("weighted_score") and j["weighted_score"] > 0:
                rid = f"{eid}::{j['respondent_key']}"
                by_resp[rid].append(j["weighted_score"])
                cat_of[rid] = cat

    cat_sd = defaultdict(list)
    for rid, sc in by_resp.items():
        if len(sc) >= 2:
            cat_sd[cat_of[rid]].append(float(np.std(sc, ddof=1)))

    rows = sorted(((c, float(np.mean(v)), float(np.median(v)), len(v)) for c, v in cat_sd.items()),
                  key=lambda x: -x[1])
    print(f"{'category':16s} {'mean SD':>10s} {'median SD':>10s} {'n_resp':>8s}")
    for c, mean, med, n in rows:
        print(f"{c:16s} {mean:>10.3f} {med:>10.3f} {n:>8d}")
    d = {c: mean for c, mean, _, _ in rows}
    med = {c: m for c, _, m, _ in rows}
    print(f"\ncode = {d['code']:.3f},  meta_alignment = {d['meta_alignment']:.3f},  "
          f"ratio = {d['code']/d['meta_alignment']:.2f}x")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "category_disagreement.json")
    json.dump({"per_category_mean_sd": d, "per_category_median_sd": med,
               "code_over_meta_ratio": d["code"] / d["meta_alignment"]}, open(out, "w"), indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
