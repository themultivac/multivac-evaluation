# The Multivac: Blind Peer Matrix Evaluation Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This dataset contains **27,540 LLM judgments** from a blind peer matrix evaluation of **55 frontier language models** across **286 evaluations** and **198 unique questions** in 9 category pools. Of the 27,540: **23,356 parsed successfully** and **22,252 carry a usable score** (the analysis set); **2,781** are intentional self-exclusions (the matrix diagonal) and **1,403** are judge failures (parse/API errors). To our knowledge, this is the largest publicly available multi-judge LLM evaluation dataset with full provenance. See `scripts/count_reconciliation.py` for the exact breakdown.

**Paper:** [The Multivac: Blind Peer Matrix Evaluation of Frontier Language Models](https://arxiv.org/abs/TODO)

## Dataset Structure

```
multivac-evaluation/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── DATASHEET.md                       # NeurIPS Datasheet for Datasets
├── CITATION.cff                       # Citation metadata
├── evaluation_framework/
│   ├── multivac.py                    # Core evaluation engine
│   ├── extract_multivac_data.py       # Data extraction pipeline
│   ├── statistical_analysis.py        # Statistical tests
│   ├── questions.py                   # Wave 1 question bank
│   └── questions_wave2_15032026.py    # Wave 2 question bank
├── data/
│   ├── peer_matrix/                   # 286 EVAL-* folders
│   └── head_to_head/                  # H2H batch folders
└── paper_tables/                      # Pre-computed tables from the paper
```

## Key Statistics

| Metric | Value |
|---|---|
| Peer matrix evaluations | 286 |
| Unique questions | 198 |
| Total judgments | 27,540 |
| Parsed judgments | 23,356 |
| Usable-scored (analysis set) | 22,252 |
| Self-excluded (diagonal) | 2,781 |
| Judge failures (parse/API) | 1,403 |
| Unique models | 55 |
| Model families | 11 |
| Category pools | 9 |
| H2H questions | 180 |
| Date range | Feb–Apr 2026 |

## Key Findings

1. **No single model dominates all categories** — 7 different models lead 9 category pools (by distinct model; `scripts/bradley_terry_ranking.py`)
2. **Same-vendor bias, corrected, is robust for only 2 of 8 families** — under a within-response fixed-effects model with judge-clustered SEs, Anthropic (+0.41) and MiniMax (+0.40) show significant favoritism; Qwen (+0.56) is significant but fragile. The large *naive* estimates — including Mistral −1.02 and Google −0.59 — are artifacts of judge leniency and respondent quality, not favoritism, and do not survive controls. See `paper_tables/FOUR_CELL_DECOMPOSITION_FINDINGS.md` and `WITHIN_RESPONSE_FINDINGS.md`. *(Supersedes the earlier "significant bias in all families" claim.)*
3. **Top 4 models are statistically indistinguishable** — the top-ranked model is not significantly separated from ranks 2–4 (bootstrap p = 0.27, 0.073, 0.071) but is from rank 5 (p = 0.027); `evaluation_framework/statistical_analysis.py`
4. **Judge disagreement is category-dependent** — code σ=1.27 vs meta-alignment σ=0.63 (ratio 2.01×; `scripts/category_disagreement.py`)
5. **Overall inter-annotator agreement**: Krippendorff's α = 0.618 (`evaluation_framework/statistical_analysis.py`)

## Intended Uses

- Model selection: Category-specific rankings for task-appropriate model choice
- DPO/RLHF training data: 90 preference pairs per evaluation at <$0.01/sample
- Judge bias research: Analysis of systematic judge behavior and family bias
- Evaluation methodology research: Comparing single-judge vs multi-judge approaches
- Safety monitoring: Tracking alignment behavior across model versions

## Limitations

- All judgments are from LLMs, not humans. Shared biases across models are not captured.
- Question selection reflects one author's judgment of what constitutes a good evaluation prompt.
- Model participation is non-uniform (10–230 evaluations per model).
- See §6 of the paper for full limitations discussion.

## Citation

```bibtex
@article{darji2026multivac,
  title={The Multivac: Blind Peer Matrix Evaluation of Frontier Language Models},
  author={Darji, Yash},
  journal={arXiv preprint arXiv:TODO},
  year={2026}
}
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contact

- Platform: [app.themultivac.com](https://app.themultivac.com)
- Discord: [discord.gg/QvVTPCxH](https://discord.gg/QvVTPCxH)
- ORCID: [0009-0009-6895-842X](https://orcid.org/0009-0009-6895-842X)
