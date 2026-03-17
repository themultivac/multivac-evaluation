#!/usr/bin/env python3
"""
Multivac V5 - Master Orchestrator
Run all 60 questions across 6 categories with staggered starts
"""

import asyncio
import subprocess
import time
from datetime import datetime
from pathlib import Path
import json

# Configuration
BUDGET_LIMIT = 37.00  # Leave $0.59 buffer
STAGGER_DELAY = 120  # 2 minutes between category starts
ESTIMATED_COST_PER_QUESTION = 0.35

# Category execution order
CATEGORY_PRIORITY = [
    "meta_alignment",
    "reasoning",
    "code",
    "analysis",
    "communication",
    "edge_cases",
]

STATE_FILE = Path("orchestrator_state.json")


class OrchestratorState:
    def __init__(self):
        self.started_at = datetime.now().isoformat()
        self.completed_questions = []
        self.failed_questions = []
        self.estimated_cost_so_far = 0.0
        self.categories_started = []
        self.categories_completed = []
        
    def save(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
    
    @classmethod
    def load(cls):
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                state = cls()
                state.__dict__.update(data)
                return state
        return cls()


async def run_single_question(question_id: str, category: str, state: OrchestratorState) -> bool:
    """Run a single question evaluation"""
    
    progress = len(state.completed_questions) + len(state.failed_questions) + 1
    budget_remaining = BUDGET_LIMIT - state.estimated_cost_so_far
    
    print(f"\n{'='*60}")
    print(f"🔮 Question {progress}/60: {question_id}")
    print(f"   Category: {category}")
    print(f"   Cost: ${ESTIMATED_COST_PER_QUESTION:.2f} | Remaining: ${budget_remaining:.2f}")
    print(f"   Completed: {len(state.completed_questions)} ✅ | Failed: {len(state.failed_questions)} ❌")
    print(f"{'='*60}")
    
    # Run evaluation
    cmd = [
        "python", "multivac.py",
        "--question-id", question_id,
        "--category", category
    ]
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=900  # 15 minute timeout
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {question_id} completed in {elapsed:.0f}s")
            state.completed_questions.append({
                "question_id": question_id,
                "category": category,
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": elapsed
            })
            state.estimated_cost_so_far += ESTIMATED_COST_PER_QUESTION
            state.save()
            return True
        else:
            print(f"❌ {question_id} failed")
            print(f"Error: {result.stderr[-500:]}")  # Last 500 chars of error
            state.failed_questions.append({
                "question_id": question_id,
                "category": category,
                "error": result.stderr[-1000:],
                "timestamp": datetime.now().isoformat()
            })
            state.save()
            return True
            
    except subprocess.TimeoutExpired:
        print(f"⏱️  {question_id} timed out (15min)")
        state.failed_questions.append({
            "question_id": question_id,
            "category": category,
            "error": "timeout_15min",
            "timestamp": datetime.now().isoformat()
        })
        state.save()
        return True
    
    except Exception as e:
        print(f"💥 {question_id} crashed: {e}")
        state.failed_questions.append({
            "question_id": question_id,
            "category": category,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
        state.save()
        return True


async def run_category(category: str, state: OrchestratorState):
    """Run all questions in a category"""
    
    print(f"\n{'#'*60}")
    print(f"📂 CATEGORY: {category.upper()}")
    print(f"{'#'*60}")
    
    state.categories_started.append({
        "category": category,
        "timestamp": datetime.now().isoformat()
    })
    state.save()
    
    from questions import get_questions_by_category
    questions = get_questions_by_category(category)
    
    print(f"   Questions: {len(questions)}")
    print(f"   Est. cost: ${len(questions) * ESTIMATED_COST_PER_QUESTION:.2f}")
    
    for i, q in enumerate(questions, 1):
        question_id = q["id"]
        
        # Skip if already done
        if any(cq["question_id"] == question_id for cq in state.completed_questions):
            print(f"⏭️  {question_id} already done")
            continue
        
        await run_single_question(question_id, category, state)
        
        # Brief pause between questions
        if i < len(questions):
            await asyncio.sleep(3)
    
    state.categories_completed.append({
        "category": category,
        "timestamp": datetime.now().isoformat()
    })
    state.save()
    
    print(f"\n✅ {category} complete!")
    return True


async def run_all_categories(state: OrchestratorState):
    """Run all categories sequentially with staggering"""
    
    print(f"\n{'='*60}")
    print(f"🚀 MULTIVAC V5 - ALL 60 QUESTIONS")
    print(f"{'='*60}")
    print(f"Budget: ${BUDGET_LIMIT:.2f}")
    print(f"Estimated total: ${60 * ESTIMATED_COST_PER_QUESTION:.2f}")
    print(f"Buffer: ${BUDGET_LIMIT - (60 * ESTIMATED_COST_PER_QUESTION):.2f}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    for i, category in enumerate(CATEGORY_PRIORITY):
        # Skip if already done
        if any(cc["category"] == category for cc in state.categories_completed):
            print(f"⏭️  {category} already complete")
            continue
        
        # Stagger between categories
        if i > 0:
            print(f"\n⏸️  Waiting {STAGGER_DELAY}s before {category}...")
            await asyncio.sleep(STAGGER_DELAY)
        
        await run_category(category, state)
    
    elapsed_hours = (time.time() - start_time) / 3600
    
    print(f"\n{'='*60}")
    print(f"🎉 EVALUATION COMPLETE!")
    print(f"{'='*60}")
    print(f"✅ Completed: {len(state.completed_questions)}/60")
    print(f"❌ Failed: {len(state.failed_questions)}/60")
    print(f"💰 Est. spend: ${state.estimated_cost_so_far:.2f}")
    print(f"⏱️  Duration: {elapsed_hours:.1f} hours")
    print(f"{'='*60}\n")
    
    if state.failed_questions:
        print("⚠️  Failed Questions:")
        for fq in state.failed_questions:
            print(f"   • {fq['question_id']}: {fq.get('error', 'unknown')[:60]}")
        print()
    
    success_rate = len(state.completed_questions) / 60 * 100
    print(f"📊 Success Rate: {success_rate:.1f}%\n")


def print_status(state: OrchestratorState):
    total = len(state.completed_questions) + len(state.failed_questions)
    
    print(f"\n{'='*60}")
    print(f"📊 RESUMING - Current Status")
    print(f"{'='*60}")
    print(f"Started: {state.started_at}")
    print(f"Progress: {total}/60 questions")
    print(f"  ✅ Done: {len(state.completed_questions)}")
    print(f"  ❌ Failed: {len(state.failed_questions)}")
    print(f"💰 Spent: ${state.estimated_cost_so_far:.2f} / ${BUDGET_LIMIT:.2f}")
    print(f"📂 Categories: {len(state.categories_completed)}/6")
    print(f"{'='*60}\n")


async def main():
    state = OrchestratorState.load()
    
    # Resume or fresh start
    if state.completed_questions or state.failed_questions:
        print_status(state)
        response = input("Resume? (yes/no): ")
        if response.lower() != "yes":
            print("Cancelled.")
            return
    else:
        print("\n🚀 ALL 60 QUESTIONS")
        print(f"💰 Budget: ${BUDGET_LIMIT:.2f}")
        print(f"📊 Est. cost: ${60 * ESTIMATED_COST_PER_QUESTION:.2f}")
        print(f"⏱️  Duration: 6-8 hours")
        print(f"📂 Order: {' → '.join(CATEGORY_PRIORITY)}")
        
        response = input("\n🚦 Start? (yes/no): ")
        if response.lower() != "yes":
            print("Cancelled.")
            return
    
    print("\n⏳ Starting in 5 seconds... (Ctrl+C to cancel)")
    await asyncio.sleep(5)
    
    await run_all_categories(state)
    
    print("\n📁 Results:")
    print("   • outputs/ - all evaluation results")
    print("   • data/tracker.json - cumulative stats")
    print("   • orchestrator_state.json - run progress")
    
    print("\n✅ Ready for multivac-evaluation repo!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopped")
        state = OrchestratorState.load()
        print(f"Progress: {len(state.completed_questions)}/60")
        print("Run again to resume.")
