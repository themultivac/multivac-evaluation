#!/usr/bin/env python3
"""
Within-response same-family bias (mixed-effects control).

Answers the decisive peer-review objections (Sander Land #1 and #2):

  #2  The naive family-bias headline averages over judges WITHOUT controlling
      for the quality of the answer being judged. If same-family judges happen
      to score genuinely-better answers, the naive `mean(same) - mean(other)`
      overstates bias. We must hold the RESPONSE fixed.

  #1  Self-exclusion only removes the diagonal; sibling-on-sibling judgments
      remain, and that is where the bias lives. This model measures exactly
      that sibling effect, net of answer quality.

Method
------
Each "response" is one model's answer to one question, identified by
    response_id = evaluation_id :: respondent_key
Multiple judges score the SAME response. We fit ONE crossed model over all data:

    weighted_score ~ C(respondent_family)          # each family's baseline quality
                   + C(judge_key)                  # each judge's general leniency  <- KEY
                   + Sum_F  same_F                  # per-family sibling effect
      with random intercept  (1 | response_id)     # answer quality / question difficulty

where `same_F` = 1 iff BOTH judge and respondent are family F, else 0.

Why both controls are load-bearing (each answers one reviewer objection):
  * (1 | response_id) holds the ANSWER fixed -> a family isn't credited for bias
    when its siblings simply wrote better answers.               (Sander #2)
  * C(judge_key) holds JUDGE LENIENCY fixed -> critical, because measured judge
    leniency spans 7.53 (OpenAI) to 9.44 (Mistral) on a 10-pt scale. Without it,
    a harsh family looks self-penalising and a lenient one self-favouring purely
    from baseline generosity, not sibling bias.                  (Sander #2 / IRT)

The `same_F` coefficient is thus the sibling effect NET of both answer quality and
judge generosity -- identified from responses judged by both a sibling and a
non-sibling. This is the number a reviewer will accept.

We report it beside the naive sibling-vs-nonsibling gap so the confound's size is
visible. No API calls -- pure re-analysis of the frozen 286-eval dataset.
"""

import json
import glob
import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

warnings.filterwarnings("ignore")  # MixedLM convergence chatter; we check status explicitly

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")

# Canonical family map -- IDENTICAL to evaluation_framework/statistical_analysis.py
FAMILIES = {
    "anthropic": ["claude_opus_46", "claude_sonnet_46", "claude_opus", "claude_sonnet", "judge_claude_sonnet"],
    "openai": ["gpt_5_4", "gpt_oss_120b", "gpt_codex", "gpt_oss_legal", "judge_gpt54"],
    "google": ["gemini_31_pro", "gemini_3_flash", "gemini_3_pro", "gemini_2_5_flash",
               "gemini_25_flash", "gemini_2_5_flash_lite", "gemma3_27b", "gemma_3n_4b"],
    "xai": ["grok_420", "grok_direct", "grok_4_1_fast", "grok_code_fast"],
    "deepseek": ["deepseek_v4", "deepseek_v3"],
    "qwen": ["qwen3_8b", "qwen3_32b", "qwen3_coder_next", "qwen35_9b", "qwen35_27b",
             "qwen35_35b_a3b", "qwen35_122b_a10b", "qwen35_397b_a17b"],
    "minimax": ["minimax_01", "minimax_m1", "minimax_m2", "minimax_m21", "minimax_m25", "minimax_m27"],
    "xiaomi": ["mimo_v2_flash"],
    "mistral": ["mistral_small_creative", "mistral_nemo", "devstral"],
    "bytedance": ["seed_16_flash", "seed_1_6_flash"],
    "meta": ["llama31_8b", "llama4_scout"],
}
MODEL_TO_FAMILY = {m: fam for fam, ms in FAMILIES.items() for m in ms}


