# Parse failures are systematic, not random (answers Sander #4)

**Date:** 2026-07-13 (corrected) · **Script:** `scripts/parse_failure_analysis.py` · **Data:** frozen 286-eval set (no API calls)
Every number below is emitted by that script (`paper_tables/parse_failure.json`) and was re-verified on a
fresh run. This revision corrects the category χ² and rates, which were stale (pre-fix) in the prior version.

## Classification of all 27,540 slots

| bucket | n | % | nature |
|---|---:|---:|---|
| valid (parsed, `error is None`) | 23,356 | 84.8% | parsed fine — includes 1,104 valid 0-scores (see `COUNT_RECONCILIATION_FINDINGS.md`) |
| self_excluded | 2,781 | 10.1% | **intentional** diagonal — not a failure |
| parse_failure | 1,192 | 4.3% | judge produced unparseable output (930 malformed JSON + 260 empty + 2 score>10) |
| api_error | 211 | 0.8% | OpenRouter 4xx/5xx, DNS, disconnect — infrastructure |

Model-attributable parse-failure rate (of attempted non-self, ex-API) = **1,192 / 24,548 = 4.9%**.

## Finding: failures concentrate massively

**By judge model** — **χ²(49) = 7,121.6, p ≈ 0.** Overall rate 4.9%, but:

| judge | fail / attempted | rate |
|---|---:|---:|
| olmo_think | 77 / 90 | **85.6%** |
| kimi_k25 | 99 / 125 | **79.2%** |
| qwen35_9b | 45 / 77 | 58.4% |
| **gemini_3_pro** | **251 / 448** | **56.0%** |
| qwen35_35b_a3b | 34 / 76 | 44.7% |
| gpt_oss_legal | 27 / 90 | 30.0% |
| qwen35_27b | 16 / 76 | 21.1% |
| glm_4_7 | 31 / 179 | 17.3% |
| qwen35_397b_a17b | 13 / 76 | 17.1% |
| gpt_oss_120b | 270 / 2112 | 12.8% |
| … | | |
| deepseek_v4 / gemini_25_flash / seed_16_flash | 0 | 0.0% |

**By category** — **χ²(8) = 673.1, p = 4.32e-140.** Overall 4.9%:

| category | fail / n | rate |
|---|---:|---:|
| qwen | 117 / 609 | 19.2% |
| edge_cases | 108 / 899 | 12.0% |
| slm | 116 / 1240 | 9.4% |
| reasoning | 287 / 4015 | 7.1% |
| code | 232 / 4447 | 5.2% |
| analysis | 182 / 4408 | 4.1% |
| meta_alignment | 72 / 3882 | 1.9% |
| communication | 68 / 4320 | 1.6% |
| minimax | 10 / 728 | 1.4% |

## Why this matters for the paper

1. **The valid-judgment pool is a biased sample of judges.** Models that cannot reliably emit the JSON
   judging schema (olmo, kimi, small Qwens, `gpt_oss`) are systematically dropped; compliant models
   (DeepSeek, Gemini Flash, Seed) are over-represented. Format compliance correlates with family and size,
   so it confounds the family-bias and ranking analyses.
2. **`gemini_3_pro` is the alarming case:** a frontier judge with 448 attempts fails **56%** of the time.
   Google's surviving judgments are carried mostly by `gemini_25_flash` (0% fail), so "Google as judge" is
   effectively "Gemini Flash as judge."
3. **Category coupling:** highest-failure categories (qwen pool, edge_cases, slm) are the small-model /
   adversarial pools — failures cluster exactly where data is thinnest.

## Fixes to state in the paper

- Report failure rate **excluding self-exclusions** (≈5%), never the conflated 19.2% (that figure is the
  mislabelled 5,286 complement; see `COUNT_RECONCILIATION_FINDINGS.md`).
- Add this per-judge / per-category breakdown as a data-quality table.
- Robustness check (`robustness_check.py`) drops the >30% judges and confirms the surviving family-bias and
  ranking findings are stable — see `ROBUSTNESS_FINDINGS.md`.

Caveat: this rate reflects **recorded** judgments; judge calls that failed hard and were never written as
rows are not visible here, so true failure ≥ this.

Reproduce: `./.venv/bin/python scripts/parse_failure_analysis.py`
