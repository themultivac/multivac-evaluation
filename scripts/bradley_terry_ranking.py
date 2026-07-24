#!/usr/bin/env python3
"""
Bradley-Terry re-ranking (answers Sander Land #2).

The paper's headline claim #1 -- "no single model dominates; 6 different models top
the 9 category pools" -- is computed by NAIVELY averaging each model's scores. But
scores come from judges with very different leniency (OpenAI 7.53 -> Mistral 9.44) and
on questions of very different difficulty. A model that happened to be judged by lenient
judges or on easy questions is flattered.

Bradley-Terry on WITHIN-JUDGE pairwise comparisons removes both confounds by
construction: every comparison pits two models that were scored by the SAME judge on the
SAME question, so judge leniency and item difficulty cancel exactly -- no modelling
assumption needed. We fit model strengths by the standard MM algorithm (Hunter 2004),
ties counted as half-wins, and compare the BT ranking to the naive-mean ranking, overall
and per category pool.

If the "6 of 9 distinct winners" claim survives, it survives a real correction. If category
winners move, the naive ranking was leniency/difficulty-driven.

No API calls -- pure re-analysis of the frozen dataset.
"""

import json
import glob
import os
import math
from collections import defaultdict

from scipy import stats

DATA_GLOB = os.path.join(os.path.dirname(__file__), "..", "data", "peer_matrix", "EVAL-*")


def _key2name():
    """Map every registry key to its display name, so ranking is over the paper's
    50 distinct models (30-model frontier + 18-model small pool) rather than the 55
    raw keys. Without this, duplicate keys (e.g. gpt_5_4 + judge_gpt54 -> 'GPT-5.4')
    inflate the frontier component to 34."""
    k2n = {}
    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        for j in ev.get("judgments", []):
            if j.get("respondent_name"):
                k2n[j["respondent_key"]] = j["respondent_name"]
            if j.get("judge_name"):
                k2n.setdefault(j["judge_key"], j["judge_name"])
    return k2n


def load(exclude_judges=None):
    """Per (eval, judge): list of (respondent, score), collapsed to display names.
    Plus naive sums per category (also by display name).
    exclude_judges: optional iterable of judge_keys to drop entirely (robustness check)."""
    exclude_judges = set(exclude_judges or ())
    k2n = _key2name()
    groups = []                                   # list of dict{respondent_name: score} per (eval,judge)
    groups_cat = []                               # parallel category label
    naive = defaultdict(lambda: defaultdict(lambda: [0.0, 0]))  # cat -> resp_name -> [sum, n]
    for p in sorted(glob.glob(DATA_GLOB)):
        ev = json.load(open(os.path.join(p, "results.json")))
        cat = ev.get("category")
        by_judge = defaultdict(lambda: defaultdict(list))     # judge_name -> resp_name -> [scores]
        for j in ev.get("judgments", []):
            if j.get("judge_key") in exclude_judges:      # robustness: drop high-failure judges
                continue
            if j.get("error") is None and j.get("weighted_score") and j["weighted_score"] > 0:
                rn = k2n.get(j["respondent_key"], j["respondent_key"])
                jn = k2n.get(j["judge_key"], j["judge_key"])
                ws = float(j["weighted_score"])
                by_judge[jn][rn].append(ws)
                naive[cat][rn][0] += ws
                naive[cat][rn][1] += 1
        for jn, scores in by_judge.items():
            collapsed = {rn: sum(v) / len(v) for rn, v in scores.items()}
            if len(collapsed) >= 2:
                groups.append(collapsed)
                groups_cat.append(cat)
    return groups, groups_cat, naive


def bt_fit(groups, min_comparisons=30, tol=1e-9, max_iter=5000):
    """MM algorithm for Bradley-Terry. groups: list of {model: score}. ties -> half-win."""
    wins = defaultdict(float)          # wins[i] += 1 (win) or 0.5 (tie)
    pair_n = defaultdict(float)        # pair_n[(i,j)] symmetric total comparisons
    for scores in groups:
        items = list(scores.items())
        for a in range(len(items)):
            for b in range(a + 1, len(items)):
                (i, si), (j, sj) = items[a], items[b]
                pair_n[(i, j)] += 1
                pair_n[(j, i)] += 1
                if si > sj:
                    wins[i] += 1
                elif sj > si:
                    wins[j] += 1
                else:
                    wins[i] += 0.5
                    wins[j] += 0.5

    models = sorted({m for pair in pair_n for m in (pair[0], pair[1])})
    total_comp = {m: sum(pair_n[(m, o)] for o in models if (m, o) in pair_n) for m in models}
    models = [m for m in models if total_comp[m] >= min_comparisons]
    mset = set(models)
    # neighbours for speed
    neigh = defaultdict(list)
    for (i, j), n in pair_n.items():
        if i in mset and j in mset:
            neigh[i].append((j, n))

    p = {m: 1.0 for m in models}
    for _ in range(max_iter):
        new = {}
        for i in models:
            denom = sum(n / (p[i] + p[j]) for j, n in neigh[i])
            new[i] = (wins[i] + 1e-9) / (denom + 1e-12)
        # normalise to geometric mean 1 (identifiability)
        gm = math.exp(sum(math.log(v) for v in new.values()) / len(new))
        new = {m: v / gm for m, v in new.items()}
        if max(abs(new[m] - p[m]) for m in models) < tol:
            p = new
            break
        p = new
    return {m: math.log(v) for m, v in p.items()}, wins, total_comp


def ranked(d):
    return [m for m, _ in sorted(d.items(), key=lambda x: -x[1])]


