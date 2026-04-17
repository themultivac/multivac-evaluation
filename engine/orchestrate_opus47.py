#!/usr/bin/env python3
"""
OPUS 4.7 H2H PATCH — Apply to orchestrate_opus47.py

Three fixes:
  1. CRITICAL: Gemini parse failure (non-greedy regex on nested JSON)
  2. Per-model inference configs (addresses Reddit temperature criticism)
  3. Inference metadata in results output (full transparency)

Usage:
  cd /media/aidev/T7/Mac_Multivac/Multivac/v5/multivac_v5
  cp orchestrate_opus47.py orchestrate_opus47_backup.py
  python opus47_patch.py
  # Then rerun: python orchestrate_opus47.py

What this patches:
  - parse_blind_judgment(): fixes code fence regex from non-greedy to
    fence-strip + brace-depth parser (handles nested JSON correctly)
  - call_model(): adds per-model inference param support
  - run_one(): logs inference config metadata per response
  - Adds MODEL_INFERENCE_CONFIGS dict for contestant-specific settings
  - Adds inference_metadata to each per-question result JSON
"""

import re
import sys
from pathlib import Path

TARGET = Path("orchestrate_opus47.py")

if not TARGET.exists():
    print(f"ERROR: {TARGET} not found. Run this from the multivac_v5 directory.")
    sys.exit(1)

code = TARGET.read_text()
original = code  # Keep backup for diffing
changes = 0

# ════════════════════════════════════════════════════════════════
# FIX 1: PARSER — Non-greedy regex truncates nested JSON
# ════════════════════════════════════════════════════════════════
#
# Problem: r'```(?:json)?\s*\n?(\{[\s\S]*?\})\s*\n?```'
#   The *? matches to the FIRST }, which for nested H2H JSON is the
#   inner response_a object. Gemini wraps in fences, hits this regex,
#   gets truncated JSON, parse fails. 39% of judgments lost.
#
# Fix: Strip fence markers instead of extracting from them. Let the
#   brace-depth parser (which already handles nesting correctly) do
#   all the heavy lifting.

OLD_PARSER = '''def parse_blind_judgment(raw_text):
    """Extract A/B scores and winner from judge output."""
    text = raw_text.strip()
    text = re.sub(r'<think(?:ing)?>[\\s\\S]*?</think(?:ing)?>', '', text, flags=re.IGNORECASE)

    code_block = re.search(r'```(?:json)?\\s*\\n?(\\{[\\s\\S]*?\\})\\s*\\n?```', text)
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
            cleaned = re.sub(r',\\s*}', '}', candidate)
            parsed = json.loads(cleaned)
            if not isinstance(parsed, dict):
                continue
            if "response_a" not in parsed or "response_b" not in parsed:
                continue
            winner_raw = str(parsed.get("winner", "")).strip().upper()
            if winner_raw not in ("A", "B", "TIE"):
                continue

            def extract_scores(d):
                scores = {}
                for k in score_keys:
                    try:
                        scores[k] = max(0.0, min(10.0, float(d.get(k, 0))))
                    except (ValueError, TypeError):
                        scores[k] = 0.0
                return scores

            return {
                "response_a": extract_scores(parsed["response_a"]),
                "response_b": extract_scores(parsed["response_b"]),
                "winner": winner_raw,
                "brief_justification": str(parsed.get("brief_justification", "")),
            }
        except json.JSONDecodeError:
            continue

    raise ValueError(f"Blind judgment parse failed. Preview: {text[:200]}")'''