def load_judgments():
    """Flat table of valid non-self judgments with known families on both sides."""
    rows = []
    for path in sorted(glob.glob(DATA_GLOB)):
        with open(os.path.join(path, "results.json")) as f:
            ev = json.load(f)
        eid = ev.get("evaluation_id") or os.path.basename(path)
        for j in ev.get("judgments", []):
            jk, rk, ws, err = j.get("judge_key"), j.get("respondent_key"), j.get("weighted_score"), j.get("error")
            if not (jk and rk and jk != rk and ws and ws > 0 and not err):
                continue
            jf, rf = MODEL_TO_FAMILY.get(jk, "unknown"), MODEL_TO_FAMILY.get(rk, "unknown")
            if jf == "unknown" or rf == "unknown":
                continue
            rows.append({
                "response_id": f"{eid}::{rk}",
                "question_id": ev.get("question_id") or eid,
                "judge_key": jk,
                "judge_family": jf,
                "respondent_family": rf,
                "weighted_score": float(ws),
            })
    return pd.DataFrame(rows)


def naive_and_counts(df, fam):
    """Raw sibling-vs-nonsibling gap for responses BY `fam`, and identifying counts."""
    sub = df[df["respondent_family"] == fam]
    same_mask = sub["judge_family"] == fam
    n_same, n_other = int(same_mask.sum()), int((~same_mask).sum())
    per_resp = sub.assign(same=same_mask.astype(int)).groupby("response_id")["same"].agg(["min", "max"])
    n_resp_both = int((per_resp["min"] != per_resp["max"]).sum())
    naive = sub.loc[same_mask, "weighted_score"].mean() - sub.loc[~same_mask, "weighted_score"].mean()
    return {"n_same": n_same, "n_other": n_other,
            "n_responses": int(len(per_resp)), "n_responses_identifying": n_resp_both,
            "naive_bias": float(naive)}


def fit_crossed(df):
    """Fit the crossed model and return (results, bonferroni_alpha). Importable so the
    robustness check can re-run it on a filtered judgment set with the exact same model."""
    df = df.copy()
    # Per-family sibling indicator columns: same_F = 1 iff judge AND respondent are F.
    fams_present = sorted(f for f in FAMILIES
                          if ((df["respondent_family"] == f) & (df["judge_family"] == f)).sum() >= 5)
    for f in fams_present:
        df[f"same_{f}"] = ((df["judge_family"] == f) & (df["respondent_family"] == f)).astype(int)

    # ONE crossed model: response random intercept + judge & respondent-family fixed
    # effects + all per-family sibling terms. Coefficient of same_F is the sibling
    # effect net of answer quality AND judge leniency.
    same_terms = " + ".join(f"same_{f}" for f in fams_present)
    formula = f"weighted_score ~ C(respondent_family) + C(judge_key) + {same_terms}"
    fit = smf.mixedlm(formula, df, groups=df["response_id"]).fit(reml=True, method="lbfgs")

    n_tests = len(fams_present)
    bonf = 0.05 / n_tests if n_tests else 0.05
    results = []
    for f in fams_present:
        nc = naive_and_counts(df, f)
        term = f"same_{f}"
        coef, se, p = float(fit.params[term]), float(fit.bse[term]), float(fit.pvalues[term])
        results.append({"family": f, **nc,
                        "within_bias": coef, "se": se,
                        "ci_lower": coef - 1.96 * se, "ci_upper": coef + 1.96 * se,
                        "p": p, "converged": bool(fit.converged)})
    return results, bonf


