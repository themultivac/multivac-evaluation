#!/usr/bin/env python3
"""
The Multivac — Research Paper Data Extraction Pipeline
Extracts all evaluation data from EVAL-* and H2H-BATCH-* folders,
generates tables for Sections 5.1–5.5 of the NeurIPS paper.

Usage:
    python3 extract_multivac_data.py /path/to/outputs/
    
Outputs:
    paper_tables/  directory with CSVs and markdown tables
"""

import json
import os
import sys
import csv
from collections import defaultdict
from pathlib import Path
import statistics

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"  WARN: Failed to load {path}: {e}")
        return None

# ─────────────────────────────────────────────
# PHASE 1: Load all EVAL-* peer matrix data
# ─────────────────────────────────────────────
def load_eval_data(outputs_dir):
    """Load all EVAL-* folders (peer matrix evaluations)."""
    evals = []
    eval_dirs = sorted([
        d for d in os.listdir(outputs_dir)
        if d.startswith("EVAL-") and os.path.isdir(os.path.join(outputs_dir, d))
    ])
    print(f"Found {len(eval_dirs)} EVAL-* directories")
    
    for ed in eval_dirs:
        rpath = os.path.join(outputs_dir, ed, "results.json")
        if not os.path.exists(rpath):
            continue
        data = load_json(rpath)
        if data is None:
            continue
        evals.append(data)
    
    print(f"Successfully loaded {len(evals)} EVAL results")
    return evals

# ─────────────────────────────────────────────
# PHASE 2: Load all H2H-BATCH-* data
# ─────────────────────────────────────────────
def load_h2h_data(outputs_dir):
    """Load all H2H batch folders."""
    h2h_questions = []
    h2h_summaries = []
    
    h2h_dirs = sorted([
        d for d in os.listdir(outputs_dir)
        if ("H2H" in d or "BATCH" in d) and os.path.isdir(os.path.join(outputs_dir, d))
        and not d.startswith("EVAL-")
    ])
    print(f"Found {len(h2h_dirs)} H2H/BATCH directories")
    
    for hd in h2h_dirs:
        hpath = os.path.join(outputs_dir, hd)
        for fname in sorted(os.listdir(hpath)):
            fpath = os.path.join(hpath, fname)
            if not fname.endswith(".json"):
                continue
            data = load_json(fpath)
            if data is None:
                continue
            if "summary" in fname.lower():
                data["_batch_dir"] = hd
                h2h_summaries.append(data)
            elif "contestants" in data:
                data["_batch_dir"] = hd
                h2h_questions.append(data)
    
    print(f"Loaded {len(h2h_questions)} H2H questions, {len(h2h_summaries)} summaries")
    return h2h_questions, h2h_summaries

# ─────────────────────────────────────────────
# TABLE 5.1: Overall Cross-Category Rankings
# ─────────────────────────────────────────────
def generate_overall_rankings(evals):
    """Aggregate model scores across all evaluations."""
    model_scores = defaultdict(list)  # model_key -> [weighted_scores]
    model_ranks = defaultdict(list)   # model_key -> [ranks per eval]
    model_wins = defaultdict(int)     # model_key -> count of rank=1
    model_top3 = defaultdict(int)     # model_key -> count of rank<=3
    model_names = {}
    
    for ev in evals:
        rankings = ev.get("rankings", {})
        for mk, rd in rankings.items():
            model_names[mk] = rd.get("display_name", mk)
            avg = rd.get("average_score")
            rank = rd.get("rank")
            if avg is not None and avg > 0:
                model_scores[mk].append(avg)
            if rank is not None:
                model_ranks[mk].append(rank)
                if rank == 1:
                    model_wins[mk] += 1
                if rank <= 3:
                    model_top3[mk] += 1
    
    # Build table
    rows = []
    for mk in model_scores:
        scores = model_scores[mk]
        ranks = model_ranks[mk]
        rows.append({
            "model_key": mk,
            "display_name": model_names.get(mk, mk),
            "avg_score": round(statistics.mean(scores), 3) if scores else 0,
            "median_score": round(statistics.median(scores), 3) if scores else 0,
            "std_score": round(statistics.stdev(scores), 3) if len(scores) > 1 else 0,
            "evaluations": len(scores),
            "avg_rank": round(statistics.mean(ranks), 2) if ranks else 0,
            "wins_rank1": model_wins[mk],
            "top3_finishes": model_top3[mk],
        })
    
    rows.sort(key=lambda r: r["avg_score"], reverse=True)
    return rows

