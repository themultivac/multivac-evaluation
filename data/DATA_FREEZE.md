# Multivac Paper Dataset Freeze

This directory contains the frozen dataset used for the Multivac paper's empirical evaluation.

## Dataset Details

- **Freeze cutoff**: April 3, 2026 (latest EVAL batch timestamp)
- **Paper tables generated**: April 12, 2026
- **Total evaluation batches**: 286 (all EVAL-* prefixed directories)

## Reproduction

To reproduce the paper's empirical results (Tables 1-4), run:

```bash
cd ../paper_tables
python extract_multivac_data.py ../data/
```

Expected output:
- Total evaluations: 27,540
- Unique questions: 22,254
- Unique contestants: 5,286
- Total batches: 286
- Unique models: 55
- Evaluation categories: 9

## Important Notes

1. This directory contains ONLY the frozen paper dataset (286 EVAL-* batches).

2. Post-freeze experiments are NOT included here:
   - Cohere ENT-45 batches (ENT-BATCH-*)
   - Q1 2026 frontier model fills (FRONTIER-Q1-*)
   - Physics synthesis experiments (PHYSICS-SYNTH-*)
   - Other experimental batches (GEMMA4-*, OPUS47-*, H2H-BATCH-*, etc.)

3. To maintain verifiability, this dataset should remain static. Any new experiments should be stored elsewhere.

## Directory Structure

Each EVAL-* batch contains:
- `results.json`: Complete evaluation results
- `report.md`: Human-readable summary (may be empty)
- `model_metadata.json`: Model configuration (if applicable)
- `summary.json`: Batch summary statistics (if applicable)

Note: `raw_responses/` and `per_question/` subdirectories have been excluded to keep repository size manageable. The complete results in `results.json` contain all necessary data for verification.