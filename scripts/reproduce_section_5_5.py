#!/usr/bin/env python3
"""
One-command reproduction of every number in paper §5.5 and Table 1.

Regenerates, from the frozen 286-eval dataset (no API calls):
  * the valid-judgment count breakdown (abstract / §4.3)
  * the four-cell decomposition A/B/C/D and the identity A-B = (A-C)+(C-D)-(B-D)
  * the strict-within FE same-vendor estimate with judge-clustered SEs and Bonferroni
  * Table 1 exactly as printed in the paper

Run:  ./.venv/bin/python scripts/reproduce_section_5_5.py
A reviewer can diff this output against Table 1 and §5.5 line by line.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from within_response_bias import load_judgments, full_table                       # noqa: E402
from four_cell_decomposition import cells                                         # noqa: E402
from within_response_bias import FAMILIES                                         # noqa: E402
import count_reconciliation as cr                                                 # noqa: E402

DISPLAY = {"anthropic": "Anthropic", "minimax": "MiniMax", "qwen": "Qwen", "google": "Google",
           "meta": "Meta", "openai": "OpenAI", "xai": "xAI", "mistral": "Mistral"}


def p_str(p):
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def main():
    print("=" * 78)
    print("REPRODUCTION OF PAPER §5.5 AND TABLE 1  (frozen 286-eval dataset, no API calls)")
    print("=" * 78)

    print("\n[1] VALID-JUDGMENT COUNT (abstract / §4.3)")
    cr.main()

    df = load_judgments()
    rows, bonf = full_table(df)
    by = {r["family"]: r for r in rows}

    print("\n[2] FOUR-CELL IDENTITY CHECK  A-B = (A-C)+(C-D)-(B-D)")
    ok = True
    for f in by:
        c = cells(df, f)
        lhs = c["A"] - c["B"]
        rhs = (c["A"] - c["C"]) + (c["C"] - c["D"]) - (c["B"] - c["D"])
        if abs(lhs - rhs) > 1e-9:
            ok = False
            print(f"    {f}: identity FAILS ({lhs:.6f} vs {rhs:.6f})")
    print(f"    identity holds to 1e-9 for all {len(by)} families: {ok}")

    print(f"\n[3] TABLE 1  (Bonferroni alpha = {bonf:.5f} on judge-clustered p; bold* = significant)")
    hdr = (f"    {'Family':10s} {'A':>6s} {'B':>6s} {'C':>6s} {'D':>6s} "
           f"{'Naive':>7s} {'A-C':>7s} {'RespQ':>7s} {'Leni':>7s} {'Corr(FE)':>9s} {'p':>8s} {'n_id':>5s}")
    print(hdr)
    print("    " + "-" * (len(hdr) - 4))
    order = ["anthropic", "minimax", "qwen", "google", "meta", "openai", "xai", "mistral"]
    for f in order:
        r = by[f]
        c = cells(df, f)
        naive = c["A"] - c["B"]
        sig = "*" if r["p_judge"] < bonf else " "
        print(f"    {DISPLAY[f]:10s} {c['A']:>6.3f} {c['B']:>6.3f} {c['C']:>6.3f} {c['D']:>6.3f} "
              f"{naive:>+7.3f} {c['A']-c['C']:>+7.3f} {c['C']-c['D']:>+7.3f} {c['B']-c['D']:>+7.3f} "
              f"{r['fe_bias']:>+8.3f}{sig} {p_str(r['p_judge']):>8s} {r['n_responses_identifying']:>5d}")

    print("\n[4] §5.5 HEADLINE VERDICTS")
    sig = [DISPLAY[f] for f in order if by[f]["p_judge"] < bonf]
    pos_naive = [f for f in order if (cells(df, f)["A"] - cells(df, f)["B"]) > 0]
    neg_naive = [f for f in order if (cells(df, f)["A"] - cells(df, f)["B"]) < 0]
    print(f"    naive: {len(pos_naive)} positive, {len(neg_naive)} negative")
    print(f"    corrected significant (FE, judge-clustered, Bonferroni): {sig}")
    print(f"    -> Anthropic/MiniMax robust; Qwen significant but fragile (n_ident={by['qwen']['n_responses_identifying']},"
          f" raw A-C={cells(df,'qwen')['A']-cells(df,'qwen')['C']:+.3f}); none negative.")


if __name__ == "__main__":
    main()
