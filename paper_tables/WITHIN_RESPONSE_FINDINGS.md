# Within-response same-family bias — strict-within FE, judge-clustered

**Date:** 2026-07-13 (corrected) · **Script:** `scripts/within_response_bias.py` · **Data:** frozen 286-eval set (no API calls)
Every number below is emitted by that script (`paper_tables/within_response_bias.json`). This revision
**supersedes** the earlier random-intercept-only writeup, which overstated significance.

## What changed and why

The earlier version fit a random-**intercept** model and reported google (+0.21) and openai (−0.14) as
significant ("PASS Bonferroni"). Two problems, both fixed here:

1. **The random-intercept (RE) estimator partially pools and is insensitive to its own identifying data.**
   Verified: dropping 64 of 434 Qwen sibling judgments moved the RE coefficient by 0.0000. So we add a
   **strict-within fixed-effects (FE)** estimator — the response is absorbed as a fixed effect, so the
   sibling coefficient is identified *only* from responses judged by both a sibling and a neutral judge.
2. **SEs were clustered on response only.** But sibling-status is assigned at the **judge** level, and each
   family's effect rests on just 2–8 sibling judge models. We now cluster SEs by `judge_key` (46 clusters).

## Result (all 8 families)

| family | naive (A−C) | RE | **FE (strict within)** | SE (judge-clust.) | **p (judge-clust.)** | Bonf | n_same | n_other | n_ident |
|---|---:|---:|---:|---:|---:|:--:|---:|---:|---:|
| qwen | −0.261 | +0.662 | +0.557 | 0.184 | 0.0025 | **PASS** | 434 | 107 | 22 |
| anthropic | +0.179 | +0.406 | +0.406 | 0.045 | 0.0000 | **PASS** | 482 | 3750 | 482 |
| minimax | +0.701 | +0.544 | +0.397 | 0.100 | 0.0001 | **PASS** | 245 | 1049 | 50 |
| google | +0.823 | +0.205 | +0.209 | 0.111 | 0.058 | fail | 426 | 3589 | 394 |
| meta | +0.463 | +0.188 | +0.195 | 0.122 | 0.108 | fail | 26 | 134 | 26 |
| xai | +0.347 | −0.094 | −0.095 | 0.158 | 0.549 | fail | 59 | 2189 | 59 |
| openai | −1.136 | −0.137 | −0.137 | 0.134 | 0.307 | fail | 385 | 3566 | 385 |
| mistral | −0.451 | −0.239 | −0.164 | 0.173 | 0.345 | fail | 25 | 545 | 25 |

Bonferroni α = 0.05/8 = 0.00625, applied to the judge-clustered p. "naive" here is the respondent-fixed
raw gap **A−C** (sibling vs neutral judge on this family's responses); the paper's published judge-fixed
bias (A−B) and its decomposition are in `FOUR_CELL_DECOMPOSITION_FINDINGS.md`.

## What holds and what does not

**Statistically defensible same-family favouritism (survives strict-within FE + judge clustering + Bonferroni):**
- **anthropic +0.406** (p < 0.001, 482 identifying responses) — robust and well-identified.
- **minimax +0.397** (p < 0.001, 50 identifying responses) — robust.
- **qwen +0.557** (p = 0.002, **only 22 identifying responses**) — significant but **uncertain**: the RE
  (+0.662) and FE (+0.557) differ, the raw A−C gap is *negative* (−0.261), and Qwen is near-siloed
  (only 107 neutral-judge observations). Report as significant-but-fragile; see the four-cell doc.

**Does NOT hold (corrected from the earlier writeup):**
- **google +0.209 — NOT significant** under judge clustering (p = 0.058). Earlier reported as PASS. The
  published −0.593 is a respondent-quality artifact, not favouritism (four-cell doc).
- **openai −0.137 — NOT significant** (p = 0.307). The earlier "small significant NEGATIVE self-critical
  effect" does not survive judge clustering; it was an artifact of OpenAI judges' general harshness.
- meta, xai, mistral — not significant (as before).

**RE ≠ FE where identification is thin.** The RE and strict-within FE agree for well-identified families
(anthropic, google, openai: |Δ| ≤ 0.004) but diverge for qwen (0.662 vs 0.557) and minimax (0.544 vs
0.397). So the earlier claim that the RE estimate is *"identified only from responses judged by both a
sibling and a non-sibling"* is **false for qwen/minimax** — only the FE estimator has that property.

## Bottom line for the paper

Same-family favouritism, net of answer quality and judge leniency and with honest (judge-clustered)
inference, is defensible for **anthropic and minimax**, and significant-but-uncertain for **qwen**. Do
**not** report google or openai as significant same-family effects.

Reproduce: `./.venv/bin/python scripts/within_response_bias.py`