# ─────────────────────────────────────────────
# TABLE 5.2: Category-Specific Rankings
# ─────────────────────────────────────────────
def generate_category_rankings(evals):
    """Per-category model rankings."""
    # category -> model_key -> [scores]
    cat_scores = defaultdict(lambda: defaultdict(list))
    model_names = {}
    
    for ev in evals:
        cat = ev.get("category", "unknown").lower()
        rankings = ev.get("rankings", {})
        for mk, rd in rankings.items():
            model_names[mk] = rd.get("display_name", mk)
            avg = rd.get("average_score")
            if avg is not None and avg > 0:
                cat_scores[cat][mk].append(avg)
    
    result = {}
    for cat in sorted(cat_scores.keys()):
        models = []
        for mk, scores in cat_scores[cat].items():
            models.append({
                "model_key": mk,
                "display_name": model_names.get(mk, mk),
                "avg_score": round(statistics.mean(scores), 3),
                "eval_count": len(scores),
                "std": round(statistics.stdev(scores), 3) if len(scores) > 1 else 0,
            })
        models.sort(key=lambda m: m["avg_score"], reverse=True)
        result[cat] = models
    
    return result

# ─────────────────────────────────────────────
# TABLE 5.3: Judge Behavior Analysis
# ─────────────────────────────────────────────
def generate_judge_analysis(evals):
    """Judge strictness/leniency across all evaluations."""
    # judge_key -> [scores_given]
    judge_scores = defaultdict(list)
    judge_names = {}
    
    for ev in evals:
        judgments = ev.get("judgments", [])
        for j in judgments:
            jk = j.get("judge_key")
            rk = j.get("respondent_key")
            ws = j.get("weighted_score")
            err = j.get("error")
            if jk and rk and jk != rk and ws and ws > 0 and not err:
                judge_scores[jk].append(ws)
                judge_names[jk] = j.get("judge_name", jk)
    
    rows = []
    for jk, scores in judge_scores.items():
        rows.append({
            "judge_key": jk,
            "judge_name": judge_names.get(jk, jk),
            "avg_score_given": round(statistics.mean(scores), 3),
            "median_score_given": round(statistics.median(scores), 3),
            "std": round(statistics.stdev(scores), 3) if len(scores) > 1 else 0,
            "total_judgments": len(scores),
            "min_given": round(min(scores), 2),
            "max_given": round(max(scores), 2),
        })
    
    rows.sort(key=lambda r: r["avg_score_given"])  # strictest first
    return rows

# ─────────────────────────────────────────────
# TABLE 5.4: Disagreement Patterns
# ─────────────────────────────────────────────
def generate_disagreement_analysis(evals):
    """Per-category agreement rates and cross-judge disagreement."""
    # For each eval, compute std of scores per respondent (judge disagreement)
    cat_disagreement = defaultdict(list)  # category -> [stdev values]
    
    # Also: pairwise judge agreement
    # judge_pair -> [agree/disagree on ranking]
    
    for ev in evals:
        cat = ev.get("category", "unknown").lower()
        judgments = ev.get("judgments", [])
        
        # Group scores by respondent
        resp_scores = defaultdict(dict)  # respondent -> {judge: score}
        for j in judgments:
            jk = j.get("judge_key")
            rk = j.get("respondent_key")
            ws = j.get("weighted_score")
            err = j.get("error")
            if jk and rk and jk != rk and ws and ws > 0 and not err:
                resp_scores[rk][jk] = ws
        
        # Compute per-respondent score stdev (measure of judge disagreement)
        for rk, judge_dict in resp_scores.items():
            if len(judge_dict) >= 3:
                scores = list(judge_dict.values())
                cat_disagreement[cat].append(statistics.stdev(scores))
    
    # Aggregate
    rows = []
    for cat in sorted(cat_disagreement.keys()):
        stds = cat_disagreement[cat]
        rows.append({
            "category": cat,
            "avg_judge_disagreement_std": round(statistics.mean(stds), 3) if stds else 0,
            "median_disagreement_std": round(statistics.median(stds), 3) if stds else 0,
            "sample_count": len(stds),
        })
    rows.sort(key=lambda r: r["avg_judge_disagreement_std"], reverse=True)
    return rows

