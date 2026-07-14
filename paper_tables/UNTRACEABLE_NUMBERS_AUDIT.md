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

## C. RESOLVED — re-run and VERIFIED this session (`evaluation_framework/statistical_analysis.py`)
- **Krippendorff's α = 0.618** (README #5) — computed 0.6177. ✓ Kept.
- **"Top four statistically indistinguishable, p>0.07"** (README #3, corrected-sections abstract) —
  reproduced exactly: rank-1 (Grok 4.1 Fast) is n.s. vs ranks 2–4 (p=0.266/0.073/0.071) but
  significant vs rank 5 (Mistral, p=0.027). ✓ `[VERIFY]` removed. *(Caveat: this uses the naive
  aggregate that §5.5 shows is leniency-confounded; the "indistinguishable" conclusion still holds.)*

---

## D. RESOLVED — scripted and VERIFIED this session (`scripts/judge_leniency_stats.py`)
Judges-page per-individual-judge stats, all reproduced from the frozen data:
- **GPT-5.4 mean 7.19** → 7.187 ✓ · **SD 2.22** → 2.215 ✓
- **Mistral Small mean 9.70** → 9.695 ✓
- **Granite 4.0 Micro SD 0.49** → 0.488 ✓
- **"2.5-point spread"** → 7.187→9.695 = 2.508 within the 15-frontier set ✓

One nuance to keep honest: Mistral Small is "most lenient" only within the curated frontier set;
across all 48 judges, Gemini 2.5 Flash-Lite (9.77) is higher. The page's "15 frontier LLMs"
framing makes the claim defensible. **Kept, now traceable.**

---

## E. Internal working notes still carrying old counts (not published; left as-is)
- `ADR029_Multivac_Paper_Resubmission_Strategy.md`
- `inventory_for_resume.md`
- `Multivac/v5/multivac_v5/post_freeze_summary.md`, `outputs/extract_inventory.py`
- `multivac-app/AUDIT_REPORT.md` (historical audit report)

Not corrected because they are personal/working artifacts, not published surfaces. Flag if you
want them swept too.
