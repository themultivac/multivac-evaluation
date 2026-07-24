#!/usr/bin/env python3
"""F1-F4: proper paired-difference separation test on the ability scale,
question-clustered, 10,000 resamples. Frozen data only. No edits."""
import json, glob, os
from collections import defaultdict
import numpy as np
GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")
RNG = np.random.default_rng(42)


def load():
    key2name = {}
    for p in sorted(glob.glob(GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        for j in ev.get("judgments", []):
            if j.get("respondent_name"): key2name[j["respondent_key"]] = j["respondent_name"]
            if j.get("judge_name"): key2name.setdefault(j["judge_key"], j["judge_name"])
    catq = defaultdict(lambda: defaultdict(list))   # cat -> qid -> [group dicts]
    modelcats = defaultdict(set)
    for p in sorted(glob.glob(GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        qid = ev.get("question_id") or os.path.basename(p); cat = ev.get("category")
        for k in set(ev.get("models_used", [])):
            modelcats[key2name.get(k, k)].add(cat)
        byj = defaultdict(lambda: defaultdict(list))
        for j in ev.get("judgments", []):
            if j.get("error") is not None or j.get("judge_key") == j.get("respondent_key"): continue
            jn = key2name.get(j["judge_key"]); rn = key2name.get(j["respondent_key"])
            if jn == rn: continue
            byj[jn][rn].append(float(j.get("weighted_score") or 0))
        for jn, sc in byj.items():
            d = {rn: float(np.mean(v)) for rn, v in sc.items()}
            if len(d) >= 2: catq[cat][qid].append(d)
    return catq, modelcats


def per_question_WC(qgroups, idx):
    M = len(idx); W = np.zeros((M, M)); C = np.zeros((M, M))
    for g in qgroups:
        items = [(idx[m], s) for m, s in g.items() if m in idx]
        for a in range(len(items)):
            for b in range(a + 1, len(items)):
                (i, si), (j, sj) = items[a], items[b]
                C[i, j] += 1; C[j, i] += 1
                if si > sj: W[i, j] += 1
                elif sj > si: W[j, i] += 1
                else: W[i, j] += 0.5; W[j, i] += 0.5
    return W, C


def mm(W, C, iters=200):
    M = W.shape[0]; wins = W.sum(1); active = C.sum(1) > 0
    p = np.ones(M)
    for _ in range(iters):
        S = p[:, None] + p[None, :]; np.fill_diagonal(S, 1)
        denom = (C / S).sum(1) + 1e-12
        pn = np.where(active, (wins + 1e-9) / denom, p)
        gm = np.exp(np.mean(np.log(pn[active]))); pn = pn / gm
        if np.max(np.abs(pn - p)) < 1e-7: p = pn; break
        p = pn
    ab = np.full(M, -np.inf); ab[active] = np.log(p[active])
    return ab


def analyze(cat, qgroups_by_q, thr=10, B=10000, top_target=None):
    models = sorted({m for gs in qgroups_by_q.values() for g in gs for m in g})
    idx = {m: i for i, m in enumerate(models)}
    Wq = {}; Cq = {}
    qs = list(qgroups_by_q)
    for q in qs:
        Wq[q], Cq[q] = per_question_WC(qgroups_by_q[q], idx)
    Ws = np.stack([Wq[q] for q in qs]); Cs = np.stack([Cq[q] for q in qs])
    tot = Cs.sum(0).sum(1)
    keep = np.where(tot >= thr)[0]
    ab_full = mm(Ws.sum(0), Cs.sum(0))
    ab_full[[i for i in range(len(models)) if i not in keep]] = -np.inf
    order = [models[i] for i in np.argsort(-ab_full) if np.isfinite(ab_full[i])]
    Q = len(qs)
    # bootstrap
    diffs12 = []; diffs13 = []; ab_top = defaultdict(list); ranks = defaultdict(list)
    A = idx.get(order[0]); Bm = idx.get(order[1]) if len(order) > 1 else None
    Cm = idx.get(order[2]) if len(order) > 2 else None
    tgt = idx.get(top_target) if top_target else None
    for _ in range(B):
        pick = RNG.integers(0, Q, Q)
        w = np.bincount(pick, minlength=Q).astype(float)
        W = np.tensordot(w, Ws, axes=(0, 0)); C = np.tensordot(w, Cs, axes=(0, 0))
        ab = mm(W, C)
        if np.isfinite(ab[A]) and Bm is not None and np.isfinite(ab[Bm]): diffs12.append(ab[A] - ab[Bm])
        if np.isfinite(ab[A]) and Cm is not None and np.isfinite(ab[Cm]): diffs13.append(ab[A] - ab[Cm])
        fin = np.isfinite(ab)
        rank = {models[i]: r + 1 for r, i in enumerate(np.argsort(-ab)) if fin[i]}
        for m in order[:3]: ranks[m].append(rank.get(m, 999))
        if tgt is not None: ranks[top_target].append(rank.get(top_target, 999))
    def ci(a): a = np.sort(a); return (round(a[int(.025*len(a))], 3), round(a[int(.975*len(a))-1], 3))
    d12 = np.array(diffs12); d13 = np.array(diffs13)
    return {"order": order[:3], "ab_full": {m: round(ab_full[idx[m]], 3) for m in order[:3]},
            "gap12": round(ab_full[A] - ab_full[Bm], 3) if Bm is not None else None,
            "ci_d12": ci(d12), "excl0_12": bool(ci(d12)[0] > 0 or ci(d12)[1] < 0),
            "ci_d13": ci(d13) if len(d13) else None,
            "excl0_13": bool(len(d13) and (ci(d13)[0] > 0 or ci(d13)[1] < 0)),
            "se12": round(d12.std(), 3), "mde12": round(2.8 * d12.std(), 3),
            "rankCI_top": (int(np.percentile(ranks[order[0]], 2.5)), int(np.percentile(ranks[order[0]], 97.5))),
            "P1_top": round(np.mean(np.array(ranks[order[0]]) == 1), 3),
            "P1_target": round(np.mean(np.array(ranks[top_target]) == 1), 3) if top_target else None,
            "rankCI_target": (int(np.percentile(ranks[top_target], 2.5)), int(np.percentile(ranks[top_target], 97.5))) if top_target else None}


def main():
    catq, modelcats = load()
    print("=== F1/F2/F3: per-pool difference test (ability scale, question-clustered, B=10,000) ===")
    print(f"{'pool':15s} {'top / 2nd / 3rd':45s} {'gap12':>6s} {'CI(diff 1-2)':>16s} {'sep?':>5s} {'MDE':>6s} {'rankCI(1)':>10s}")
    sepcount = 0
    for cat in sorted(catq):
        r = analyze(cat, catq[cat], thr=10, B=10000)
        o = r["order"]; ab = r["ab_full"]
        trip = f"{o[0]}({ab[o[0]]}) / {o[1]}({ab[o[1]]}) / {o[2]}({ab[o[2]]})"[:45]
        sep = "YES" if r["excl0_12"] else "no"
        if r["excl0_12"]: sepcount += 1
        print(f"{cat:15s} {trip:45s} {r['gap12']:>6.2f} {str(r['ci_d12']):>16s} {sep:>5s} {r['mde12']:>6.2f} {str(r['rankCI_top']):>10s}")
    print(f"\nSEPARATED by difference test (CI excludes 0): {sepcount} of 9 pools")

    print("\n=== generalist pool (>=3 cats): GPT-5.4 vs runner-up, difference test, B=10,000 ===")
    genq = defaultdict(list)
    broad = {m for m in modelcats if len(modelcats[m]) >= 3}
    for cat in catq:
        for q, gs in catq[cat].items():
            for g in gs:
                gg = {m: s for m, s in g.items() if m in broad}
                if len(gg) >= 2: genq[q].append(gg)
    rg = analyze("generalist", genq, thr=30, B=10000, top_target="GPT-5.4")
    print(f"  order: {rg['order']}  abilities {rg['ab_full']}")
    print(f"  GPT-5.4 vs 2nd: gap={rg['gap12']}  CI(diff)={rg['ci_d12']}  excludes0={rg['excl0_12']}")
    print(f"  GPT-5.4 P(rank1)={rg['P1_top']}  rankCI={rg['rankCI_top']}   (150 gave P=0.97)")


if __name__ == "__main__":
    main()
