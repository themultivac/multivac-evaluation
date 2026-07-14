# Bradley-Terry re-ranking (answers Sander #2)

**Date:** 2026-07-13 · **Script:** `scripts/bradley_terry_ranking.py` · **Data:** frozen 286-eval set (no API calls)

Sander #2: the paper reports large judge bias, then builds rankings by naively averaging
over those same judges with no correction. We re-rank with **Bradley-Terry on within-judge
pairwise comparisons** — every comparison pits two models scored by the *same* judge on the
*same* question, so judge leniency (OpenAI 7.53 → Mistral 9.44) and item difficulty cancel by
construction. Fit by the MM algorithm (Hunter 2004); ties (18.5%) counted as half-wins.

Two findings, one of them a hard limitation of the benchmark itself.

## Finding 1 — the benchmark is NOT globally rankable (design limitation)

The comparison graph has **2 disconnected components**:

| component | n models | who |
|---|---:|---|
| 0 — frontier pool | 34 | claude*, gpt*, gemini*, grok*, deepseek*, minimax*, seed*, mimo … |
| 1 — small-model pool | 18 | qwen* (all), gemma*, llama*, kimi, phi4, devstral, granite, mistral_nemo |

`gpt_5_4` and `qwen35_122b_a10b` are **never** judged head-to-head — the small-model category
pools (qwen/minimax/slm/edge_cases) were run against each other, never against frontier models.
**A single 55-model leaderboard is therefore not identifiable** — the models live on two
scales that share no anchor. (A naive first BT pass "proved" every Qwen beats every frontier
model by ~20-million×; that was pure component-floating, and is exactly what a reviewer would
pounce on.) This belongs in the paper as a stated limitation and a design fix for Paper 2:
seed cross-pool comparisons so the graph connects.

## Finding 2 — within a rankable pool, correction reorders heavily

**Frontier pool (34 models):** Spearman(naive-mean, BT) = **0.621** — substantial disagreement.
The naive leaderboard is leniency/difficulty-driven. Biggest corrections:

| model | naive rank | BT rank | move |
|---|---:|---:|---:|
| gpt_5_4 | 10 | **1** | +9 |
| claude_opus_46 | 20 | 6 | +14 |
| grok_420 | 17 | 3 | +14 |
| seed_1_6_flash | **1** | 18 | −17 |
| gpt_oss_legal | 2 | 24 | −22 |
| grok_4_1_fast | 3 | 15 | −12 |
| gemini_2_5_flash_lite | 15 | 29 | −14 |

`gpt_5_4` ranks only **10th of 34 by naive average** (8.95) but has the **best head-to-head win
rate** — it is systematically judged by harsher judges / on harder questions, so averaging held it
back. That is precisely the confound BT removes. (Small-model pool by contrast is stable, Spearman
0.912 — a homogeneous pool has little leniency spread to correct.)

## Finding 3 — the headline "who tops each pool" is not robust

Claim #1 ("6 different models top the 9 category pools") — our recomputation gives **7** distinct
winners under both naive and BT; the paper reports 6 (that 6-vs-7 difference is not reconciled here).
Regardless, the **identity of the winner flips in 7 of 9 pools**:

| pool | naive winner | BT winner |
|---|---|---|
| analysis | claude_sonnet | **gpt_5_4** |
| code | grok_code_fast | **gpt_5_4** |
| communication | claude_sonnet | **mistral_small_creative** |
| edge_cases | grok_direct | **gemini_3_flash** |
| meta_alignment | claude_sonnet | **claude_opus_46** |
| reasoning | claude_opus | **gpt_5_4** |
| qwen | qwen3_32b | **qwen35_122b_a10b** |
| minimax | judge_gpt54 | judge_gpt54 (same) |
| slm | qwen3_8b | qwen3_8b (same) |

**All 5 well-sampled categories (analysis, code, communication, meta_alignment, reasoning) change
winner.** So the paper's specific "model X tops pool Y" statements are artifacts of naive
averaging; the higher-level "no single model dominates" claim actually *survives* (arguably
strengthens — gpt_5_4 tops 3 pools but not all).

## What to say in the paper

1. Report rankings as **BT (within-judge pairwise)**, not naive means — it is the correction
   Sander asked for and needs no leniency model.
2. State the **disconnection limitation** honestly and restrict any leaderboard to a connected
   pool. Do not publish a unified 55-model table.
3. Re-state claim #1 at the robust altitude ("no model dominates across pools") and drop the
   specific per-pool winner narrative, or report it as BT winners with the caveat that small
   pools (edge_cases/qwen/minimax/slm) are thinly sampled.

Caveat: absolute BT values are per-component (arbitrary additive constant); only *within-component*
order is meaningful. BT/MM here is the pairwise sibling of the IRT-style joint estimation in
`within_response_bias.py`; both point the same way.

Reproduce: `./.venv/bin/python scripts/bradley_terry_ranking.py` (writes `paper_tables/bradley_terry.json`).
