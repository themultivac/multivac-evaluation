# Multivac paper: corrected sections (v2)

Rebuilt on the verified four-cell decomposition and strict-within FE estimates with judge-clustered SEs. Replaces the abstract, §5.5, Table 1, Figure 4, and the Conclusion's second finding.

**Changes from v1:** real numbers throughout; Mistral corrected (it does not flip sign, it collapses toward zero); the estimand is now defined precisely, because A minus C and the FE estimate are different quantities; Qwen demoted out of the abstract.

> **Number provenance (verified 2026-07-13).** Every figure below is reproduced by a script in this repo and re-run this session: §5.5 / Table 1 by `within_response_bias.py`, `four_cell_decomposition.py`, `count_reconciliation.py` (one command: `reproduce_section_5_5.py`); Figure 4 by `make_figure4.py`; parse stats by `parse_failure_analysis.py`; finding 3 by `category_disagreement.py`; **Krippendorff α = 0.618 and the "top four indistinguishable" (p > 0.07) by `evaluation_framework/statistical_analysis.py`** (re-verified this session); per-judge leniency (§judges page) by `judge_leniency_stats.py`. No `[VERIFY]` markers remain.
> **Valid-judgment count (Task 1 resolved):** of 27,540 total judgment slots, **22,252** carry a usable in-range score (this is the successor to the previously published 22,254, which double-counted 2 pre-clamp score>10 rows); **23,356** parsed successfully (`error is None`, includes 1,104 valid zero-scores for refused responses); 2,781 self-excluded; 1,403 genuine judge failures. The abstract uses the usable-scored figure; §4.3 and the dataset cards must carry the full breakdown.

---

## Abstract (revised)

Single-judge evaluation of large language models introduces systematic bias. We propose the Blind Peer Matrix, a multi-judge methodology in which N frontier models both generate responses and evaluate each other's outputs in a fully blinded N x N matrix, with self-judgments excluded. We apply it across 286 evaluations spanning 198 unique questions in nine category pools, producing 22,252 valid judgments from 55 models across 11 vendor families.

Three findings stand out. First, no single model dominates across all categories: seven different models hold the top position across the nine pools (by distinct model, both naive and Bradley-Terry ranking; `bradley_terry_ranking.py`), and the top four are statistically indistinguishable in aggregate — the top-ranked model is not significantly separated from ranks two through four (bootstrap p = 0.27, 0.073, 0.071) but is from rank five (p = 0.027; `evaluation_framework/statistical_analysis.py`) — contradicting aggregate leaderboard rankings.

Second, and centrally, we show that the standard estimator for same-vendor judge bias is confounded. Estimating bias as the difference between a judge family's mean score to its own siblings and to other vendors conflates three distinct quantities: judge favoritism, respondent quality, and judge leniency. We decompose all eight testable families algebraically and re-estimate with a within-response fixed-effects model with judge-clustered standard errors. Only two families show robust same-vendor favoritism (Anthropic +0.41, MiniMax +0.40); a third (Qwen +0.56) is significant but identified from only 22 responses and is not relied upon. No family shows significant negative bias. The naive estimator errs in both directions: it reports a strong negative bias for Mistral (-1.02) that is an artifact of Mistral judges' leniency toward all respondents, a strong negative bias for Google (-0.59) that is an artifact of Google's weaker responses, and a strong positive bias for xAI (+0.75) that does not survive controls.

Third, judge disagreement is category-dependent: code evaluation produces just over double the inter-judge disagreement of meta-alignment tasks (within-response score SD 1.269 vs 0.632, ratio 2.01x; `category_disagreement.py`).

We release the complete evaluation dataset, an open-source evaluation framework, all question prompts, and a one-command reproduction pipeline under MIT license.

---

## 5.5 Same-Vendor Rating Bias (rewritten)

### 5.5.1 The naive estimator is confounded

The standard approach estimates same-vendor bias as the difference between the mean score a judge family gives its own siblings and the mean it gives other vendors. Writing the four relevant cells as

- A: same-vendor judge scoring a same-vendor respondent
- B: same-vendor judge scoring an other-vendor respondent
- C: other-vendor judge scoring a same-vendor respondent
- D: other-vendor judge scoring an other-vendor respondent

the naive estimate is A minus B, which decomposes exactly as

    A - B = (A - C) + (C - D) - (B - D)

Here (C minus D) is a **respondent-quality** term: how good the family's answers are, as assessed by neutral judges. (B minus D) is a **judge-leniency** term: how generous the family's judges are toward everyone. Neither has anything to do with favoritism. We verify this identity holds to 1e-9 across all eight families and confirm our A minus B values reproduce the published naive estimates exactly.

The naive estimator therefore reports favoritism contaminated by two nuisance terms, and in our data both contaminate materially, in opposite directions.

