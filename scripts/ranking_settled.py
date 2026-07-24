#!/usr/bin/env python3
"""
Settled ranking pipeline (Phase A decisions):
  A1  collapse duplicate display names -> rank distinct MODELS, not registry keys
  A2  zeros-INCLUDED Bradley-Terry for ranks, CIs, figures
  A3  bootstrap resampled at the QUESTION level (66 questions repeat)
Writes paper_tables/ranking_settled.json consumed by the figures and tables.
No API calls -- frozen data only.
"""
import json, glob, os, random
from collections import defaultdict
import numpy as np, sys
sys.path.insert(0, os.path.dirname(__file__))
from bradley_terry_ranking import bt_fit, components, ranked

GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")
N_BOOT = 150
SEED = 42


def load_collapsed_zeros_incl():
    """BT groups keyed by DISPLAY NAME (collapse), zeros INCLUDED, tagged with question_id.
    Also returns per-model received means (zeros incl) and naive per-category."""
    key2name = {}
    for p in sorted(glob.glob(GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        for j in ev.get("judgments", []):
            if j.get("respondent_name"): key2name[j["respondent_key"]] = j["respondent_name"]
            if j.get("judge_name"): key2name.setdefault(j["judge_key"], j["judge_name"])
    tagged, recv = [], defaultdict(lambda: {"s": 0.0, "n": 0})
    for p in sorted(glob.glob(GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        qid = ev.get("question_id") or os.path.basename(p)
        byj = defaultdict(lambda: defaultdict(list))
        for j in ev.get("judgments", []):
            if j.get("error") is not None or j.get("judge_key") == j.get("respondent_key"):
                continue
            jn = key2name.get(j["judge_key"], j["judge_key"])
            rn = key2name.get(j["respondent_key"], j["respondent_key"])
            if jn == rn:                       # self after collapse
                continue
            ws = float(j.get("weighted_score") or 0.0)
            byj[jn][rn].append(ws)
            recv[rn]["s"] += ws; recv[rn]["n"] += 1
        for jn, sc in byj.items():
            d = {rn: float(np.mean(v)) for rn, v in sc.items()}
            if len(d) >= 2:
                tagged.append((qid, d))
    return tagged, recv, key2name


def fit(tagged):
    groups = [g for _, g in tagged]
    bt = bt_fit(groups, min_comparisons=30)[0]
    comps = components(groups)
    return bt, comps


def frontier_ranks(bt, comps):
    frontier = max(comps, key=len)
    order = ranked({m: bt[m] for m in bt if m in frontier})
    return frontier, order, {m: i + 1 for i, m in enumerate(order)}


def bootstrap(tagged, top_models, level="question"):
    q2 = defaultdict(list)
    for qid, g in tagged: q2[qid].append(g)
    allq = list(q2); groups = [g for _, g in tagged]
    rng = random.Random(SEED); dist = defaultdict(list)
    for _ in range(N_BOOT):
        if level == "question":
            samp = [g for q in (allq[rng.randrange(len(allq))] for _ in allq) for g in q2[q]]
        else:
            samp = [groups[rng.randrange(len(groups))] for _ in range(len(groups))]
        bt = bt_fit(samp, min_comparisons=30)[0]
        fr = max(components(samp), key=len)
        pos = {m: i + 1 for i, m in enumerate(ranked({m: bt[m] for m in bt if m in fr}))}
        for m in top_models:
            dist[m].append(pos.get(m, len(fr) + 1))
    out = {}
    for m in top_models:
        v = sorted(dist[m])
        out[m] = {"lo": v[int(0.025 * len(v))], "hi": v[min(len(v) - 1, int(0.975 * len(v)))],
                  "p1": float(np.mean([x == 1 for x in dist[m]]))}
    return out


def main():
    tagged, recv, key2name = load_collapsed_zeros_incl()
    bt, comps = fit(tagged)
    frontier, order, frank = frontier_ranks(bt, comps)
    small = min(comps, key=len) if len(comps) > 1 else set()

    distinct_names = set(key2name.values())
    rankable = set(bt.keys())
    excluded = sorted(distinct_names - rankable)
    print("=== A1a: counts ===")
    print(f"registry keys (models_used)          : {len(set(key2name))}")
    print(f"distinct display names               : {len(distinct_names)}")
    print(f"rankable models (BT, >=30 comps)     : {len(rankable)}")
    print(f"frontier component (rankable)        : {len([m for m in frontier if m in bt])}")
    print(f"small component (rankable)           : {len([m for m in small if m in bt])}")
    print(f"distinct names NOT rankable ({len(excluded)}): {excluded}")

    print("\n=== collapsed zeros-included BT frontier ranking (top 10) ===")
    naive = {m: recv[m]["s"] / recv[m]["n"] for m in recv if recv[m]["n"]}
    fr_naive = {m: naive[m] for m in frontier if m in naive}
    nrank = {m: i + 1 for i, m in enumerate(ranked(fr_naive))}
    for m in order[:10]:
        print(f"  BT#{frank[m]:2d} {m:26s} bt={bt[m]:+.3f}  naive={naive.get(m,0):.3f} naiveRank={nrank.get(m,'-')}")

    # naive leaders' new BT ranks (for Figure 1)
    print("\n=== naive top-5 (collapsed) -> BT rank ===")
    for m in ranked(fr_naive)[:5]:
        print(f"  {m:26s} naiveRank={nrank[m]} BTrank={frank[m]} bt={bt[m]:+.3f}")

    # bootstrap for top-8
    top8 = order[:8]
    bq = bootstrap(tagged, top8, "question")
    bc = bootstrap(tagged, top8, "comparison")
    print("\n=== A2a: bootstrap (question-clustered) + top-tier membership ===")
    top_hi = bq[order[0]]["hi"]
    print(f"top model = {order[0]} (rank 1), its CI = [1,{top_hi}]")
    print(f"{'model':26s} {'ptR':>3s} {'Qcluster CI':>12s} {'P1':>5s} {'ruleA':>6s} {'ruleB':>6s}")
    memberA, memberB = [], []
    for m in top8:
        lo, hi, p1 = bq[m]["lo"], bq[m]["hi"], bq[m]["p1"]
        a = lo == 1
        b = lo <= top_hi                    # CI overlaps [1, top_hi]
        if a: memberA.append(m)
        if b: memberB.append(m)
        print(f"{m:26s} {frank[m]:>3d} {'['+str(lo)+','+str(hi)+']':>12s} {p1:>5.2f} "
              f"{'YES' if a else '-':>6s} {'YES' if b else '-':>6s}")
    print(f"\nRule (a) CI includes rank 1  -> {memberA}")
    print(f"Rule (b) CI overlaps top's CI -> {memberB}")

    out = {"counts": {"registry": len(set(key2name)), "distinct": len(distinct_names),
                      "rankable": len(rankable),
                      "frontier": len([m for m in frontier if m in bt]),
                      "small": len([m for m in small if m in bt]), "excluded": excluded},
           "bt": bt, "frontier_order": order, "frank": frank, "naive": naive, "nrank": nrank,
           "boot_question": bq, "boot_comparison": bc}
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "paper_tables",
                                      "ranking_settled.json"), "w"), indent=2)
    print("\nWrote paper_tables/ranking_settled.json")


if __name__ == "__main__":
    main()
