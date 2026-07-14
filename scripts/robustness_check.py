#!/usr/bin/env python3
"""
Robustness re-run: do the corrected findings survive dropping the worst judges?

The parse-failure analysis showed a handful of judges fail to emit valid JSON most of
the time (olmo_think 86%, kimi 79%, gemini_3_pro 56%, small Qwens, gpt_oss_legal). Their
few surviving judgments may be a non-random subset. If our corrected findings depend on
them, the systematic-failure bias (Sander #4) has contaminated the results.

We drop every judge whose parse-failure rate > 30% (n >= 20) and re-run:
  A. the within-response same-family bias  (crossed mixed model)
  B. the Bradley-Terry per-category winners
comparing FULL vs FILTERED. Stable => the corrections are not artifacts of the bad judges.

No API calls -- pure re-analysis. Reads paper_tables/parse_failure.json for the drop list.
"""

import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from within_response_bias import load_judgments, fit_within_fe, naive_and_counts, FAMILIES  # noqa: E402
from bradley_terry_ranking import load, bt_fit, ranked                   # noqa: E402

HERE = os.path.dirname(__file__)
FAIL_THRESHOLD = 0.30
MIN_N = 20


def high_failure_judges():
    pf = json.load(open(os.path.join(HERE, "..", "paper_tables", "parse_failure.json")))
    drop = {r["judge"]: r["rate"] for r in pf["judge_chi2"]["rows"]
            if r["rate"] > FAIL_THRESHOLD and r["n"] >= MIN_N}
    return drop


def category_winners(exclude):
    groups, groups_cat, naive = load(exclude_judges=exclude)
    cat_groups = defaultdict(list)
    for g, c in zip(groups, groups_cat):
        cat_groups[c].append(g)
    winners = {}
    for cat in sorted(naive):
        try:
            btc, _, _ = bt_fit(cat_groups[cat], min_comparisons=10)
            winners[cat] = ranked(btc)[0] if btc else "-"
        except Exception:
            winners[cat] = "-"
    return winners


def main():
    drop = high_failure_judges()
    print(f"Dropping {len(drop)} judges with parse-failure > {int(FAIL_THRESHOLD*100)}% (n>={MIN_N}):")
    for j, r in sorted(drop.items(), key=lambda x: -x[1]):
        print(f"    {j:20s} {100*r:.0f}%")
    dropset = set(drop)

    # ---------- A. within-response same-family bias (STRICT-WITHIN FE) ----------
    print("\n" + "=" * 78)
    print("A. STRICT-WITHIN FE SAME-FAMILY BIAS, judge-clustered  (full vs high-fail dropped)")
    print("=" * 78)
    print("   (uses the strict-within FE estimator, NOT the random-intercept one -- the RE model")
    print("    is insensitive to data removal, which made the previous robustness check vacuous.)")
    df = load_judgments()
    bonf = 0.05 / len([f for f in FAMILIES
                       if ((df.respondent_family == f) & (df.judge_family == f)).sum() >= 5])
    full = fit_within_fe(df)
    filt = fit_within_fe(df[~df["judge_key"].isin(dropset)])

    print(f"\n  {'family':10s} {'FE full':>8s} {'p_j':>7s} {'sig':>4s}   "
          f"{'FE drop':>8s} {'p_j':>7s} {'sig':>4s}   {'Δ':>7s}  verdict")
    for fam in sorted(full, key=lambda k: -full[k]["fe"]):
        a = full[fam]
        b = filt.get(fam)
        sa = "PASS" if a["p_judge"] < bonf else "ns"
        if not b:
            print(f"  {fam:10s} {a['fe']:>+8.3f} {a['p_judge']:>7.3f} {sa:>4s}   {'(dropped)':>8s}")
            continue
        sb = "PASS" if b["p_judge"] < bonf else "ns"
        delta = b["fe"] - a["fe"]
        verdict = "stable" if (sa == "PASS") == (sb == "PASS") else "CHANGED sig."
        print(f"  {fam:10s} {a['fe']:>+8.3f} {a['p_judge']:>7.3f} {sa:>4s}   "
              f"{b['fe']:>+8.3f} {b['p_judge']:>7.3f} {sb:>4s}   {delta:>+7.3f}  {verdict}")
    print(f"\n  Bonferroni alpha = {bonf:.5f} applied to judge-clustered p")

    # ---------- B. Bradley-Terry per-category winners ----------
    print("\n" + "=" * 72)
    print("B. BRADLEY-TERRY PER-CATEGORY WINNER  (full vs high-fail judges dropped)")
    print("=" * 72)
    win_full = category_winners(exclude=None)
    win_filt = category_winners(exclude=dropset)
    print(f"  {'category':15s} {'BT winner (full)':24s} {'BT winner (dropped)':24s} verdict")
    n_stable = 0
    for cat in sorted(win_full):
        a, b = win_full[cat], win_filt.get(cat, "-")
        stable = a == b
        n_stable += stable
        print(f"  {cat:15s} {a:24s} {b:24s} {'stable' if stable else 'CHANGED'}")
    print(f"\n  category winners stable to dropping bad judges: {n_stable}/{len(win_full)}")

    print("\nInterpretation: 'stable' => the corrected finding does not depend on the "
          "systematically-failing judges, so parse-failure bias (Sander #4) did not drive it.")


if __name__ == "__main__":
    main()
