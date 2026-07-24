#!/usr/bin/env python3
"""Finding 1 under the settled definitions (collapse + zeros-included + question-clustered):
  (1) per-category difference-test table  -> paper_tables/finding1_percategory.tex
  (2) aggregation-ladder figure            -> paper_tables/fig_ranks_naive_vs_bt.{pdf,png}
No API calls -- frozen data only."""
import json, glob, os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from audit_separation import load, per_question_WC, mm
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

RNG = np.random.default_rng(42); B = 2000
def wp(d): return 1 / (1 + np.exp(-d))
LAB = {"code": "code", "reasoning": "reasoning", "analysis": "analysis", "communication": "communication",
       "meta_alignment": "meta-alignment", "edge_cases": "edge cases", "minimax": "MiniMax", "qwen": "Qwen", "slm": "SLM"}


def pool_diff(q2groups, thr=10):
    models = sorted({m for gs in q2groups.values() for g in gs for m in g}); idx = {m: i for i, m in enumerate(models)}
    qs = list(q2groups)
    Ws = np.stack([per_question_WC(q2groups[q], idx)[0] for q in qs]); Cs = np.stack([per_question_WC(q2groups[q], idx)[1] for q in qs])
    ab0 = mm(Ws.sum(0), Cs.sum(0)); ab0[Cs.sum(0).sum(1) < thr] = -np.inf
    order = [models[i] for i in np.argsort(-ab0) if np.isfinite(ab0[i])]
    A, Bm = idx[order[0]], idx[order[1]]; Q = len(qs); d = []
    for _ in range(B):
        w = np.bincount(RNG.integers(0, Q, Q), minlength=Q).astype(float)
        ab = mm(np.tensordot(w, Ws, (0, 0)), np.tensordot(w, Cs, (0, 0)))
        if np.isfinite(ab[A]) and np.isfinite(ab[Bm]): d.append(ab[A] - ab[Bm])
    d = np.sort(d); lo, hi = d[int(.025 * len(d))], d[int(.975 * len(d)) - 1]
    return order[0], order[1], ab0[A], ab0[A] - ab0[Bm], (lo, hi), bool(lo > 0)


