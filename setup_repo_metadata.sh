#!/bin/bash
# setup_repo_metadata.sh
# Run this from inside ~/Hub/multivac-evaluation/ AFTER the rsync block.
# Creates: README.md, DATASHEET.md, LICENSE, CITATION.cff

set -e

# ─────────────────────────────────────────────
# LICENSE
# ─────────────────────────────────────────────
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 Yash Darji

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), and the
accompanying dataset ("Dataset"), to deal in the Software and Dataset without
restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software and
Dataset, and to permit persons to whom the Software and Dataset are furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software and Dataset.

When using the Dataset in published research, please cite:

  Darji, Y. (2026). The Multivac: Blind Peer Matrix Evaluation of Frontier
  Language Models. arXiv preprint arXiv:[ID pending].

THE SOFTWARE AND DATASET ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR DATASET OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE OR DATASET.
EOF
echo "✓ LICENSE created"

# ─────────────────────────────────────────────
# CITATION.cff
# ─────────────────────────────────────────────
cat > CITATION.cff << 'EOF'
cff-version: 1.2.0
message: "If you use this dataset or framework, please cite it as below."
authors:
  - family-names: "Darji"
    given-names: "Yash"
    orcid: "https://orcid.org/0009-0009-6895-842X"
    email: "yashdarji2378@gmail.com"
    affiliation: "Independent Researcher"
title: "The Multivac: Blind Peer Matrix Evaluation of Frontier Language Models"
version: 1.0.0
date-released: 2026-04-12
url: "https://github.com/themultivac/multivac-evaluation"
repository-code: "https://github.com/themultivac/multivac-evaluation"
license: MIT
keywords:
  - "LLM evaluation"
  - "peer evaluation"
  - "multi-judge"
  - "model comparison"
  - "benchmark"
  - "judge disagreement"
preferred-citation:
  type: article
  authors:
    - family-names: "Darji"
      given-names: "Yash"
      orcid: "https://orcid.org/0009-0009-6895-842X"
  title: "The Multivac: Blind Peer Matrix Evaluation of Frontier Language Models"
  year: 2026
  journal: "arXiv preprint"
  url: "https://github.com/themultivac/multivac-evaluation"
EOF
echo "✓ CITATION.cff created"

# ─────────────────────────────────────────────
# README.md
# ─────────────────────────────────────────────
cat > README.md << 'EOF'
# The Multivac: Blind Peer Matrix Evaluation Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This dataset contains **27,540 LLM judgments** from a blind peer matrix evaluation of **55 frontier language models** across **286 evaluations** and **198 unique questions** in 9 category pools. Of the 27,540: **23,356 parsed successfully** and **22,252 carry a usable score** (the analysis set); **2,781** are intentional self-exclusions and **1,403** are judge failures. To our knowledge, this is the largest publicly available multi-judge LLM evaluation dataset with full provenance.

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
EOF
echo "✓ README.md created"

# ─────────────────────────────────────────────
# DATASHEET.md (NeurIPS Datasheet for Datasets)
# ─────────────────────────────────────────────
cat > DATASHEET.md << 'EOF'
# Datasheet: The Multivac Evaluation Dataset

Following Gebru et al. (2021), "Datasheets for Datasets."

## Motivation

**For what purpose was the dataset created?** To enable reproducible, multi-judge evaluation of frontier language models and to study systematic patterns in LLM-as-judge behavior including judge disagreement, family bias, and category-specific capability variation.

**Who created the dataset?** Yash Darji (Independent Researcher). Self-funded, total API cost approximately $700–850 USD.

## Composition

**What do the instances represent?** Each instance is a judgment: one LLM (judge) evaluating another LLM's (respondent's) response to a question, producing scores across five dimensions (correctness, completeness, clarity, depth, usefulness).

**How many instances?** 27,540 total judgment slots: 23,356 parsed, of which 22,252 usable-scored (analysis set); 2,781 intentional self-exclusions; 1,403 genuine judge failures. (The real self-exclusion count is 2,781, not the previously stated 5,286.)

**What data does each instance contain?** Judge identity, respondent identity, question text, response text, five dimension scores (0–10), weighted composite score, raw judgment text, error flag.

**Is any information missing?** Judgments that failed to parse into structured scores are flagged with an error field. Approximately 10% of Phase 2 judgments have parse failures; Phase 1 had ~41.5% before protocol improvements.

**Are there errors or sources of noise?** Two Phase 1 judgments contained scores of 100 (on a 0–10 scale) due to absent range clamping in the early parser. Both are explicitly flagged as `parse_error_excluded_score_over_10`.

**Is the dataset self-contained?** Yes. All questions, responses, and judgments are included.

**Does the dataset contain confidential data?** No. All data is generated by publicly available LLM APIs responding to authored questions.

## Collection Process

**How was the data acquired?** Via API calls to language model providers (OpenRouter and direct Anthropic API) between February and April 2026.

**Who was involved?** One author designed questions, configured pools, ran the pipeline. No crowdworkers or human annotators were involved.

**Were ethical reviews conducted?** No formal IRB review. The dataset contains only AI-generated text responding to authored prompts. No human subjects were involved.

## Preprocessing

**Was any preprocessing applied?** Self-judgments (diagonal of the N×N matrix) are excluded by design. Parse failures are flagged but retained for transparency. No scores were manually adjusted except two explicitly documented parse-error exclusions.

**Was raw data saved?** Yes. Raw judge output text is included in the `raw_judgment` field of each judgment record.

## Uses

**Has the dataset been used for tasks already?** Yes, for the analyses reported in the accompanying paper.

**What other tasks could it be used for?** DPO/RLHF preference pair generation, reward model training, judge calibration research, model selection for specific task types, AI safety alignment monitoring.

**Are there tasks it should not be used for?** Not for definitive claims about model safety or alignment properties — the methodology tests output quality rather than reasoning processes.

## Distribution

**How is it distributed?** Via GitHub (github.com/themultivac/multivac-evaluation) under MIT License.

**Will there be restrictions?** No. Model providers' terms of service may restrict certain uses of model outputs — users should review applicable terms.

## Maintenance

**Who maintains the dataset?** Yash Darji (Independent Researcher).

**Contact:** Via project website (app.themultivac.com) or Discord (discord.gg/QvVTPCxH).

**Will it be updated?** The evaluation framework is ongoing. Future evaluation batches may be released as dataset extensions.
EOF
echo "✓ DATASHEET.md created"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "All 4 metadata files created in: $(pwd)"
echo "═══════════════════════════════════════════════════════════"
ls -la README.md DATASHEET.md LICENSE CITATION.cff
echo ""
echo "Next steps:"
echo "  1. git add README.md DATASHEET.md LICENSE CITATION.cff"
echo "  2. git add evaluation_framework/ paper_tables/ data/"
echo "  3. git status     # verify"
echo "  4. git commit -m 'Release v1.0: paper-accompanying dataset (22,252 scored judgments, 55 models)'"
echo "  5. git tag v1.0.0"
echo "  6. git push origin main --tags"
