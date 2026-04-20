# Physics Synthesis Protocol — Raw Data

This directory contains the full output of Multivac Physics synthesis runs: three graduate-level physics problems, each evaluated by seven frontier LLMs (Claude Opus 4.7, GPT-5.4, OpenAI o3-mini-high, Gemini 3.1 Pro Preview, DeepSeek R1, Qwen 3.6 Plus, Grok 4.20), with universal decomposer (Claude Opus 4.6) and cross-family adversarial confirmation.

Protocol version: v0.2. Run date: 2026-04-18.

Companion writeups: [multivacphysics.com](https://multivacphysics.com)

## Directory structure

Each `PHYSICS-SYNTH-*` directory is a complete run:

```
PHYSICS-SYNTH-<problem-id>-<timestamp>/
├── problem.json                    # The physics problem posed (question, ground truth, key steps)
├── full_state.json                 # Complete state snapshot (Layer 1 + 2 + 4 verdicts)
├── synthesis.json                  # Aggregated per-contestant metrics
├── SUMMARY.md                      # Human-readable summary
├── layer1_<model>_answer.txt       # Each contestant's full derivation (one per model)
├── layer2_<model>_claims.json      # Decomposed atomic claims (one per model)
├── layer2_<model>_raw.txt          # Decomposer's raw JSON response (for diagnostics)
├── layer4_<model>_verdicts.json    # Adversarial verdicts on each contestant's claims
├── layer4b_confirmations.json      # Cross-family confirmation of flagged errors
└── raw_responses/                  # Full OpenRouter response JSON for every API call
```

## The three problems

| Directory | Problem | Ground truth answer |
|---|---|---|
| `PHYSICS-SYNTH-schwarzschild-v0-*` | Schwarzschild radius from Einstein field equations | r_s = 2GM/c² |
| `rindler-unruh-v0-*` | Rindler coordinates + Unruh temperature derivation | T = ℏa/(2πck_B) |
| `PHYSICS-SYNTH-casimir-v0-*` | Casimir force between parallel plates | F/A = -π²ℏc/(240 d⁴) |

## Headline results

| Problem | Errors flagged | Errors confirmed (cross-family) | Confirmation rate |
|---|---|---|---|
| Schwarzschild | 14 | 4 | 28.6% |
| Rindler/Unruh | 21 | 7 | 33.3% |
| Casimir | 20 | 6 | 30.0% |

The ~30% cross-family confirmation rate appears stable across three graduate physics problems. Single-adversary error flags systematically overstate derivation errors by roughly 3.3x relative to cross-family confirmation.

## What this data is and is not

**What it is:** Independent cross-family peer evaluation of LLM physics reasoning. Every Layer 1 response (the full derivation), every Layer 2 atomic claim, every Layer 4 adversarial verdict, and every Layer 4b cross-family confirmation is preserved verbatim with full provenance.

**What it is not:** Symbolically verified physics. No SymPy check, no theorem prover, no expert physicist review. A "confirmed error" means two LLMs from different model families independently flagged a derivation step as wrong — it does not mean the step is mathematically incorrect. Manual verification is required before citing specific claims as physics errors.

## Known limitations

- **Stochastic verdicts.** Layer 4b sampling variance: running on the same Rindler output twice gave us 10 confirmed first time, 7 second time. Reported numbers are single-run.
- **Parse failure rate.** ~33% of Layer 4b calls returned unparseable responses (primarily from o3-mini on OpenRouter). Parse failures are treated as non-confirmations.
- **Regex-based completeness detection.** The `detect_final_answers` function uses hand-tuned regex per problem. Only Rindler/Unruh has a validated detector at this protocol version; Schwarzschild and Casimir completeness scores are marked "not auto-checked" and require manual verification.
- **Ground truth in prompt.** The final-answer check is whether the target formula string appears in the response. It does not verify the derivation constitutes a valid proof.

## Roadmap

- **Layer 3 (planned).** SymPy-based symbolic verification of algebraic claims: Christoffel symbols, dimensional analysis, tensor manipulation.
- **Protocol v0.3.** Majority-vote Layer 4b (three confirmations instead of one) to reduce sampling noise.
- **More problems.** Next batch expected within 4-6 weeks, covering Kerr metric, one-loop QED self-energy, and related graduate-level problems.

## How to cite

If you use this data in academic work, please cite the forthcoming arXiv preprint (in preparation). Until then:
Darji, Y. (2026). Multivac Physics: Cross-Family Peer Evaluation of LLM Physics Reasoning. Raw data. https://github.com/themultivac/multivac-evaluation

## License

MIT License. See `../../LICENSE`.

## Contact

If you find a methodology error, a physics error we missed, or want to propose a new problem, email yash@themultivac.com.