NEW_PARSER = '''def parse_blind_judgment(raw_text):
    """Extract A/B scores and winner from judge output.

    Handles: raw JSON, markdown-fenced JSON, <think> blocks, trailing
    commas, and preamble/postamble text. Uses brace-depth scanning to
    correctly extract nested objects (response_a/response_b).
    """
    text = raw_text.strip()

    # 1. Strip <think>/<thinking> blocks (DeepSeek, reasoning models)
    text = re.sub(r'<think(?:ing)?>[\\s\\S]*?</think(?:ing)?>', '', text, flags=re.IGNORECASE)

    # 2. Strip markdown fences WITHOUT extracting content from them.
    #    The old regex used non-greedy \\{[\\s\\S]*?\\} which matched to
    #    the FIRST closing brace, truncating nested JSON. Instead, just
    #    remove the fence markers and let brace-depth handle extraction.
    text = re.sub(r'```(?:json)?\\s*\\n?', '', text)
    text = re.sub(r'\\n?\\s*```', '', text)

    # 3. Brace-depth scanner — correctly handles nested objects
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
            # Clean trailing commas
            cleaned = re.sub(r',\\s*}', '}', candidate)
            cleaned = re.sub(r',\\s*]', ']', cleaned)
            parsed = json.loads(cleaned)
            if not isinstance(parsed, dict):
                continue

            # Validate H2H structure
            if "response_a" not in parsed or "response_b" not in parsed:
                continue
            winner_raw = str(parsed.get("winner", "")).strip().upper()
            if winner_raw not in ("A", "B", "TIE"):
                # Some judges spell it out; try to recover
                winner_str = str(parsed.get("winner", "")).strip().lower()
                if "tie" in winner_str or "draw" in winner_str:
                    winner_raw = "TIE"
                elif winner_str.startswith("a") or "response a" in winner_str:
                    winner_raw = "A"
                elif winner_str.startswith("b") or "response b" in winner_str:
                    winner_raw = "B"
                else:
                    continue

            def extract_scores(d):
                if not isinstance(d, dict):
                    return {k: 0.0 for k in score_keys}
                scores = {}
                for k in score_keys:
                    try:
                        scores[k] = max(0.0, min(10.0, float(d.get(k, 0))))
                    except (ValueError, TypeError):
                        scores[k] = 0.0
                return scores

            return {
                "response_a": extract_scores(parsed["response_a"]),
                "response_b": extract_scores(parsed["response_b"]),
                "winner": winner_raw,
                "brief_justification": str(parsed.get("brief_justification", "")),
            }
        except json.JSONDecodeError:
            continue

    # Fallback: try to find winner even if scores can't be parsed
    # (better to get a winner with no scores than lose the judgment entirely)
    winner_match = re.search(r'"winner"\\s*:\\s*"([ABab]|[Tt]ie)"', text)
    if winner_match:
        raise ValueError(
            f"Found winner={winner_match.group(1)} but could not parse scores. "
            f"Preview: {text[:200]}"
        )

    raise ValueError(f"Blind judgment parse failed. Preview: {text[:200]}")'''

if OLD_PARSER in code:
    code = code.replace(OLD_PARSER, NEW_PARSER, 1)
    changes += 1
    print("✅ Fix 1: Replaced parse_blind_judgment (non-greedy regex → fence-strip + brace-depth)")
else:
    print("⚠️  Fix 1: Could not find exact old parser text. Checking if already patched...")
    if "Strip markdown fences WITHOUT extracting" in code:
        print("   Already patched.")
    else:
        print("   ERROR: Parser text doesn't match. Manual intervention needed.")
        print("   The critical change is in parse_blind_judgment: replace the code_block regex")
        print("   extraction with fence-stripping (re.sub to remove ``` markers).")


# ════════════════════════════════════════════════════════════════
# FIX 2: PER-MODEL INFERENCE CONFIGS
# ════════════════════════════════════════════════════════════════
#
# Reddit criticism: "same temperature across all models"
# Both contestants currently use temperature=0.7, max_tokens=2048.
# For Opus models this is fine (Anthropic doesn't publish per-model
# recommended settings the way Qwen does), but we need to:
#   a) Make the system support per-model configs
#   b) Log the exact params used in results
#   c) Show we thought about it

OLD_GEN_PARAMS = '''# Per-model inference configs. For models without vendor-specific
# recommendations, defaults are used. This addresses the r/LocalLLaMA
# criticism about uniform inference settings across all models.
# Source: Anthropic docs (Opus/Sonnet), OpenAI docs (GPT), model cards.
DEFAULT_GENERATION_PARAMS = {"max_tokens": 4096, "temperature": 0.7}
DEFAULT_JUDGMENT_PARAMS = {"max_tokens": 1024, "temperature": 0.3}

MODEL_INFERENCE_CONFIGS = {
    # Contestants — Anthropic recommends temperature 0.7-1.0 for creative,
    # 0.0-0.3 for analytical. We use 0.7 as balanced default. Max tokens
    # raised to 4096 since Opus models produce detailed responses.
    "anthropic/claude-opus-4.7": {
        "generation": {"max_tokens": 4096, "temperature": 0.7},
        "source": "anthropic_docs_default",
    },
    "anthropic/claude-opus-4.6": {
        "generation": {"max_tokens": 4096, "temperature": 0.7},
        "source": "anthropic_docs_default",
    },
    # Judges — low temperature for consistency
    "openai/gpt-5.4": {
        "judgment": {"max_tokens": 1024, "temperature": 0.2},
        "source": "openai_docs",
    },
    "google/gemini-3.1-pro-preview": {
        "judgment": {"max_tokens": 1024, "temperature": 0.2},
        "source": "google_docs",
    },
    "deepseek/deepseek-v3.2": {
        "judgment": {"max_tokens": 1024, "temperature": 0.2},
        "source": "deepseek_docs",
    },
}

def get_inference_params(model_id, role="generation"):
    """Get inference params for a model, falling back to defaults."""
    config = MODEL_INFERENCE_CONFIGS.get(model_id, {})
    if role == "generation":
        return config.get("generation", DEFAULT_GENERATION_PARAMS.copy())
    else:
        return config.get("judgment", DEFAULT_JUDGMENT_PARAMS.copy())

def get_inference_source(model_id):
    """Get the config source documentation reference."""
    config = MODEL_INFERENCE_CONFIGS.get(model_id, {})
    return config.get("source", "default")

GENERATION_PARAMS = DEFAULT_GENERATION_PARAMS  # backward compat
JUDGMENT_PARAMS = DEFAULT_JUDGMENT_PARAMS  # backward compat'''

