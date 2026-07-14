#!/usr/bin/env python3
"""
Four-cell decomposition of the naive same-family bias, for all 8 families.

The paper's published bias is the JUDGE-FIXED gap A - B (per statistical_analysis.py):
for family F, how much higher F's judges score F's responses (A) vs how F's judges score
everyone else (B). This CONFLATES real favoritism with the quality of F's own responses.

Split the pool into four cells (self-judgments excluded throughout):
    A = mean score  F-judge  -> F-respondent
    B = mean score  F-judge  -> other-respondent
    C = mean score  other-judge -> F-respondent
    D = mean score  other-judge -> other-respondent

Exact accounting identity for the published bias:
    A - B  =  (A - C)   +   (C - D)   -   (B - D)
             favoritism    respondent    F-judges' leniency
             (raw, same    quality       toward non-siblings
             response)     (neutral      (vs neutral judges)
                           judges)

So a large negative published bias can come entirely from (C - D) < 0 -- F's responses
being genuinely weaker -- with no unfavourable judging at all. The favoritism estimate net
of the judge's general leniency is the strict-within FE coefficient (within_response_bias.py).

No API calls -- pure re-analysis of the frozen dataset.
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from within_response_bias import load_judgments, fit_within_fe, FAMILIES   # noqa: E402

# Published judge-fixed bias (A-B) from ADR-029 Appendix A, for cross-checking.
ADR_NAIVE = {"qwen": 0.913, "xai": 0.745, "anthropic": 0.616, "minimax": 0.314,
             "openai": 0.229, "google": -0.593, "meta": -0.681, "mistral": -1.017}


def cells(df, f):
    gj = df["judge_family"] == f
    gr = df["respondent_family"] == f
    def m(mask):
        s = df.loc[mask, "weighted_score"]
        return (float(s.mean()) if len(s) else float("nan"), int(len(s)))
    A, nA = m(gj & gr)
    B, nB = m(gj & ~gr)
    C, nC = m(~gj & gr)
    D, nD = m(~gj & ~gr)
    return dict(A=A, B=B, C=C, D=D, nA=nA, nB=nB, nC=nC, nD=nD)


def main():
    df = load_judgments()
    fe = fit_within_fe(df)
    fams = [f for f in FAMILIES if ((df.respondent_family == f) & (df.judge_family == f)).sum() >= 5]

    rows = []
    for f in fams:
        c = cells(df, f)
        naive_AB = c["A"] - c["B"]          # published judge-fixed bias
        favor_AC = c["A"] - c["C"]          # raw favoritism (same responses)
        respq_CD = c["C"] - c["D"]          # respondent quality
        leni_BD = c["B"] - c["D"]           # F-judges' leniency toward non-siblings
        rows.append(dict(family=f, **c, naive_AB=naive_AB, favor_AC=favor_AC,
                         respq_CD=respq_CD, leni_BD=leni_BD,
                         fe=fe[f]["fe"], p_judge=fe[f]["p_judge"], n_ident=None))

    print("=== FOUR CELLS (self-judgments excluded) ===")
    print(f"  {'family':10s} {'A(FF)':>7s} {'B(Fo)':>7s} {'C(oF)':>7s} {'D(oo)':>7s}  "
          f"{'nA':>4s} {'nC':>5s}")
    for r in rows:
        print(f"  {r['family']:10s} {r['A']:>7.3f} {r['B']:>7.3f} {r['C']:>7.3f} {r['D']:>7.3f}  "
              f"{r['nA']:>4d} {r['nC']:>5d}")

    print("\n=== DECOMPOSITION of published bias  A-B = (A-C) + (C-D) - (B-D) ===")
    print(f"  {'family':10s} {'pub(A-B)':>9s} {'ADR':>7s} {'favor(A-C)':>11s} "
          f"{'respQ(C-D)':>11s} {'leni(B-D)':>10s} {'FE net':>8s} {'p_j':>7s}  driver")
    for r in sorted(rows, key=lambda x: x["naive_AB"]):
        chk = r["favor_AC"] + r["respq_CD"] - r["leni_BD"]     # must equal naive_AB
        assert abs(chk - r["naive_AB"]) < 1e-9
        adr = ADR_NAIVE.get(r["family"], float("nan"))
        # which term dominates the published bias?
        mags = {"favoritism": r["favor_AC"], "respondent-quality": r["respq_CD"],
                "leniency": -r["leni_BD"]}
        driver = max(mags, key=lambda k: abs(mags[k]))
        print(f"  {r['family']:10s} {r['naive_AB']:>+9.3f} {adr:>+7.3f} {r['favor_AC']:>+11.3f} "
              f"{r['respq_CD']:>+11.3f} {r['leni_BD']:>+10.3f} {r['fe']:>+8.3f} {r['p_judge']:>7.3f}  {driver}")

    # Judge leniency by family (mean score GIVEN) -- motivates controlling for it; the spread
    # cited across the findings docs ("OpenAI ... Mistral ...") is traceable here.
    print("\n=== JUDGE LENIENCY: mean weighted_score GIVEN, by judge family ===")
    len_rows = []
    for f in sorted(set(df["judge_family"])):
        s = df.loc[df["judge_family"] == f, "weighted_score"]
        len_rows.append((f, float(s.mean()), int(len(s))))
    for f, mu, n in sorted(len_rows, key=lambda x: x[1]):
        print(f"  {f:12s} {mu:6.3f}  (n={n})")
    print(f"  grand mean = {df['weighted_score'].mean():.3f}")

    print("\n  pub(A-B)  = published judge-fixed same-family bias (matches ADR Appendix A column)")
    print("  favor(A-C)= raw favoritism: sibling vs neutral judge on the SAME responses")
    print("  respQ(C-D)= respondent quality: F's responses vs others, scored by NEUTRAL judges")
    print("  leni(B-D) = F-judges' leniency toward non-siblings vs neutral judges")
    print("  FE net    = strict-within favoritism, net of judge leniency (judge-clustered)")
    print("  driver    = the term with the largest magnitude contribution to pub(A-B)")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "four_cell_decomposition.json")
    with open(out, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
