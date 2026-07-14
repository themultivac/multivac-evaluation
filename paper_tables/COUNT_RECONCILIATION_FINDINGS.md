# Judgment-count reconciliation: 27,540 / 22,254 / 23,356

**Date:** 2026-07-13 · **Script:** `scripts/count_reconciliation.py` · **Data:** frozen 286-eval set (no API calls)
Every number below is emitted by that script (`paper_tables/count_reconciliation.json`).

## The conflict

- Paper (`dataset_stats.json`, `DATASHEET.md`, `README.md`): **27,540 total, 22,254 valid, "5,286 self-excluded."**
- `parse_failure_analysis.py`: **23,356 valid.**

Both "valid" numbers are real; they use different definitions. The **"5,286 self-excluded" label is false.**

## Where each number comes from (all reproduced exactly)

| quantity | value | exact source |
|---|---:|---|
| total slots | 27,540 | recount = `Σ meta_analysis.total_judgments` |
| paper "valid" | 22,254 | `Σ meta_analysis.valid_judgments` (reproduces exactly) |
| script "valid" | 23,356 | judgments with `error is None` |
| gap | 1,104 | parsed fine (`error=None`) but `weighted_score == 0` |

The paper's 22,254 = judgments with a usable positive score. Recounting `error is None AND ws>0`
gives **22,252**; the +2 is the two `score_over_10` Phase-1 clamps that `meta` counts as valid before
clamping. So the paper's 22,254 is the **usable-scored** count.

## The 1,104 gap is not failures — it is valid zero-scores

All 1,104 judgments in the gap parsed correctly and **deliberately scored a refused/empty response 0**;
1,100 carry a justification such as *"No response was provided to evaluate."* They are valid judge
outputs about failed *responses* — excluded from bias/ranking analysis only because a 0-for-refusal is
uninformative about judge behaviour. They are neither self-exclusions nor parse failures.

## Full breakdown of the 27,540 slots

| bucket | n | % |
|---|---:|---:|
| valid, scored > 0 (analysis input) | 22,252 | 80.8% |
| valid, scored 0 (respondent refused/empty) | 1,104 | 4.0% |
| **— parsed judge outputs (`error is None`)** | **23,356** | **84.8%** |
| self-excluded (intentional diagonal) | 2,781 | 10.1% |
| parse failures (malformed / no JSON) | 930 | 3.4% |
| empty-error silent no-score | 260 | 0.9% |
| API / infra errors | 211 | 0.8% |
| score>10 clamp (Phase 1) | 2 | 0.0% |
| **total** | **27,540** | |

Genuine judge failures = 930 + 260 + 211 + 2 = **1,403 (5.1%)**. Real self-exclusions = **2,781 (10.1%)**.
Within-response analysis input (score>0, non-self, both families in the map) = **21,413**.

## Verdicts

1. **27,540 total — correct.**
2. **22,254 valid — correct and reproducible**, defined as usable positive scores (= 22,252 + 2 pre-clamp).
   The script's 23,356 is also correct, defined as parse-success (it additionally counts the 1,104 valid
   zero-scores). Per session decision, **docs report both**: 23,356 parsed / 22,252 usable-scored.
3. **"5,286 self-excluded" — FALSE.** 5,286 = 27,540 − 22,254 conflates **2,781 self-exclusions +
   1,403 genuine failures + 1,104 valid zero-scores.** Real self-exclusions are 2,781. Correct wherever
   it appears: `dataset_stats.json`, `DATASHEET.md`, `README.md`, `setup_repo_metadata.sh`, `analyze_outputs.py`.
4. **The April-3-2026 freeze is not a factor.** Eval timestamps span 2026-02-07 → 2026-04-03, all within
   the freeze; the +2 gap between 22,252 and 22,254 is fully explained by the two Phase-1 score>10 clamps.
5. This resolves the previously-"unverifiable" 19.2%: 5,286/27,540 = 19.2% is exactly the mislabelled
   complement above, and should be decomposed, never cited as one "invalid" number.

Reproduce: `./.venv/bin/python scripts/count_reconciliation.py`