**Defining the estimand.** The residual term (A minus C) is the same response scored by a sibling judge versus a neutral judge. It is closer to favoritism but is not yet clean, because the sibling and neutral judge pools differ in baseline strictness. Our reported estimate is the coefficient on the same-vendor indicator in a within-response fixed-effects model that absorbs the response and adjusts for judge-level baseline strictness, with standard errors clustered by judge. This isolates the judge's differential treatment of a sibling's output, holding both the output and judge strictness fixed. It is the quantity the literature intends to measure and does not.

The distinction matters. For OpenAI the raw A minus C gap is -1.136, apparently a large aversion to its own siblings, but OpenAI judges are the strictest in the pool (leniency -1.052), so the corrected estimate is -0.137 and not significant.

### 5.5.2 Two artifacts, two mechanisms

**Google: a respondent-quality artifact.** Naive estimate -0.593. Neutral judges score Google's responses 0.938 below other responses (C minus D), so Google judges score Google responses lower simply because those responses are weaker. Corrected: +0.209, not significant under judge-clustered SEs (p = 0.058). The naive figure measures response quality, not bias.

**Mistral: a judge-leniency artifact.** Naive estimate -1.017, the largest absolute value in the published table. Mistral judges score all respondents 1.094 above the neutral baseline (B minus D), and Mistral's own responses are above average (C minus D = +0.527). Corrected: -0.164 (p = 0.345), indistinguishable from zero. The apparent negative bias does not reverse under controls, it collapses toward zero: the family's judges are simply generous to everyone, which inflates B and drags A minus B negative.

**xAI: a false positive.** Naive +0.745, corrected -0.095 (p = 0.549). The naive figure is driven by xAI's strong responses (C minus D = +0.414), not by favoritism.

These are mechanistically distinct confounds producing similar superficial signatures. Any same-vendor bias estimate computed as a raw score gap is vulnerable to all of them.

### 5.5.3 Corrected estimates

Table 1 reports the naive estimate, the three decomposition terms, the corrected estimate, and the identifying sample for all eight testable families.

Two families show robust same-vendor favoritism: Anthropic (+0.406, p < 0.001, 482 identifying responses) and MiniMax (+0.397, p < 0.001, 50). Qwen (+0.557, p = 0.002) is significant but rests on 22 identifying responses drawn from a focused Qwen-family batch pool in which same-vendor membership is nearly collinear with pool composition, and its raw A minus C gap is negative, meaning the estimate is driven entirely by the leniency adjustment. We report it but do not rely on it. Google, OpenAI, xAI, Meta, and Mistral show no significant effect.

The headline correction: the naive estimator called five families positive and three negative. Under controls, two are robustly positive, one is fragile, and none are negative.

### 5.5.4 Robustness and power

Five judges fail to produce parseable output more than 30% of the time. Excluding them and re-fitting the fixed-effects specification leaves every family verdict unchanged. An earlier random-intercept specification was insensitive to removal of its own identifying data, which makes robustness checks on that estimator uninformative by construction; all robustness results reported here use the fixed-effects estimator.

**Power.** xAI (59 same-vendor judgments), Meta (26), Mistral (25), and Qwen (22 identifying responses) have small samples. Their null results should be read as an absence of demonstrated bias, not as demonstrated absence of bias. Meta's corrected estimate (+0.195, p = 0.108) is positive and directionally suggestive but underpowered. Larger samples for these families are the clearest next step.

---

## Table 1 (replaces the naive bias table)

Composite score units on the 0 to 10 scale. `Naive (A-B)` is the previously published naive estimate.

| Family | A | B | C | D | Naive (A-B) | A-C | RespQ (C-D) | Leniency (B-D) | **Corrected (FE)** | p (judge-clustered) | n ident |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Anthropic | 8.803 | 8.187 | 8.624 | 8.437 | +0.616 | +0.179 | +0.187 | -0.250 | **+0.406** | < 0.001 | 482 |
| MiniMax | 8.488 | 8.175 | 7.787 | 8.491 | +0.314 | +0.701 | -0.704 | -0.316 | **+0.397** | < 0.001 | 50 |
| Qwen | 9.007 | 8.095 | 9.268 | 8.420 | +0.913 | -0.261 | +0.848 | -0.325 | **+0.557** | 0.002 | 22 |
| Google | 8.404 | 8.997 | 7.581 | 8.519 | -0.593 | +0.823 | -0.938 | +0.478 | +0.209 | 0.058 | 394 |
| Meta | 8.440 | 9.121 | 7.978 | 8.433 | -0.681 | +0.463 | -0.456 | +0.688 | +0.195 | 0.108 | 26 |
| OpenAI | 7.737 | 7.508 | 8.873 | 8.560 | +0.229 | -1.136 | +0.313 | -1.052 | -0.137 | 0.307 | 385 |
| xAI | 9.149 | 8.405 | 8.802 | 8.388 | +0.745 | +0.347 | +0.414 | +0.017 | -0.095 | 0.549 | 59 |
| Mistral | 8.470 | 9.487 | 8.921 | 8.393 | -1.017 | -0.451 | +0.527 | +1.094 | -0.164 | 0.345 | 25 |

