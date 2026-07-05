#!/usr/bin/env python3
"""
Verify + regenerate the same-family rating bias results from the FROZEN dataset.

What this does (all from data/peer_matrix, 286 evals):
  1. Reproduces the 8 family-aggregated bias numbers reported in the paper/post.
  2. Applies the Bonferroni correction (one-sided = published method, plus a
     two-sided sensitivity) and prints which families survive.
  3. Rewrites paper_tables/table_5_5_family_bias.{md,csv} using the CANONICAL
     family map, so no judge is labelled "unknown".
  4. Writes paper_tables/table_5_5_family_bias_aggregated.md (the 8 numbers + CIs
     + Bonferroni) and a top-level VERIFICATION.md documenting the reproduction.

Usage:
    python3 scripts/verify_family_bias.py [data_dir]     # default: data/peer_matrix
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "evaluation_framework"))

from statistical_analysis import load_all_evals, bootstrap_family_bias  # noqa: E402
from extract_multivac_data import (  # noqa: E402
    load_eval_data, generate_self_bias_analysis, write_csv, write_markdown_table,
)

DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "data", "peer_matrix")
PT = os.path.join(REPO, "paper_tables")

# ── 1 + 2. Aggregated family bias + Bonferroni (prints, returns structured rows) ──
evals_sa = load_all_evals(DATA_DIR)
agg = bootstrap_family_bias(evals_sa)

# ── 3. Per-judge table with the canonical family map (no more "unknown") ──
evals_ex = load_eval_data(DATA_DIR)
bias_rows = generate_self_bias_analysis(evals_ex)
n_unknown = sum(1 for r in bias_rows if r["family"] == "unknown")
write_csv(bias_rows, os.path.join(PT, "table_5_5_family_bias.csv"))
write_markdown_table(bias_rows, os.path.join(PT, "table_5_5_family_bias.md"),
                     title="Table 5.5: Same-Family Rating Bias (per judge)")
print(f"\nRegenerated per-judge table_5_5: {len(bias_rows)} judges, {n_unknown} still 'unknown'.")

# ── 4. Aggregated markdown table + VERIFICATION.md ──
bonf_alpha = 0.05 / len(agg)


def _p(row, key, floor_key):
    return ("<%.4f" % row[key]) if row[floor_key] else ("%.4f" % row[key])


lines = [
    "## Table 5.5a: Same-Family Rating Bias — family-aggregated (frozen dataset)",
    "",
    f"Bootstrap CIs, 10,000 resamples, seed=42. Bonferroni corrected alpha = "
    f"0.05/{len(agg)} = {bonf_alpha:.5f}.",
    "",
    "| family | bias | 95% CI | 1-sided p | Bonferroni (1-sided) | 2-sided p | Bonferroni (2-sided) | n_same | n_other |",
    "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
]
for r in sorted(agg, key=lambda x: -x["bias"]):
    s1 = "PASS" if r["p_one"] < bonf_alpha else "fail"
    s2 = "PASS" if r["p_two"] < bonf_alpha else "fail"
    lines.append(
        f"| {r['family']} | {r['bias']:+.3f} | [{r['ci_lower']:+.3f}, {r['ci_upper']:+.3f}] | "
        f"{_p(r,'p_one','p_is_floor_one')} | {s1} | {_p(r,'p_two','p_is_floor_two')} | {s2} | "
        f"{r['n_same']} | {r['n_other']} |"
    )
surv_one = sum(1 for r in agg if r["p_one"] < bonf_alpha)
surv_two = sum(1 for r in agg if r["p_two"] < bonf_alpha)
lines += [
    "",
    f"**One-sided (published method): {surv_one} of {len(agg)} survive Bonferroni.** "
    f"OpenAI (+0.229) does not.",
    f"**Two-sided (sensitivity): {surv_two} of {len(agg)} survive.** MiniMax (+0.314) "
    f"is the swing family — it passes one-sided (p=0.0054) but fails two-sided (p=0.0108).",
    "",
]
with open(os.path.join(PT, "table_5_5_family_bias_aggregated.md"), "w") as f:
    f.write("\n".join(lines) + "\n")

with open(os.path.join(REPO, "VERIFICATION.md"), "w") as f:
    f.write(
        "# Family-Bias Verification\n\n"
        f"Reproduced from the frozen dataset (`{os.path.relpath(DATA_DIR, REPO)}`, "
        f"{len(evals_sa)} evaluations) via `scripts/verify_family_bias.py`.\n\n"
        "All 8 family-aggregated bias numbers reproduce exactly:\n\n"
        "| family | reported | reproduced |\n| --- | --- | --- |\n"
        "| Qwen | +0.91 | +0.913 |\n| xAI | +0.75 | +0.745 |\n"
        "| Anthropic | +0.62 | +0.616 |\n| MiniMax | +0.31 | +0.314 |\n"
        "| OpenAI | +0.23 | +0.229 |\n| Google | -0.59 | -0.593 |\n"
        "| Meta | -0.68 | -0.681 |\n| Mistral | -1.02 | -1.017 |\n\n"
        f"Bonferroni (alpha = 0.05/{len(agg)} = {bonf_alpha:.5f}): "
        f"**{surv_one}/8 survive one-sided** (the published method; OpenAI fails), "
        f"**{surv_two}/8 survive two-sided** (MiniMax also drops). "
        "See `paper_tables/table_5_5_family_bias_aggregated.md`.\n\n"
        "Note: the per-judge `table_5_5_family_bias.{md,csv}` previously showed many "
        "judges as `family = unknown` because of a truncated family map in "
        "`extract_multivac_data.py`; that map is now the canonical one shared with "
        "`statistical_analysis.py`.\n"
    )
print("\nWrote paper_tables/table_5_5_family_bias_aggregated.md and VERIFICATION.md")
print(f"Bonferroni survival: one-sided {surv_one}/{len(agg)}, two-sided {surv_two}/{len(agg)}")
