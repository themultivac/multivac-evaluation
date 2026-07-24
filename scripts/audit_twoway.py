#!/usr/bin/env python3
"""Item 3: re-fit the within-response FE same-vendor model with TWO-WAY clustering
by judge AND by question, vs the paper's judge-only clustering. Frozen data only."""
import json, glob, os, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
warnings.filterwarnings("ignore")
import sys; sys.path.insert(0, os.path.dirname(__file__))
from within_response_bias import FAMILIES, MODEL_TO_FAMILY as M2F

GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")

rows = []
for p in sorted(glob.glob(GLOB)):
    ev = json.load(open(os.path.join(p, "results.json")))
    eid = ev.get("evaluation_id") or os.path.basename(p)
    qid = ev.get("question_id") or eid
    for j in ev.get("judgments", []):
        jk, rk, ws, err = j.get("judge_key"), j.get("respondent_key"), j.get("weighted_score"), j.get("error")
        if not (jk and rk and jk != rk and ws and ws > 0 and not err):
            continue
        jf, rf = M2F.get(jk, "unknown"), M2F.get(rk, "unknown")
        if jf == "unknown" or rf == "unknown":
            continue
        rows.append({"response_id": f"{eid}::{rk}", "question_id": qid,
                     "judge_key": jk, "judge_family": jf, "respondent_family": rf,
                     "weighted_score": float(ws)})
df = pd.DataFrame(rows).reset_index(drop=True)
print(f"n judgments={len(df)}, responses={df.response_id.nunique()}, "
      f"questions={df.question_id.nunique()}, judges={df.judge_key.nunique()}")

fams = [f for f in FAMILIES
        if ((df.respondent_family == f) & (df.judge_family == f)).sum() >= 5]
for f in fams:
    df[f"same_{f}"] = ((df.judge_family == f) & (df.respondent_family == f)).astype(float)
cols = [f"same_{f}" for f in fams]
jd = pd.get_dummies(df["judge_key"], prefix="j", drop_first=True).astype(float)
X = pd.concat([df[cols], jd], axis=1)
y = df["weighted_score"].astype(float)
g = df["response_id"]
Xd = (X - X.groupby(g).transform("mean")).values
yd = (y - y.groupby(g).transform("mean")).values
base = sm.OLS(yd, Xd)

fit_j = base.fit(cov_type="cluster", cov_kwds={"groups": df["judge_key"].values})
jcodes = df["judge_key"].astype("category").cat.codes.values
qcodes = df["question_id"].astype("category").cat.codes.values
fit_jq = base.fit(cov_type="cluster", cov_kwds={"groups": np.column_stack([jcodes, qcodes])})

names = list(X.columns)
bonf = 0.05 / len(fams)
print(f"\nBonferroni alpha = 0.05/{len(fams)} = {bonf:.5f}\n")
print(f"{'family':10s} {'coef':>8s} | {'SE_judge':>8s} {'p_judge':>8s} {'verdict':>7s} | "
      f"{'SE_j+q':>8s} {'p_j+q':>8s} {'verdict':>7s} | change")
print("-" * 92)
T2 = {"anthropic":"PASS","minimax":"PASS","qwen":"(0.002)","google":"fail","meta":"fail",
      "openai":"fail","xai":"fail","mistral":"fail"}
for f in fams:
    i = names.index(f"same_{f}")
    b = fit_j.params[i]
    se_j, se_jq = fit_j.bse[i], fit_jq.bse[i]
    p_j = 2 * stats.norm.sf(abs(b / se_j))
    p_jq = 2 * stats.norm.sf(abs(b / se_jq))
    v_j = "PASS" if p_j < bonf else "fail"
    v_jq = "PASS" if p_jq < bonf else "fail"
    chg = "" if v_j == v_jq else "  <-- VERDICT CHANGES"
    print(f"{f:10s} {b:>+8.3f} | {se_j:>8.3f} {p_j:>8.4f} {v_j:>7s} | "
          f"{se_jq:>8.3f} {p_jq:>8.4f} {v_jq:>7s} |{chg}")
print("\n(verdict = passes Bonferroni at alpha above; Table 2 bolds Anthropic & MiniMax only)")
