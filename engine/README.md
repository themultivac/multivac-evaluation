# The Multivac — Evaluation Engine

Blind peer evaluation of AI models. One prompt, all models, blind judging.
Insufficient data for a meaningful answer... but every eval gets us closer.

## Quick Start
```bash
git clone https://github.com/themultivac/multivac-evaluation.git
cd multivac-evaluation/engine
cp .env.example .env
# Edit .env and add your API keys
pip install -r requirements.txt
```

### Run a single evaluation
```bash
python multivac.py --question-id CODE-011 --category code
```

### Run a batch
```bash
python orchestrate.py          # Frontier models, Wave 1
python orchestrate_slm.py      # Small language models
python orchestrate_qwen.py     # Qwen family
```

### Upload results to database (optional)
```bash
python upload_evals.py --pattern "EVAL-YYYYMMDD-*"
```

## How It Works

1. **Prompt** — All models receive the identical prompt
2. **Respond** — Each model generates a response independently
3. **Judge** — Each model scores every other model's response (blind, anonymized)
4. **Validate** — Judgments that don't follow the scoring format are dropped
5. **Aggregate** — Valid scores are averaged. Models must complete 80%+ of evals for aggregate ranking.

## Files

| File | Purpose |
|------|---------|
| `multivac.py` | Core engine: prompt, model calls, judging, scoring |
| `orchestrate.py` | Batch runner for frontier models |
| `orchestrate_slm.py` | Batch runner for SLMs |
| `orchestrate_qwen.py` | Batch runner for Qwen family |
| `category_loader.py` | Routes categories to model pools |
| `questions.py` | Wave 1 questions (60) |
| `questions_wave2_15032026.py` | Wave 2 questions (130) |
| `upload_evals.py` | Sync results to Neon database |
| `config.py` | Configuration and API settings |
| `discover_models.py` | OpenRouter model discovery utility |

## Model Pools (in /models)

| File | Pool |
|------|------|
| `code_models.py` | Frontier code models (V2) |
| `reasoning_models.py` | Frontier reasoning models |
| `analysis_models.py` | Frontier analysis models |
| `communication_models.py` | Frontier communication models |
| `meta_alignment_models.py` | Frontier meta/alignment models |
| `slm_models.py` | Small language models |
| `qwen_models.py` | Qwen family (Project Qwen) |

## Known Limitations

- **AI-as-judge**: Peer consensus, not ground truth. Human baseline study in progress.
- **Provider variance**: API quantization not controlled. Results reflect API output.
- **Inference settings**: Models may not run with recommended parameters via API.
- **Invalid judgments**: ~40% fail parsing. Improving parser and rubric clarity.
- **80% rule**: Models must complete 80%+ of evals for aggregate rankings.

## Contributing

Report bugs, suggest improvements, or submit PRs.
Join the Discord for methodology discussion and coordination.

## License

MIT — use it, modify it, run your own evals.
