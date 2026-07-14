# Number-provenance audit (2026-07-13)

Grep of the whole `Mac_Multivac` tree (all repos + both sites) for figures that appear in
prose. Each is classed: **A** corrected this session · **B** superseded, needs the LaTeX source ·
**C** traceable to an existing script but not re-verified this session · **D** in NO script
(untraceable — compute or remove) · **E** internal working notes, left as-is.

The rule: a number ships only if a script in the repo produces it and it was re-run.

---

## A. Superseded numbers CORRECTED this session

### A1. Valid-judgment count 22,254 / "5,286 self-excluded" → corrected breakdown
Real breakdown (`scripts/count_reconciliation.py`): 27,540 total = 23,356 parsed / 22,252
usable-scored / 2,781 self-excluded / 1,403 genuine failures. "5,286 self-excluded" was the
mislabelled complement. Fixed in:
- `multivac-evaluation/README.md` (overview + Key Statistics table)
- `multivac-evaluation/DATASHEET.md`
- `multivac-evaluation/data/DATA_FREEZE.md` (two blocks)
- `multivac-evaluation/paper_tables/dataset_stats.json`
- `multivac-evaluation/setup_repo_metadata.sh` (generator, 3 spots)
- `themultivac.github.io/judges/index.html` (7 occurrences → 22,252)
- `multivac-app/analyze_outputs.py` (paper_claims dict)
- `multivac-app/RECONCILIATION_REPORT.md` (correction banner; report had validated the wrong 5,286)

### A2. Same-vendor bias "significant in all families" / "negative bias in Mistral & Google"
Superseded by the corrected within-response FE analysis (only Anthropic/MiniMax robust; negatives
are artifacts). Fixed in:
- `multivac-evaluation/README.md` (Key Findings #2)
- `themultivac.github.io/judges/index.html` (CTA line)
- `themultivac.github.io/papers/SUPERSEDED.md` (new dated notice for the PDF)

### A3. Smaller corrections
- "6 models top 9 pools" → **7** (by distinct model; `bradley_terry_ranking.py`) — README #1, corrected-sections abstract. *(Convention-dependent: "6" needs model-version merging.)*
- Parse stats "~10% Phase 2 / ~41.5% Phase 1" → 4.9% systematic (`parse_failure_analysis.py`) — DATASHEET.
- "code σ=1.27 vs meta-alignment σ=0.71" → 1.269 vs **0.632**, ratio 2.01× (`category_disagreement.py`) — README #4. The old 0.71 is not reproduced by the within-response-SD metric.

---

## B. Superseded, NOT fixable without the LaTeX source

- `themultivac.github.io/papers/blind-peer-matrix.pdf` — the compiled paper carries every old
  number (counts, naive bias table, "significant in all families"). It cannot be rebuilt here
  (no source in-repo). A dated `papers/SUPERSEDED.md` notice was added. **Rebuild pending your `.tex`.**

---

## C. Traceable to an EXISTING script, but NOT re-verified this session
`evaluation_framework/statistical_analysis.py` contains the functions, but they were not re-run
this session (Krippendorff needs `pip install krippendorff`), so per the "re-run before asserting"
rule they are unverified:
- **Krippendorff's α = 0.618** (README #5) — `compute_krippendorff_alpha`.
- **"Top four statistically indistinguishable, p>0.07"** (README #3, corrected-sections abstract `[VERIFY]`) — bootstrap model-ranking CIs.

Recommend: re-run and confirm, or mark as pending.

---

## D. In NO script — untraceable, must compute or remove before shipping
On `themultivac.github.io/judges/index.html` (per-**individual-judge** stats; only per-**family**
leniency is scripted, via `four_cell_decomposition.py`):
- "**2.5-point spread**" across judges (line ~634).
- Per-judge means: **GPT-5.4 7.19 / 7.2**, **Mistral Small 9.70 / 9.7** (chart + headline).
- Per-judge score SD: **GPT-5.4 2.22**, **Granite 4.0 Micro 0.49** (line ~634).

These are plausibly from an earlier per-judge analysis but no committed script reproduces them.
Left in place (not clearly wrong); flagged for you to back with a script or remove.

---

## E. Internal working notes still carrying old counts (not published; left as-is)
- `ADR029_Multivac_Paper_Resubmission_Strategy.md`
- `inventory_for_resume.md`
- `Multivac/v5/multivac_v5/post_freeze_summary.md`, `outputs/extract_inventory.py`
- `multivac-app/AUDIT_REPORT.md` (historical audit report)

Not corrected because they are personal/working artifacts, not published surfaces. Flag if you
want them swept too.
