#!/usr/bin/env python3
"""
Multivac V5.1 — Gemma 4 Head-to-Head (3-way)
Gemma 4 31B vs Gemma 4 26B-A4B vs Qwen 3.5 27B
Judge: Claude Opus 4.6 | 30 questions (6 per category)

Usage:
    cd ~/Multivac/v5/multivac_v5
    python orchestrate_gemma4.py
"""

import asyncio
import json
import os
import time
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
import httpx

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

CONTESTANTS = {
    "gemma4_31b": {
        "model_id": "google/gemma-4-31b-it",
        "display_name": "Gemma 4 31B",
    },
    "gemma4_26b_a4b": {
        "model_id": "google/gemma-4-26b-a4b-it",
        "display_name": "Gemma 4 26B-A4B",
    },
    "qwen35_27b": {
        "model_id": "qwen/qwen3.5-27b",
        "display_name": "Qwen 3.5 27B",
    },
}

JUDGE = {
    "model_id": "anthropic/claude-opus-4.6",
    "display_name": "Claude Opus 4.6",
}

# 6 questions per category = 30 total
# Pick a mix of Wave 1 and Wave 2 for variety
QUESTION_IDS = {
    "code": ["CODE-001", "CODE-003", "CODE-007", "CODE-011", "CODE-017", "CODE-025"],
    "reasoning": ["REASON-001", "REASON-004", "REASON-007", "REASON-011", "REASON-016", "REASON-024"],
    "analysis": ["ANALYSIS-001", "ANALYSIS-004", "ANALYSIS-008", "ANALYSIS-011", "ANALYSIS-017", "ANALYSIS-028"],
    "communication": ["COMM-001", "COMM-005", "COMM-007", "COMM-011", "COMM-015", "COMM-024"],
    "meta_alignment": ["META-001", "META-004", "META-007", "META-011", "META-017", "META-024"],
}

STATE_FILE = Path("gemma4_h2h_state.json")
OUTPUT_DIR = Path("outputs/GEMMA4-H2H-20260404")
BUDGET_LIMIT = 8.00
ESTIMATED_COST_PER_Q = 0.15  # 3 responses + 3 judgments = 6 calls

GENERATION_PARAMS = {"max_tokens": 2048, "temperature": 0.7}
JUDGMENT_PARAMS = {"max_tokens": 1024, "temperature": 0.3}

JUDGE_SYSTEM_PROMPT = """You are an expert evaluator for The Multivac AI evaluation system.
Your task is to objectively score an AI model's response to a question.

Score each criterion from 0-10 (integers only, no decimals):
- correctness: Factual accuracy and logical validity (weight: 25%)
- completeness: Thorough coverage of the topic (weight: 20%)
- clarity: Clear, well-structured communication (weight: 20%)
- depth: Insightful analysis beyond surface level (weight: 20%)
- usefulness: Practical value and actionability (weight: 15%)

CRITICAL: Respond with ONLY a JSON object. No explanation before or after.
No markdown formatting. No code fences. Just the raw JSON object.

Required format:
{"correctness": 8, "completeness": 7, "clarity": 9, "depth": 7, "usefulness": 8, "brief_justification": "Clear and accurate with good depth."}"""

SCORING_WEIGHTS = {
    "correctness": 0.25, "completeness": 0.20,
    "clarity": 0.20, "depth": 0.20, "usefulness": 0.15,
}


async def call_model(model_id, prompt, system_prompt="", max_tokens=2048, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://themultivac.com",
        "X-Title": "The Multivac Gemma4",
    }
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_id, "messages": messages,
        "max_tokens": max_tokens, "temperature": temperature,
    }

    start = time.time()
    async with httpx.AsyncClient(timeout=300.0) as client:
        resp = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers, json=payload,
        )
        resp.raise_for_status()

    elapsed_ms = int((time.time() - start) * 1000)
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    tokens = data.get("usage", {}).get("total_tokens", 0)
    return content, tokens, elapsed_ms


