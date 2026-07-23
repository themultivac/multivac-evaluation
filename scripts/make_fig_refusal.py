#!/usr/bin/env python3
"""
Refusal figure (§5.1): scored-only mean vs mean including non-responses, as paired bars, for
the highest-refusal models, with the zero-refusal frontier tier as a flat control.
Generated ENTIRELY from paper_tables/finding1_leaderboard.json -- no hand numbers.

Output: paper_tables/fig_refusal_paired.pdf (+ .png)
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(__file__)
CONTROL = ["GPT-5.4", "Claude Opus 4.5", "Claude Sonnet 4.5", "Grok 4.1 Fast", "Mistral Small Creative"]


def main():
    rows = json.load(open(os.path.join(HERE, "..", "paper_tables", "finding1_leaderboard.json")))["rows"]
    by_name = {}
    for r in rows:                                    # keep the higher-n entry per display name
        if r["model"] not in by_name or r["n"] > by_name[r["model"]]["n"]:
            by_name[r["model"]] = r
    high = sorted([r for r in by_name.values() if r["refusal"] > 0], key=lambda x: -x["refusal"])[:5]
    ctrl = [by_name[n] for n in CONTROL if n in by_name and by_name[n]["refusal"] < 0.01][:5]
    group = high + ctrl
    labels = [r["model"] for r in group]

    x = np.arange(len(group)); w = 0.38
    fig, ax = plt.subplots(figsize=(10, 5.2))
    scored = [r["mean_excl"] for r in group]
    incl = [r["mean_incl"] for r in group]
    ax.bar(x - w / 2, scored, w, label="scored-only (non-responses discarded)", color="#9aa0a6")
    ax.bar(x + w / 2, incl, w, label="incl. non-responses (genuine zeros counted)", color="#1a7f37")
    for xi, r in zip(x, group):
        ax.text(xi, max(r["mean_excl"], r["mean_incl"]) + 0.12, f"{100*r['refusal']:.0f}%",
                ha="center", va="bottom", fontsize=8.5, color="#5f6368")
    n_high = len(high)
    ax.axvline(n_high - 0.5, color="#ccc", ls="--", lw=1)
    ax.text((n_high - 1) / 2, 10.2, "highest-refusal models", ha="center", fontsize=9, style="italic")
    ax.text(n_high + (len(ctrl) - 1) / 2, 10.2, "zero-refusal frontier (control)",
            ha="center", fontsize=9, style="italic")
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=9)
    ax.set_ylabel("Mean composite score (0–10)")
    ax.set_ylim(0, 11); ax.set_yticks(range(0, 11, 2))
    ax.legend(loc="lower left", fontsize=9, frameon=True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    out = os.path.join(HERE, "..", "paper_tables", "fig_refusal_paired")
    fig.savefig(out + ".pdf"); fig.savefig(out + ".png", dpi=200)
    print("Wrote", out + ".pdf")
    print("High-refusal:", [(r["model"], round(100*r["refusal"]), round(r["mean_excl"],2),
                             round(r["mean_incl"],2)) for r in high])
    print("Control (0%):", [r["model"] for r in ctrl])


if __name__ == "__main__":
    main()