Bold = significant under FE with judge-clustered SEs and Bonferroni correction. Qwen is significant but fragile (see §5.5.3).

**Figure 4 (replace).** Drop the naive forest plot. Use a paired plot: naive estimate and corrected estimate per family, connected (generated by `make_figure4.py` from the JSON; `paper_tables/figure4_naive_vs_corrected.png/.pdf`). **Four** families cross zero under correction — the two large-magnitude flips (Google -0.593 to +0.209; xAI +0.745 to -0.095) plus two smaller ones (OpenAI +0.229 to -0.137; Meta -0.681 to +0.195). Annotate all four as sign flips. Mistral (-1.017 to -0.164) is a **collapse toward zero**, not a flip: it does not cross the axis. Do not label Mistral as a sign flip.

---

## Conclusion (revised second finding)

Second, we show that the standard estimator for same-vendor judge bias is confounded by respondent quality and judge leniency, and that correcting for both substantially changes the conclusions. Under a within-response fixed-effects specification with judge-clustered standard errors, only two of eight vendor families show robust same-vendor favoritism (Anthropic +0.41, MiniMax +0.40), a third is significant but fragile (Qwen +0.56, identified from 22 responses), and no family shows significant negative bias. The naive estimator misreports in both directions: an apparent -1.02 for Mistral is an artifact of that family's judges being lenient toward all respondents, an apparent -0.59 for Google is an artifact of Google's weaker responses, and an apparent +0.75 for xAI does not survive controls. We provide the algebraic decomposition, the corrected estimates, and a one-command reproduction pipeline.

---

## §4.4 Data validity and the filter chain (new / rewrite)

Every reported number derives from an explicit, reproducible filter over the 27,540 raw
judgment slots (`scripts/count_reconciliation.py`, run against the frozen dataset):

```
27,540  total judgment slots            (= 286 evals' N×N matrices = Σ meta_analysis.total_judgments)
 −2,781  intentional self-exclusions     (matrix diagonal: judge == respondent)
========
24,759  attempted cross-model judgments
 −1,403  judge failures                  (930 malformed/unparseable JSON + 260 empty no-score
                                          + 211 API/infra errors + 2 Phase-1 score>10 clamps)
========
23,356  successfully parsed judgments    (error field is null)
 −1,104  valid zero-scores               (judge parsed fine and scored a refused/empty response 0;
                                          excluded from bias analysis as uninformative, not a failure)
========
22,252  usable scored judgments          (the "valid" set; = the previously published 22,254 minus
                                          the 2 score>10 rows that meta_analysis counted pre-clamp)
 −  839  judgments with an unmapped vendor on either side
========
21,413  same-vendor analysis set         (§5.5; non-self, both vendor families known, score > 0)
```

| Bucket | n | % of 27,540 |
|---|---:|---:|
| Usable scored (analysis input) | 22,252 | 80.8 |
| Valid zero-scores (refused/empty response) | 1,104 | 4.0 |
| Self-excluded (intentional) | 2,781 | 10.1 |
| Judge failures (parse/API) | 1,403 | 5.1 |
| **Total** | **27,540** | **100** |

This supersedes the earlier description of "22,254 valid judgments (5,286 self-excluded)": the
5,286 was the complement 27,540 − 22,254 and conflated 2,781 self-exclusions with 1,403 failures
and 1,104 valid zero-scores. The true self-exclusion count is **2,781**. Genuine judge-failure
rate is 1,403 / 24,759 = **5.7%** of attempted cross-model judgments (and 4.9% by the
model-attributable parse-only measure of §4.3).

## Other required edits elsewhere in the paper

- **§1.3 Contribution 2.** Currently claims "statistically significant bias in every vendor family with sufficient sample size." Now false. Rewrite as the confound-and-correction contribution.
- **§3.3 Blinding.** Currently asserts that "any non-zero family bias under this protocol is evidence that stylistic identification is occurring." False: non-zero naive bias arises from respondent quality or judge leniency with no identification at all. Rewrite so only the corrected favoritism term supports that inference.
- **§7.2 Implications for AI Safety.** Currently claims a model evaluated by siblings "inherits roughly a one-point composite-score lift." Corrected maximum is about +0.4 (Anthropic +0.406). Rescale.
- **§4.3 / §4.4 parse failures.** Update to verified values: chi-square(8) = 673.1, p = 4.32e-140; rates slm 9.4%, reasoning 7.1%, communication 1.6%.
- **Abstract, §1.3, §4.3, §5, dataset cards.** Replace 22,254 with the resolved breakdown (22,252 usable-scored / 23,356 parsed; see provenance note above). DATASHEET.md, README.md, dataset_stats.json, analyze_outputs.py, and setup_repo_metadata.sh all still carry the old figure and the false "5,286 self-excluded" label (real self-exclusions = 2,781).
- **Positioning.** Cut the EU AI Act market framing from the abstract and §7.4. It reads as commercial and adds nothing for a TMLR reviewer.
