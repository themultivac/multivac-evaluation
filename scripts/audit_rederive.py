#!/usr/bin/env python3
"""Independent re-derivation for the pre-submission audit. Frozen data only."""
import json, glob, os
from collections import defaultdict, Counter
import numpy as np

HERE = os.path.dirname(__file__)
GLOB = os.path.join(HERE, "..", "data", "peer_matrix", "EVAL-*")
FAMILIES = {
    "anthropic": ["claude_opus_46","claude_sonnet_46","claude_opus","claude_sonnet","judge_claude_sonnet"],
    "openai": ["gpt_5_4","gpt_oss_120b","gpt_codex","gpt_oss_legal","judge_gpt54"],
    "google": ["gemini_31_pro","gemini_3_flash","gemini_3_pro","gemini_2_5_flash","gemini_25_flash",
               "gemini_2_5_flash_lite","gemma3_27b","gemma_3n_4b","judge_gemini"],
    "xai": ["grok_420","grok_direct","grok_4_1_fast","grok_code_fast"],
    "deepseek": ["deepseek_v4","deepseek_v3"],
    "qwen": ["qwen3_8b","qwen3_32b","qwen3_coder_next","qwen35_9b","qwen35_27b","qwen35_35b_a3b",
             "qwen35_122b_a10b","qwen35_397b_a17b"],
    "minimax": ["minimax_01","minimax_m1","minimax_m2","minimax_m21","minimax_m25","minimax_m27"],
    "xiaomi": ["mimo_v2_flash"], "mistral": ["mistral_small_creative","mistral_nemo","devstral"],
    "bytedance": ["seed_16_flash","seed_1_6_flash"], "meta": ["llama31_8b","llama4_scout"],
}
M2F = {m: f for f, ms in FAMILIES.items() for m in ms}

evs = []
for p in sorted(glob.glob(GLOB)):
    evs.append((os.path.basename(p), json.load(open(os.path.join(p, "results.json")))))
print(f"[canonical] {len(evs)} evaluations in data/peer_matrix\n")

# ---------- COUNTS (§4.4, §4.3) ----------
tot = self_ex = parsed = zero = scored = api = parse_fail = 0
scored_mapped = scored_unmapped = 0
for eid, ev in evs:
    for j in ev.get("judgments", []):
        tot += 1
        jk, rk, err = j.get("judge_key"), j.get("respondent_key"), j.get("error")
        ws = j.get("weighted_score")
        if jk == rk or err == "self_judgment_excluded":
            self_ex += 1; continue
        if err is not None:
            if "api" in str(err).lower() or "timeout" in str(err).lower() or "rate" in str(err).lower():
                api += 1
            else:
                parse_fail += 1
            continue
        parsed += 1
        if (ws or 0) > 0:
            scored += 1
            if M2F.get(rk) and M2F.get(jk): scored_mapped += 1
            else: scored_unmapped += 1
        else:
            zero += 1
print("=== COUNTS ===")
print(f"total slots            = {tot}   (claim 27,540)")
print(f"self-exclusions        = {self_ex}   (claim 2,781)")
print(f"judge failures (err)   = {parse_fail+api}   (claim 1,403)  [parse={parse_fail}, api={api}]")
print(f"parsed (err None)      = {parsed}   (claim 23,356)")
print(f"zero-scores            = {zero}   (claim 1,104)")
print(f"usable scored (>0)     = {scored}   (claim 22,252)")
print(f"  of which unmapped    = {scored_unmapped}   (claim 839)")
print(f"  same-vendor set      = {scored_mapped}   (claim 21,413)")
print(f"27,540-2,781           = {27540-2781}  (claim 24,759) ; -1,403 = {27540-2781-1403} (claim 23,356)")
print(f"parse rate 1,192/24,548= {1192/24548*100:.2f}%   ; 24,759-24,548={24759-24548} vs 1,403-1,192={1403-1192}")

# ---------- REPEAT STRUCTURE (item 2) ----------
qid_evals = defaultdict(list); qid_cats = defaultdict(set); cat_evals = Counter(); cat_qs = defaultdict(set)
eval_pool = {}   # eid -> frozenset(models_used)
for eid, ev in evs:
    qid = ev.get("question_id"); cat = ev.get("category")
    cat_evals[cat] += 1
    if qid:
        qid_evals[qid].append(eid); qid_cats[qid].add(cat); cat_qs[cat].add(qid)
    eval_pool[eid] = frozenset(ev.get("models_used", []))
print("\n=== REPEAT STRUCTURE ===")
rep_dist = Counter(len(v) for v in qid_evals.values())
print("evals-per-question distribution:", dict(sorted(rep_dist.items())))
print(f"unique questions = {len(qid_evals)} (claim 198); total evals over them = {sum(len(v) for v in qid_evals.values())}")
repeats = {q: eids for q, eids in qid_evals.items() if len(eids) > 1}
print(f"questions re-evaluated (>1): {len(repeats)}  (claim 66)")
same_pool = diff_pool = 0
for q, eids in repeats.items():
    pools = {eval_pool[e] for e in eids}
    if len(pools) == 1: same_pool += 1
    else: diff_pool += 1
