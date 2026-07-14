# What the published same-family bias actually measures: a four-cell decomposition

**Date:** 2026-07-13 · **Script:** `scripts/four_cell_decomposition.py` · **Data:** frozen 286-eval set (no API calls)
Every number below is emitted by that script (`paper_tables/four_cell_decomposition.json`); the
strict-within FE column comes from `within_response_bias.py`.

## The problem

The paper's headline same-family bias is the **judge-fixed gap A − B**: how much higher family F's
judges score F's own responses (A) than F's judges score everyone else (B). This conflates two
different things — genuine favouritism, and the fact that F's *responses* may simply be better or
worse than the pool average. Split each family into four cells (self-judgments excluded):

- **A** = F-judge → F-respondent
- **B** = F-judge → other-respondent
- **C** = neutral-judge → F-respondent
- **D** = neutral-judge → other-respondent

Exact accounting identity (verified in code to 1e-9):

```
A − B  =  (A − C)      +   (C − D)        −   (B − D)
          favouritism      respondent          F-judges' leniency
          (same responses)  quality             toward non-siblings
                            (neutral judges)
```

## The four cells (all 8 families)

| family | A (F→F) | B (F→o) | C (o→F) | D (o→o) | nA | nC |
|---|---:|---:|---:|---:|---:|---:|
| anthropic | 8.803 | 8.187 | 8.624 | 8.437 | 482 | 3750 |
| openai | 7.737 | 7.508 | 8.873 | 8.560 | 385 | 3566 |
| google | 8.404 | 8.997 | 7.581 | 8.519 | 426 | 3589 |
| xai | 9.149 | 8.405 | 8.802 | 8.388 | 59 | 2189 |
| qwen | 9.007 | 8.095 | 9.268 | 8.420 | 434 | **107** |
| minimax | 8.488 | 8.175 | 7.787 | 8.491 | 245 | 1049 |
| mistral | 8.470 | 9.487 | 8.921 | 8.393 | 25 | 545 |
| meta | 8.440 | 9.121 | 7.978 | 8.433 | 26 | 134 |

## Decomposition of the published bias

`published = A−B` reproduces ADR Appendix A **exactly** for all 8 families. `FE net` is the
strict-within favouritism (response absorbed as fixed effect, judge leniency controlled,
**judge-clustered** p). `n_ident` = responses judged by both a sibling and a neutral judge.

| family | published (A−B) | favouritism (A−C) | respondent-quality (C−D) | leniency (B−D) | **FE net** | p (judge-clust.) | n_ident | dominant driver of A−B |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| mistral | −1.017 | −0.451 | **+0.527** | +1.094 | −0.164 | 0.345 | 25 | **leniency** |
| meta | −0.681 | +0.463 | −0.456 | +0.688 | +0.195 | 0.108 | 26 | leniency |
| google | −0.593 | +0.823 | **−0.938** | +0.478 | +0.209 | 0.058 | 394 | **respondent-quality** |
| openai | +0.229 | −1.136 | +0.313 | −1.052 | −0.137 | 0.307 | 385 | favouritism (self-critical, cancels) |
| minimax | +0.314 | +0.701 | −0.704 | −0.316 | **+0.397** | **0.000** | 50 | respondent-quality |
| anthropic | +0.616 | +0.179 | +0.187 | −0.250 | **+0.406** | **0.000** | 482 | leniency |
| xai | +0.745 | +0.347 | +0.414 | +0.017 | −0.095 | 0.549 | 59 | respondent-quality |
| qwen | +0.913 | −0.261 | +0.848 | −0.325 | +0.557 | 0.002 | **22** | respondent-quality |

## What is judge favouritism versus respondent quality

**Only three families show statistically significant same-family favouritism** under the strict-within
FE estimator with judge-clustered SEs (Bonferroni α = 0.00625):

- **anthropic +0.406** (p < 0.001, 482 identifying responses) — the clean case. Real, robust, well-identified.
- **minimax +0.397** (p < 0.001, 50 identifying responses) — real, despite minimax's responses being *below* average (C−D = −0.704).
- **qwen +0.557** (p = 0.002, **only 22 identifying responses**) — significant on the FE test but **uncertain** (see caveat below).

The published bias is driven by *something other than favouritism* in most families:

- **google −0.593 is a respondent-quality artifact.** Google's responses are genuinely weaker — neutral
  judges score them **−0.938** below the pool (C−D). The favouritism component (FE net +0.209) is **not
  significant** (p = 0.058). The −0.593 is not unfavourable judging.
- **qwen +0.913 is largely respondent quality too.** Qwen responses are strong (C−D = +0.848), and the
  *raw* favouritism (A−C) is actually **negative** (−0.261).
- **openai +0.229 is a near-cancellation.** OpenAI judges score OpenAI responses far *lower* than neutral
  judges do (A−C = −1.136) but are equally harsh to everyone (B−D = −1.052); net FE favouritism is
  −0.137, **not significant** (p = 0.307). No real self-criticism once leniency is controlled.

## Is Mistral's −1.017 the same artifact as Google's? No — different mechanism.

Explicitly tested. Google's −0.593 is **respondent quality** (C−D = −0.938). Mistral's −1.017 is a
**judge-leniency** artifact: Mistral is the most lenient judge in the dataset, and it lavishes
non-siblings especially — B−D = **+1.094** (Mistral judges score other families 1.09 above neutral
judges). Meanwhile Mistral's own responses are **above** average (C−D = +0.527, i.e. C = 8.921 > D =
8.393), the opposite of Google. So −1.017 reflects Mistral over-scoring *everyone else*, not
disfavouring itself.

**Estimability:** Mistral has n_same = 25 and **n_ident = 25** identifying responses — it *is* estimable
under the strict-within FE model, giving FE net = **−0.164, p = 0.345 (not significant)**. So Mistral
shows no significant same-family effect in either direction; the published −1.017 is entirely an
artifact of the naive judge-fixed framing. (25 identifying responses is thin, so power is low — this is
a null with wide error, not a confident zero.)

## Caveat on qwen (must state in the paper)

Qwen's FE favouritism (+0.557, p = 0.002) rests on **only 22 identifying responses**, and the raw
respondent-fixed gap (A−C = −0.261) has the **opposite sign**. This is because Qwen operates in a
near-siloed evaluation pool: only **107** judgments come from neutral judges scoring Qwen responses
(nC = 107, vs 3589 for Google). The FE and the raw gap disagree because they weight a small, possibly
unrepresentative subset differently. **Qwen's favouritism should be reported as significant-but-uncertain**,
explicitly tied to the pool-disconnection limitation documented in `BRADLEY_TERRY_FINDINGS.md`.

## One-line summary for the paper

Of eight families, **same-family favouritism is statistically defensible for anthropic and minimax
(and, with caveats, qwen)**; the large published negatives for Google and Mistral are artifacts of
respondent quality and judge leniency respectively, not unfavourable judging.

Reproduce: `./.venv/bin/python scripts/four_cell_decomposition.py`