def fit_within_fe(df):
    """STRICT within-response fixed-effects estimator with JUDGE-clustered SEs.

    The RE model (fit_crossed) uses a random *intercept* per response, which partially
    pools and is insensitive to its own identifying data. This instead ABSORBS the response
    as a fixed effect (within transformation: demean every variable by response_id), so the
    same_F coefficient is identified ONLY from responses judged by both a sibling and a
    non-sibling. Judge fixed effects (dummies) remain to control leniency. SEs are clustered
    by judge_key -- the level at which sibling-status is assigned -- because the effect rests
    on a handful of sibling judge models, and response-clustered SEs understate that.

    Returns {family: {fe, se_judge, p_judge}}.
    """
    df = df.copy().reset_index(drop=True)
    fams = [f for f in FAMILIES
            if ((df["respondent_family"] == f) & (df["judge_family"] == f)).sum() >= 5]
    for f in fams:
        df[f"same_{f}"] = ((df["judge_family"] == f) & (df["respondent_family"] == f)).astype(float)
    cols = [f"same_{f}" for f in fams]
    jd = pd.get_dummies(df["judge_key"], prefix="j", drop_first=True).astype(float)
    X = pd.concat([df[cols], jd], axis=1)
    y = df["weighted_score"].astype(float)
    g = df["response_id"]
    Xd = X - X.groupby(g).transform("mean")          # absorb response fixed effects
    yd = y - y.groupby(g).transform("mean")
    mj = sm.OLS(yd.values, Xd.values).fit(cov_type="cluster",
                                          cov_kwds={"groups": df["judge_key"].values})
    # PRIMARY spec: two-way clustering by judge AND question (repeated questions correlate)
    jq = np.column_stack([df["judge_key"].astype("category").cat.codes.values,
                          df["question_id"].astype("category").cat.codes.values])
    mjq = sm.OLS(yd.values, Xd.values).fit(cov_type="cluster", cov_kwds={"groups": jq})
    names = list(X.columns)
    out = {}
    for f in fams:
        i = names.index(f"same_{f}")
        b = float(mj.params[i]); se_j = float(mj.bse[i]); se_jq = float(mjq.bse[i])
        out[f] = {"fe": b, "se_judge": se_j, "p_judge": float(2 * stats.norm.sf(abs(b / se_j))),
                  "se_twoway": se_jq, "p_twoway": float(2 * stats.norm.sf(abs(b / se_jq)))}
    return out


def full_table(df):
    """Merge RE (fit_crossed) and strict-within FE (judge-clustered) into one per-family record."""
    re_results, bonf = fit_crossed(df)
    fe = fit_within_fe(df)
    rows = []
    for r in re_results:
        f = r["family"]
        rows.append({**r,                          # naive_bias, within_bias(=RE), n_same, n_other, n_responses_identifying, p(RE)
                     "re_bias": r["within_bias"], "p_re": r["p"],
                     "fe_bias": fe[f]["fe"], "se_judge": fe[f]["se_judge"], "p_judge": fe[f]["p_judge"],
                     "se_twoway": fe[f]["se_twoway"], "p_twoway": fe[f]["p_twoway"]})
    return rows, bonf


def main():
    df = load_judgments()
    print(f"Loaded {len(df):,} parsed non-self judgments with score>0 across "
          f"{df['response_id'].nunique():,} responses "
          f"and {df['judge_key'].nunique()} distinct judges.\n")
    print("Fitting: (1) RE random-intercept, (2) strict-within FE with judge-clustered SEs...\n")
    rows, bonf = full_table(df)
    n_tests = len(rows)

    header = (f"{'family':10s} {'naive':>7s} {'RE':>7s} {'FE(within)':>10s} "
              f"{'SE_judge':>9s} {'p_judge':>9s} {'Bonf':>5s} "
              f"{'n_same':>7s} {'n_other':>8s} {'n_ident':>8s}")
    print(header)
    print("-" * len(header))
    for r in sorted(rows, key=lambda x: -x["fe_bias"]):
        surv = "PASS" if r["p_judge"] < bonf else "fail"
        print(f"{r['family']:10s} {r['naive_bias']:>+7.3f} {r['re_bias']:>+7.3f} {r['fe_bias']:>+10.3f} "
              f"{r['se_judge']:>9.3f} {r['p_judge']:>9.4f} {surv:>5s} "
              f"{r['n_same']:>7d} {r['n_other']:>8d} {r['n_responses_identifying']:>8d}")

    print(f"\nBonferroni alpha = 0.05/{n_tests} = {bonf:.5f}  (applied to p_judge)")
    print("naive   = respondent-fixed raw gap, A-C: mean(sibling-judge) - mean(non-sibling-judge) on this family's responses")
    print("RE      = random-intercept-per-response estimate (partially pooled; insensitive to identifying data)")
    print("FE      = STRICT within: response absorbed as fixed effect; identified only from n_ident responses")
    print("SE_judge/p_judge = clustered by judge_key (the level sibling-status is assigned)")
    print("n_ident = responses judged by BOTH a sibling and a non-sibling (the only ones that identify FE)")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "within_response_bias.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({"bonferroni_alpha": bonf, "results": rows}, f, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    sys.exit(main())
