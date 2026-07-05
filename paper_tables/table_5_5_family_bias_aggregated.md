## Table 5.5a: Same-Family Rating Bias — family-aggregated (frozen dataset)

Bootstrap CIs, 10,000 resamples, seed=42. Bonferroni corrected alpha = 0.05/8 = 0.00625.

| family | bias | 95% CI | 1-sided p | Bonferroni (1-sided) | 2-sided p | Bonferroni (2-sided) | n_same | n_other |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qwen | +0.913 | [+0.603, +1.234] | <0.0001 | PASS | <0.0001 | PASS | 434 | 130 |
| xai | +0.745 | [+0.405, +1.012] | 0.0001 | PASS | 0.0002 | PASS | 59 | 2269 |
| anthropic | +0.616 | [+0.486, +0.740] | <0.0001 | PASS | <0.0001 | PASS | 482 | 3719 |
| minimax | +0.314 | [+0.077, +0.543] | 0.0054 | PASS | 0.0108 | fail | 245 | 1493 |
| openai | +0.229 | [+0.033, +0.420] | 0.0105 | fail | 0.0210 | fail | 385 | 3315 |
| google | -0.593 | [-0.817, -0.379] | <0.0001 | PASS | <0.0001 | PASS | 426 | 3346 |
| meta | -0.681 | [-1.361, -0.200] | 0.0008 | PASS | 0.0016 | PASS | 26 | 121 |
| mistral | -1.017 | [-1.359, -0.693] | <0.0001 | PASS | <0.0001 | PASS | 25 | 532 |

**One-sided (published method): 7 of 8 survive Bonferroni.** OpenAI (+0.229) does not.
**Two-sided (sensitivity): 6 of 8 survive.** MiniMax (+0.314) is the swing family — it passes one-sided (p=0.0054) but fails two-sided (p=0.0108).

