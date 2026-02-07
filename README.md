# The Multivac - AI Model Evaluation Dataset

**A 10×10 peer matrix evaluation dataset for frontier AI model assessment**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dataset: Phase 2](https://img.shields.io/badge/Dataset-Phase%202-blue.svg)](./data/)

## Overview

The Multivac is a novel AI evaluation methodology where models evaluate each other in a **10×10 peer matrix**. Each question receives 10 model responses, and each model judges all 9 other responses, creating a comprehensive cross-evaluation matrix of 90 judgments per question.

**Key Innovation**: Unlike human-evaluated benchmarks, The Multivac uses AI-to-AI peer evaluation to measure model performance across diverse capabilities, reducing human bottlenecks while maintaining rigorous standards.

## Dataset Statistics

- **Phase**: Phase 2 (60-question baseline)
- **Questions**: 60 curated evaluation prompts
- **Categories**: 6 specialized domains (Code, Reasoning, Analysis, Communication, Meta-Alignment, Edge Cases)
- **Model Pool**: 10 frontier models per category (category-optimized selection)
- **Total Evaluations**: 60 questions × 100 judgments = 6,000 model-to-model evaluations
- **Coverage**: ~5,400 valid peer judgments (self-judgments excluded)

## Methodology

### 10×10 Peer Matrix

For each question:
1. **Response Generation**: 10 models generate independent responses
2. **Peer Judging**: Each model evaluates all other responses (9 judgments per judge)
3. **Scoring**: 5 weighted criteria (correctness 25%, completeness 20%, clarity 20%, depth 20%, usefulness 15%)
4. **Ranking**: Aggregate scores determine final rankings
5. **Meta-Analysis**: Judge strictness, agreement rates, and bias detection

### Category-Specific Model Pools

Models are selected per category based on domain expertise:
- **Code**: Top programming models (SWE-Bench, agentic coding benchmarks)
- **Reasoning**: Logic, probability, game theory specialists  
- **Analysis**: Research critique, data quality, competitive analysis
- **Communication**: Technical writing, explanation, audience adaptation
- **Meta-Alignment**: Uncertainty calibration, self-critique, honesty
- **Edge Cases**: Context handling, instruction following, adversarial robustness

### Contamination Resistance

- **Novel questions**: Custom-designed prompts not in training data
- **Meta-evaluation questions**: Test honesty, not just capability
- **Adversarial formats**: Unicode edge cases, conflicting instructions
- **Peer validation**: Cross-model agreement detects gaming

## Repository Structure
```
multivac-evaluation/
├── README.md                  # This file
├── data/
│   ├── evaluations/           # 60 evaluation JSONs (one per question)
│   ├── aggregated.json        # Combined dataset
│   └── tracker.json           # Cumulative model statistics
├── analysis/
│   ├── rankings.csv           # Model rankings per question
│   ├── judge_bias.csv         # Judge strictness analysis
│   └── statistics.ipynb       # Analysis notebook (coming soon)
├── paper/
│   ├── methodology.md         # Detailed methodology
│   └── results.md             # Phase 2 findings
├── scripts/
│   ├── multivac.py            # Evaluation engine
│   ├── questions.py           # Question bank
│   ├── category_loader.py    # Model pool manager
│   └── aggregate_data.py      # Data aggregation script
├── .gitignore
└── LICENSE
```

## Quick Start

### Viewing Results
```bash
# Clone the repository
git clone https://github.com/themultivac/multivac-evaluation.git
cd multivac-evaluation

# View aggregated results
cat data/aggregated.json

# Analyze specific evaluation
cat data/evaluations/EVAL-*/results.json
```

### Running Evaluations (Requires API Keys)
```bash
# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Edit .env with your OPENROUTER_API_KEY and XAI_API_KEY

# Run single evaluation
python scripts/multivac.py --question-id CODE-001

# List available questions
python scripts/multivac.py --list-questions

# Interactive mode
python scripts/multivac.py --interactive
```

## Data Format

### Evaluation Result Schema
```json
{
  "evaluation_id": "EVAL-20260207-130753",
  "timestamp": "2026-02-07T13:07:53.252687",
  "question_id": "META-001",
  "category": "meta_alignment",
  "models_used": ["claude_opus", "gemini_3_pro", ...],
  "responses": [
    {
      "model_key": "claude_opus",
      "model_name": "Claude Opus 4.5",
      "response": "...",
      "generation_time_ms": 9381,
      "tokens_used": 379
    }
  ],
  "judgments": [
    {
      "judge_key": "gemini_3_pro",
      "respondent_key": "claude_opus",
      "correctness": 10,
      "completeness": 9,
      "weighted_score": 9.6,
      "brief_justification": "..."
    }
  ],
  "rankings": {
    "claude_opus": {
      "rank": 1,
      "average_score": 9.43,
      "std_dev": 0.51
    }
  },
  "meta_analysis": {
    "judge_strictness": {...},
    "strictest_judge": "gpt_codex",
    "most_lenient_judge": "gemini_3_flash"
  }
}
```

## Key Findings (Phase 2)

### Overall Model Performance

*Full analysis in `paper/results.md`*

**Top Performers by Category:**
- **Code**: Grok Code Fast 1, Claude Opus 4.5, Gemini 3 Flash
- **Reasoning**: GPT-OSS-120B, Claude Opus 4.5, DeepSeek V3.2
- **Meta-Alignment**: GPT-OSS-120B, Grok 4.1 Fast, MiMo-V2-Flash

### Judge Behavior Patterns

- **Strictest Judges**: GPT-5.2-Codex, Claude Opus 4.5 (avg scores: 8.0-8.1/10)
- **Most Lenient**: Gemini models (avg scores: 9.8-10.0/10)
- **Agreement Rate**: 67% within 1-point range across judges
- **Self-Exclusion**: All 600 self-judgments correctly excluded

## Citation

If you use this dataset in your research, please cite:
```bibtex
@dataset{multivac2026phase2,
  title={The Multivac: A 10×10 Peer Matrix Evaluation Dataset for Frontier AI Models},
  author={Darji, Yash and Patel, Meet},
  year={2026},
  month={February},
  publisher={GitHub},
  url={https://github.com/themultivac/multivac-evaluation},
  note={Phase 2: 60-question baseline evaluation}
}
```

## Reproducibility

### Verification Steps

1. **Response Consistency**: Re-run evaluations and compare response variance
2. **Judge Agreement**: Calculate inter-judge reliability (Krippendorff's alpha)
3. **Contamination Check**: Search training data for question text matches
4. **Temporal Stability**: Track rankings across weekly re-evaluations

### Known Limitations

- **Temperature Variance**: Models use temperature=0.7 (responses not deterministic)
- **Judge Bias**: Models may favor responses similar to their own style
- **Cost Constraints**: Full 10×10 matrix costly (~$0.35/question with OpenRouter)
- **Prompt Sensitivity**: Small wording changes can affect rankings

## Roadmap

### Phase 3 (Q1 2026)
- Domain specialization (10 questions each: medical, legal, financial, scientific)
- Extended model pool (15-20 models per category)
- Longitudinal tracking (monthly re-evaluation)

### Phase 4 (Q2 2026)
- Multimodal evaluation (vision, audio)
- Multi-turn conversation assessment
- Contamination detection tooling

## Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines.

**Areas for contribution:**
- New question categories
- Analysis scripts (bias detection, agreement matrices)
- Visualization tools
- Replication studies

## License

This dataset is released under the [MIT License](LICENSE).

**Code**: MIT License  
**Data**: CC BY 4.0  
**Questions**: CC BY 4.0

## Contact

- **Project**: [The Multivac](https://multivac.com)
- **Authors**: Yash Darji, Meet Patel
- **Email**: contact@multivac.com
- **Issues**: [GitHub Issues](https://github.com/themultivac/multivac-evaluation/issues)

## Acknowledgments

- OpenRouter for API access to frontier models
- xAI for Grok API access
- Claude, GPT, Gemini, and other model teams for building evaluation-worthy systems

---

**Last Updated**: February 7, 2026  
**Dataset Version**: Phase 2.0  
**Status**: ✅ Complete (60/60 questions)
