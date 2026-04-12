#!/usr/bin/env python3
"""
The Multivac — Statistical Analysis Scripts
Run these on your VM against the raw evaluation data.

Usage:
    python3 statistical_analysis.py /path/to/outputs/

Generates:
    - Krippendorff's alpha (inter-annotator agreement)
    - Bootstrap confidence intervals for family bias
    - Bootstrap confidence intervals for model rankings
"""

import json
import os
import sys
import csv
import numpy as np
from collections import defaultdict
from pathlib import Path

# ─────────────────────────────────────────────
# HELPER: Load all EVAL-* data
# ─────────────────────────────────────────────
def load_all_evals(outputs_dir):
    evals = []
    for d in sorted(os.listdir(outputs_dir)):
        if d.startswith("EVAL-") and os.path.isdir(os.path.join(outputs_dir, d)):
            rpath = os.path.join(outputs_dir, d, "results.json")
            if os.path.exists(rpath):
                try:
                    with open(rpath) as f:
                        evals.append(json.load(f))
                except:
                    pass
    print(f"Loaded {len(evals)} evaluations")
    return evals


# ═════════════════════════════════════════════
# 1. KRIPPENDORFF'S ALPHA
# ═════════════════════════════════════════════
def compute_krippendorff_alpha(evals):
    """
    Compute Krippendorff's alpha across all evaluations.
    
    We treat each (evaluation, respondent) pair as an "item" and each judge 
    as a "coder". The value is the weighted_score. Self-judgments are excluded.
    
    Requires: pip install krippendorff
    """
    try:
        import krippendorff
    except ImportError:
        print("ERROR: Install krippendorff first: pip install krippendorff")
        return None

    print("\n" + "=" * 60)
    print("KRIPPENDORFF'S ALPHA (Inter-Annotator Agreement)")
    print("=" * 60)

    # Build the reliability data matrix
    # Rows = judges (coders), Columns = items (eval_id × respondent)
    # We need to handle the fact that not all judges appear in all evals
    
    all_judges = set()
    items = []  # list of (eval_idx, respondent_key)
    item_scores = {}  # (eval_idx, respondent_key, judge_key) -> score

    for eval_idx, ev in enumerate(evals):
        judgments = ev.get("judgments", [])
        for j in judgments:
            jk = j.get("judge_key")
            rk = j.get("respondent_key")
            ws = j.get("weighted_score")
            err = j.get("error")
            if jk and rk and jk != rk and ws and ws > 0 and not err:
                all_judges.add(jk)
                item_key = (eval_idx, rk)
                if item_key not in item_scores:
                    items.append(item_key)
                    item_scores[item_key] = {}
                item_scores[item_key][jk] = ws

    judges_list = sorted(all_judges)
    judge_to_idx = {j: i for i, j in enumerate(judges_list)}
    
    # Build matrix: rows = judges, cols = items
    # Use np.nan for missing values
    n_judges = len(judges_list)
    n_items = len(items)
    
    print(f"  Judges: {n_judges}")
    print(f"  Items (eval × respondent pairs): {n_items}")
    
    reliability_data = np.full((n_judges, n_items), np.nan)
    
    for col_idx, item_key in enumerate(items):
        scores_dict = item_scores[item_key]
        for jk, score in scores_dict.items():
            row_idx = judge_to_idx[jk]
            reliability_data[row_idx, col_idx] = score

    # Compute alpha
    alpha = krippendorff.alpha(
        reliability_data=reliability_data,
        level_of_measurement="interval"
    )
    
    print(f"\n  Krippendorff's α (interval) = {alpha:.4f}")
    print(f"  Interpretation:")
    if alpha >= 0.8:
        print(f"    Good agreement (α ≥ 0.8)")
    elif alpha >= 0.667:
        print(f"    Tentative agreement (0.667 ≤ α < 0.8)")
    else:
        print(f"    Low agreement (α < 0.667)")
    
    # Also compute per-category
    print(f"\n  Per-category breakdown:")
    cat_evals = defaultdict(list)
    for ev in evals:
        cat = ev.get("category", "unknown").lower()
        cat_evals[cat].append(ev)
    
    for cat in sorted(cat_evals.keys()):
        cat_items = []
        cat_item_scores = {}
        cat_judges = set()
        
        for eval_idx, ev in enumerate(cat_evals[cat]):
            for j in ev.get("judgments", []):
                jk = j.get("judge_key")
                rk = j.get("respondent_key")
                ws = j.get("weighted_score")
                err = j.get("error")
                if jk and rk and jk != rk and ws and ws > 0 and not err:
                    cat_judges.add(jk)
                    item_key = (eval_idx, rk)
                    if item_key not in cat_item_scores:
                        cat_items.append(item_key)
                        cat_item_scores[item_key] = {}
                    cat_item_scores[item_key][jk] = ws
        
        if len(cat_judges) < 2 or len(cat_items) < 2:
            continue
            
        cat_judges_list = sorted(cat_judges)
        cat_judge_to_idx = {j: i for i, j in enumerate(cat_judges_list)}
        cat_matrix = np.full((len(cat_judges_list), len(cat_items)), np.nan)
        
        for col_idx, item_key in enumerate(cat_items):
            for jk, score in cat_item_scores[item_key].items():
                row_idx = cat_judge_to_idx[jk]
                cat_matrix[row_idx, col_idx] = score
        
        try:
            cat_alpha = krippendorff.alpha(
                reliability_data=cat_matrix,
                level_of_measurement="interval"
            )
            print(f"    {cat:20s}: α = {cat_alpha:.4f} (n_items={len(cat_items)}, n_judges={len(cat_judges_list)})")
        except:
            print(f"    {cat:20s}: computation failed")
    
    return alpha