# ─────────────────────────────────────────────
# TABLE 5.5: Self-Enhancement Bias Detection
# ─────────────────────────────────────────────
def generate_self_bias_analysis(evals):
    """Check if models score themselves higher (self-judgments should be excluded,
    but if any leaked through, detect the pattern).
    
    Instead: compare how judge X rates model Y vs how other judges rate model Y.
    Look for systematic over/under-rating of same-family models.
    """
    # judge_key -> respondent_key -> [scores]
    judge_resp_scores = defaultdict(lambda: defaultdict(list))
    
    for ev in evals:
        judgments = ev.get("judgments", [])
        for j in judgments:
            jk = j.get("judge_key")
            rk = j.get("respondent_key")
            ws = j.get("weighted_score")
            err = j.get("error")
            if jk and rk and jk != rk and ws and ws > 0 and not err:
                judge_resp_scores[jk][rk].append(ws)
    
    # Define model families
    families = {
        "anthropic": ["claude_opus_46", "claude_sonnet_46"],
        "openai": ["gpt_5_4", "gpt_oss_120b"],
        "google": ["gemini_31_pro"],
        "xai": ["grok_420"],
        "deepseek": ["deepseek_v4"],
        "xiaomi": ["mimo_v2_flash"],
        "mistral": ["mistral_small_creative"],
        "bytedance": ["seed_16_flash"],
    }
    
    model_to_family = {}
    for fam, models in families.items():
        for m in models:
            model_to_family[m] = fam
    
    # For each judge, compute avg score given to same-family vs other-family
    rows = []
    for jk in judge_resp_scores:
        j_family = model_to_family.get(jk, "unknown")
        same_fam_scores = []
        other_fam_scores = []
        for rk, scores in judge_resp_scores[jk].items():
            r_family = model_to_family.get(rk, "unknown")
            if r_family == j_family and jk != rk:
                same_fam_scores.extend(scores)
            else:
                other_fam_scores.extend(scores)
        
        if same_fam_scores and other_fam_scores:
            rows.append({
                "judge": jk,
                "family": j_family,
                "avg_same_family": round(statistics.mean(same_fam_scores), 3),
                "avg_other_family": round(statistics.mean(other_fam_scores), 3),
                "same_family_bias": round(
                    statistics.mean(same_fam_scores) - statistics.mean(other_fam_scores), 3
                ),
                "n_same": len(same_fam_scores),
                "n_other": len(other_fam_scores),
            })
    
    rows.sort(key=lambda r: r["same_family_bias"], reverse=True)
    return rows

# ─────────────────────────────────────────────
# DIMENSION BREAKDOWN (for appendix)
# ─────────────────────────────────────────────
def generate_dimension_breakdown(evals):
    """Per-model breakdown by scoring dimension."""
    dims = ["correctness", "completeness", "clarity", "depth", "usefulness"]
    model_dims = defaultdict(lambda: defaultdict(list))
    model_names = {}
    
    for ev in evals:
        for j in ev.get("judgments", []):
            jk = j.get("judge_key")
            rk = j.get("respondent_key")
            err = j.get("error")
            if jk and rk and jk != rk and not err:
                model_names[rk] = j.get("respondent_name", rk)
                for dim in dims:
                    val = j.get(dim)
                    if val and val > 0:
                        model_dims[rk][dim].append(val)
    
    rows = []
    for mk in model_dims:
        row = {"model_key": mk, "display_name": model_names.get(mk, mk)}
        for dim in dims:
            vals = model_dims[mk][dim]
            row[f"{dim}_avg"] = round(statistics.mean(vals), 3) if vals else 0
            row[f"{dim}_n"] = len(vals)
        rows.append(row)
    
    rows.sort(key=lambda r: r.get("correctness_avg", 0), reverse=True)
    return rows

# ─────────────────────────────────────────────
# DATASET STATISTICS (for Section 4)
# ─────────────────────────────────────────────
def generate_dataset_stats(evals, h2h_questions, h2h_summaries):
    """Summary statistics for the paper."""
    categories = defaultdict(int)
    total_judgments = 0
    valid_judgments = 0
    models_seen = set()
    questions_seen = set()
    
    for ev in evals:
        cat = ev.get("category", "unknown")
        categories[cat] += 1
        questions_seen.add(ev.get("question_id", ""))
        for m in ev.get("models_used", []):
            models_seen.add(m)
        meta = ev.get("meta_analysis", {})
        total_judgments += meta.get("total_judgments", 0)
        valid_judgments += meta.get("valid_judgments", 0)
    
    return {
        "total_peer_matrix_evals": len(evals),
        "unique_questions": len(questions_seen),
        "categories": dict(categories),
        "total_judgments": total_judgments,
        "valid_judgments": valid_judgments,
        "self_excluded": total_judgments - valid_judgments,
        "unique_models": len(models_seen),
        "models": sorted(models_seen),
        "h2h_questions": len(h2h_questions),
        "h2h_batches": len(h2h_summaries),
    }

# ─────────────────────────────────────────────
# OUTPUT HELPERS
# ─────────────────────────────────────────────
def write_csv(rows, path, fieldnames=None):
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  Written: {path}")

