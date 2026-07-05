# Family-Bias Verification

Reproduced from the frozen dataset (`data/peer_matrix`, 286 evaluations) via `scripts/verify_family_bias.py`.

All 8 family-aggregated bias numbers reproduce exactly:

| family | reported | reproduced |
| --- | --- | --- |
| Qwen | +0.91 | +0.913 |
| xAI | +0.75 | +0.745 |
| Anthropic | +0.62 | +0.616 |
| MiniMax | +0.31 | +0.314 |
| OpenAI | +0.23 | +0.229 |
| Google | -0.59 | -0.593 |
| Meta | -0.68 | -0.681 |
| Mistral | -1.02 | -1.017 |

Bonferroni (alpha = 0.05/8 = 0.00625): **7/8 survive one-sided** (the published method; OpenAI fails), **6/8 survive two-sided** (MiniMax also drops). See `paper_tables/table_5_5_family_bias_aggregated.md`.

Note: the per-judge `table_5_5_family_bias.{md,csv}` previously showed many judges as `family = unknown` because of a truncated family map in `extract_multivac_data.py`; that map is now the canonical one shared with `statistical_analysis.py`.
