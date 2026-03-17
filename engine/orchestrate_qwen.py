#!/usr/bin/env python3
"""
Multivac V5.1 - Project Qwen
Dedicated evaluation of ALL available Qwen models on OpenRouter.

Community requested: Qwen 3.5 9B, 27B, 35B-A3B, 122B-A10B, Flash, Plus, 397B,
                     Qwen 3 Coder Next, Qwen 3 8B, 32B (baselines from SLM batch)

This runs the same 10 hard questions from the SLM batch so results are
directly comparable. The r/LocalLLaMA community asked for this specifically.

Usage:
    cd ~/Multivac/v5/multivac_v5
    python orchestrate_qwen.py --dry-run          # See the plan
    python orchestrate_qwen.py                    # Run all 10 questions
    python orchestrate_qwen.py --questions 5      # Run first 5 only
    python orchestrate_qwen.py --resume           # Resume from checkpoint

Output: outputs/QWEN-BATCH-YYYYMMDD/
Cost estimate: ~$3-8 (the 397B and Plus models cost more per token)
Time estimate: 3-5 hours
"""

import asyncio
import subprocess
import time
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════
# QWEN MODEL POOL - ALL AVAILABLE ON OPENROUTER
# ═══════════════════════════════════════

QWEN_MODELS = {
    # --- Qwen 3.5 Series (community's #1 request) ---
    "qwen35_9b": {
        "model_id": "qwen/qwen3.5-9b",
        "display_name": "Qwen 3.5 9B",
        "provider": "openrouter",
        "parameters": "9B",
        "series": "3.5",
        "context_window": 256000,
        "cost_input": 0.05,
        "cost_output": 0.15,
        "active": True
    },
    "qwen35_27b": {
        "model_id": "qwen/qwen3.5-27b",
        "display_name": "Qwen 3.5 27B",
        "provider": "openrouter",
        "parameters": "27B dense",
        "series": "3.5",
        "context_window": 262000,
        "cost_input": 0.195,
        "cost_output": 1.56,
        "active": True
    },
    "qwen35_35b_a3b": {
        "model_id": "qwen/qwen3.5-35b-a3b",
        "display_name": "Qwen 3.5 35B-A3B",
        "provider": "openrouter",
        "parameters": "35B / 3B active MoE",
        "series": "3.5",
        "context_window": 262000,
        "cost_input": 0.1625,
        "cost_output": 1.30,
        "active": True
    },
    "qwen35_122b_a10b": {
        "model_id": "qwen/qwen3.5-122b-a10b",
        "display_name": "Qwen 3.5 122B-A10B",
        "provider": "openrouter",
        "parameters": "122B / 10B active MoE",
        "series": "3.5",
        "context_window": 262000,
        "cost_input": 0.26,
        "cost_output": 2.08,
        "active": True
    },
    "qwen35_flash": {
        "model_id": "qwen/qwen3.5-flash",
        "display_name": "Qwen 3.5 Flash",
        "provider": "openrouter",
        "parameters": "MoE hybrid attention",
        "series": "3.5",
        "context_window": 1000000,
        "cost_input": 0.065,
        "cost_output": 0.26,
        "active": True
    },
    "qwen35_397b_a17b": {
        "model_id": "qwen/qwen3.5-397b-a17b",
        "display_name": "Qwen 3.5 397B-A17B",
        "provider": "openrouter",
        "parameters": "397B / 17B active MoE",
        "series": "3.5",
        "context_window": 262000,
        "cost_input": 0.39,
        "cost_output": 2.34,
        "active": True
    },

    # --- Qwen 3 Series (baselines from SLM batch) ---
    "qwen3_8b": {
        "model_id": "qwen/qwen3-8b",
        "display_name": "Qwen 3 8B",
        "provider": "openrouter",
        "parameters": "8B",
        "series": "3",
        "context_window": 32768,
        "cost_input": 0.05,
        "cost_output": 0.25,
        "active": True
    },
    "qwen3_32b": {
        "model_id": "qwen/qwen3-32b",
        "display_name": "Qwen 3 32B",
        "provider": "openrouter",
        "parameters": "32B",
        "series": "3",
        "context_window": 41000,
        "cost_input": 0.08,
        "cost_output": 0.24,
        "active": True
    },

    # --- Qwen 3 Coder (community requested) ---
    "qwen3_coder_next": {
        "model_id": "qwen/qwen3-coder-next",
        "display_name": "Qwen 3 Coder Next",
        "provider": "openrouter",
        "parameters": "80B / 3B active MoE",
        "series": "3-coder",
        "context_window": 262000,
        "cost_input": 0.12,
        "cost_output": 0.75,
        "active": True
    },

    # --- Qwen 3.5 Plus (premium tier) ---
    "qwen35_plus": {
        "model_id": "qwen/qwen3.5-plus-2026-02-15",
        "display_name": "Qwen 3.5 Plus",
        "provider": "openrouter",
        "parameters": "MoE (proprietary)",
        "series": "3.5",
        "context_window": 1000000,
        "cost_input": 0.26,
        "cost_output": 1.56,
        "active": True
    },
}