def main():
    catq, modelcats = load()
    # ---------- (1) per-category difference-test table ----------
    rows = [r"\begin{table}[h]\centering\small",
            r"\caption{Per-category Bradley--Terry winner vs.\ runner-up, question-clustered bootstrap. "
            r"``Win vs.\ 2nd'' is the top model's pairwise win probability over second place; the difference CI is the "
            r"95\% interval on that win probability. No pool has a separated winner---every interval spans 50\%.}",
            r"\label{tab:percat}", r"\begin{tabular}{llrrl}", r"\toprule",
            r"Pool & Winner (2nd) & Win vs.\ 2nd & 95\% CI on win & Separated? \\", r"\midrule"]
    nsep = 0
    for cat in ["code", "reasoning", "analysis", "communication", "meta_alignment", "edge_cases", "minimax", "qwen", "slm"]:
        w, r2, ab, gap, ci, sep = pool_diff(catq[cat])
        nsep += sep
        rows.append(f"{LAB[cat]} & {w} ({r2}) & {wp(gap)*100:.0f}\\% & "
                    f"[{wp(ci[0])*100:.0f}\\%, {wp(ci[1])*100:.0f}\\%] & {'yes' if sep else 'no'} \\\\")
    rows += [r"\midrule", rf"\multicolumn{{5}}{{l}}{{Separated winners: {nsep} of 9 pools}} \\",
             r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    open(os.path.join(os.path.dirname(__file__), "..", "paper_tables", "finding1_percategory.tex"), "w").write("\n".join(rows))
    print(f"per-category table written; separated winners = {nsep}/9")

    # ---------- (2) aggregation ladder ----------
    # frontier (all categories, collapsed) naive + leniency-BT ; generalist (>=3 cat) exposure-BT
    allq = defaultdict(list)
    for c in catq:
        for q, gs in catq[c].items(): allq[q].extend(gs)
    # naive means (collapsed, zeros incl)
    recv = defaultdict(lambda: [0.0, 0])
    for c in catq:
        for q, gs in catq[c].items():
            for g in gs:
                for m, s in g.items(): recv[m][0] += s; recv[m][1] += 1
    models = sorted({m for gs in allq.values() for g in gs for m in g}); idx = {m: i for i, m in enumerate(models)}
    qs = list(allq); Ws = np.stack([per_question_WC(allq[q], idx)[0] for q in qs]); Cs = np.stack([per_question_WC(allq[q], idx)[1] for q in qs])
    ab = mm(Ws.sum(0), Cs.sum(0)); ab[Cs.sum(0).sum(1) < 30] = -np.inf
    # frontier component
    from bradley_terry_ranking import components
    fr = max(components([g for gs in allq.values() for g in gs]), key=len)
    frm = [m for m in models if m in fr and np.isfinite(ab[idx[m]])]
    naive = {m: recv[m][0] / recv[m][1] for m in frm}
    nrank = {m: i + 1 for i, m in enumerate(sorted(frm, key=lambda x: -naive[x]))}
    brank = {m: i + 1 for i, m in enumerate(sorted(frm, key=lambda x: -ab[idx[x]]))}
    broad = {m for m in modelcats if len(modelcats[m]) >= 3}
    gq = defaultdict(list)
    for c in catq:
        for q, gs in catq[c].items():
            for g in gs:
                gg = {m: s for m, s in g.items() if m in broad}
                if len(gg) >= 2: gq[q].append(gg)
    gm = sorted({m for gs in gq.values() for g in gs for m in g}); gidx = {m: i for i, m in enumerate(gm)}
    gWs = np.stack([per_question_WC(gq[q], gidx)[0] for q in gq]); gCs = np.stack([per_question_WC(gq[q], gidx)[1] for q in gq])
    gab = mm(gWs.sum(0), gCs.sum(0)); gab[gCs.sum(0).sum(1) < 30] = -np.inf
    grank = {m: i + 1 for i, m in enumerate(sorted([m for m in gm if np.isfinite(gab[gidx[m]])], key=lambda x: -gab[gidx[x]]))}

    N = len(frm)
    fig, ax = plt.subplots(figsize=(8.4, 8.6))
    champs = {1: sorted(frm, key=lambda x: -naive[x])[0], 2: sorted(frm, key=lambda x: -ab[idx[x]])[0]}
    for m in frm:
        x = [0, 1]; y = [nrank[m], brank[m]]
        if m in grank: x.append(2); y.append(grank[m])
        gpt = (m == "GPT-5.4"); spec = (m not in broad) and brank[m] <= 6
        c = "#1a7f37" if gpt else ("#e08b00" if spec else "#c7ccd1")
        lw = 2.6 if (gpt or spec) else 1.0
        ax.plot(x, y, color=c, lw=lw, zorder=4 if gpt else (3 if spec else 1), solid_capstyle="round")
        ax.scatter(x, y, s=[24] * len(x), color=c, zorder=5)
        if gpt or spec:
            ax.text(x[-1] + 0.04, y[-1], m, va="center", fontsize=8.5, color=c)
            if m in (champs[1], champs[2]):
                ax.text(-0.04, nrank[m], m, va="center", ha="right", fontsize=8.5, color=c)
    ax.set_xlim(-0.9, 2.9); ax.set_ylim(N + 1, 0)
    ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["Naive mean\n(leniency)", "Leniency-adjusted\nBT", "Exposure-restricted\nBT (≥3 cat)"], fontsize=10)
    ax.set_ylabel("Rank"); [ax.spines[s].set_visible(False) for s in ("top", "right")]; ax.tick_params(length=0)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "..", "paper_tables", "fig_ranks_naive_vs_bt")
    fig.savefig(out + ".pdf"); fig.savefig(out + ".png", dpi=200)
    print(f"ladder written. champions: naive={champs[1]}, leniency-BT={champs[2]}, generalist={sorted(grank,key=grank.get)[0]}")


if __name__ == "__main__":
    main()
