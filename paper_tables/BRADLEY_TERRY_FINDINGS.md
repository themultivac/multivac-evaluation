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

Registry keys are collapsed to the 50 distinct display names first (so duplicate keys such as
`gpt_5_4` + `judge_gpt54` → GPT-5.4 count once), matching the paper's model accounting:

| component | n models | who |
|---|---:|---|
| 0 — frontier pool | 30 | Claude Opus/Sonnet, GPT-5.4, Gemini, Grok, DeepSeek, MiniMax, Seed, MiMo … |
| 1 — small-model pool | 18 | Qwen (all), Gemma, Llama, Kimi, Phi-4, Devstral, Granite, Mistral Nemo |

GPT-5.4 and Qwen 3.5 122B-A10B are **never** judged head-to-head — the small-model category
pools (qwen/minimax/slm/edge_cases) were run against each other, never against frontier models.
**A single 48-model leaderboard is therefore not identifiable** — the models live on two
scales that share no anchor. (A naive first BT pass "proved" every Qwen beats every frontier
model by ~20-million×; that was pure component-floating, and is exactly what a reviewer would
pounce on.) This belongs in the paper as a stated limitation and a design fix for Paper 2:
seed cross-pool comparisons so the graph connects.

## Finding 2 — within a rankable pool, correction reorders heavily

**Frontier pool (30 models):** Spearman(naive-mean, BT) = **0.647** — substantial disagreement.
The naive leaderboard is leniency/difficulty-driven. Biggest corrections:

| model | naive rank | BT rank | move |
|---|---:|---:|---:|
| GPT-5.4 | 8 | **1** | +7 |
| Grok 4.20 | 14 | 3 | +11 |
| Claude Opus 4.6 | 16 | 5 | +11 |
| Claude Sonnet 4.6 | 17 | 7 | +10 |
| GPT-OSS-120B (Legal) | **1** | 22 | −21 |
| Gemini 2.5 Flash-Lite | 12 | 26 | −14 |
| Grok 4.1 Fast | 2 | 13 | −11 |

GPT-5.4 ranks only **8th of 30 by naive average** (8.96) but has the **best head-to-head win
rate** — it is systematically judged by harsher judges / on harder questions, so averaging held it
back. That is precisely the confound BT removes. (Small-model pool by contrast is stable, Spearman
0.912 — a homogeneous pool has little leniency spread to correct.)

## Finding 3 — the headline "who tops each pool" is not robust

Claim #1 ("6 different models top the 9 category pools") — our recomputation gives **7** distinct
winners under both naive and BT; the paper reports 6 (that 6-vs-7 difference is not reconciled here).
Regardless, the **identity of the winner flips in 7 of 9 pools**:

| pool | naive winner | BT winner |
|---|---|---|
| analysis | Claude Sonnet 4.5 | **GPT-5.4** |
| code | Grok Code Fast 1 | **GPT-5.4** |
| communication | Claude Sonnet 4.5 | **Mistral Small Creative** |
| edge_cases | Grok 3 (Direct) | **Gemini 3 Flash Preview** |
| meta_alignment | Claude Sonnet 4.5 | **Claude Opus 4.6** |
| reasoning | Claude Opus 4.5 | **GPT-5.4** |
| qwen | Qwen 3 32B | **Qwen 3.5 122B-A10B** |
| minimax | GPT-5.4 | GPT-5.4 (same) |
| slm | Qwen 3 8B | Qwen 3 8B (same) |

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