# Category metadata for category_loader compatibility
MODELS = QWEN_MODELS

CATEGORY_INFO = {
    "name": "qwen",
    "display_name": "Project Qwen (All Qwen Models)",
    "description": "Dedicated evaluation of all available Qwen models across generations",
    "model_count": len(QWEN_MODELS),
    "version": "v1_march2026"
}

def get_active_models():
    return [k for k, v in sorted(MODELS.items(), key=lambda x: x[1].get("cost_input", 0)) if v.get("active", True)]


# ═══════════════════════════════════════
# SAME 10 HARD QUESTIONS FROM SLM BATCH
# (for direct comparison)
# ═══════════════════════════════════════

QWEN_EVAL_QUESTIONS = [
    {
        "id": "QWEN-CODE-001",
        "category": "code",
        "title": "Distributed Lock Race Condition",
        "question": """This distributed lock implementation has a subtle race condition that can cause two processes to hold the lock simultaneously. Find the bug and fix it.

```python
import redis
import time
import uuid

class DistributedLock:
    def __init__(self, redis_client, lock_name, timeout=10):
        self.redis = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.timeout = timeout
        self.token = str(uuid.uuid4())

    def acquire(self):
        while True:
            if self.redis.setnx(self.lock_name, self.token):
                self.redis.expire(self.lock_name, self.timeout)
                return True
            time.sleep(0.1)

    def release(self):
        if self.redis.get(self.lock_name) == self.token:
            self.redis.delete(self.lock_name)
```

Explain why this is dangerous in production and provide a correct implementation."""
    },
    {
        "id": "QWEN-CODE-002",
        "category": "code",
        "title": "Fix Go Concurrency Bug",
        "question": """This Go code processes orders concurrently but occasionally produces incorrect totals. Find and fix all concurrency issues.

```go
package main

import (
    "fmt"
    "sync"
)

type OrderProcessor struct {
    totalRevenue float64
    orderCount   int
    errors       []string
}

func (op *OrderProcessor) ProcessOrder(amount float64, wg *sync.WaitGroup) {
    defer wg.Done()

    if amount <= 0 {
        op.errors = append(op.errors, fmt.Sprintf("invalid amount: %.2f", amount))
        return
    }

    op.totalRevenue += amount
    op.orderCount++
}

func main() {
    op := &OrderProcessor{}
    var wg sync.WaitGroup

    orders := []float64{99.99, 149.50, -10.00, 299.99, 49.99, 0, 199.99}

    for _, amount := range orders {
        wg.Add(1)
        go op.ProcessOrder(amount, &wg)
    }

    wg.Wait()
    fmt.Printf("Total: $%.2f from %d orders\\n", op.totalRevenue, op.orderCount)
}
```"""
    },
    {
        "id": "QWEN-CODE-003",
        "category": "code",
        "title": "SQL Query Optimization",
        "question": """This SQL query takes 45 seconds on a table with 10M rows. Rewrite it to run in under 1 second. Explain your optimization strategy.

```sql
SELECT u.name, u.email,
       (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
       (SELECT SUM(amount) FROM orders o WHERE o.user_id = u.id) as total_spent,
       (SELECT MAX(created_at) FROM orders o WHERE o.user_id = u.id) as last_order
FROM users u
WHERE u.created_at > '2024-01-01'
AND (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) > 5
ORDER BY total_spent DESC
LIMIT 100;
```

Assume standard B-tree indexes on primary keys only. What indexes would you add?"""
    },
    {
        "id": "QWEN-CODE-004",
        "category": "code",
        "title": "Debug Production 502 Errors",
        "question": """Your Node.js API is responding with 502 errors under load. Here's the relevant code and infrastructure:

- Express.js API behind an Nginx reverse proxy
- Connection pool to PostgreSQL (max 20 connections)
- Average response time: 50ms normally, 30s+ during incidents
- Error logs show: "connect ETIMEDOUT" and "too many clients already"
- The issue starts when traffic exceeds 200 req/s

```javascript
app.get('/api/users/:id', async (req, res) => {
  const client = await pool.connect();
  const result = await client.query('SELECT * FROM users WHERE id = $1', [req.params.id]);
  res.json(result.rows[0]);
});
```

What's wrong? Provide the fix and explain the connection pool exhaustion pattern."""
    },
    {
        "id": "QWEN-CODE-005",
        "category": "code",
        "title": "LRU Cache with TTL",
        "question": "Implement an LRU cache with per-key TTL (time-to-live) support. Requirements: O(1) get/put, thread-safe, lazy expiration (don't use background threads), configurable max size, eviction callback, and cache hit/miss statistics. Include comprehensive tests."
    },
    {
        "id": "QWEN-REASON-001",
        "category": "reasoning",
        "title": "Bayesian Medical Diagnosis",
        "question": "A disease affects 1 in 10,000 people. A test is 99% sensitive (true positive rate) and 99.5% specific (true negative rate). A patient tests positive. (1) What is the probability they have the disease? (2) If they test positive twice with independent tests, what is the probability? (3) A doctor says 'You tested positive, so you almost certainly have it.' Critique this reasoning. (4) Design a testing protocol that achieves >95% positive predictive value."
    },
    {
        "id": "QWEN-REASON-002",
        "category": "reasoning",
        "title": "Simpson's Paradox",
        "question": "Hospital A has a higher survival rate than Hospital B for both heart surgery (A: 90%, B: 85%) and knee surgery (A: 95%, B: 92%). But Hospital B has a higher overall survival rate (B: 91%, A: 89%). (1) Construct exact numbers that produce this paradox. (2) Which hospital is actually better? (3) A health insurance company uses overall survival rate to recommend hospitals. What goes wrong? (4) How should the comparison be done correctly?"
    },
    {
        "id": "QWEN-REASON-003",
        "category": "reasoning",
        "title": "Decision Under Deep Uncertainty",
        "question": "You must choose between three investments. Investment A returns 10% with 90% probability, -50% with 10% probability. Investment B returns 5% with certainty. Investment C returns 100% with 20% probability, 0% with 80% probability. (1) Rank them by expected value. (2) Rank them by the Kelly criterion. (3) You have $10,000 your entire savings. Does this change your answer? Why? (4) Now you have $10,000,000. Does it change again? Derive the general principle."
    },
    {
        "id": "QWEN-REASON-004",
        "category": "reasoning",
        "title": "Arrow's Impossibility in Practice",
        "question": "A committee of 5 people must rank 3 candidates (A, B, C). Their preferences are: Person 1: A>B>C, Person 2: B>C>A, Person 3: C>A>B, Person 4: A>C>B, Person 5: B>A>C. (1) Show that majority rule produces a cycle. (2) Apply Borda count, instant-runoff, and Condorcet methods. Do they agree? (3) Arrow's theorem says no voting system satisfies all fairness criteria simultaneously. Which criterion would you sacrifice, and why?"
    },
    {
        "id": "QWEN-REASON-005",
        "category": "reasoning",
        "title": "Survivorship Bias Analysis",
        "question": "During WWII, analysts studied bullet holes on returning bombers to decide where to add armor. They found most damage on the wings and fuselage, almost none on the engines. Their recommendation: armor the wings. Abraham Wald disagreed. (1) What was Wald's reasoning? (2) Give 5 modern examples of survivorship bias in business/tech. (3) 'We studied 100 successful startups and found they all did X.' Why is this analysis worthless without a control group?"
    },
]


