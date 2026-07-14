# Robustness: corrected findings survive dropping the worst judges

**Date:** 2026-07-13 (corrected) · **Script:** `scripts/robustness_check.py` · **Data:** frozen 286-eval set (no API calls)
Every number below is emitted by that script. This revision runs against the **strict-within FE**
estimator with **judge-clustered** SEs, not the random-intercept one.

## Why this revision

The earlier robustness check re-fit the **random-intercept (RE)** model after dropping judges. That was
uninformative by construction: the RE estimator is insensitive to data removal (dropping 64 of 434 Qwen
sibling judgments moved its coefficient by 0.0000). We now re-run the **strict-within FE** estimator —
which *is* identified from the sibling-vs-neutral contrasts — with judge-clustered significance.

We drop every judge with parse-failure rate > 30% (n ≥ 20): **olmo_think 86%, kimi_k25 79%, qwen35_9b 58%,
gemini_3_pro 56%, qwen35_35b_a3b 45%** (5 judges).

## A. Strict-within FE same-family bias (judge-clustered) — all verdicts stable

| family | FE full | p (full) | FE dropped | p (dropped) | Δ | verdict |
|---|---:|---:|---:|---:|---:|---|
| qwen | +0.557 | 0.002 **PASS** | +0.557 | 0.002 **PASS** | +0.000 | stable |
| anthropic | +0.406 | 0.000 **PASS** | +0.408 | 0.000 **PASS** | +0.002 | stable |
| minimax | +0.397 | 0.000 **PASS** | +0.398 | 0.000 **PASS** | +0.000 | stable |
| google | +0.209 | 0.058 ns | +0.220 | 0.066 ns | +0.010 | stable |
| meta | +0.195 | 0.108 ns | +0.195 | 0.109 ns | −0.000 | stable |
| xai | −0.095 | 0.549 ns | −0.083 | 0.606 ns | +0.012 | stable |
| openai | −0.137 | 0.307 ns | −0.138 | 0.300 ns | −0.002 | stable |
| mistral | −0.164 | 0.345 ns | −0.163 | 0.345 ns | +0.000 | stable |

Bonferroni α = 0.00625 on the judge-clustered p. Every coefficient moves by ≤0.012 and **every
significance verdict is preserved**: the three significant families (anthropic, minimax, qwen) stay
significant; google and openai stay non-significant. Notably, dropping `gemini_3_pro` (a Google judge
failing 56% of the time) does not rescue Google's effect (+0.209 → +0.220, p 0.058 → 0.066, still ns).

## B. Bradley-Terry per-category winners — 8 of 9 stable

| category | BT winner (full) | BT winner (dropped) | verdict |
|---|---|---|---|
| analysis / code / reasoning | gpt_5_4 | gpt_5_4 | stable |
| communication | mistral_small_creative | mistral_small_creative | stable |
| edge_cases | gemini_3_flash | gemini_3_flash | stable |
| meta_alignment | claude_opus_46 | claude_opus_46 | stable |
| minimax | judge_gpt54 | judge_gpt54 | stable |
| slm | qwen3_8b | qwen3_8b | stable |
| **qwen** | qwen35_122b_a10b | qwen35_397b_a17b | CHANGED |

All 5 well-sampled frontier categories are stable. The only flip is the small **qwen** pool — expected,
since two dropped judges live in it and its top two models were near-tied.

## Bottom line for the paper

The systematic parse failures are real (see `PARSE_FAILURE_FINDINGS.md`) but do **not** drive the
corrected conclusions: dropping the highest-failing judges leaves every same-family verdict unchanged
(|Δ| ≤ 0.012) and 8 of 9 category winners identical, **now measured with the sensitive strict-within
estimator rather than the rigid random-intercept one.**

Reproduce: `./.venv/bin/python scripts/robustness_check.py`
