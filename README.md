# The Multivac: Blind Peer Matrix Evaluation Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This dataset contains **27,540 LLM judgments** (22,254 valid after self-exclusion) from a blind peer matrix evaluation of **55 frontier language models** across **286 evaluations** and **198 unique questions** in 9 category pools. To our knowledge, this is the largest publicly available multi-judge LLM evaluation dataset with full provenance.

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
| Valid judgments (self-excluded) | 22,254 |
| Unique models | 55 |
| Model families | 11 |
| Category pools | 9 |
| H2H questions | 180 |
| Date range | Feb–Apr 2026 |

## Key Findings

1. **No single model dominates all categories** — 6 different models lead 9 category pools
2. **Same-family rating bias is real in all directions** — ranges from +0.91 (Qwen) to −1.02 (Mistral), all statistically significant
3. **Top 4 models are statistically indistinguishable** — overlapping bootstrap confidence intervals (p > 0.07)
4. **Judge disagreement is category-dependent** — code σ=1.27 vs meta-alignment σ=0.71
5. **Overall inter-annotator agreement**: Krippendorff's α = 0.618

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