# ═══════════════════════════════════════
# BATCH STATE
# ═══════════════════════════════════════

BATCH_DATE = datetime.now().strftime("%Y%m%d")
BATCH_DIR = Path(f"outputs/QWEN-BATCH-{BATCH_DATE}")
STATE_FILE = Path(f"qwen_batch_state_{BATCH_DATE}.json")
TIMEOUT = 1200  # 15 minutes (some Qwen models are verbose)
DELAY = 5

class BatchState:
    def __init__(self):
        self.batch_id = f"QWEN-BATCH-{BATCH_DATE}"
        self.started_at = datetime.now().isoformat()
        self.completed = []
        self.failed = []
        self.estimated_cost = 0.0

    def save(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.__dict__, f, indent=2)

    @classmethod
    def load(cls):
        if STATE_FILE.exists():
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                state = cls()
                state.__dict__.update(data)
                return state
        return cls()

    def is_done(self, qid):
        return any(c["question_id"] == qid for c in self.completed)


# ═══════════════════════════════════════
# EXECUTION
# ═══════════════════════════════════════

async def run_qwen_eval(question, state):
    qid = question["id"]
    progress = len(state.completed) + len(state.failed) + 1
    total = len(QWEN_EVAL_QUESTIONS)

    print(f"\n{'='*60}")
    print(f"  [{progress}/{total}] {qid}: {question['title']}")
    print(f"  Models: {len(get_active_models())} Qwen models")
    print(f"  Cost so far: ${state.estimated_cost:.2f}")
    print(f"{'='*60}")

    # Use --category qwen (requires qwen_models.py to be registered)
    # Fallback: use --category code/reasoning and let it use qwen pool
    cmd = [
        "python", "multivac.py",
        "--question", question["question"],
        "--category", "qwen"
    ]

    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        elapsed = time.time() - start

        if result.returncode == 0:
            print(f"  Completed in {elapsed:.0f}s")
            state.completed.append({
                "question_id": qid,
                "title": question["title"],
                "category": question["category"],
                "duration_s": round(elapsed, 1),
                "timestamp": datetime.now().isoformat(),
            })
            state.estimated_cost += 0.50  # Higher estimate for Qwen mix (some expensive models)
            state.save()
            return True
        else:
            err = result.stderr[-500:] if result.stderr else "unknown"
            print(f"  FAILED: {err[:120]}")
            state.failed.append({"question_id": qid, "error": err, "timestamp": datetime.now().isoformat()})
            state.save()
            return False

    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT ({TIMEOUT}s)")
        state.failed.append({"question_id": qid, "error": f"timeout_{TIMEOUT}s", "timestamp": datetime.now().isoformat()})
        state.save()
        return False
    except Exception as e:
        print(f"  CRASH: {e}")
        state.failed.append({"question_id": qid, "error": str(e), "timestamp": datetime.now().isoformat()})
        state.save()
        return False


