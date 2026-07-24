#!/usr/bin/env python3
"""
Finding 1 leaderboard, rebuilt (answers the §5.1-vs-§5.5 inconsistency + the zero-score issue).

Two corrections vs the paper's original Finding 1:
  1. Genuine zero-scores are INCLUDED. The 1,104 error-null / weighted_score==0 judgments are
     real judge decisions (mostly of refused/empty responses; see count_reconciliation + the
     parser in multivac.py). Excluding them inflated refusing models by up to +4 points. We
     include them and report each model's refusal/zero rate.
  2. Rankings are reported by Bradley-Terry (leniency-adjusted, within-judge pairwise), with the
     naive mean shown alongside as the confounded quantity BT corrects (per §5.5).

Self-judgments (error == 'self_judgment_excluded') and parse/API failures (error set) are still
excluded -- only genuine parsed judgments (error is None) count, zeros included.

No API calls -- frozen data only.
"""

import json
import glob
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from bradley_terry_ranking import bt_fit, components, ranked   # noqa: E402

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")


def load_incl_zeros():
    """Received scores per respondent (zeros incl.) + BT groups (zeros incl.)."""
    received = defaultdict(lambda: {"scored": [], "zero": 0})
    names = {}
    groups = []
    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        by_judge = defaultdict(dict)
        for j in ev.get("judgments", []):
            if j.get("error") is not None or j.get("judge_key") == j.get("respondent_key"):
                continue                                  # skip self + parse/API failures
            rk, ws = j["respondent_key"], float(j.get("weighted_score") or 0.0)
            if j.get("respondent_name"):
                names[rk] = j["respondent_name"]
            if j.get("judge_name"):
                names.setdefault(j["judge_key"], j["judge_name"])
            if ws > 0:
                received[rk]["scored"].append(ws)
            else:
                received[rk]["zero"] += 1
            by_judge[j["judge_key"]][rk] = ws             # zeros included in BT groups
        for jk, sc in by_judge.items():
            if len(sc) >= 2:
                groups.append(sc)
    return received, names, groups


def collapse_by_name(groups, names):
    """Collapse per-(eval,judge) score dicts from registry keys to distinct display
    names (averaging any within-group duplicates), so connectivity is computed over
    the 50 distinct models the paper reports -- not the 55 raw registry keys. Without
    this, duplicate keys (e.g. gpt_5_4 + judge_gpt54 -> 'GPT-5.4') split the frontier
    into 34 nodes instead of the paper's 30."""
    out = []
    for g in groups:
        agg = defaultdict(list)
        for k, v in g.items():
            agg[names.get(k, k)].append(v)
        d = {nm: float(np.mean(vs)) for nm, vs in agg.items()}
        if len(d) >= 2:
            out.append(d)
    return out


def main():
    received, names, groups = load_incl_zeros()
    bt, _, _ = bt_fit(groups, min_comparisons=30)
    # Connectivity / frontier membership are reported over distinct display names
    # (the paper's 30-model frontier + 18-model small pool), so the released cache
    # matches the paper rather than the 55-key graph.
    groups_named = collapse_by_name(groups, names)
    comps = components(groups_named)
    frontier = max(comps, key=len)                 # set of display names

    rows = []
    for m, d in received.items():
        n1, n0 = len(d["scored"]), d["zero"]
        if n1 + n0 < 30:
            continue
        mean_incl = sum(d["scored"]) / (n1 + n0)
        rows.append({"model": names.get(m, m), "key": m, "refusal": n0 / (n1 + n0),
                     "n": n1 + n0, "mean_incl": mean_incl,
                     "mean_excl": (np.mean(d["scored"]) if n1 else 0.0),
                     "bt": bt.get(m), "frontier": names.get(m, m) in frontier})

    naive_rank = {r["key"]: i for i, r in enumerate(sorted(rows, key=lambda x: -x["mean_incl"]))}
    # BT rank is only valid WITHIN a connected component (pools are disconnected);
    # components are over display names, so group rows by their display name.
    bt_rank = {}
    for cset in comps:
        comp_rows = [r for r in rows if r["bt"] is not None and r["model"] in cset]
        for i, r in enumerate(sorted(comp_rows, key=lambda x: -x["bt"])):
            bt_rank[r["key"]] = i

    print("FINDING 1 LEADERBOARD (zeros included; BT = leniency-adjusted)\n")
    print(f"{'model':26s} {'refusal%':>8s} {'naive(incl)':>11s} {'(excl)':>7s} "
          f"{'nR':>4s} {'BT':>7s} {'BTr':>4s} {'pool':>9s}")
    for r in sorted(rows, key=lambda x: -x["mean_incl"]):
        btr = bt_rank.get(r["key"])
        pool = "frontier" if r["frontier"] else "small"
        bt_s = f"{r['bt']:>+7.2f}" if r["bt"] is not None else f"{'--':>7s}"
        btr_s = f"{btr + 1:>4d}" if btr is not None else f"{'--':>4s}"
        print(f"{r['model']:26s} {100*r['refusal']:>7.1f}% {r['mean_incl']:>11.3f} {r['mean_excl']:>7.3f} "
              f"{naive_rank[r['key']]+1:>4d} {bt_s} {btr_s} {pool:>9s}")

    print(f"\ncomponents: {[len(c) for c in comps]}  (BT not identifiable across pools)")
    print("naive(incl) = mean composite INCLUDING zero-scores;  (excl) = old scored-only mean")
    print("refusal% = share of received judgments that were genuine 0-scores (refused/empty/broken)")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "finding1_leaderboard.json")
    small = min(comps, key=len) if len(comps) > 1 else []
    json.dump({
        "rows": rows,                                   # one row per registry key (55 -> 50 with n>=30)
        "components": [len(c) for c in comps],          # over distinct display names: [30, 18]
        "frontier_models": sorted(frontier),            # the 30 distinct frontier models (paper's figure)
        "small_models": sorted(small),                  # the 18 distinct small-pool models
        "note": ("components/frontier are over distinct display names (the paper's 30-model frontier "
                 "and 18-model small pool); rows are keyed by the 55 raw registry keys, so a display "
                 "name with duplicate keys (e.g. GPT-5.4) yields more than one frontier=true row."),
    }, open(out, "w"), indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