def write_markdown_table(rows, path, title=""):
    if not rows:
        return
    keys = list(rows[0].keys())
    with open(path, "w") as f:
        if title:
            f.write(f"## {title}\n\n")
        f.write("| " + " | ".join(keys) + " |\n")
        f.write("| " + " | ".join(["---"] * len(keys)) + " |\n")
        for r in rows:
            f.write("| " + " | ".join(str(r.get(k, "")) for k in keys) + " |\n")
    print(f"  Written: {path}")

def write_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Written: {path}")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_multivac_data.py /path/to/outputs/")
        sys.exit(1)
    
    outputs_dir = sys.argv[1]
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paper_tables")
    os.makedirs(out_dir, exist_ok=True)
    
    print("=" * 60)
    print("THE MULTIVAC — Paper Data Extraction Pipeline")
    print("=" * 60)
    
    # Load data
    print("\n[1/2] Loading EVAL-* peer matrix data...")
    evals = load_eval_data(outputs_dir)
    
    print("\n[2/2] Loading H2H batch data...")
    h2h_questions, h2h_summaries = load_h2h_data(outputs_dir)
    
    if not evals:
        print("ERROR: No EVAL data found!")
        sys.exit(1)
    
    # Generate tables
    print("\n" + "=" * 60)
    print("GENERATING TABLES")
    print("=" * 60)
    
    # Dataset stats
    print("\n--- Dataset Statistics (Section 4) ---")
    stats = generate_dataset_stats(evals, h2h_questions, h2h_summaries)
    write_json(stats, os.path.join(out_dir, "dataset_stats.json"))
    print(f"  Peer matrix evals: {stats['total_peer_matrix_evals']}")
    print(f"  Unique questions: {stats['unique_questions']}")
    print(f"  Categories: {stats['categories']}")
    print(f"  Total judgments: {stats['total_judgments']}")
    print(f"  Valid judgments (self-excluded): {stats['valid_judgments']}")
    print(f"  Unique models: {stats['unique_models']}")
    print(f"  H2H questions: {stats['h2h_questions']}")
    
    # Table 5.1
    print("\n--- Table 5.1: Overall Rankings ---")
    overall = generate_overall_rankings(evals)
    write_csv(overall, os.path.join(out_dir, "table_5_1_overall_rankings.csv"))
    write_markdown_table(overall, os.path.join(out_dir, "table_5_1_overall_rankings.md"),
                        "Table 5.1: Cross-Category Model Rankings")
    
    # Table 5.2
    print("\n--- Table 5.2: Category-Specific Rankings ---")
    cat_ranks = generate_category_rankings(evals)
    write_json(cat_ranks, os.path.join(out_dir, "table_5_2_category_rankings.json"))
    # Also write per-category markdown
    for cat, models in cat_ranks.items():
        write_markdown_table(
            models[:10],  # top 10 per category
            os.path.join(out_dir, f"table_5_2_{cat}.md"),
            f"Table 5.2: Top Models — {cat.title()}"
        )
    
    # Table 5.3
    print("\n--- Table 5.3: Judge Behavior ---")
    judges = generate_judge_analysis(evals)
    write_csv(judges, os.path.join(out_dir, "table_5_3_judge_behavior.csv"))
    write_markdown_table(judges, os.path.join(out_dir, "table_5_3_judge_behavior.md"),
                        "Table 5.3: Judge Strictness Distribution")
    
    # Table 5.4
    print("\n--- Table 5.4: Disagreement Patterns ---")
    disagree = generate_disagreement_analysis(evals)
    write_csv(disagree, os.path.join(out_dir, "table_5_4_disagreement.csv"))
    write_markdown_table(disagree, os.path.join(out_dir, "table_5_4_disagreement.md"),
                        "Table 5.4: Judge Disagreement by Category")
    
    # Table 5.5
    print("\n--- Table 5.5: Family Bias Analysis ---")
    bias = generate_self_bias_analysis(evals)
    write_csv(bias, os.path.join(out_dir, "table_5_5_family_bias.csv"))
    write_markdown_table(bias, os.path.join(out_dir, "table_5_5_family_bias.md"),
                        "Table 5.5: Same-Family Rating Bias")
    
    # Appendix: Dimension Breakdown
    print("\n--- Appendix: Dimension Breakdown ---")
    dims = generate_dimension_breakdown(evals)
    write_csv(dims, os.path.join(out_dir, "appendix_dimension_breakdown.csv"))
    
    # H2H Summaries
    print("\n--- H2H Batch Summaries ---")
    for s in h2h_summaries:
        write_json(s, os.path.join(out_dir, f"h2h_{s.get('_batch_dir', 'unknown')}.json"))
    
    print("\n" + "=" * 60)
    print(f"DONE. All outputs in: {out_dir}/")
    print("=" * 60)

if __name__ == "__main__":
    main()
