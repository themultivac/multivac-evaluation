#!/usr/bin/env python3
"""
Multivac V5.1 - SLM Batch Orchestrator
Run 10 hard frontier questions against 10 small language models.

WHY hard questions, not easy ones:
    r/LocalLLaMA doesn't care that a 32B model can summarize text.
    They care where a 32B model BREAKS compared to GPT-5.4 on the SAME hard task,
    and where it surprisingly holds up. That's the post that gets upvoted.

Questions selected: 5 code + 5 reasoning from Wave 2 (hardest, most diagnostic)
Models: 10 SLMs from models_15032026.py pool

Usage:
    cd ~/Multivac/v5/multivac_v5
    python orchestrate_slm.py                    # Run all 10 questions
    python orchestrate_slm.py --questions 5      # Run first 5 only (budget test)
    python orchestrate_slm.py --dry-run          # Show what would run, no API calls
    python orchestrate_slm.py --resume           # Resume from last checkpoint

Output:
    outputs/SLM-BATCH-YYYYMMDD/
        EVAL-{timestamp}/results.json
        EVAL-{timestamp}/report.md
    outputs/SLM-BATCH-YYYYMMDD/batch_summary.json

Estimated cost: $0.15-0.25 per eval (SLMs are cheap) = $1.50-2.50 total for 10 evals
Estimated time: 2-4 hours
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
# CONFIGURATION
# ═══════════════════════════════════════

BATCH_DATE = datetime.now().strftime("%Y%m%d")
BATCH_DIR = Path(f"outputs/SLM-BATCH-{BATCH_DATE}")
STATE_FILE = Path(f"slm_batch_state_{BATCH_DATE}.json")

# Budget: SLMs cost ~10-20% of frontier models
ESTIMATED_COST_PER_EVAL = 0.20
BUDGET_LIMIT = 5.00  # generous for 10 evals

# Pause between evals to respect rate limits
DELAY_BETWEEN_EVALS = 5  # seconds

# ═══════════════════════════════════════
# HARD FRONTIER QUESTIONS FOR SLMs
# These are the same questions frontier models get.
# The story is: where do SLMs break vs hold up?
# ═══════════════════════════════════════

SLM_EVAL_QUESTIONS = [
    # 5 CODE questions (diagnostic, real-world, testable)
    {
        "id": "SLM-CODE-001",
        "source_id": "CODE-011",
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

Explain why this is dangerous in production and provide a correct implementation.""",
        "why_diagnostic": "Tests whether small models understand distributed systems atomicity. The setnx+expire race is subtle."
    },
    {
        "id": "SLM-CODE-002",
        "source_id": "CODE-017",
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
```""",
        "why_diagnostic": "Tests cross-language reasoning. Go race conditions require mutex understanding that smaller models often miss."
    },
    {
        "id": "SLM-CODE-003",
        "source_id": "CODE-013",
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

Assume standard B-tree indexes on primary keys only. What indexes would you add?""",
        "why_diagnostic": "Tests practical optimization. Small models often suggest indexes without eliminating correlated subqueries first."
    },
    {
        "id": "SLM-CODE-004",
        "source_id": "CODE-028",
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

What's wrong? Provide the fix and explain the connection pool exhaustion pattern.""",
        "why_diagnostic": "Tests whether models spot the missing client.release(). Practical debugging that separates real capability from memorized patterns."
    },
    {
        "id": "SLM-CODE-005",
        "source_id": "CODE-025",
        "category": "code",
        "title": "LRU Cache with TTL",
        "question": "Implement an LRU cache with per-key TTL (time-to-live) support. Requirements: O(1) get/put, thread-safe, lazy expiration (don't use background threads), configurable max size, eviction callback, and cache hit/miss statistics. Include comprehensive tests.",
        "why_diagnostic": "Tests data structure design. Small models struggle with combining LRU ordering + TTL expiration + thread safety simultaneously."
    },

    # 5 REASONING questions (hard logic, no pattern matching)
    {
        "id": "SLM-REASON-001",
        "source_id": "REASON-012",
        "category": "reasoning",
        "title": "Bayesian Medical Diagnosis",
        "question": "A disease affects 1 in 10,000 people. A test is 99% sensitive (true positive rate) and 99.5% specific (true negative rate). A patient tests positive. (1) What is the probability they have the disease? (2) If they test positive twice with independent tests, what is the probability? (3) A doctor says 'You tested positive, so you almost certainly have it.' Critique this reasoning. (4) Design a testing protocol that achieves >95% positive predictive value.",
        "why_diagnostic": "Base rate neglect is the most common failure mode for small models. The correct answer (~2%) is counterintuitive."
    },
    {
        "id": "SLM-REASON-002",
        "source_id": "REASON-016",
        "category": "reasoning",
        "title": "Simpson's Paradox",
        "question": "Hospital A has a higher survival rate than Hospital B for both heart surgery (A: 90%, B: 85%) and knee surgery (A: 95%, B: 92%). But Hospital B has a higher overall survival rate (B: 91%, A: 89%). (1) Construct exact numbers that produce this paradox. (2) Which hospital is actually better? (3) A health insurance company uses overall survival rate to recommend hospitals. What goes wrong? (4) How should the comparison be done correctly?",
        "why_diagnostic": "Requires constructing concrete numbers, not just explaining the concept. Most small models can explain Simpson's paradox but fail to construct valid examples."
    },
    {
        "id": "SLM-REASON-003",
        "source_id": "REASON-019",
        "category": "reasoning",
        "title": "Decision Under Deep Uncertainty",
        "question": "You must choose between three investments. Investment A returns 10% with 90% probability, -50% with 10% probability. Investment B returns 5% with certainty. Investment C returns 100% with 20% probability, 0% with 80% probability. (1) Rank them by expected value. (2) Rank them by the Kelly criterion. (3) You have $10,000 your entire savings. Does this change your answer? Why? (4) Now you have $10,000,000. Does it change again? Derive the general principle.",
        "why_diagnostic": "Tests multi-step mathematical reasoning with context sensitivity. Small models often get EV right but fail Kelly criterion."
    },
    {
        "id": "SLM-REASON-004",
        "source_id": "REASON-014",
        "category": "reasoning",
        "title": "Arrow's Impossibility in Practice",
        "question": "A committee of 5 people must rank 3 candidates (A, B, C). Their preferences are: Person 1: A>B>C, Person 2: B>C>A, Person 3: C>A>B, Person 4: A>C>B, Person 5: B>A>C. (1) Show that majority rule produces a cycle. (2) Apply Borda count, instant-runoff, and Condorcet methods. Do they agree? (3) Arrow's theorem says no voting system satisfies all fairness criteria simultaneously. Which criterion would you sacrifice, and why?",
        "why_diagnostic": "Tests whether models can execute multiple voting algorithms correctly on the same data. Computation-heavy reasoning."
    },
    {
        "id": "SLM-REASON-005",
        "source_id": "REASON-029",
        "category": "reasoning",
        "title": "Survivorship Bias Analysis",
        "question": "During WWII, analysts studied bullet holes on returning bombers to decide where to add armor. They found most damage on the wings and fuselage, almost none on the engines. Their recommendation: armor the wings. Abraham Wald disagreed. (1) What was Wald's reasoning? (2) Give 5 modern examples of survivorship bias in business/tech. (3) 'We studied 100 successful startups and found they all did X.' Why is this analysis worthless without a control group?",
        "why_diagnostic": "Tests depth of reasoning. Small models can explain Wald but struggle to generate 5 novel, non-obvious modern examples."
    },
]


# ═══════════════════════════════════════
# BATCH STATE MANAGEMENT
# ═══════════════════════════════════════

class BatchState:
    def __init__(self):
        self.batch_id = f"SLM-BATCH-{BATCH_DATE}"
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

    def is_done(self, question_id):
        return any(c["question_id"] == question_id for c in self.completed)


# ═══════════════════════════════════════
# EXECUTION
# ═══════════════════════════════════════

async def run_slm_eval(question: dict, state: BatchState) -> bool:
    """Run one evaluation using multivac.py with SLM category"""
    qid = question["id"]
    progress = len(state.completed) + len(state.failed) + 1
    total = len(SLM_EVAL_QUESTIONS)

    print(f"\n{'='*60}")
    print(f"  [{progress}/{total}] {qid}: {question['title']}")
    print(f"  Category: {question['category']} (using SLM model pool)")
    print(f"  Cost so far: ${state.estimated_cost:.2f} / ${BUDGET_LIMIT:.2f}")
    print(f"{'='*60}")

    # We pass the question directly (not by ID, since these are custom IDs)
    # Use --question flag with --category slm
    cmd = [
        "python", "multivac.py",
        "--question", question["question"],
        "--category", "slm"
    ]

    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=900  # 10 min timeout (SLMs are faster)
        )

        elapsed = time.time() - start_time

        if result.returncode == 0:
            print(f"  Completed in {elapsed:.0f}s")
            state.completed.append({
                "question_id": qid,
                "source_id": question["source_id"],
                "title": question["title"],
                "category": question["category"],
                "duration_s": round(elapsed, 1),
                "timestamp": datetime.now().isoformat(),
            })
            state.estimated_cost += ESTIMATED_COST_PER_EVAL
            state.save()
            return True
        else:
            err = result.stderr[-500:] if result.stderr else "unknown"
            print(f"  FAILED: {err[:100]}")
            state.failed.append({
                "question_id": qid,
                "error": err,
                "timestamp": datetime.now().isoformat(),
            })
            state.save()
            return False

    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT (10min)")
        state.failed.append({
            "question_id": qid,
            "error": "timeout_10min",
            "timestamp": datetime.now().isoformat(),
        })
        state.save()
        return False

    except Exception as e:
        print(f"  CRASH: {e}")
        state.failed.append({
            "question_id": qid,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        })
        state.save()
        return False


async def run_batch(questions: list, state: BatchState):
    """Run the full SLM batch"""

    # Create batch output directory
    BATCH_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'#'*60}")
    print(f"  MULTIVAC SLM BATCH - {state.batch_id}")
    print(f"{'#'*60}")
    print(f"  Questions: {len(questions)}")
    print(f"  Models: 10 SLMs (Qwen 32B, Kimi K2.5, Devstral, Gemma 27B,")
    print(f"          Llama 4 Scout, Phi-4, Granite 4.0, Qwen 8B,")
    print(f"          Mistral Nemo 12B, Llama 3.1 8B)")
    print(f"  Est. cost: ${len(questions) * ESTIMATED_COST_PER_EVAL:.2f}")
    print(f"  Est. time: {len(questions) * 15}-{len(questions) * 25} minutes")
    print(f"{'#'*60}\n")

    start = time.time()

    for i, q in enumerate(questions):
        if state.is_done(q["id"]):
            print(f"  Skip (already done): {q['id']}")
            continue

        await run_slm_eval(q, state)

        # Pause between evals
        if i < len(questions) - 1:
            print(f"  Waiting {DELAY_BETWEEN_EVALS}s...")
            await asyncio.sleep(DELAY_BETWEEN_EVALS)

    elapsed_min = (time.time() - start) / 60

    # Write batch summary
    summary = {
        "batch_id": state.batch_id,
        "completed": len(state.completed),
        "failed": len(state.failed),
        "total_questions": len(questions),
        "estimated_cost": round(state.estimated_cost, 2),
        "duration_minutes": round(elapsed_min, 1),
        "questions_used": [{"id": q["id"], "title": q["title"], "category": q["category"]} for q in questions],
        "methodology": "SLM models evaluated on hard frontier questions (same difficulty as GPT-5.4/Claude Opus 4.6 evaluations)",
        "purpose": "Determine where small open-weight models break vs hold up compared to frontier models on identical tasks",
    }

    summary_path = BATCH_DIR / "batch_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print(f"  BATCH COMPLETE: {state.batch_id}")
    print(f"{'='*60}")
    print(f"  Completed: {len(state.completed)}/{len(questions)}")
    print(f"  Failed: {len(state.failed)}/{len(questions)}")
    print(f"  Cost: ~${state.estimated_cost:.2f}")
    print(f"  Time: {elapsed_min:.1f} minutes")
    print(f"  Summary: {summary_path}")
    print(f"  Results: outputs/ (individual EVAL-* folders)")
    print(f"{'='*60}")

    if state.failed:
        print(f"\n  Failed questions:")
        for f_item in state.failed:
            print(f"    {f_item['question_id']}: {f_item.get('error', '?')[:60]}")

    print(f"\n  NEXT STEPS:")
    print(f"  1. Copy results to ~/Hub/multivac-evaluation/data/evaluations/")
    print(f"  2. Sync to Neon database using upload script")
    print(f"  3. Push to GitHub: cd ~/Hub/multivac-evaluation && git add -A && git push")
    print(f"  4. Use content prompt v5 on the most surprising result")
    print(f"  5. Post to r/LocalLLaMA with: SLM vs frontier comparison")
    print()


def dry_run():
    """Show what would run without making API calls"""
    print(f"\n{'='*60}")
    print("  DRY RUN - No API calls")
    print(f"{'='*60}\n")

    for i, q in enumerate(SLM_EVAL_QUESTIONS, 1):
        print(f"  {i:2}. [{q['id']}] {q['title']}")
        print(f"      Category: {q['category']}")
        print(f"      Source: {q['source_id']} (Wave 2)")
        print(f"      Diagnostic: {q['why_diagnostic'][:80]}")
        print()

    total_cost = len(SLM_EVAL_QUESTIONS) * ESTIMATED_COST_PER_EVAL
    print(f"  Total questions: {len(SLM_EVAL_QUESTIONS)}")
    print(f"  Estimated cost: ${total_cost:.2f}")
    print(f"  Models: 10 SLMs via slm_models.py")
    print(f"  Output: {BATCH_DIR}/")
    print()


def main():
    parser = argparse.ArgumentParser(description="Multivac SLM Batch Orchestrator")
    parser.add_argument("--questions", type=int, default=10, help="Number of questions to run (default: all 10)")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without running")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint")
    args = parser.parse_args()

    if args.dry_run:
        dry_run()
        return

    questions = SLM_EVAL_QUESTIONS[:args.questions]

    if args.resume:
        state = BatchState.load()
        print(f"  Resuming: {len(state.completed)} done, {len(state.failed)} failed")
    else:
        state = BatchState()

    print(f"\n  Running {len(questions)} SLM evaluations")
    print(f"  Estimated cost: ${len(questions) * ESTIMATED_COST_PER_EVAL:.2f}")
    print(f"  Estimated time: {len(questions) * 15}-{len(questions) * 25} min")

    response = input("\n  Start? (yes/no): ")
    if response.lower() != "yes":
        print("  Cancelled.")
        return

    asyncio.run(run_batch(questions, state))


if __name__ == "__main__":
    main()