# ═════════════════════════════════════════════
# 2. BOOTSTRAP CI FOR FAMILY BIAS
# ═════════════════════════════════════════════
def bootstrap_family_bias(evals, n_bootstrap=10000):
    """
    Bootstrap confidence intervals for same-family rating bias.
    Tests whether the observed bias is statistically significant.
    """
    print("\n" + "=" * 60)
    print("BOOTSTRAP CI: SAME-FAMILY RATING BIAS")
    print("=" * 60)

    # Expanded family mapping
    families = {
        "anthropic": ["claude_opus_46", "claude_sonnet_46", "claude_opus", "claude_sonnet", "judge_claude_sonnet"],
        "openai": ["gpt_5_4", "gpt_oss_120b", "gpt_codex", "gpt_oss_legal", "judge_gpt54"],
        "google": ["gemini_31_pro", "gemini_3_flash", "gemini_3_pro", "gemini_2_5_flash", 
                    "gemini_25_flash", "gemini_2_5_flash_lite", "gemma3_27b", "gemma_3n_4b"],
        "xai": ["grok_420", "grok_direct", "grok_4_1_fast", "grok_code_fast"],
        "deepseek": ["deepseek_v4", "deepseek_v3"],
        "qwen": ["qwen3_8b", "qwen3_32b", "qwen3_coder_next", "qwen35_9b", "qwen35_27b",
                 "qwen35_35b_a3b", "qwen35_122b_a10b", "qwen35_397b_a17b"],
        "minimax": ["minimax_01", "minimax_m1", "minimax_m2", "minimax_m21", "minimax_m25", "minimax_m27"],
        "xiaomi": ["mimo_v2_flash"],
        "mistral": ["mistral_small_creative", "mistral_nemo", "devstral"],
        "bytedance": ["seed_16_flash", "seed_1_6_flash"],
        "meta": ["llama31_8b", "llama4_scout"],
    }
    
    model_to_family = {}
    for fam, models in families.items():
        for m in models:
            model_to_family[m] = fam
    
    # Collect per-judgment data: (judge_key, respondent_key, score, same_family)
    judgment_data = []
    for ev in evals:
        for j in ev.get("judgments", []):
            jk = j.get("judge_key")
            rk = j.get("respondent_key")
            ws = j.get("weighted_score")
            err = j.get("error")
            if jk and rk and jk != rk and ws and ws > 0 and not err:
                j_fam = model_to_family.get(jk, "unknown")
                r_fam = model_to_family.get(rk, "unknown")
                if j_fam != "unknown" and r_fam != "unknown":
                    same = (j_fam == r_fam)
                    judgment_data.append((jk, rk, ws, same, j_fam))
    
    print(f"  Total judgments with known families: {len(judgment_data)}")
    
    # Per-family analysis
    for fam in sorted(families.keys()):
        fam_judgments = [(jk, rk, ws, same) for jk, rk, ws, same, jf in judgment_data if jf == fam]
        same_scores = [ws for _, _, ws, same in fam_judgments if same]
        other_scores = [ws for _, _, ws, same in fam_judgments if not same]
        
        if len(same_scores) < 5 or len(other_scores) < 5:
            continue
        
        observed_bias = np.mean(same_scores) - np.mean(other_scores)
        
        # Bootstrap
        np.random.seed(42)
        bootstrap_biases = []
        for _ in range(n_bootstrap):
            boot_same = np.random.choice(same_scores, size=len(same_scores), replace=True)
            boot_other = np.random.choice(other_scores, size=len(other_scores), replace=True)
            bootstrap_biases.append(np.mean(boot_same) - np.mean(boot_other))
        
        ci_lower = np.percentile(bootstrap_biases, 2.5)
        ci_upper = np.percentile(bootstrap_biases, 97.5)
        p_value = np.mean([b <= 0 for b in bootstrap_biases]) if observed_bias > 0 else np.mean([b >= 0 for b in bootstrap_biases])
        
        sig = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "n.s."
        
        print(f"\n  {fam.upper():12s}: bias = {observed_bias:+.3f}  "
              f"95% CI [{ci_lower:+.3f}, {ci_upper:+.3f}]  "
              f"p = {p_value:.4f} {sig}")
        print(f"    same-family: n={len(same_scores)}, mean={np.mean(same_scores):.3f}")
        print(f"    other-family: n={len(other_scores)}, mean={np.mean(other_scores):.3f}")