def components(groups):
    """Connected components of the co-comparison graph (edge = scored by same judge/eval).
    BT is only identified WITHIN a component: two models in different components were never
    judged head-to-head, so their relative strength is undefined."""
    adj = defaultdict(set)
    for scores in groups:
        ms = list(scores)
        for a in range(len(ms)):
            for b in range(a + 1, len(ms)):
                adj[ms[a]].add(ms[b])
                adj[ms[b]].add(ms[a])
    seen, comps = set(), []
    for n in adj:
        if n in seen:
            continue
        stack, comp = [n], set()
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            comp.add(x)
            stack.extend(adj[x] - seen)
        comps.append(comp)
    return sorted(comps, key=len, reverse=True)


def main():
    groups, groups_cat, naive = load()
    # within-judge pairwise comparison count + tie fraction (ties -> half-wins in bt_fit)
    n_pairs = n_ties = 0
    for sc in groups:
        v = list(sc.values())
        for a in range(len(v)):
            for b in range(a + 1, len(v)):
                n_pairs += 1
                n_ties += (v[a] == v[b])
    print(f"{len(groups):,} (eval,judge) comparison groups; "
          f"{n_pairs:,} within-judge pairwise comparisons, {n_ties:,} ties "
          f"({100*n_ties/n_pairs:.1f}%)\n")

    # ---- CONNECTIVITY: is a single global ranking even identifiable? ----
    comps = components(groups)
    print("=" * 64)
    print("CONNECTIVITY of the comparison graph")
    print("=" * 64)
    print(f"  {len(comps)} disconnected component(s). A single ranking across components")
    print("  is NOT identifiable (no head-to-head comparisons between them).")
    for i, c in enumerate(comps):
        print(f"    component {i}: {len(c):2d} models  e.g. {sorted(c)[:5]}")
    print()

    naive_all = defaultdict(lambda: [0.0, 0])
    for cat in naive:
        for r, (s, n) in naive[cat].items():
            naive_all[r][0] += s
            naive_all[r][1] += n
    naive_mean = {r: s / n for r, (s, n) in naive_all.items() if n >= 30}
    bt, wins, comp = bt_fit(groups, min_comparisons=30)   # abilities valid WITHIN each component

    # Report naive-vs-BT SEPARATELY per component (never across).
    global_json = {}
    for i, cset in enumerate(comps):
        common = [m for m in bt if m in naive_mean and m in cset]
        if len(common) < 3:
            continue
        nr = {m: k for k, m in enumerate(ranked({m: naive_mean[m] for m in common}))}
        br = {m: k for k, m in enumerate(ranked({m: bt[m] for m in common}))}
        rho, _ = stats.spearmanr([nr[m] for m in common], [br[m] for m in common])
        label = "FRONTIER pool" if len(cset) == max(len(c) for c in comps) else "SMALL-MODEL pool"
        print(f"--- component {i} ({label}): {len(common)} models, "
              f"Spearman(naive, BT) = {rho:.3f} ---")
        print(f"  {'model':22s} {'naive':>6s} {'nR':>4s} {'BT':>7s} {'BTR':>4s} {'move':>5s}")
        for m in ranked({m: bt[m] for m in common}):
            move = nr[m] - br[m]
            tag = "  <== up" if move >= 4 else ("  ==> down" if move <= -4 else "")
            print(f"  {m:22s} {naive_mean[m]:>6.2f} {nr[m]+1:>4d} {bt[m]:>+7.2f} {br[m]+1:>4d} {move:>+5d}{tag}")
            global_json[m] = {"component": i, "naive": naive_mean[m], "bt": bt[m],
                              "naive_rank": nr[m] + 1, "bt_rank": br[m] + 1}
        print()

    # ---- PER CATEGORY: does "6 of 9 distinct winners" survive? ----
    print("\n" + "=" * 64)
    print("PER-CATEGORY WINNER: naive mean vs Bradley-Terry")
    print("=" * 64)
    cat_groups = defaultdict(list)
    for g, c in zip(groups, groups_cat):
        cat_groups[c].append(g)

    naive_winners, bt_winners = {}, {}
    print(f"  {'category':15s} {'naive winner':22s} {'BT winner':22s} {'changed?'}")
    for cat in sorted(naive):
        nm = {r: s / n for r, (s, n) in naive[cat].items() if n >= 10}
        if not nm:
            continue
        nwin = ranked(nm)[0]
        naive_winners[cat] = nwin
        try:
            btc, _, _ = bt_fit(cat_groups[cat], min_comparisons=10)
            bwin = ranked(btc)[0] if btc else "-"
        except Exception:
            bwin = "-"
        bt_winners[cat] = bwin
        changed = "" if bwin == nwin else "  <-- CHANGED"
        print(f"  {cat:15s} {nwin:22s} {bwin:22s}{changed}")

    print(f"\n  distinct naive winners: {len(set(naive_winners.values()))} of {len(naive_winners)} pools")
    print(f"  distinct BT winners:    {len(set(bt_winners.values()))} of {len(bt_winners)} pools")
    n_changed = sum(1 for c in naive_winners if bt_winners.get(c) != naive_winners[c])
    print(f"  pools whose winner changed under BT correction: {n_changed}/{len(naive_winners)}")

    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "bradley_terry.json")
    with open(out, "w") as f:
        json.dump({"n_components": len(comps),
                   "components": [sorted(c) for c in comps],
                   "per_model": global_json,
                   "naive_winners": naive_winners, "bt_winners": bt_winners,
                   "n_pools_changed": n_changed}, f, indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
