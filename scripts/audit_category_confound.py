#!/usr/bin/env python3
"""C1/C2: is the global BT ranking measuring category exposure rather than ability?
Frozen data only. Collapsed by display name, zeros included (settled defs)."""
import json, glob, os, random
from collections import defaultdict
import numpy as np, sys
sys.path.insert(0, os.path.dirname(__file__))
from bradley_terry_ranking import bt_fit, components, ranked

GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")


def load():
    key2name = {}
    for p in sorted(glob.glob(GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        for j in ev.get("judgments", []):
            if j.get("respondent_name"): key2name[j["respondent_key"]] = j["respondent_name"]
            if j.get("judge_name"): key2name.setdefault(j["judge_key"], j["judge_name"])
    tagged = []                      # (qid, cat, group)
    evcat = defaultdict(set)         # model -> set of (eid) ; and cats
    modelcats = defaultdict(set); modelevals = defaultdict(set)
    for p in sorted(glob.glob(GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        eid = os.path.basename(p); qid = ev.get("question_id") or eid; cat = ev.get("category")
        for k in set(ev.get("models_used", [])):
            nm = key2name.get(k, k); modelcats[nm].add(cat); modelevals[nm].add(eid)
        byj = defaultdict(lambda: defaultdict(list))
        for j in ev.get("judgments", []):
            if j.get("error") is not None or j.get("judge_key") == j.get("respondent_key"): continue
            jn = key2name.get(j["judge_key"]); rn = key2name.get(j["respondent_key"])
            if jn == rn: continue
            byj[jn][rn].append(float(j.get("weighted_score") or 0))
        for jn, sc in byj.items():
            d = {rn: float(np.mean(v)) for rn, v in sc.items()}
            if len(d) >= 2: tagged.append((qid, cat, d))
    return tagged, modelcats, modelevals


def fit_ranks(groups):
    bt = bt_fit(groups, min_comparisons=30)[0]
    fr = max(components(groups), key=len)
    order = ranked({m: bt[m] for m in bt if m in fr})
    return bt, fr, order


def boot(tagged, top, keep=None, N=150, seed=42):
    q2 = defaultdict(list)
    for qid, cat, g in tagged:
        gg = {m: s for m, s in g.items() if keep is None or m in keep}
        if len(gg) >= 2: q2[qid].append(gg)
    allq = list(q2); rng = random.Random(seed); dist = defaultdict(list)
    for _ in range(N):
        samp = [g for q in (allq[rng.randrange(len(allq))] for _ in allq) for g in q2[q]]
        bt = bt_fit(samp, min_comparisons=30)[0]
        fr = max(components(samp), key=len)
        pos = {m: i + 1 for i, m in enumerate(ranked({m: bt[m] for m in bt if m in fr}))}
        for m in top: dist[m].append(pos.get(m, 999))
    return {m: (sorted(dist[m])[int(.025*len(dist[m]))], sorted(dist[m])[min(len(dist[m])-1,int(.975*len(dist[m]))-1)],
                float(np.mean([x == 1 for x in dist[m]]))) for m in top}


def main():
    tagged, modelcats, modelevals = load()
    groups = [g for _, _, g in tagged]
    bt, fr, order = fit_ranks(groups)

    print("=== C1: category participation + eval count for frontier ranking pool (top 15 by BT) ===")
    print(f"{'model':26s} {'evals':>5s} {'#cat':>4s}  categories")
    for m in order[:15]:
        print(f"{m:26s} {len(modelevals[m]):>5d} {len(modelcats[m]):>4d}  {sorted(modelcats[m])}")

    print("\n=== C1: top tier under >=3 category participation (refit) ===")
    broad = {m for m in bt if len(modelcats[m]) >= 3}
    gb = [g for g in groups]
    bt3 = bt_fit([{m: s for m, s in g.items() if m in broad} for g in gb if sum(1 for m in g if m in broad) >= 2],
                 min_comparisons=30)[0]
    fr3 = max(components([{m: s for m, s in g.items() if m in broad} for g in gb if sum(1 for m in g if m in broad) >= 2]), key=len)
    order3 = ranked({m: bt3[m] for m in bt3 if m in fr3})
    print(f"broad-participation frontier size: {len(order3)}")
    ci3 = boot(tagged, order3[:6], keep=broad)
    for m in order3[:6]:
        lo, hi, p1 = ci3[m]; print(f"  BT#{order3.index(m)+1} {m:26s} CI[{lo},{hi}] P1={p1:.2f}  ({len(modelcats[m])} cats)")

    print("\n=== C2: participation-threshold effect on the top tier ===")
    for thr in (1, 10, 30):
        keep = {m for m in bt if len(modelevals[m]) >= thr}
        gk = [{m: s for m, s in g.items() if m in keep} for g in groups]
        gk = [g for g in gk if len(g) >= 2]
        b = bt_fit(gk, min_comparisons=30)[0]; f = max(components(gk), key=len)
        o = ranked({m: b[m] for m in b if m in f})
        ci = boot(tagged, o[:5], keep=keep)
        tier_a = [m for m in o[:6] if ci.get(m, (9,9,0))[0] == 1] if False else None
        print(f"  >= {thr:2d} evals: frontier={len(o)}  top5={[ (m, f'[{ci[m][0]},{ci[m][1]}]') for m in o[:5]]}")

    print("\n=== C1: per-category BT top-3 with CIs (all 9 pools) ===")
    catg = defaultdict(list)
    for qid, cat, g in tagged: catg[cat].append((qid, g))
    for cat in sorted(catg):
        gs = [g for _, g in catg[cat]]
        try:
            b = bt_fit(gs, min_comparisons=10)[0]
            fcomp = max(components(gs), key=len)
            o = ranked({m: b[m] for m in b if m in fcomp})[:3]
            # per-category question bootstrap
            q2 = defaultdict(list)
            for qid, g in catg[cat]: q2[qid].append(g)
            allq = list(q2); rng = random.Random(42); dist = defaultdict(list)
            for _ in range(120):
                samp = [g for q in (allq[rng.randrange(len(allq))] for _ in allq) for g in q2[q]]
                bb = bt_fit(samp, min_comparisons=10)[0]
                ff = max(components(samp), key=len)
                pos = {m: i+1 for i, m in enumerate(ranked({m: bb[m] for m in bb if m in ff}))}
                for m in o: dist[m].append(pos.get(m, 999))
            cis = {m: (sorted(dist[m])[3], sorted(dist[m])[-3]) for m in o}
            print(f"  {cat:15s}: " + ", ".join(f"{m} CI{cis[m]}" for m in o))
        except Exception as e:
            print(f"  {cat:15s}: err {e}")


if __name__ == "__main__":
    main()