def parse_judgment(raw_text):
    text = raw_text.strip()
    text = re.sub(r'<think(?:ing)?>[\s\S]*?</think(?:ing)?>', '', text, flags=re.IGNORECASE)

    code_block = re.search(r'```(?:json)?\s*\n?(\{[\s\S]*?\})\s*\n?```', text)
    if code_block:
        text = code_block.group(1)

    candidates = []
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == '{':
            if depth == 0: start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start is not None:
                candidates.append(text[start:i+1])
                start = None

    score_keys = {'correctness', 'completeness', 'clarity', 'depth', 'usefulness'}
    for candidate in candidates:
        try:
            cleaned = re.sub(r',\s*}', '}', candidate)
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict) and len(score_keys.intersection(parsed.keys())) >= 3:
                scores = {}
                for key in score_keys:
                    val = parsed.get(key, 0)
                    try: val = float(val)
                    except: val = 0.0
                    scores[key] = max(0.0, min(10.0, val))
                scores['brief_justification'] = str(parsed.get('brief_justification', ''))
                return scores
        except json.JSONDecodeError:
            continue

    scores = {}
    for key in score_keys:
        m = re.search(rf'{key}\W*[:=]\s*([\d]+(?:\.\d+)?)', text, re.IGNORECASE)
        if m:
            scores[key] = max(0.0, min(10.0, float(m.group(1))))
    if len(scores) >= 3:
        for key in score_keys:
            if key not in scores: scores[key] = 0.0
        scores['brief_justification'] = ''
        return scores

    raise ValueError(f"Parse failed. Preview: {text[:200]}")


def weighted_score(scores):
    return round(sum(scores.get(k, 0) * w for k, w in SCORING_WEIGHTS.items()), 2)


def get_questions():
    from questions import get_question_by_id as w1
    from questions_wave2_15032026 import get_wave2_question_by_id as w2

    def get_q(qid):
        return w1(qid) or w2(qid)

    all_q = []
    for cat, ids in QUESTION_IDS.items():
        for qid in ids:
            q = get_q(qid)
            if q:
                all_q.append((qid, cat, q["question"]))
            else:
                print(f"  Warning: {qid} not found, skipping")
    return all_q


class H2HState:
    def __init__(self):
        self.started_at = datetime.now().isoformat()
        self.completed = []
        self.failed = []
        self.cost = 0.0

    def save(self):
        STATE_FILE.write_text(json.dumps(self.__dict__, indent=2))

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


async def run_one(qid, category, question, state):
    n = len(state.completed) + len(state.failed) + 1
    budget_left = BUDGET_LIMIT - state.cost

    if budget_left < ESTIMATED_COST_PER_Q:
        print(f"  Budget exhausted. Stopping.")
        return False

    print(f"\n[{n}] {qid} ({category}) -- ${budget_left:.2f} left")

    result = {
        "question_id": qid, "category": category,
        "question_text": question[:200],
        "timestamp": datetime.now().isoformat(),
        "judge": JUDGE["display_name"],
        "contestants": {},
    }

    # Generate responses from all 3 contestants
    for key, config in CONTESTANTS.items():
        try:
            text, tokens, ms = await call_model(
                config["model_id"], question,
                max_tokens=GENERATION_PARAMS["max_tokens"],
                temperature=GENERATION_PARAMS["temperature"],
            )
            result["contestants"][key] = {
                "display_name": config["display_name"],
                "model_id": config["model_id"],
                "response": text, "tokens": tokens, "time_ms": ms,
            }
            print(f"  {config['display_name']}: {ms}ms, {tokens} tok")
        except Exception as e:
            result["contestants"][key] = {
                "display_name": config["display_name"],
                "model_id": config["model_id"],
                "error": str(e)[:200],
            }
            print(f"  {config['display_name']}: ERROR - {str(e)[:60]}")

    # Judge each response
    for key, cdata in result["contestants"].items():
        if "error" in cdata:
            cdata["judgment"] = {"error": "no_response"}
            continue

        judge_prompt = f"Question asked:\n{question}\n\nResponse to evaluate:\n{cdata['response']}\n\nProvide your scores as JSON only."

        try:
            judgment_text, _, _ = await call_model(
                JUDGE["model_id"], judge_prompt,
                system_prompt=JUDGE_SYSTEM_PROMPT,
                max_tokens=JUDGMENT_PARAMS["max_tokens"],
                temperature=JUDGMENT_PARAMS["temperature"],
            )
            scores = parse_judgment(judgment_text)
            scores["weighted_score"] = weighted_score(scores)
            cdata["judgment"] = scores
            print(f"  Judge -> {cdata['display_name']}: {scores['weighted_score']}")
        except Exception as e:
            cdata["judgment"] = {"error": str(e)[:200]}
            print(f"  Judge -> {cdata['display_name']}: PARSE ERROR")

    # Determine winner
    scores_map = {}
    for key, cdata in result["contestants"].items():
        j = cdata.get("judgment", {})
        if "weighted_score" in j:
            scores_map[key] = j["weighted_score"]

    if len(scores_map) >= 2:
        ranked = sorted(scores_map.items(), key=lambda x: -x[1])
        result["winner"] = CONTESTANTS[ranked[0][0]]["display_name"]
        result["ranking"] = [
            {"model": CONTESTANTS[k]["display_name"], "score": s}
            for k, s in ranked
        ]
    else:
        result["winner"] = "incomplete"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / f"{qid}.json").write_text(json.dumps(result, indent=2))

    state.completed.append({"qid": qid, "cat": category, "winner": result["winner"]})
    state.cost += ESTIMATED_COST_PER_Q
    state.save()
    return True