async def run_batch(questions, state):
    BATCH_DIR.mkdir(parents=True, exist_ok=True)

    models = get_active_models()
    total_cost_est = len(questions) * 0.50

    print(f"\n{'#'*60}")
    print(f"  PROJECT QWEN - {state.batch_id}")
    print(f"{'#'*60}")
    print(f"  Questions: {len(questions)} (same hard tasks as SLM batch)")
    print(f"  Models: {len(models)} Qwen models across 3 generations:")
    print(f"")
    for mk in models:
        m = QWEN_MODELS[mk]
        print(f"    {m['display_name']:<25} [{m['parameters']}] ${m['cost_input']}/{m['cost_output']} per M tokens")
    print(f"")
    print(f"  Est. cost: ${total_cost_est:.2f}")
    print(f"  Est. time: {len(questions) * 20}-{len(questions) * 35} minutes")
    print(f"{'#'*60}\n")

    start = time.time()
    for i, q in enumerate(questions):
        if state.is_done(q["id"]):
            print(f"  Skip (done): {q['id']}")
            continue
        await run_qwen_eval(q, state)
        if i < len(questions) - 1:
            await asyncio.sleep(DELAY)

    elapsed_min = (time.time() - start) / 60

    summary = {
        "batch_id": state.batch_id,
        "completed": len(state.completed),
        "failed": len(state.failed),
        "total_questions": len(questions),
        "estimated_cost": round(state.estimated_cost, 2),
        "duration_minutes": round(elapsed_min, 1),
        "models": {k: {"name": v["display_name"], "params": v["parameters"], "series": v["series"]} for k, v in QWEN_MODELS.items() if v["active"]},
        "purpose": "Community-requested evaluation of all Qwen model generations on identical hard frontier tasks. Direct comparison: Qwen 3 vs 3.5 vs Coder on same questions.",
    }

    with open(BATCH_DIR / "batch_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print(f"  PROJECT QWEN COMPLETE")
    print(f"{'='*60}")
    print(f"  Completed: {len(state.completed)}/{len(questions)}")
    print(f"  Failed: {len(state.failed)}")
    print(f"  Cost: ~${state.estimated_cost:.2f}")
    print(f"  Time: {elapsed_min:.1f} min")
    print(f"\n  NEXT:")
    print(f"  1. cd ~/Hub/multivac-app && python upload_evals.py --pattern 'EVAL-{BATCH_DATE}-*'")
    print(f"  2. cp -r outputs/EVAL-{BATCH_DATE}-* ~/Hub/multivac-evaluation/data/evaluations/")
    print(f"  3. Reply to r/LocalLLaMA commenters with results links")
    print(f"  4. Substack post: 'Qwen 3 vs 3.5: Same questions, every model, blind eval'")
    print()


def dry_run():
    models = get_active_models()
    print(f"\n{'='*60}")
    print("  PROJECT QWEN - DRY RUN")
    print(f"{'='*60}\n")

    print(f"  Models ({len(models)}):")
    for mk in models:
        m = QWEN_MODELS[mk]
        print(f"    {m['display_name']:<25} [{m['parameters']}] series={m['series']}")

    print(f"\n  Questions ({len(QWEN_EVAL_QUESTIONS)}):")
    for i, q in enumerate(QWEN_EVAL_QUESTIONS, 1):
        print(f"    {i:2}. [{q['id']}] {q['title']} ({q['category']})")

    est = len(QWEN_EVAL_QUESTIONS) * 0.50
    print(f"\n  Est. cost: ${est:.2f}")
    print(f"  Est. time: {len(QWEN_EVAL_QUESTIONS) * 20}-{len(QWEN_EVAL_QUESTIONS) * 35} min")
    print(f"  Output: {BATCH_DIR}/")
    print()


def main():
    parser = argparse.ArgumentParser(description="Project Qwen - Full Qwen Model Evaluation")
    parser.add_argument("--questions", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        dry_run()
        return

    questions = QWEN_EVAL_QUESTIONS[:args.questions]
    state = BatchState.load() if args.resume else BatchState()

    if args.resume:
        print(f"  Resuming: {len(state.completed)} done, {len(state.failed)} failed")

    response = input(f"\n  Run {len(questions)} evals across {len(get_active_models())} Qwen models? (yes/no): ")
    if response.lower() != "yes":
        print("  Cancelled.")
        return

    asyncio.run(run_batch(questions, state))


if __name__ == "__main__":
    main()
