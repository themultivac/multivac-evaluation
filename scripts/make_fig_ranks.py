#!/usr/bin/env python3
"""
Finding 1 figure (§5.1): naive-mean rank vs Bradley-Terry rank for the 34-model frontier pool.
Slope chart generated ENTIRELY from paper_tables/finding1_leaderboard.json -- no hand numbers.
The four naive leaders (Seed 1.6 Flash, GPT-OSS-120B-Legal, Grok 4.1 Fast, Grok Code Fast 1)
that collapse to BT ranks 20/25/14/6 are highlighted; GPT-5.4 (naive 5 -> BT 1) is the riser.

Output: paper_tables/fig_ranks_naive_vs_bt.pdf (+ .png)
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
FALLERS = {"seed_16_flash", "gpt_oss_legal", "grok_4_1_fast", "grok_code_fast"}


def main():
    rows = json.load(open(os.path.join(HERE, "..", "paper_tables", "finding1_leaderboard.json")))["rows"]
    fr = [r for r in rows if r["frontier"] and r["bt"] is not None]
    naive = sorted(fr, key=lambda x: -x["mean_incl"])
    bt = sorted(fr, key=lambda x: -x["bt"])
    nrank = {r["key"]: i + 1 for i, r in enumerate(naive)}
    brank = {r["key"]: i + 1 for i, r in enumerate(bt)}
    N = len(fr)

    fig, ax = plt.subplots(figsize=(7.2, 8.2))
    for r in fr:
        k = r["key"]; y0, y1 = nrank[k], brank[k]
        if k in FALLERS:
            c, lw, z = "#d1495b", 2.6, 4
        elif r["model"] == "GPT-5.4" and y1 == 1:
            c, lw, z = "#1a7f37", 2.6, 4
        else:
            c, lw, z = "#c7ccd1", 1.2, 2
        ax.plot([0, 1], [y0, y1], color=c, lw=lw, zorder=z, solid_capstyle="round")
        ax.scatter([0, 1], [y0, y1], s=[26, 26], color=c, zorder=z + 1)
        if k in FALLERS or (r["model"] == "GPT-5.4" and y1 == 1):
            ax.text(-0.03, y0, f"{r['model']}", ha="right", va="center", fontsize=8.5, color=c)
            ax.text(1.03, y1, f"{r['model']}", ha="left", va="center", fontsize=8.5, color=c)

    ax.set_xlim(-0.75, 1.75)
    ax.set_ylim(N + 0.5, 0.5)                         # rank 1 at top
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Naive-mean\nrank", "Bradley–Terry\nrank"], fontsize=11)
    ax.set_yticks([1, 5, 10, 15, 20, 25, 30, N])
    ax.set_ylabel(f"Rank within the {N}-model frontier pool")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    fig.tight_layout()
    out = os.path.join(HERE, "..", "paper_tables", "fig_ranks_naive_vs_bt")
    fig.savefig(out + ".pdf"); fig.savefig(out + ".png", dpi=200)
    print("Wrote", out + ".pdf")
    print("Naive top-4 -> BT rank:", {r["model"]: brank[r["key"]] for r in naive[:4]})


if __name__ == "__main__":
    main()
