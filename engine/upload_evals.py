#!/usr/bin/env python3
"""
Multivac - Upload Evaluation Results to Neon PostgreSQL
Syncs results.json files from the eval pipeline into the SaaS database.

Usage:
    cd ~/Hub/multivac-app
    python upload_evals.py                              # Upload all new EVAL-20260315-* from pipeline
    python upload_evals.py --eval-dir ~/Multivac/v5/multivac_v5/outputs  # Custom source dir
    python upload_evals.py --eval-id EVAL-20260315-033810  # Upload one specific eval
    python upload_evals.py --dry-run                     # Show what would be uploaded
    python upload_evals.py --check-schema                # Verify DB schema compatibility

Reads DATABASE_URL from .env.local in the current directory.
"""

import json
import os
import sys
import argparse
import glob
from datetime import datetime
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    print("Install psycopg2: pip install psycopg2-binary --break-system-packages")
    sys.exit(1)

# ═══════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════

DEFAULT_EVAL_DIR = os.path.expanduser("~/Multivac/v5/multivac_v5/outputs")

# Category mapping: pipeline category names → database enum values
# Check what your DB enum allows. If 'slm' isn't in the enum, we map it.
CATEGORY_MAP = {
    "code": "code",
    "reasoning": "reasoning",
    "analysis": "analysis",
    "communication": "communication",
    "meta_alignment": "meta_alignment",
    "edge_cases": "edge_cases",
    "slm": "code",  # SLM evals: map to the question's actual category, fallback to code
}

# SLM model display names → model IDs for ai_models table
SLM_MODEL_MAP = {
    "qwen3_32b": {"id": "qwen3_32b", "name": "Qwen 3 32B", "provider": "openrouter"},
    "kimi_k25": {"id": "kimi_k25", "name": "Kimi K2.5", "provider": "openrouter"},
    "devstral": {"id": "devstral", "name": "Devstral Small", "provider": "openrouter"},
    "gemma3_27b": {"id": "gemma3_27b", "name": "Gemma 3 27B", "provider": "openrouter"},
    "llama4_scout": {"id": "llama4_scout", "name": "Llama 4 Scout", "provider": "openrouter"},
    "phi4": {"id": "phi4", "name": "Phi-4 14B", "provider": "openrouter"},
    "granite_40": {"id": "granite_40", "name": "Granite 4.0 Micro", "provider": "openrouter"},
    "qwen3_8b": {"id": "qwen3_8b", "name": "Qwen 3 8B", "provider": "openrouter"},
    "mistral_nemo": {"id": "mistral_nemo", "name": "Mistral Nemo 12B", "provider": "openrouter"},
    "llama31_8b": {"id": "llama31_8b", "name": "Llama 3.1 8B", "provider": "openrouter"},
}


def get_db_url():
    """Read DATABASE_URL from .env.local"""
    env_file = Path(".env.local")
    if not env_file.exists():
        env_file = Path(".env")
    if not env_file.exists():
        print("No .env.local or .env found. Run from ~/Hub/multivac-app/")
        sys.exit(1)

    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("DATABASE_URL="):
                url = line.split("=", 1)[1].strip().strip('"').strip("'")
                return url

    print("DATABASE_URL not found in .env.local")
    sys.exit(1)


def get_connection():
    """Get a database connection"""
    url = get_db_url()
    return psycopg2.connect(url)


def check_enum_values(conn):
    """Check what values the category enum allows"""
    cur = conn.cursor()
    cur.execute("""
        SELECT t.typname, e.enumlabel
        FROM pg_type t
        JOIN pg_enum e ON t.oid = e.enumtypid
        ORDER BY t.typname, e.enumsortorder
    """)
    enums = {}
    for typname, label in cur.fetchall():
        if typname not in enums:
            enums[typname] = []
        enums[typname].append(label)
    return enums


