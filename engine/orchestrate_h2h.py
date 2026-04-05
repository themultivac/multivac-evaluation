#!/usr/bin/env python3
"""
Multivac V5.1 — Head-to-Head Evaluation
2 contestants, 1 external judge, 150 questions.

Contestants: Qwen 3.6 Plus, DeepSeek V3.2
Judge: Claude Opus 4.6

Usage:
    cd ~/Multivac/v5/multivac_v5
    python orchestrate_h2h.py
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

# ── Config ──
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

CONTESTANTS = {
    "qwen36_plus": {
        "model_id": "qwen/qwen3.6-plus:free",
        "display_name": "Qwen 3.6 Plus",
    },
    "deepseek_v32": {
        "model_id": "deepseek/deepseek-v3.2",
        "display_name": "DeepSeek V3.2",
    },
}

JUDGE = {
    "model_id": "anthropic/claude-opus-4.6",
    "display_name": "Claude Opus 4.6",
}

CATEGORIES = ["code", "reasoning", "analysis", "communication", "meta_alignment"]

STATE_FILE = Path("h2h_state.json")
OUTPUT_DIR = Path("outputs/H2H-BATCH-20260403")
BUDGET_LIMIT = 15.00
ESTIMATED_COST_PER_QUESTION = 0.08  # 4 API calls per question

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
    "correctness": 0.25,
    "completeness": 0.20,
    "clarity": 0.20,
    "depth": 0.20,
    "usefulness": 0.15,
}


# ── API ──
async def call_model(model_id, prompt, system_prompt="", max_tokens=2048, temperature=0.7):
    """Call a model via OpenRouter. Returns (text, tokens, time_ms)."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://themultivac.com",
        "X-Title": "The Multivac H2H",
    }
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_id,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    start = time.time()
    async with httpx.AsyncClient(timeout=180.0) as client:
        resp = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
        )
        resp.raise_for_status()

    elapsed_ms = int((time.time() - start) * 1000)
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    tokens = data.get("usage", {}).get("total_tokens", 0)
    return content, tokens, elapsed_ms


# ── Parser ──
def parse_judgment(raw_text):
    """Extract scores from judge output."""
    text = raw_text.strip()
    text = re.sub(r'<think(?:ing)?>[\s\S]*?</think(?:ing)?>', '', text, flags=re.IGNORECASE)

    code_block = re.search(r'```(?:json)?\s*\n?(\{[\s\S]*?\})\s*\n?```', text)
    if code_block:
        text = code_block.group(1)

    # Find JSON objects
    candidates = []
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == '{':
            if depth == 0:
                start = i
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
                    try:
                        val = float(val)
                    except (ValueError, TypeError):
                        val = 0.0
                    scores[key] = max(0.0, min(10.0, val))
                scores['brief_justification'] = str(parsed.get('brief_justification', ''))
                return scores
        except json.JSONDecodeError:
            continue

    # Regex fallback
    scores = {}
    for key in score_keys:
        m = re.search(rf'{key}\W*[:=]\s*([\d]+(?:\.\d+)?)', text, re.IGNORECASE)
        if m:
            scores[key] = max(0.0, min(10.0, float(m.group(1))))

    if len(scores) >= 3:
        for key in score_keys:
            if key not in scores:
                scores[key] = 0.0
        scores['brief_justification'] = ''
        return scores

    raise ValueError(f"Parse failed. Preview: {text[:200]}")


def weighted_score(scores):
    return round(sum(scores.get(k, 0) * w for k, w in SCORING_WEIGHTS.items()), 2)


# ── Questions ──
def get_all_questions():
    from questions import QUESTIONS
    from questions_wave2_15032026 import WAVE2_QUESTIONS

    all_q = []
    for cat in CATEGORIES:
        for q in QUESTIONS.get(cat, []):
            all_q.append((q["id"], cat, q["question"]))
        for q in WAVE2_QUESTIONS.get(cat, []):
            all_q.append((q["id"], cat, q["question"]))
    return all_q


# ── State ──
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


