# Number provenance for `multivac_paper.tex` (rebuilt)

Maps every substantive figure in the corrected paper to the script + output that generates it.
Re-verified 2026 against the frozen 286-eval dataset. Numbers **not** produced by any repo script
are listed at the bottom.

## Mapped to a script (reproducible)

| Paper numbers | Script | Output |
|---|---|---|
| 27,540 total; 23,356 parsed; 22,252 usable-scored; 2,781 self-excluded; 1,403 failures; 1,104 zero-scores; 839 unmapped; 21,413 analysis set (abstract, §1.3, §4.4, §5, Conclusion) | `count_reconciliation.py` | `count_reconciliation.json` |
| 286 evals, 198 unique questions, 9 pools, 55 model configurations (50 distinct by display name), 17 vendor families. §4.2 question distribution (30/30/30/30/30/14/13/11/10 = 198) vs per-pool eval counts (50/49/48/47/44/14/13/11/10 = 286); 66 of 198 questions re-evaluated (up to 6×) | `make_appendices.py` (config/family diagnostics), `dataset_stats.json` | `appendix_A_models.tex` |
| Figure 1 (§5.1): naive-mean rank vs BT rank, 34-model frontier pool; 3 naive leaders collapse (Seed→20, GPT-OSS-Legal→25, Grok 4.1 Fast→14), Grok Code Fast 1 holds (naive 4 → BT 6), GPT-5.4 rises (naive 5 → BT 1) | `make_fig_ranks.py` | `fig_ranks_naive_vs_bt.pdf` |
| Figure 2 (§5.1): refusal — scored-only vs incl. non-responses (5 highest-refusal + 0%-refusal frontier control) | `make_fig_refusal.py` | `fig_refusal_paired.pdf` |
| Figure 3 (§5.4): within-response disagreement σ by category, mean + median | `make_fig_disagreement.py` | `fig_disagreement_by_category.pdf` |
| Figure 4 (§5.5): naive (A−B) vs corrected FE same-vendor estimate, per family (renamed from `make_figure4.py`) | `make_fig_bias.py` | `fig_bias_naive_vs_corrected.pdf` |
| Appendix A/C/E tables (55-config model list, EVAL-20260403-112809 score matrix, per-model dimensions for 33 models ≥100 judgments) | `make_appendices.py` | `appendix_A_models.tex`, `appendix_C_matrix.tex`, `appendix_E_dimensions.tex` |
| Appendix B (12 sample questions), Appendix D (judge prompt, anonymized) | `questions.py`, `engine/multivac.py` (extracted) | `appendix_B_questions.tex`, `appendix_D_prompt.tex` |
| Table 1: all A/B/C/D cells, Naive (A−B), Favor (A−C), RespQ (C−D); the identity to 1e-9; Google C−D=−0.938, Mistral B−D=+1.094/C−D=+0.527, OpenAI A−C=−1.136/leniency=−1.052, xAI | `four_cell_decomposition.py` | `four_cell_decomposition.json` |
| Table 1: Corrected (FE) column + judge-clustered p (Anthropic +0.406, MiniMax +0.397, Qwen +0.557, Google +0.209/0.058, OpenAI −0.137/0.307, xAI −0.095/0.549, Mistral −0.164/0.345, Meta +0.195/0.108); n_ident (482, 50, 22, …); "5 judges >30% dropped, verdicts unchanged" | `within_response_bias.py`, `robustness_check.py` | `within_response_bias.json` |
| §5.1 refusal rates + naive means (MiniMax M2.1 53% 7.53→3.51, Qwen 32B 42% 9.13→5.33, Kimi 43% 8.63→4.94, MiniMax M2 42%, Olmo 37%); naive top (Seed 9.43, GPT-OSS-Legal 9.34, Grok 4.1 Fast 9.20); BT frontier top tier; 34/18 pools; 7 distinct pool winners | `finding1_leaderboard.py`, `bradley_terry_ranking.py` | `finding1_leaderboard.json`, `bradley_terry.json` |
| §5.1 BT bootstrap: GPT-5.4 P(rank 1)=70%, rank 95% CI [1,3] | `bradley_terry_ranking.py` (bootstrap harness) | (stdout; harness in commit) |
| §5.3 judge behavior: GPT-5.4 7.187/SD 2.215, Mistral Small 9.695, spread 2.51, Seed SD 0.877, Granite SD 0.488, Gemini 2.5 Flash-Lite 9.765 | `judge_leniency_stats.py` | `judge_leniency_stats.json` |
| §5.4 disagreement: code σ 1.269, meta-alignment 0.632, ratio 2.01×, edge_cases mean 1.033/median 0.665 | `category_disagreement.py` | `category_disagreement.json` |
| §4.3 parse: 4.9% rate, χ²(49)=7122, χ²(8)=673.1 p=4.3e-140, olmo 85.6%, gemini_3_pro 56.0%, SLM 9.4%/reasoning 7.1%/communication 1.6% | `parse_failure_analysis.py` | `parse_failure.json` |
| §6.6 Krippendorff α=0.618; reasoning 0.687, MiniMax 0.673, communication 0.354, edge 0.436; §5.1 top-four p=0.266/0.073/0.071, rank-5 p=0.027 | `evaluation_framework/statistical_analysis.py` | (stdout; run `... data/peer_matrix`) |
| §4.2 SLM pool means (Qwen 3 8B 9.343, Phi-4 8.917, Gemma 8.828; Qwen 3 32B 8.93→5.44, Kimi →4.94 with refusal) | `slm_pool_means.py` | `slm_pool_means.json` |
| §4.2 dimension means (clarity 8.583, depth 7.622; largest gap Llama 3.1 8B +1.780; 25 of 33 >0.8) | `dimension_means.py` | `dimension_means.json` |
| §4.1 participation ranges (core 163–238, extended 30–60, focused 1–25) | `participation_ranges.py` | `participation_ranges.json` |
| §5.6 H2H (Qwen 3.6 Plus 107–11, 26 ties, 151 q; 185 total, 5 batches) | `h2h_results.py` | `h2h_results.json` |
| §5.1 refusal-effect table (MiniMax M2.1 53% 7.53→3.51, Kimi 43% 8.63→4.94, MiniMax M2 42% 7.21→4.21, Qwen 32B 42% 9.13→5.33, Olmo 37% 7.94→4.99) | `finding1_leaderboard.py` | `finding1_leaderboard.json` |

## NOT produced by any repo script (operational / external — footnote as such)

Only two classes remain, neither derivable from the evaluation data:

1. **Operational/cost** — \$2–3 per eval, \$700–850 total, 90 preference pairs, <\$0.01/sample, 70% distillation estimate.
2. **External-citation figures** (from cited works, not our data) — 80% agreement, 23% unanimity, 112% Arena gain, 27 Llama variants, 57 MMLU domains.

All data-derived numbers in the paper are now mapped to a script above.