# ═════════════════════════════════════════════
# 3. BOOTSTRAP CI FOR MODEL RANKINGS
# ═════════════════════════════════════════════
def bootstrap_ranking_ci(evals, n_bootstrap=5000):
    """
    Bootstrap confidence intervals for model rankings.
    Shows which ranking differences are statistically significant.
    """
    print("\n" + "=" * 60)
    print("BOOTSTRAP CI: MODEL RANKING STABILITY")
    print("=" * 60)

    # Collect per-evaluation scores for each model
    model_eval_scores = defaultdict(list)  # model -> [(eval_idx, avg_score)]
    model_names = {}
    
    for eval_idx, ev in enumerate(evals):
        rankings = ev.get("rankings", {})
        for mk, rd in rankings.items():
            model_names[mk] = rd.get("display_name", mk)
            avg = rd.get("average_score")
            if avg and avg > 0:
                model_eval_scores[mk].append(avg)
    
    # Only include models with 30+ evals for meaningful CIs
    eligible = {mk: scores for mk, scores in model_eval_scores.items() if len(scores) >= 30}
    print(f"  Models with ≥30 evals: {len(eligible)}")
    
    # Bootstrap mean scores
    np.random.seed(42)
    bootstrap_means = {mk: [] for mk in eligible}
    
    for _ in range(n_bootstrap):
        for mk, scores in eligible.items():
            boot = np.random.choice(scores, size=len(scores), replace=True)
            bootstrap_means[mk].append(np.mean(boot))
    
    # Compute CIs and print
    results = []
    for mk in eligible:
        means = bootstrap_means[mk]
        results.append({
            "model": mk,
            "name": model_names[mk],
            "observed_mean": np.mean(eligible[mk]),
            "ci_lower": np.percentile(means, 2.5),
            "ci_upper": np.percentile(means, 97.5),
            "n_evals": len(eligible[mk]),
        })
    
    results.sort(key=lambda r: r["observed_mean"], reverse=True)
    
    print(f"\n  {'Rank':<5s} {'Model':<30s} {'Mean':>6s} {'95% CI':>20s} {'N':>5s}")
    print(f"  {'─'*5} {'─'*30} {'─'*6} {'─'*20} {'─'*5}")
    for i, r in enumerate(results, 1):
        ci_str = f"[{r['ci_lower']:.3f}, {r['ci_upper']:.3f}]"
        print(f"  {i:<5d} {r['name']:<30s} {r['observed_mean']:>6.3f} {ci_str:>20s} {r['n_evals']:>5d}")
    
    # Pairwise significance for top-10
    print(f"\n  Pairwise significance (top 10):")
    top10 = results[:10]
    for i in range(len(top10)):
        for j in range(i+1, len(top10)):
            # Check if CIs overlap
            if top10[i]["ci_lower"] > top10[j]["ci_upper"]:
                sig = "SIGNIFICANT (no CI overlap)"
            elif top10[j]["ci_lower"] > top10[i]["ci_upper"]:
                sig = "SIGNIFICANT (no CI overlap, reversed)"
            else:
                # CIs overlap — compute bootstrap p-value
                diffs = [bootstrap_means[top10[i]["model"]][k] - bootstrap_means[top10[j]["model"]][k] 
                         for k in range(n_bootstrap)]
                p = np.mean([d <= 0 for d in diffs])
                sig = f"p = {p:.3f}" + (" *" if p < 0.05 else " n.s.")
            print(f"    {top10[i]['name'][:20]:20s} vs {top10[j]['name'][:20]:20s}: {sig}")

    return results


# ═════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 statistical_analysis.py /path/to/outputs/")
        sys.exit(1)
    
    outputs_dir = sys.argv[1]
    evals = load_all_evals(outputs_dir)
    
    if not evals:
        print("ERROR: No evaluation data found!")
        sys.exit(1)
    
    # 1. Krippendorff's alpha
    alpha = compute_krippendorff_alpha(evals)
    
    # 2. Family bias bootstrap
    bootstrap_family_bias(evals)
    
    # 3. Ranking CIs
    bootstrap_ranking_ci(evals)
    
    print("\n" + "=" * 60)
    print("DONE. Paste the output back for paper integration.")
    print("=" * 60)


if __name__ == "__main__":
    main()