# ── Single eval ──
async def run_one(qid, category, question, state):
    """Run one question: 2 responses + 2 judgments."""
    n = len(state.completed) + len(state.failed) + 1
    budget_left = BUDGET_LIMIT - state.cost

    if budget_left < ESTIMATED_COST_PER_QUESTION:
        print(f"  Budget exhausted. Stopping.")
        return False

    print(f"\n[{n}] {qid} ({category}) -- ${budget_left:.2f} left")

    result = {
        "question_id": qid,
        "category": category,
        "question_text": question[:200],
        "timestamp": datetime.now().isoformat(),
        "judge": JUDGE["display_name"],
        "judge_model_id": JUDGE["model_id"],
        "contestants": {},
    }

    # Generate responses
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
                "response": text,
                "tokens": tokens,
                "time_ms": ms,
            }
            print(f"  {config['display_name']}: {ms}ms, {tokens} tokens")
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

    if len(scores_map) == 2:
        keys = list(scores_map.keys())
        if scores_map[keys[0]] > scores_map[keys[1]]:
            result["winner"] = CONTESTANTS[keys[0]]["display_name"]
        elif scores_map[keys[1]] > scores_map[keys[0]]:
            result["winner"] = CONTESTANTS[keys[1]]["display_name"]
        else:
            result["winner"] = "tie"
        result["margin"] = round(abs(scores_map[keys[0]] - scores_map[keys[1]]), 2)
    else:
        result["winner"] = "incomplete"

    # Save individual result
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUT_DIR / f"{qid}.json"
    result_path.write_text(json.dumps(result, indent=2))

    state.completed.append({"qid": qid, "cat": category, "winner": result["winner"]})
    state.cost += ESTIMATED_COST_PER_QUESTION
    state.save()
    return True


# ── Main ──
async def run_batch():
    all_questions = get_all_questions()
    state = H2HState.load()

    if state.done_ids:
        remaining = [(q, c, t) for q, c, t in all_questions if q not in state.done_ids]
        print(f"\n  Resuming: {len(state.completed)} done, {len(state.failed)} failed, {len(remaining)} remaining")
        print(f"  Spent: ${state.cost:.2f}/${BUDGET_LIMIT:.2f}")
        if input("Continue? (yes/no): ").lower() != "yes":
            return
    else:
        remaining = all_questions
        print(f"\n  HEAD-TO-HEAD EVALUATION")
        print(f"  Contestants: {', '.join(c['display_name'] for c in CONTESTANTS.values())}")
        print(f"  Judge: {JUDGE['display_name']}")
        print(f"  Questions: {len(all_questions)}")
        print(f"  Est. cost: ${len(all_questions) * ESTIMATED_COST_PER_QUESTION:.2f}")
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

    # ── Summary ──
    print(f"\n{'='*60}")
    print(f"  HEAD-TO-HEAD COMPLETE")
    print(f"{'='*60}")

    wins = defaultdict(int)
    ties = 0
    incomplete = 0
    cat_wins = defaultdict(lambda: defaultdict(int))

    for e in state.completed:
        w = e.get("winner", "incomplete")
        if w == "tie":
            ties += 1
        elif w == "incomplete":
            incomplete += 1
        else:
            wins[w] += 1
        cat_wins[e["cat"]][w] += 1

    total_decided = sum(wins.values()) + ties
    print(f"\n  Total: {len(state.completed)} evals")
    print(f"  Cost: ${state.cost:.2f}")

    for name, count in sorted(wins.items(), key=lambda x: -x[1]):
        pct = count / total_decided * 100 if total_decided else 0
        print(f"  {name}: {count} wins ({pct:.1f}%)")
    print(f"  Ties: {ties}")
    if incomplete:
        print(f"  Incomplete: {incomplete}")

    print(f"\n  By category:")
    for cat in CATEGORIES:
        cw = cat_wins.get(cat, {})
        parts = []
        for name in [c["display_name"] for c in CONTESTANTS.values()]:
            if cw.get(name, 0) > 0:
                parts.append(f"{name}: {cw[name]}")
        if cw.get("tie", 0) > 0:
            parts.append(f"Tie: {cw['tie']}")
        print(f"    {cat:20s} {', '.join(parts)}")

    # Save summary
    summary = {
        "batch_id": "H2H-BATCH-20260403",
        "timestamp": datetime.now().isoformat(),
        "contestants": {k: v for k, v in CONTESTANTS.items()},
        "judge": JUDGE,
        "total_questions": len(state.completed),
        "wins": dict(wins),
        "ties": ties,
        "incomplete": incomplete,
        "category_breakdown": {cat: dict(cat_wins.get(cat, {})) for cat in CATEGORIES},
        "cost": state.cost,
    }
    (OUTPUT_DIR / "h2h_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\n  Summary saved to: {OUTPUT_DIR}/h2h_summary.json")


if __name__ == "__main__":
    asyncio.run(run_batch())