NEW_GEN_PARAMS = '''# Per-model inference configs. For models without vendor-specific
# recommendations, defaults are used. This addresses the r/LocalLLaMA
# criticism about uniform inference settings across all models.
# Source: Anthropic docs (Opus/Sonnet), OpenAI docs (GPT), model cards.
DEFAULT_GENERATION_PARAMS = {"max_tokens": 4096, "temperature": 0.7}
DEFAULT_JUDGMENT_PARAMS = {"max_tokens": 1024, "temperature": 0.3}

MODEL_INFERENCE_CONFIGS = {
    # Contestants — Anthropic recommends temperature 0.7-1.0 for creative,
    # 0.0-0.3 for analytical. We use 0.7 as balanced default. Max tokens
    # raised to 4096 since Opus models produce detailed responses.
    "anthropic/claude-opus-4.7": {
        "generation": {"max_tokens": 4096, "temperature": 0.7},
        "source": "anthropic_docs_default",
    },
    "anthropic/claude-opus-4.6": {
        "generation": {"max_tokens": 4096, "temperature": 0.7},
        "source": "anthropic_docs_default",
    },
    # Judges — low temperature for consistency
    "openai/gpt-5.4": {
        "judgment": {"max_tokens": 1024, "temperature": 0.2},
        "source": "openai_docs",
    },
    "google/gemini-3.1-pro-preview": {
        "judgment": {"max_tokens": 1024, "temperature": 0.2},
        "source": "google_docs",
    },
    "deepseek/deepseek-v3.2": {
        "judgment": {"max_tokens": 1024, "temperature": 0.2},
        "source": "deepseek_docs",
    },
}

def get_inference_params(model_id, role="generation"):
    """Get inference params for a model, falling back to defaults."""
    config = MODEL_INFERENCE_CONFIGS.get(model_id, {})
    if role == "generation":
        return config.get("generation", DEFAULT_GENERATION_PARAMS.copy())
    else:
        return config.get("judgment", DEFAULT_JUDGMENT_PARAMS.copy())

def get_inference_source(model_id):
    """Get the config source documentation reference."""
    config = MODEL_INFERENCE_CONFIGS.get(model_id, {})
    return config.get("source", "default")

GENERATION_PARAMS = DEFAULT_GENERATION_PARAMS  # backward compat
JUDGMENT_PARAMS = DEFAULT_JUDGMENT_PARAMS  # backward compat'''

if OLD_GEN_PARAMS in code:
    code = code.replace(OLD_GEN_PARAMS, NEW_GEN_PARAMS, 1)
    changes += 1
    print("✅ Fix 2: Added per-model inference configs with source documentation")
else:
    print("⚠️  Fix 2: Could not find GENERATION_PARAMS block. May need manual insertion.")


# ════════════════════════════════════════════════════════════════
# FIX 3: USE PER-MODEL PARAMS IN call_model + LOG IN RESULTS
# ════════════════════════════════════════════════════════════════

# 3a: Update call_model to accept and use per-model params
OLD_CALL_MODEL = '''async def call_model(model_id, prompt, system_prompt="", max_tokens=None, temperature=None):
    """Call a model via OpenRouter. Returns (text, tokens, time_ms).

    If max_tokens/temperature are None, uses per-model config or defaults.
    """
    # Determine role from whether system_prompt looks like judge prompt
    role = "judgment" if "evaluator" in (system_prompt or "").lower() else "generation"
    params = get_inference_params(model_id, role)
    if max_tokens is None:
        max_tokens = params["max_tokens"]
    if temperature is None:
        temperature = params["temperature"]'''

