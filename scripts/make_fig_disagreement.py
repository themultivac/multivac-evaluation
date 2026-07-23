#!/usr/bin/env python3
"""
Finding 3 figure (§5.4): within-response disagreement sigma by category, showing BOTH the mean
and the median (the mean-median gap -- right-skew, extreme in edge_cases -- is part of the claim).
Generated ENTIRELY from paper_tables/category_disagreement.json -- no hand numbers.

Output: paper_tables/fig_disagreement_by_category.pdf (+ .png)
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(__file__)
LABEL = {"code": "code", "edge_cases": "edge cases", "reasoning": "reasoning", "minimax": "MiniMax",
         "slm": "SLM", "analysis": "analysis", "qwen": "Qwen", "communication": "communication",
         "meta_alignment": "meta-alignment"}


def main():
    d = json.load(open(os.path.join(HERE, "..", "paper_tables", "category_disagreement.json")))
    mean = d["per_category_mean_sd"]; med = d["per_category_median_sd"]
    cats = sorted(mean, key=lambda c: -mean[c])       # order by mean disagreement
    y = np.arange(len(cats))
    means = [mean[c] for c in cats]; meds = [med[c] for c in cats]

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.barh(y, means, color="#c7ccd1", height=0.6, label="mean σ", zorder=2)
    ax.scatter(meds, y, color="#d1495b", s=55, zorder=4, label="median σ")
    for yi, c in zip(y, cats):
        ax.plot([med[c], mean[c]], [yi, yi], color="#d1495b", lw=1, ls=":", zorder=3)
    # highlight the headline extremes: code (highest) and meta-alignment (lowest)
    for c, txt in [("code", "highest"), ("meta_alignment", "lowest")]:
        yi = cats.index(c)
        ax.text(mean[c] + 0.02, yi, f"{mean[c]:.2f} ({txt})", va="center", fontsize=8.5, color="#333")

    ax.set_yticks(y); ax.set_yticklabels([LABEL[c] for c in cats], fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Within-response disagreement σ (composite-score SD)")
    ax.set_xlim(0, 1.5)
    ax.legend(loc="lower right", fontsize=9, frameon=True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    out = os.path.join(HERE, "..", "paper_tables", "fig_disagreement_by_category")
    fig.savefig(out + ".pdf"); fig.savefig(out + ".png", dpi=200)
    print("Wrote", out + ".pdf")
    print("code:", round(mean["code"],3), "meta:", round(mean["meta_alignment"],3),
          "ratio:", round(mean["code"]/mean["meta_alignment"],2),
          "| edge mean/median:", round(mean["edge_cases"],3), round(med["edge_cases"],3))


if __name__ == "__main__":
    main()
