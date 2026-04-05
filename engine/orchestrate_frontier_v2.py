#!/usr/bin/env python3
"""
Multivac V5.1 - Frontier Batch Orchestrator (V2 Model Pools)
Runs all 150 questions (Wave 1 + Wave 2) across 5 categories.

Usage:
    cd ~/Multivac/v5/multivac_v5
    python orchestrate_frontier_v2.py
"""

import subprocess
import time
import json
from datetime import datetime
from pathlib import Path

# Budget
BUDGET_LIMIT = 70.00
ESTIMATED_COST_PER_EVAL = 0.35

# Categories and their question pools
CATEGORIES = ["code", "reasoning", "analysis", "communication", "meta_alignment"]

STATE_FILE = Path("frontier_v2_state.json")
STAGGER_DELAY = 60  # seconds between categories


def get_all_question_ids():
    """Collect all question IDs from Wave 1 + Wave 2 for frontier categories."""
    from questions import QUESTIONS
    from questions_wave2_15032026 import WAVE2_QUESTIONS

    all_questions = []

    for cat in CATEGORIES:
        # Wave 1
        for q in QUESTIONS.get(cat, []):
            all_questions.append((q["id"], cat))
        # Wave 2
        for q in WAVE2_QUESTIONS.get(cat, []):
            all_questions.append((q["id"], cat))

    return all_questions


class BatchState:
    def __init__(self):
        self.started_at = datetime.now().isoformat()
        self.completed = []
        self.failed = []
        self.cost = 0.0

    def save(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.__dict__, f, indent=2)

    @classmethod
    def load(cls):
        if STATE_FILE.exists():
            s = cls()
            s.__dict__.update(json.loads(STATE_FILE.read_text()))
            return s
        return cls()

    @property
    def done_ids(self):
        return {e["qid"] for e in self.completed} | {e["qid"] for e in self.failed}


def run_eval(qid, category, state):
    """Run a single evaluation."""
    n = len(state.completed) + len(state.failed) + 1
    budget_left = BUDGET_LIMIT - state.cost

    if budget_left < ESTIMATED_COST_PER_EVAL:
        print(f"  Budget exhausted (${state.cost:.2f}/${BUDGET_LIMIT:.2f}). Stopping.")
        return False

    print(f"\n{'='*60}")
    print(f"[{n}] {qid} ({category}) -- ${budget_left:.2f} remaining")
    print(f"{'='*60}")

    start = time.time()
    try:
        result = subprocess.run(
            ["python", "multivac.py", "--question-id", qid, "--category", category],
            capture_output=True, text=True, timeout=900
        )
        elapsed = time.time() - start

        if result.returncode == 0:
            print(f"  Done: {qid} -- {elapsed:.0f}s")
            state.completed.append({"qid": qid, "cat": category, "time": elapsed})
        else:
            err = result.stderr[-300:] if result.stderr else "unknown error"
            print(f"  FAILED: {qid} -- {err}")
            state.failed.append({"qid": qid, "cat": category, "error": result.stderr[-500:] if result.stderr else "unknown"})

    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: {qid}")
        state.failed.append({"qid": qid, "cat": category, "error": "timeout_15min"})

    state.cost += ESTIMATED_COST_PER_EVAL
    state.save()
    return True


def main():
    all_questions = get_all_question_ids()
    state = BatchState.load()

    # Resume check
    if state.done_ids:
        remaining = [q for q in all_questions if q[0] not in state.done_ids]
        print(f"\n  Resuming: {len(state.completed)} done, {len(state.failed)} failed, {len(remaining)} remaining")
        print(f"  Spent: ${state.cost:.2f}/${BUDGET_LIMIT:.2f}")
        resp = input("Continue? (yes/no): ")
        if resp.lower() != "yes":
            return
    else:
        remaining = all_questions
        print(f"\n  FRONTIER BATCH V2")
        print(f"  Questions: {len(all_questions)} (Wave 1 + Wave 2)")
        print(f"  Categories: {', '.join(CATEGORIES)}")
        print(f"  Budget: ${BUDGET_LIMIT:.2f}")
        print(f"  Est. cost: ${len(all_questions) * ESTIMATED_COST_PER_EVAL:.2f}")
        resp = input("\nStart? (yes/no): ")
        if resp.lower() != "yes":
            return

    print(f"\n  Starting in 5 seconds...")
    time.sleep(5)

    current_cat = None
    for qid, cat in remaining:
        if cat != current_cat:
            if current_cat is not None:
                print(f"\n  Category switch -> {cat}. Waiting {STAGGER_DELAY}s...")
                time.sleep(STAGGER_DELAY)
            current_cat = cat
            print(f"\n{'#'*60}")
            print(f"  CATEGORY: {cat.upper()}")
            print(f"{'#'*60}")

        ok = run_eval(qid, cat, state)
        if not ok:
            break
        time.sleep(3)

    # Summary
    print(f"\n{'='*60}")
    print(f"  BATCH COMPLETE")
    print(f"  Completed: {len(state.completed)}")
    print(f"  Failed: {len(state.failed)}")
    print(f"  Spent: ${state.cost:.2f}")
    print(f"{'='*60}")

    if state.failed:
        print("\nFailed evals:")
        for f in state.failed:
            err_preview = f["error"][:60] if f.get("error") else "unknown"
            print(f"  {f['qid']}: {err_preview}")


if __name__ == "__main__":
    main()
