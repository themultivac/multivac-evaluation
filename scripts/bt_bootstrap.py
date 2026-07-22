#!/usr/bin/env python3
"""
Bootstrap the Bradley-Terry frontier-pool ranking (backs §5.1's "top tier indistinguishable").

Resamples the (eval, judge) comparison groups with replacement, refits BT, and records each
frontier model's rank. Reports the rank 95% CI and P(rank == 1) for the top models -- the basis
for the claim that GPT-5.4 leads a statistically indistinguishable top tier.

No API calls -- frozen data only.
"""

import os
import sys
import random
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from bradley_terry_ranking import load, bt_fit, components, ranked   # noqa: E402

N_RESAMPLE = 150
SEED = 42


def main():
    groups, _, _ = load()
    frontier = max(components(groups), key=len)
    rng = random.Random(SEED)
    rankdist = defaultdict(list)
    for _ in range(N_RESAMPLE):
        samp = [groups[rng.randrange(len(groups))] for _ in range(len(groups))]
        bt, _, _ = bt_fit(samp, min_comparisons=30)
        order = ranked({m: bt[m] for m in bt if m in frontier})
        for i, m in enumerate(order):
            rankdist[m].append(i + 1)

    bt, _, _ = bt_fit(groups, min_comparisons=30)
    point_order = ranked({m: bt[m] for m in bt if m in frontier})
    print(f"Frontier BT bootstrap ({N_RESAMPLE} resamples, seed {SEED}):")
    print(f"  {'model':22s} {'pt rank':>7s} {'rank 95% CI':>14s} {'P(rank=1)':>10s}")
    for m in point_order[:8]:
        rd = sorted(rankdist[m])
        lo, hi = rd[int(0.025 * len(rd))], rd[int(0.975 * len(rd)) - 1]
        p1 = sum(1 for r in rd if r == 1) / len(rd)
        print(f"  {m:22s} {point_order.index(m)+1:>7d} {f'[{lo},{hi}]':>14s} {p1:>10.2f}")


if __name__ == "__main__":
    main()
