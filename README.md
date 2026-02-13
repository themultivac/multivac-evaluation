<p align="center">
  <h1 align="center">🔮 The Multivac</h1>
  <p align="center"><strong>10×10 Blind Peer Matrix for AI Model Evaluation</strong></p>
  <p align="center">Every model answers. Every model judges. No single-judge bias.</p>
</p>

<p align="center">
  <a href="https://themultivac.com">Website</a> •
  <a href="https://themultivac.substack.com">Substack</a> •
  <a href="https://huggingface.co/spaces/themultivac/leaderboard">Live Leaderboard</a> •
  <a href="#methodology">Methodology</a> •
  <a href="#data">Raw Data</a>
</p>

---

### 📊 Current Stats

| Metric | Value |
|--------|-------|
| Total Evaluations | 34+ |
| Total Judgments | 1,100+ |
| Models Tested | 20+ |
| Category Pools | 6 |
| Cost Per Evaluation | ~$2-3 |
| Publication | Daily on [Substack](https://themultivac.substack.com) |

---

## The Problem

AI model benchmarks are broken:

- **Contamination**: Models train on test data. Static benchmarks become meaningless over time.
- **Single-judge bias**: GPT-4 as sole evaluator selects GPT-4-generated responses **87.76%** of the time vs. 47.61% for humans (Zheng et al., NeurIPS 2023).
- **Gaming**: Meta tested 27 private Llama-4 variants on Chatbot Arena before publishing only the best scores — inflating performance by up to 112% ([Leaderboard Illusion, April 2025](https://arxiv.org/abs/2504.20879)).
- **Aggregate blindness**: Leaderboard rankings hide category-specific strengths and weaknesses.

As models converge in capability over the next 2-3 years, the question shifts from "which model is best?" to **"which model is best for THIS specific task?"** Category-specific, multi-judge evaluation becomes the decision layer.

## The Solution

<a name="methodology"></a>

### 10×10 Blind Peer Matrix

```
Question → 10 Models Generate Responses → 10 Models Judge All 10 Responses
                                          (Self-judgments excluded)
                                                    ↓
                                          100 judgments per evaluation
                                          90 valid (diagonal excluded)
                                                    ↓
                                          Rankings + Meta-Analysis
```

**How it works:**

1. **Fresh question** selected (daily, from 60+ question bank across 6 categories)
2. **10 category-optimized models** generate responses (blind — no model knows the question is an evaluation)
3. **Same 10 models judge all 10 responses** — each judge sees only the response text, never the model identity
4. **Self-judgments excluded** — models cannot rate their own responses (diagonal of the matrix)
5. **Weighted scoring** across 5 criteria: Correctness (25%), Completeness (20%), Clarity (20%), Depth (20%), Usefulness (15%)
6. **Meta-analysis**: Judge strictness, agreement rates, sycophancy detection

### Why This Matters

- **No single-judge bias** — consensus of 9 independent judges per response
- **Fresh questions** — can't be memorized or gamed (new daily, never reused)
- **Category-specific pools** — code questions evaluated by code-optimized models, not general-purpose
- **Meta-analysis reveals judge behavior** — which models are strict? Which are lenient? Which show self-preference?

---

## Key Findings

> **No single model dominates across all categories.**

| Task | Winner | Score | Category |
|------|--------|-------|----------|
| Sycophancy Resistance | GPT-OSS-120B | 9.88 | Meta/Alignment |
| Legal Document Analysis | GPT-OSS Legal | 9.85 | Analysis |
| Async Bug Hunt | Claude Opus 4.5 | 9.49 | Code |
| Hidden Detail in Long Doc | Grok 4.1 Fast | 9.47 | Edge Cases |
| Nested JSON Parser | DeepSeek V3.2 | 9.39 | Code |
| Epistemic Calibration | Gemini 3 Flash | 9.32 | Meta/Alignment |

**Judge behavior analysis:**
- GPT-OSS-120B is consistently the strictest judge
- Mistral models tend lenient in scoring
- Some models rate themselves higher when self-judgment isn't excluded (detected via control runs)

---

## Category Pools (V5)

| Category | Day | Example Models | Focus |
|----------|-----|----------------|-------|
| Programming | Mon | Grok Code Fast, Claude Opus, DeepSeek V3.2 | Code quality, debugging, security |
| Reasoning | Tue | MiMo-V2-Flash, Claude Sonnet, Gemini 3 | Logic, math, causal analysis |
| Analysis | Wed | GPT-OSS-120B, Claude Opus, MiniMax | Data interpretation, critique |
| Communication | Thu | GPT-5.2, Claude Opus, Gemini Pro | Writing, persuasion, explanation |
| Meta/Alignment | Sat | All models | Sycophancy, calibration, honesty |
| SLMs (<48B) | Fri | Qwen 3 32B, Kimi K2, Gemma 3 27B | Efficiency vs quality |

---

<a name="data"></a>

## Data Access

### 📁 Raw Evaluation Data

Every evaluation is stored as JSON in [`/data`](./data/):

```
data/
├── tracker.json                    # Master index of all evaluations
└── evaluations/
    ├── EVAL-20260113-CODE-001/
    │   ├── results.json            # Complete results (responses + judgments + rankings)
    │   └── report.md               # Human-readable report
    ├── EVAL-20260114-REASON-001/
    └── ...
```

Each `results.json` contains:
- **Full model responses** (not just scores — you can read exactly what each model said)
- **Complete 10×10 judgment matrix** (every judge's scores + justifications for every response)
- **Rankings** with mean, min, max, and standard deviation
- **Meta-analysis** of judge strictness and agreement

### 🔍 Interactive Leaderboard

- **HuggingFace Spaces**: [huggingface.co/spaces/themultivac/leaderboard](https://huggingface.co/spaces/themultivac/leaderboard)
- **Website**: [themultivac.com/leaderboard](https://themultivac.com/leaderboard)

---

## Known Limitations

We believe in radical transparency about what this methodology can and cannot measure:

1. **LLM-as-judge concerns**: Multi-judge reduces but does not eliminate the fundamental limitation that LLMs evaluate LLMs. We are working on human correlation studies.

2. **Output alignment vs. reasoning alignment**: The current methodology primarily measures whether a response is correct and well-structured (output quality). It does not yet measure whether the model's *reasoning process* was sound or whether it demonstrated genuine epistemic calibration. V6 will add reasoning alignment as a first-class scoring criterion.

3. **Sample size**: 34 evaluations is a meaningful start but insufficient for high-confidence statistical claims about model ordering. We target 100+ evaluations for the methodology paper.

4. **Cost constraints**: Running 10×10 evaluations costs ~$2-3 each, limiting daily throughput. We prioritize question diversity over volume.

5. **Category pool selection**: Which 10 models appear in each category pool is a human decision that influences rankings. We document selection rationale in each evaluation report.

---

## Technical Stack

- **Language**: Python 3.11+ (asyncio, httpx)
- **APIs**: OpenRouter (90% of models) + xAI Direct (Grok)
- **Output**: JSON + Markdown reports
- **Publication**: Substack (daily) + GitHub (raw data)
- **Leaderboard**: Gradio on HuggingFace Spaces + DataTables.js on GitHub Pages

---

## Running Your Own Evaluations

```bash
# Clone
git clone https://github.com/themultivac/multivac-evaluations.git
cd multivac-evaluations

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your OPENROUTER_API_KEY and XAI_API_KEY

# Run a single evaluation
python multivac.py --question "Explain quicksort" --category code

# Run a pre-defined question
python multivac.py --question-id CODE-001

# List all categories and models
python multivac.py --list-categories

# Interactive mode
python multivac.py --interactive
```

---

## Citation

If you use The Multivac data or methodology in your research:

```bibtex
@misc{multivac2026,
  title={The Multivac: Blind Peer Matrix Evaluation of Frontier AI Models},
  author={Darji, Yash},
  year={2026},
  url={https://github.com/themultivac/multivac-evaluations}
}
```

---

## Roadmap

- [x] Phase 1: Foundation (21 questions, single-judge baseline)
- [x] Phase 2: 10×10 Peer Matrix (category-specific pools, meta-analysis)
- [ ] Phase 3: Data Engine (vector store, disagreement extraction, API access)
- [ ] Phase 4: Fork the Judge (open evaluation framework for custom criteria)
- [ ] Phase 5: Ship a Model (Multivec-Judge — distilled evaluation model)

---

## Links

- **Website**: [themultivac.com](https://themultivac.com)
- **Substack**: [themultivac.substack.com](https://themultivac.substack.com)
- **Leaderboard**: [HuggingFace Spaces](https://huggingface.co/spaces/themultivac/leaderboard)
- **Twitter/X**: [@themultivac](https://twitter.com/themultivac)

---

<p align="center">
  <em>One question. All frontier models. Blind peer evaluation. Daily.</em>
</p>