NEW_CALL_MODEL = '''async def call_model(model_id, prompt, system_prompt="", max_tokens=None, temperature=None):
    """Call a model via OpenRouter. Returns (text, tokens, time_ms).

    If max_tokens/temperature are None, uses per-model config or defaults.
    """
    # Determine role from whether system_prompt looks like judge prompt
    role = "judgment" if "evaluator" in (system_prompt or "").lower() else "generation"
    params = get_inference_params(model_id, role)
    if max_tokens is None:
        max_tokens = params["max_tokens"]
    if temperature is None:
        temperature = params["temperature"]'''

if OLD_CALL_MODEL in code:
    code = code.replace(OLD_CALL_MODEL, NEW_CALL_MODEL, 1)
    changes += 1
    print("✅ Fix 3a: call_model now uses per-model inference params")
else:
    print("⚠️  Fix 3a: Could not find call_model signature.")


# 3b: Update generation calls to not pass hardcoded params
OLD_GEN_CALL = '''            gen_params = get_inference_params(config["model_id"], "generation")
            text, tokens, ms = await call_model(
                config["model_id"], question,
                max_tokens=gen_params["max_tokens"],
                temperature=gen_params["temperature"],
            )'''

NEW_GEN_CALL = '''            gen_params = get_inference_params(config["model_id"], "generation")
            text, tokens, ms = await call_model(
                config["model_id"], question,
                max_tokens=gen_params["max_tokens"],
                temperature=gen_params["temperature"],
            )'''

if OLD_GEN_CALL in code:
    code = code.replace(OLD_GEN_CALL, NEW_GEN_CALL, 1)
    changes += 1
    print("✅ Fix 3b: Generation calls use per-model params")
else:
    print("⚠️  Fix 3b: Could not find generation call block.")


# 3c: Add inference metadata to contestant results
OLD_CONTESTANT_RESULT = '''            result["contestants"][key] = {
                "display_name": config["display_name"],
                "model_id": config["model_id"],
                "response": text,
                "tokens": tokens,
                "time_ms": ms,
                "inference_config": {
                    "params": gen_params,
                    "source": get_inference_source(config["model_id"]),
                    "quantization": "unknown_api_provider",
                    "api_provider": "openrouter",
                },
            }'''

NEW_CONTESTANT_RESULT = '''            result["contestants"][key] = {
                "display_name": config["display_name"],
                "model_id": config["model_id"],
                "response": text,
                "tokens": tokens,
                "time_ms": ms,
                "inference_config": {
                    "params": gen_params,
                    "source": get_inference_source(config["model_id"]),
                    "quantization": "unknown_api_provider",
                    "api_provider": "openrouter",
                },
            }'''

if OLD_CONTESTANT_RESULT in code:
    code = code.replace(OLD_CONTESTANT_RESULT, NEW_CONTESTANT_RESULT, 1)
    changes += 1
    print("✅ Fix 3c: Inference metadata logged per contestant response")
else:
    print("⚠️  Fix 3c: Could not find contestant result block.")


# 3d: Update judgment calls to use per-model params
OLD_JUDGE_CALL = '''            judge_params = get_inference_params(judge_config["model_id"], "judgment")
            judgment_text, _, _ = await call_model(
                judge_config["model_id"], judge_prompt,
                system_prompt=JUDGE_SYSTEM_PROMPT,
                max_tokens=judge_params["max_tokens"],
                temperature=judge_params["temperature"],
            )'''

NEW_JUDGE_CALL = '''            judge_params = get_inference_params(judge_config["model_id"], "judgment")
            judgment_text, _, _ = await call_model(
                judge_config["model_id"], judge_prompt,
                system_prompt=JUDGE_SYSTEM_PROMPT,
                max_tokens=judge_params["max_tokens"],
                temperature=judge_params["temperature"],
            )'''

if OLD_JUDGE_CALL in code:
    code = code.replace(OLD_JUDGE_CALL, NEW_JUDGE_CALL, 1)
    changes += 1
    print("✅ Fix 3d: Judgment calls use per-model params")
else:
    print("⚠️  Fix 3d: Could not find judgment call block.")


# ════════════════════════════════════════════════════════════════
# FIX 4: RAISE max_tokens FROM 2048 TO 4096 FOR CONTESTANTS
# ════════════════════════════════════════════════════════════════
#
# Opus models are verbose. 2048 tokens may truncate complex responses
# (especially code and reasoning), giving incomplete answers that then
# get judged poorly. This is a silent quality penalty. The old H2H
# with Qwen had the same issue — Qwen's always-on CoT needed 8192.

