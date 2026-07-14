#!/usr/bin/env python3
"""
Parse-failure analysis: random or systematic?  (answers Sander Land #4)

The paper reports ~19% invalid judgments but never checks whether the failures
are random noise or systematically concentrated in particular judge models or
categories. If systematic, the surviving (valid) judgments are a biased sample
and every downstream number inherits that bias.

We classify every judgment's `error` into:
  * valid          -> error is None (parsed fine)
  * self_excluded  -> intentional diagonal exclusion (NOT a failure; dropped)
  * parse_failure  -> judge produced unparseable output (malformed JSON,
                      missing score keys, NoneType, score>10). The JUDGE's fault.
  * api_error      -> OpenRouter 4xx/5xx, DNS, disconnect. Infrastructure, not the
                      model's text. Reported separately, excluded from the parse test.

Then, over ATTEMPTED non-self judgments (valid + parse_failure), we test whether the
parse-failure rate is independent of (a) the judge model and (b) the category, with a
chi-square test of independence. Rejecting independence => systematic, not random.

No API calls -- pure re-analysis of the frozen dataset.
"""

import json
import glob
import os
from collections import defaultdict

import numpy as np
from scipy import stats

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")

API_MARKERS = ("Client error", "Server error", "name resolution", "disconnected",
               "peer closed connection", "incomplete chunked", "Temporary failure")


def classify(err):
    if err is None:
        return "valid"
    if str(err).strip() == "":
        return "parse_failure"   # blank error but ws==0 (verified): silent no-score failure
    if err == "self_judgment_excluded":
        return "self_excluded"
    if any(m in str(err) for m in API_MARKERS):
        return "api_error"
    return "parse_failure"        # JSON errors, parse_failed, NoneType, score>10, 'choices'


def chi2_rate_table(counts):
    """counts: {group: [n_fail, n_ok]} -> chi2 test + per-group rates, sorted worst-first."""
    groups = [g for g, (f, o) in counts.items() if (f + o) >= 20]  # stable rates only
    table = np.array([counts[g] for g in groups])  # rows=group, cols=[fail, ok]
    chi2, p, dof, _ = stats.chi2_contingency(table)
    rows = []
    for g in groups:
        f, o = counts[g]
        n = f + o
        rows.append((g, f, n, f / n))
    rows.sort(key=lambda r: -r[3])
    overall = table[:, 0].sum() / table.sum()
    return chi2, p, dof, overall, rows


def main():
    by_kind = defaultdict(int)
    judge_counts = defaultdict(lambda: [0, 0])     # judge -> [fail, ok]
    cat_counts = defaultdict(lambda: [0, 0])       # category -> [fail, ok]
    api_by_judge = defaultdict(int)
    total = 0

    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        cat = ev.get("category")
        for j in ev.get("judgments", []):
            total += 1
            kind = classify(j.get("error"))
            by_kind[kind] += 1
            jk = j.get("judge_key")
            if kind == "api_error":
                api_by_judge[jk] += 1
                continue
            if kind in ("self_excluded",):
                continue
            # attempted, model-attributable: valid or parse_failure
            idx = 0 if kind == "parse_failure" else 1
            judge_counts[jk][idx] += 1
            cat_counts[cat][idx] += 1

    print(f"Total judgment slots: {total:,}\n")
    print("=== classification ===")
    for k in ("valid", "self_excluded", "parse_failure", "api_error"):
        print(f"  {k:15s} {by_kind[k]:6d}  ({100*by_kind[k]/total:.1f}%)")
    attempted = by_kind["valid"] + by_kind["parse_failure"]
    print(f"\n  Model-attributable parse-failure rate (of attempted non-self, ex-API): "
          f"{by_kind['parse_failure']}/{attempted} = {100*by_kind['parse_failure']/attempted:.1f}%")

    print("\n" + "=" * 62)
    print("PARSE FAILURE BY JUDGE MODEL  (systematic?)")
    print("=" * 62)
    chi2, pval, dof, overall, rows = chi2_rate_table(judge_counts)
    print(f"overall rate = {100*overall:.1f}%   chi2({dof}) = {chi2:.1f}, p = {pval:.2e}")
    print(f"=> {'SYSTEMATIC (reject uniform)' if pval < 0.05 else 'consistent with random'}\n")
    print(f"  {'judge':22s} {'fail':>5s} {'n':>5s} {'rate':>7s}")
    for g, f, n, r in rows[:12]:
        flag = "  <-- outlier" if r > 3 * overall else ""
        print(f"  {g:22s} {f:>5d} {n:>5d} {100*r:>6.1f}%{flag}")
    print("  ...")
    for g, f, n, r in rows[-3:]:
        print(f"  {g:22s} {f:>5d} {n:>5d} {100*r:>6.1f}%")

    print("\n" + "=" * 62)
    print("PARSE FAILURE BY CATEGORY  (systematic?)")
    print("=" * 62)
    chi2c, pvalc, dofc, overallc, rowsc = chi2_rate_table(cat_counts)
    print(f"overall rate = {100*overallc:.1f}%   chi2({dofc}) = {chi2c:.1f}, p = {pvalc:.2e}")
    print(f"=> {'SYSTEMATIC (reject uniform)' if pvalc < 0.05 else 'consistent with random'}\n")
    print(f"  {'category':22s} {'fail':>5s} {'n':>5s} {'rate':>7s}")
    for g, f, n, r in rowsc:
        print(f"  {g:22s} {f:>5d} {n:>5d} {100*r:>6.1f}%")

    if api_by_judge:
        print("\n=== API/infra errors by judge (separate, not model text) ===")
        for jk, n in sorted(api_by_judge.items(), key=lambda x: -x[1])[:8]:
            print(f"  {jk:22s} {n:>4d}")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "parse_failure.json")
    with open(out, "w") as f:
        json.dump({
            "classification": dict(by_kind), "total": total,
            "judge_chi2": {"chi2": chi2, "p": pval, "dof": dof, "overall_rate": overall,
                           "rows": [{"judge": g, "fail": f, "n": n, "rate": r} for g, f, n, r in rows]},
            "category_chi2": {"chi2": chi2c, "p": pvalc, "dof": dofc, "overall_rate": overallc,
                              "rows": [{"category": g, "fail": f, "n": n, "rate": r} for g, f, n, r in rowsc]},
        }, f, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
