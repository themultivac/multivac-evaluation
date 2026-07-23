#!/usr/bin/env python3
"""
Finding 2 figure (§5.5): naive (A-B) vs corrected (strict-within FE) same-vendor estimate, per family.

Paired slope plot generated ENTIRELY from paper_tables/four_cell_decomposition.json and
within_response_bias.json -- no hand-entered numbers. A connecting segment that crosses the
x=0 axis is a sign flip (highlighted). Mistral does NOT cross zero (it collapses toward zero)
and is annotated as such, per the paper.

Output: paper_tables/fig_bias_naive_vs_corrected.png (+ .pdf)
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
DISPLAY = {"anthropic": "Anthropic", "minimax": "MiniMax", "qwen": "Qwen", "google": "Google",
           "meta": "Meta", "openai": "OpenAI", "xai": "xAI", "mistral": "Mistral"}


def main():
    fc = json.load(open(os.path.join(HERE, "..", "paper_tables", "four_cell_decomposition.json")))
    wr = {r["family"]: r for r in json.load(
        open(os.path.join(HERE, "..", "paper_tables", "within_response_bias.json")))["results"]}
    bonf = json.load(open(os.path.join(HERE, "..", "paper_tables", "within_response_bias.json")))["bonferroni_alpha"]

    rows = []
    for r in fc:
        f = r["family"]
        rows.append(dict(family=f, naive=r["naive_AB"], corr=r["fe"],
                         p=wr[f]["p_judge"], n_ident=wr[f]["n_responses_identifying"]))
    rows.sort(key=lambda x: x["naive"])                       # ascending naive, most-negative at bottom

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.axvline(0, color="#888", lw=1, zorder=1)

    for i, r in enumerate(rows):
        flip = (r["naive"] > 0) != (r["corr"] > 0)            # sign change = crosses zero
        line_c = "#d1495b" if flip else "#9aa0a6"             # red = sign flip
        ax.plot([r["naive"], r["corr"]], [i, i], color=line_c, lw=2.4, zorder=2,
                solid_capstyle="round")
        # naive marker (open), corrected marker (filled; green if significant else grey)
        ax.scatter(r["naive"], i, s=70, facecolors="white", edgecolors="#5f6368",
                   linewidths=1.6, zorder=3)
        sig = r["p"] < bonf
        ax.scatter(r["corr"], i, s=90, color="#1a7f37" if sig else "#5f6368", zorder=4)
        # arrowhead toward corrected
        ax.annotate("", xy=(r["corr"], i), xytext=(r["naive"], i),
                    arrowprops=dict(arrowstyle="-|>", color=line_c, lw=0), zorder=2)
        star = " *" if sig else ""
        ax.text(min(r["naive"], r["corr"]) - 0.06, i, DISPLAY[r["family"]] + star,
                ha="right", va="center", fontsize=10)

    # callouts: all sign flips are shown in red (data-driven); Mistral is the large
    # naive value that collapses toward zero WITHOUT crossing -- annotate it explicitly.
    flips = [DISPLAY[r["family"]] for r in rows if (r["naive"] > 0) != (r["corr"] > 0)]
    labels = {r["family"]: (r["naive"], r["corr"], i) for i, r in enumerate(rows)}
    mn, mc, mi = labels["mistral"]
    ax.text((mn + mc) / 2, mi + 0.30, "collapse toward 0 (not a flip)", ha="center",
            va="bottom", fontsize=8, color="#5f6368", style="italic")

    ax.set_yticks([])
    ax.set_ylim(-0.8, len(rows) - 0.2)
    ax.set_xlabel("Same-vendor estimate (0–10 composite units)")
    # No baked-in title: the LaTeX \caption is the sole figure label (avoids a
    # duplicate "Figure 4" that conflicts with the compiled figure number).
    # legend proxies
    from matplotlib.lines import Line2D
    leg = [Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
                  markeredgecolor="#5f6368", markersize=9, label="naive (A−B)"),
           Line2D([0], [0], marker="o", color="w", markerfacecolor="#1a7f37", markersize=9,
                  label="corrected, significant"),
           Line2D([0], [0], marker="o", color="w", markerfacecolor="#5f6368", markersize=9,
                  label="corrected, n.s.")]
    ax.legend(handles=leg, loc="lower right", fontsize=8, frameon=True)
    ax.grid(axis="x", color="#eee", zorder=0)
    fig.tight_layout()

    out = os.path.join(HERE, "..", "paper_tables", "fig_bias_naive_vs_corrected")
    fig.savefig(out + ".png", dpi=200)
    fig.savefig(out + ".pdf")
    print(f"Wrote {out}.png and .pdf")
    print("\nSign-flip audit (naive vs corrected cross zero):")
    for r in rows:
        flip = (r["naive"] > 0) != (r["corr"] > 0)
        print(f"  {DISPLAY[r['family']]:10s} naive {r['naive']:+.3f} -> corr {r['corr']:+.3f}"
              f"   {'SIGN FLIP' if flip else ''}")


if __name__ == "__main__":
    main()