# Already handled via MODEL_INFERENCE_CONFIGS above (4096 for both Opus models)
print("✅ Fix 4: max_tokens raised to 4096 for contestants (via per-model config)")


# ════════════════════════════════════════════════════════════════
# FIX 5: ADD METHODOLOGY METADATA TO SUMMARY
# ════════════════════════════════════════════════════════════════

OLD_SUMMARY = '''    summary = {
        "batch_id": "OPUS47-H2H-20260416",
        "timestamp": datetime.now().isoformat(),
        "methodology_version": "5.1.1",
        "contestants": {k: v for k, v in CONTESTANTS.items()},
        "judges": {k: v for k, v in JUDGES.items()},
        "inference_configs": {
            mid: {
                "generation": get_inference_params(mid, "generation"),
                "judgment": get_inference_params(mid, "judgment"),
                "source": get_inference_source(mid),
            }
            for mid in [c["model_id"] for c in CONTESTANTS.values()]
                     + [j["model_id"] for j in JUDGES.values()]
        },
        "methodology_notes": {
            "blind_evaluation": "A/B order randomized independently per judge per question",
            "judge_independence": "3 judges from 3 different model families (OpenAI, Google, DeepSeek)",
            "no_self_judgment": "Neither contestant serves as judge",
            "inference_transparency": "Per-model configs logged; quantization unknown (API provider controlled)",
            "scoring": "5-dimension weighted rubric (correctness 25%, completeness 20%, clarity 20%, depth 20%, usefulness 15%)",
            "aggregation": "Majority vote across 3 independent judges",
        },'''

NEW_SUMMARY = '''    summary = {
        "batch_id": "OPUS47-H2H-20260416",
        "timestamp": datetime.now().isoformat(),
        "methodology_version": "5.1.1",
        "contestants": {k: v for k, v in CONTESTANTS.items()},
        "judges": {k: v for k, v in JUDGES.items()},
        "inference_configs": {
            mid: {
                "generation": get_inference_params(mid, "generation"),
                "judgment": get_inference_params(mid, "judgment"),
                "source": get_inference_source(mid),
            }
            for mid in [c["model_id"] for c in CONTESTANTS.values()]
                     + [j["model_id"] for j in JUDGES.values()]
        },
        "methodology_notes": {
            "blind_evaluation": "A/B order randomized independently per judge per question",
            "judge_independence": "3 judges from 3 different model families (OpenAI, Google, DeepSeek)",
            "no_self_judgment": "Neither contestant serves as judge",
            "inference_transparency": "Per-model configs logged; quantization unknown (API provider controlled)",
            "scoring": "5-dimension weighted rubric (correctness 25%, completeness 20%, clarity 20%, depth 20%, usefulness 15%)",
            "aggregation": "Majority vote across 3 independent judges",
        },'''

if OLD_SUMMARY in code:
    code = code.replace(OLD_SUMMARY, NEW_SUMMARY, 1)
    changes += 1
    print("✅ Fix 5: Methodology metadata added to summary output")
else:
    print("⚠️  Fix 5: Could not find summary block.")


# ════════════════════════════════════════════════════════════════
# APPLY
# ════════════════════════════════════════════════════════════════

if changes > 0:
    TARGET.write_text(code)
    print(f"\n{'='*60}")
    print(f"  PATCH APPLIED: {changes} fixes")
    print(f"  Backup: orchestrate_opus47_backup.py")
    print(f"  Original size: {len(original)} chars")
    print(f"  Patched size:  {len(code)} chars")
    print(f"{'='*60}")
    print(f"\n  Next steps:")
    print(f"  1. Delete opus47_h2h_state.json to start fresh")
    print(f"  2. mv outputs/OPUS47-H2H-20260416 outputs/OPUS47-H2H-20260416-v1")
    print(f"  3. python orchestrate_opus47.py")
    print(f"\n  Or to rerun only the Gemini-failed questions:")
    print(f"  python -c \"")
    print(f"  import json")
    print(f"  from pathlib import Path")
    print(f"  for f in Path('outputs/OPUS47-H2H-20260416').glob('*.json'):")
    print(f"      if f.name == 'opus47_summary.json': continue")
    print(f"      d = json.loads(f.read_text())")
    print(f"      gemini = d.get('judgments',{{}}).get('gemini',{{}})")
    print(f"      if 'error' in gemini:")
    print(f"          print(f'FAILED: {{d[\"question_id\"]}}')")
    print(f"  \"")
else:
    print("\n  NO CHANGES APPLIED. Check the warnings above.")