async def run_batch():
    all_questions = get_questions()
    state = H2HState.load()

    if state.done_ids:
        remaining = [(q, c, t) for q, c, t in all_questions if q not in state.done_ids]
        print(f"\n  Resuming: {len(state.completed)} done, {len(remaining)} remaining")
        print(f"  Spent: ${state.cost:.2f}/${BUDGET_LIMIT:.2f}")
        if input("Continue? (yes/no): ").lower() != "yes":
            return
    else:
        remaining = all_questions
        print(f"\n  GEMMA 4 HEAD-TO-HEAD (3-way)")
        print(f"  Contestants: {', '.join(c['display_name'] for c in CONTESTANTS.values())}")
        print(f"  Judge: {JUDGE['display_name']}")
        print(f"  Questions: {len(all_questions)} (6 per category)")
        print(f"  Est. cost: ${len(all_questions) * ESTIMATED_COST_PER_Q:.2f}")
        print(f"  Budget: ${BUDGET_LIMIT:.2f}")
        if input("\nStart? (yes/no): ").lower() != "yes":
            return

    print(f"\n  Starting in 5 seconds...")
    time.sleep(5)

    current_cat = None
    for qid, cat, question in remaining:
        if cat != current_cat:
            if current_cat is not None:
                time.sleep(10)
            current_cat = cat
            print(f"\n{'#'*60}")
            print(f"  CATEGORY: {cat.upper()}")
            print(f"{'#'*60}")

        ok = await run_one(qid, cat, question, state)
        if not ok:
            break
        await asyncio.sleep(2)

    # Summary
    print(f"\n{'='*60}")
    print(f"  GEMMA 4 H2H COMPLETE")
    print(f"{'='*60}")

    wins = defaultdict(int)
    cat_wins = defaultdict(lambda: defaultdict(int))

    for e in state.completed:
        w = e.get("winner", "incomplete")
        if w != "incomplete":
            wins[w] += 1
        cat_wins[e["cat"]][w] += 1

    total = sum(wins.values())
    print(f"\n  Total: {len(state.completed)} evals, Cost: ${state.cost:.2f}")
    for name, count in sorted(wins.items(), key=lambda x: -x[1]):
        pct = count / total * 100 if total else 0
        print(f"  {name}: {count} wins ({pct:.1f}%)")

    print(f"\n  By category:")
    for cat in QUESTION_IDS:
        cw = cat_wins.get(cat, {})
        parts = [f"{name}: {count}" for name, count in sorted(cw.items(), key=lambda x: -x[1]) if name != "incomplete"]
        print(f"    {cat:20s} {', '.join(parts)}")

    # Compute average scores per model
    print(f"\n  Average scores:")
    model_scores = defaultdict(list)
    for e in state.completed:
        qid = e["qid"]
        result_path = OUTPUT_DIR / f"{qid}.json"
        if result_path.exists():
            data = json.loads(result_path.read_text())
            for key, cdata in data.get("contestants", {}).items():
                j = cdata.get("judgment", {})
                if "weighted_score" in j:
                    model_scores[cdata["display_name"]].append(j["weighted_score"])

    for name, scores in sorted(model_scores.items(), key=lambda x: -sum(x[1])/len(x[1])):
        avg = sum(scores) / len(scores)
        print(f"    {name:25s} avg: {avg:.2f} ({len(scores)} evals)")

    summary = {
        "batch_id": "GEMMA4-H2H-20260404",
        "timestamp": datetime.now().isoformat(),
        "contestants": {k: v for k, v in CONTESTANTS.items()},
        "judge": JUDGE,
        "total_questions": len(state.completed),
        "wins": dict(wins),
        "category_breakdown": {cat: dict(cat_wins.get(cat, {})) for cat in QUESTION_IDS},
        "cost": state.cost,
    }
    (OUTPUT_DIR / "gemma4_h2h_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\n  Summary saved to: {OUTPUT_DIR}/gemma4_h2h_summary.json")


if __name__ == "__main__":
    asyncio.run(run_batch())