def map_category(raw_category, question_text=""):
    """Map pipeline category to DB enum value"""
    # If it's a known category, use it directly
    if raw_category in CATEGORY_MAP and raw_category != "slm":
        return CATEGORY_MAP[raw_category]

    # For SLM evals, try to infer the actual category from the question
    question_lower = question_text.lower()
    if any(kw in question_lower for kw in ["code", "function", "implement", "debug", "sql", "cache", "lock", "bug"]):
        return "code"
    elif any(kw in question_lower for kw in ["bayesian", "paradox", "probability", "investment", "arrow", "bias", "reasoning"]):
        return "reasoning"
    elif any(kw in question_lower for kw in ["analysis", "market", "audit"]):
        return "analysis"
    elif any(kw in question_lower for kw in ["write", "explain", "communicate"]):
        return "communication"
    else:
        return "code"  # Safe fallback


def load_eval_result(eval_dir):
    """Load and parse a results.json file"""
    results_path = Path(eval_dir) / "results.json"
    if not results_path.exists():
        return None

    with open(results_path) as f:
        return json.load(f)


def ensure_models_exist(conn, models_used, data):
    """Insert any new models into ai_models table"""
    cur = conn.cursor()

    # Get existing model IDs
    cur.execute("SELECT id FROM ai_models")
    existing = {row[0] for row in cur.fetchall()}

    for model_key in models_used:
        if model_key not in existing:
            # Try to get display name from the results data
            display_name = model_key
            provider = "openrouter"

            # Check rankings for display name
            if model_key in data.get("rankings", {}):
                display_name = data["rankings"][model_key].get("display_name", model_key)

            # Check SLM map
            if model_key in SLM_MODEL_MAP:
                display_name = SLM_MODEL_MAP[model_key]["name"]
                provider = SLM_MODEL_MAP[model_key]["provider"]

            cur.execute(
                "INSERT INTO ai_models (id, name, provider, is_active) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                (model_key, display_name, provider, True)
            )
            print(f"    Added model: {model_key} ({display_name})")

    conn.commit()