print(f"  repeats with identical pool composition: {same_pool}")
print(f"  repeats with >=2 distinct pool compositions: {diff_pool}")

# per-pool question counts (item 4)
print("\nper-pool: evals vs distinct questions")
for c in sorted(cat_evals, key=lambda x: -cat_evals[x]):
    print(f"  {c:16s} evals={cat_evals[c]:3d}  questions={len(cat_qs[c]):3d}")

# ---------- CROSS-POOL EDGES (item 2/7) ----------
# Build the comparison graph: two models share an edge if co-judged in some eval.
# Frontier vs small pool: does any question-repeat or eval connect them?
# Define pools by finding1 frontier/small components via co-occurrence.
adj = defaultdict(set)
for eid, ev in evs:
    ms = [m for m in ev.get("models_used", [])]
    for a in ms:
        for b in ms:
            if a != b: adj[a].add(b)
# connected components
seen=set(); comps=[]
for m in adj:
    if m in seen: continue
    stack=[m]; comp=set()
    while stack:
        x=stack.pop()
        if x in seen: continue
        seen.add(x); comp.add(x)
        stack.extend(adj[x]-seen)
    comps.append(comp)
comps.sort(key=len, reverse=True)
print("\n=== CROSS-POOL CONNECTIVITY ===")
print("component sizes:", [len(c) for c in comps], " (claim 34-model frontier + 18-model small)")
if len(comps) >= 2:
    inter = comps[0] & comps[1]
    print(f"edges between the two largest components: {len(inter)} shared models (want 0)")
    print(f"graph fully connected? {'NO' if len(comps)>1 else 'YES'} -> no single 55-leaderboard identifiable: {'confirmed' if len(comps)>1 else 'FALSE'}")

# ---------- REFUSAL TABLE (Table 1) ----------
recv = defaultdict(lambda: {"s": [], "z": 0}); names = {}
for eid, ev in evs:
    for j in ev.get("judgments", []):
        if j.get("error") is not None or j.get("judge_key") == j.get("respondent_key"): continue
        rk = j["respondent_key"]; ws = float(j.get("weighted_score") or 0)
        names[rk] = j.get("respondent_name", rk)
        recv[rk]["s"].append(ws) if ws > 0 else recv[rk].__setitem__("z", recv[rk]["z"]+1)
print("\n=== TABLE 1 (refusal, all-pool) ===")
tbl1 = {"MiniMax M2.1":"minimax_m21","Kimi K2.5":"kimi_k25","MiniMax M2":"minimax_m2",
        "Qwen 3 32B":"qwen3_32b","Olmo 3.1 32B Think":"olmo_think"}
claims1 = {"MiniMax M2.1":(53,7.53,3.51),"Kimi K2.5":(43,8.63,4.94),"MiniMax M2":(42,7.21,4.21),
           "Qwen 3 32B":(42,9.13,5.33),"Olmo 3.1 32B Think":(37,7.94,4.99)}
for nm, k in tbl1.items():
    # find key by display name if needed
    key = k if k in recv else next((rk for rk,n in names.items() if n==nm), None)
    d = recv.get(key, {"s":[],"z":0}); n1=len(d["s"]); n0=d["z"]; n=n1+n0
    ref = 100*n0/n if n else 0; excl = np.mean(d["s"]) if n1 else 0; incl = sum(d["s"])/n if n else 0
    print(f"  {nm:20s} refusal={ref:4.0f}% scored={excl:.2f} incl={incl:.2f}  claim={claims1[nm]}")

# ---------- DIMENSION MEANS + GAP (Table 5, §5.2) ----------
DIMS=["correctness","completeness","clarity","depth","usefulness"]
dim_all=defaultdict(list); per_model=defaultdict(lambda: defaultdict(list))
for eid, ev in evs:
    for j in ev.get("judgments", []):
        if j.get("error") is not None or j.get("judge_key")==j.get("respondent_key"): continue
        rk=j["respondent_key"]
        for dd in DIMS:
            if j.get(dd) is not None:
                dim_all[dd].append(float(j[dd])); per_model[rk][dd].append(float(j[dd]))
print("\n=== DIMENSION MEANS (all judgments, zeros incl) ===")
for dd in DIMS: print(f"  {dd:13s} {np.mean(dim_all[dd]):.3f}")
gaps=[]
for rk,dd in per_model.items():
    if len(dd["clarity"])>=100:
        gaps.append((names.get(rk,rk), np.mean(dd["clarity"])-np.mean(dd["depth"])))
gaps.sort(key=lambda x:-x[1])
n_over=sum(1 for _,g in gaps if g>0.8)
print(f"models with >=100 judgments: {len(gaps)} (claim 33); with gap>0.8: {n_over} (claim 25)")
print("  top-3 gaps:", [(nm,round(g,3)) for nm,g in gaps[:3]], " (claim Llama 1.780, Nemo 1.505, Codex 1.504)")

# ---------- H2H (item 9) ----------
print("\n=== H2H arithmetic ===")
print(f"107+11+26+7 = {107+11+26+7} (claim 151) ; 151+31 = {151+31} <=185 recorded (claim)")
