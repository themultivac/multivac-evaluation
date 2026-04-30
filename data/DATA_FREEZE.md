# Multivac Paper Dataset Freeze

This directory contains the frozen dataset used for the empirical evaluation
in *The Multivac: Blind Peer Matrix Evaluation of Frontier Language Models*.

## Dataset Details

- **Freeze cutoff:** April 3, 2026 (timestamp of the latest EVAL batch)
- **Paper tables generated:** April 12, 2026
- **Total evaluation batches:** 286 (all EVAL-* prefixed directories)
- **Unique questions:** 198
- **Unique models:** 55
- **Category pools:** 9 (code, analysis, communication, reasoning,
  meta_alignment, edge_cases, SLM, MiniMax, Qwen)

## Judgment Counts

- **Total judgments:** 27,540
- **Valid judgments (after self-exclusion):** 22,254
- **Self-excluded judgments:** 5,286

Self-exclusion criteria are defined per-batch in each `results.json` file's
`meta_analysis` field. The valid-judgment count reflects these criteria
applied across all 286 batches.

## Reproduction

To reproduce the paper's empirical numbers, run:

```bash
cd ../paper_tables
python extract_multivac_data.py ../data/
```

The script writes summary statistics to `paper_tables/dataset_stats.json`.
Expected values:

| Metric                 | Value  |
| ---------------------- | ------ |
| Total judgments        | 27,540 |
| Valid judgments        | 22,254 |
| Self-excluded          |  5,286 |
| Evaluation batches     |    286 |
| Unique questions       |    198 |
| Unique models          |     55 |
| Category pools         |      9 |

## Scope

This directory contains *only* the frozen paper dataset. Post-freeze
experiments are deliberately excluded to keep the paper's empirical claims
reproducible against a fixed snapshot. Excluded batch types:

- `ENT-BATCH-*` — Cohere enterprise evaluation (April 26, post-freeze)
- `FRONTIER-Q1-*` — Q1 2026 frontier model fill (April 28, post-freeze)
- `PHYSICS-SYNTH-*` — Physics synthesis protocol (separate paper in preparation)
- `H2H-BATCH-*`, `GEMMA4-*`, `OPUS47-*`, `MINIMAX-*`, `QWEN-*`, `SLM-*` — head-to-head and specialty batches not part of the peer-matrix dataset

These experiments are tracked in separate repositories or will appear in
follow-up papers.

## Directory Structure

Each `EVAL-*` batch contains:

- `results.json` — full evaluation results, including the `judgments` array
  and per-batch `meta_analysis` field
- `report.md` — human-readable summary (may be empty for some batches)
- `model_metadata.json` — model configuration (present in most batches)
- `summary.json` — batch-level summary statistics (present in some batches)

Per-question and raw-response subdirectories (`per_question/`,
`per_contestant/`, `raw_responses/`) have been excluded from the public repo
for size reasons. All numbers in the paper are derived from `results.json`
files, which contain everything needed for verification.

## Stability

This dataset is intended to remain static. Any future revisions to the
paper that change these numbers will be accompanied by a new DATA_FREEZE
date and a corresponding commit in this repository.

## Note on `model_metadata.json`

This file is present in batches from approximately April 2026 onward
(when the metadata-emission feature was added to the eval pipeline) and
absent from earlier batches (February and March 2026). All numbers in
the paper are derived from `results.json`, which is present in every
batch and contains everything needed for verification. The presence or
absence of `model_metadata.json` does not affect reproducibility.
