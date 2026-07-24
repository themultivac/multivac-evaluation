#!/usr/bin/env bash
# One-command reproduction: raw frozen data (data/peer_matrix) -> tables + figures -> both PDFs.
# Every table/figure is regenerated from data/peer_matrix/EVAL-*/results.json; no cached
# intermediate is trusted as a source. Run from a clean checkout:
#     bash scripts/reproduce_all.sh
#
# Requires: a Python venv at ./.venv with numpy, scipy, matplotlib; tectonic on PATH.
set -euo pipefail

cd "$(dirname "$0")/.."
PY="./.venv/bin/python"
command -v tectonic >/dev/null || { echo "ERROR: tectonic not found on PATH (install from https://tectonic-typesetting.github.io)" >&2; exit 1; }

# Bootstrap the analysis venv on first run so this is genuinely one command from a
# fresh checkout. Needs python3 on PATH; deps come from requirements.txt (numpy,
# scipy, matplotlib, pandas). Skipped if ./.venv already has them.
if ! "$PY" -c "import numpy, scipy, matplotlib" >/dev/null 2>&1; then
  echo "== 0/3  Bootstrapping ./.venv from requirements.txt =="
  command -v python3 >/dev/null || { echo "ERROR: python3 not found on PATH" >&2; exit 1; }
  python3 -m venv .venv
  "$PY" -m pip install --quiet --upgrade pip
  "$PY" -m pip install --quiet -r requirements.txt
fi

echo "== 1/3  Compute tables from raw (data/peer_matrix) =="
for s in count_reconciliation participation_ranges parse_failure_analysis \
         dimension_means judge_leniency_stats slm_pool_means category_disagreement \
         within_response_bias four_cell_decomposition bradley_terry_ranking \
         finding1_leaderboard h2h_results ranking_settled make_appendices \
         make_appendix_modelids; do
  echo "   -> scripts/$s.py"
  "$PY" "scripts/$s.py" >/dev/null
done

echo "== 2/3  Regenerate figures =="
# Figure 1 is computed directly from raw (make_finding1.py); Figures 2-4 from the
# just-regenerated caches. make_finding1.py is the SOLE Figure 1 generator.
for s in make_finding1 make_fig_refusal make_fig_disagreement make_fig_bias; do
  echo "   -> scripts/$s.py"
  "$PY" "scripts/$s.py" >/dev/null
done

echo "== 3/3  Build both PDFs =="
"$PY" scripts/make_nonanon.py            # regenerate non-anon .tex from anon (body verbatim)
tectonic -X compile multivac_paper.tex          2>/dev/null || tectonic multivac_paper.tex
tectonic -X compile multivac_paper_nonanon.tex  2>/dev/null || tectonic multivac_paper_nonanon.tex

echo "Done: multivac_paper.pdf and multivac_paper_nonanon.pdf regenerated from raw."