def upload_evaluation(conn, data, eval_dir_name, dry_run=False):
    """Upload one evaluation to the database"""
    eval_id = data["evaluation_id"]
    question = data.get("question_text", "")
    question_id = data.get("question_id", eval_id)
    raw_category = data.get("category", "code")
    category = map_category(raw_category, question)
    timestamp = data.get("timestamp", datetime.now().isoformat())
    models_used = data.get("models_used", [])

    # Parse timestamp
    try:
        eval_date = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except:
        eval_date = datetime.now()

    display_date = eval_date.strftime("%b %d, %Y")

    # Find winner from rankings
    rankings = data.get("rankings", {})
    winner_key = None
    winner_score = 0.0
    avg_scores = []

    for model_key, rank_data in rankings.items():
        score = rank_data.get("average_score", 0)
        if score > 0:
            avg_scores.append(score)
        if rank_data.get("rank") == 1:
            winner_key = model_key
            winner_score = score

    overall_avg = sum(avg_scores) / len(avg_scores) if avg_scores else 0

    # Count valid judgments
    judgments = data.get("judgments", [])
    valid_judgments = [j for j in judgments if j.get("weighted_score", 0) > 0 and j.get("error") is None]
    matrix_size = len(valid_judgments)

    if dry_run:
        print(f"  Would upload: {eval_id}")
        print(f"    Category: {raw_category} -> {category}")
        print(f"    Winner: {winner_key} ({winner_score:.2f})")
        print(f"    Avg score: {overall_avg:.2f}")
        print(f"    Judgments: {matrix_size}")
        print(f"    Models: {len(models_used)}")
        return True

    cur = conn.cursor()

    # Check if already exists
    cur.execute("SELECT id FROM evaluations WHERE id = %s", (eval_id,))
    if cur.fetchone():
        print(f"  Skip (exists): {eval_id}")
        return False

    # Ensure all models exist in ai_models
    ensure_models_exist(conn, models_used, data)

    # Insert evaluation
    cur.execute("""
        INSERT INTO evaluations (id, question_id, question, category, date, display_date,
                                  winner_model_id, winner_score, avg_score, matrix_size,
                                  folder, published_at, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (
        eval_id,
        question_id,
        question[:2000],  # Truncate very long questions
        category,
        eval_date,
        display_date,
        winner_key,
        winner_score,
        overall_avg,
        matrix_size,
        eval_dir_name,
        eval_date,
        eval_date,
    ))

    # Insert judgments
    judgment_rows = []
    for j in valid_judgments:
        judge_key = j.get("judge_key", "")
        respondent_key = j.get("respondent_key", "")
        score = j.get("weighted_score", 0)
        reasoning = j.get("brief_justification", "")

        if judge_key and respondent_key and score > 0:
            judgment_rows.append((
                eval_id,
                judge_key,
                respondent_key,
                score,
                (reasoning or "")[:500],  # Truncate long reasoning
            ))

    if judgment_rows:
        execute_values(
            cur,
            """INSERT INTO judgments (evaluation_id, judge_model_id, respondent_model_id, score, reasoning)
               VALUES %s""",
            judgment_rows,
            template="(%s, %s, %s, %s, %s)"
        )

    conn.commit()
    print(f"  Uploaded: {eval_id} | {category} | winner={winner_key} ({winner_score:.2f}) | {len(judgment_rows)} judgments")
    return True


def check_schema(conn):
    """Verify the DB schema is compatible"""
    enums = check_enum_values(conn)
    print("\nDatabase enum values:")
    for name, values in enums.items():
        print(f"  {name}: {values}")

    # Check if 'slm' category exists
    cat_enum_name = None
    for name, values in enums.items():
        if "code" in values and "reasoning" in values:
            cat_enum_name = name
            break

    if cat_enum_name:
        print(f"\n  Category enum: {cat_enum_name}")
        print(f"  Values: {enums[cat_enum_name]}")
        if "slm" not in enums[cat_enum_name]:
            print(f"  Note: 'slm' is NOT in the enum. SLM evals will be mapped to their actual category (code/reasoning).")
    else:
        print("\n  Warning: Could not identify category enum.")

    # Check row counts
    cur = conn.cursor()
    for table in ["evaluations", "judgments", "ai_models"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"  {table}: {count} rows")


def main():
    parser = argparse.ArgumentParser(description="Upload Multivac eval results to Neon DB")
    parser.add_argument("--eval-dir", default=DEFAULT_EVAL_DIR, help="Directory containing EVAL-* folders")
    parser.add_argument("--eval-id", help="Upload one specific evaluation by ID")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be uploaded")
    parser.add_argument("--check-schema", action="store_true", help="Check DB schema compatibility")
    parser.add_argument("--pattern", default="EVAL-20260315-*", help="Glob pattern for eval folders (default: today's evals)")
    args = parser.parse_args()

    conn = get_connection()

    if args.check_schema:
        check_schema(conn)
        conn.close()
        return

    eval_dir = Path(args.eval_dir)

    if args.eval_id:
        # Upload single eval
        target = eval_dir / args.eval_id
        if not target.exists():
            print(f"Not found: {target}")
            sys.exit(1)
        data = load_eval_result(target)
        if data:
            upload_evaluation(conn, data, args.eval_id, dry_run=args.dry_run)
    else:
        # Upload all matching evals
        pattern = str(eval_dir / args.pattern)
        eval_dirs = sorted(glob.glob(pattern))

        if not eval_dirs:
            print(f"No eval folders found matching: {pattern}")
            print(f"Try: python upload_evals.py --pattern 'EVAL-*'")
            sys.exit(1)

        print(f"\n{'='*60}")
        print(f"MULTIVAC - Upload Evaluations to Neon DB")
        print(f"{'='*60}")
        print(f"Source: {eval_dir}")
        print(f"Pattern: {args.pattern}")
        print(f"Found: {len(eval_dirs)} eval folders")
        if args.dry_run:
            print(f"MODE: DRY RUN (no writes)")
        print(f"{'='*60}\n")

        uploaded = 0
        skipped = 0
        failed = 0

        for ed in eval_dirs:
            eval_name = os.path.basename(ed)
            data = load_eval_result(ed)

            if not data:
                print(f"  Skip (no results.json): {eval_name}")
                skipped += 1
                continue

            try:
                result = upload_evaluation(conn, data, eval_name, dry_run=args.dry_run)
                if result:
                    uploaded += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"  FAILED: {eval_name} - {e}")
                failed += 1
                conn.rollback()

        print(f"\n{'='*60}")
        print(f"Done: {uploaded} uploaded, {skipped} skipped, {failed} failed")
        print(f"{'='*60}\n")

    conn.close()


if __name__ == "__main__":
    main()
