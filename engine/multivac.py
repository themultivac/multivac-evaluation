"""
Multivac V5 - AI Model Evaluation Engine
10×10 Peer Matrix Evaluation System with Category-Specific Model Pools

Usage:
    python multivac.py --question "Your question here" --category code
    python multivac.py --question-id CODE-001
    python multivac.py --interactive
    python multivac.py --list-questions
    python multivac.py --list-models --category code
"""

import asyncio
import json
import re
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional
import httpx
from dataclasses import dataclass, asdict
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Category-specific model loading
from category_loader import (
    get_models_for_category,
    get_active_models_for_category,
    get_model_display_name,
    get_model_config,
    get_category_info,
    list_all_categories,
    get_category_summary
)

from questions import get_question_by_id, get_questions_by_category

# ============================================================
# CONFIGURATION
# ============================================================

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_BASE_URL = "https://api.x.ai/v1"

# Paths
PATHS = {
    "outputs": "outputs",
    "tracker": "data/tracker.json"
}

# Generation parameters
GENERATION_PARAMS = {
    "max_tokens": 2048,
    "temperature": 0.7
}

# Judgment parameters
JUDGMENT_PARAMS = {
    "max_tokens": 1024,
    "temperature": 0.3  # Lower temp for more consistent judging
}

# Scoring weights
SCORING = {
    "criteria": {
        "correctness": {"weight": 0.25, "description": "Factual accuracy and logical validity"},
        "completeness": {"weight": 0.20, "description": "Thorough coverage of the topic"},
        "clarity": {"weight": 0.20, "description": "Clear, well-structured communication"},
        "depth": {"weight": 0.20, "description": "Insightful analysis beyond surface level"},
        "usefulness": {"weight": 0.15, "description": "Practical value and actionability"}
    }
}

# Judge prompts
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

JUDGE_USER_PROMPT_TEMPLATE = """Question asked:
{question}

Response to evaluate:
{response}

Provide your scores as JSON only."""


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class ModelResponse:
    """A single model's response to a question"""
    model_key: str
    model_name: str
    response: str
    generation_time_ms: int
    tokens_used: int
    error: Optional[str] = None

@dataclass  
class JudgmentScore:
    """A single judgment of one response by one judge"""
    judge_key: str
    judge_name: str
    respondent_key: str
    respondent_name: str
    correctness: float
    completeness: float
    clarity: float
    depth: float
    usefulness: float
    weighted_score: float
    brief_justification: str
    error: Optional[str] = None

@dataclass
class EvaluationResult:
    """Complete evaluation result for a question"""
    evaluation_id: str
    timestamp: str
    question_id: str
    question_text: str
    category: str
    models_used: list[str]  # Track which model pool was used
    responses: list  # list[ModelResponse] as dicts
    judgments: list  # list[JudgmentScore] as dicts - 10×10 = 100 judgments
    rankings: dict  # Final rankings
    meta_analysis: dict  # Which judges are strictest, agreement rates, etc.


# ============================================================
# API CLIENTS
# ============================================================

class OpenRouterClient:
    """Client for OpenRouter API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = OPENROUTER_BASE_URL
    
    async def generate(
        self, 
        model_id: str, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> tuple[str, int, int]:
        """Generate a response from a model. Returns (response, tokens, time_ms)"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://multivac.com",
            "X-Title": "The Multivac"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        start_time = datetime.now()
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
        elapsed_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        data = response.json()
        
        content = data["choices"][0]["message"]["content"]
        tokens = data.get("usage", {}).get("total_tokens", 0)
        
        return content, tokens, elapsed_ms


class XAIClient:
    """Client for xAI (Grok) API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = XAI_BASE_URL
    
    async def generate(
        self, 
        model_id: str, 
        prompt: str, 
        system_prompt: str = "",
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> tuple[str, int, int]:
        """Generate a response from Grok. Returns (response, tokens, time_ms)"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        start_time = datetime.now()
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
        elapsed_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        data = response.json()
        
        content = data["choices"][0]["message"]["content"]
        tokens = data.get("usage", {}).get("total_tokens", 0)
        
        return content, tokens, elapsed_ms


# ============================================================
# EVALUATION ENGINE
# ============================================================

class MultivacEngine:
    """Main evaluation engine for The Multivac"""
    
    def __init__(self):
        # Validate API keys
        if not OPENROUTER_API_KEY:
            print("⚠️  Warning: OPENROUTER_API_KEY not set in environment")
        if not XAI_API_KEY:
            print("⚠️  Warning: XAI_API_KEY not set in environment")
            
        self.openrouter = OpenRouterClient(OPENROUTER_API_KEY) if OPENROUTER_API_KEY else None
        self.xai = XAIClient(XAI_API_KEY) if XAI_API_KEY else None
        self.tracker_path = Path(PATHS["tracker"])
        self.outputs_path = Path(PATHS["outputs"])
        
        # Ensure directories exist
        self.tracker_path.parent.mkdir(parents=True, exist_ok=True)
        self.outputs_path.mkdir(parents=True, exist_ok=True)
        
        # Current category context (set during evaluation)
        self._current_category = None
    
    def _get_model_config(self, model_key: str) -> dict:
        """Get model config using current category context"""
        return get_model_config(self._current_category, model_key)
    
    def _get_model_display_name(self, model_key: str) -> str:
        """Get model display name using current category context"""
        return get_model_display_name(self._current_category, model_key)
    
    async def _generate_single(self, model_key: str, prompt: str) -> ModelResponse:
        """Generate response from a single model"""
        model_config = self._get_model_config(model_key)
        model_name = model_config.get("display_name", model_key)
        model_id = model_config.get("model_id", model_key)
        provider = model_config.get("provider", "openrouter")
        
        try:
            if provider == "openrouter":
                if not self.openrouter:
                    raise ValueError("OpenRouter API key not configured")
                response, tokens, time_ms = await self.openrouter.generate(
                    model_id=model_id,
                    prompt=prompt,
                    max_tokens=GENERATION_PARAMS["max_tokens"],
                    temperature=GENERATION_PARAMS["temperature"]
                )
            elif provider == "xai":
                if not self.xai:
                    raise ValueError("xAI API key not configured")
                response, tokens, time_ms = await self.xai.generate(
                    model_id=model_id,
                    prompt=prompt,
                    max_tokens=GENERATION_PARAMS["max_tokens"],
                    temperature=GENERATION_PARAMS["temperature"]
                )
            else:
                raise ValueError(f"Unknown provider: {provider}")
            
            return ModelResponse(
                model_key=model_key,
                model_name=model_name,
                response=response,
                generation_time_ms=time_ms,
                tokens_used=tokens
            )
            
        except Exception as e:
            print(f"      ❌ {model_name}: {str(e)[:50]}")
            return ModelResponse(
                model_key=model_key,
                model_name=model_name,
                response="",
                generation_time_ms=0,
                tokens_used=0,
                error=str(e)
            )
    

    def _parse_judgment_json(self, raw_text):
        """Robustly extract judgment scores from model output."""
        text = raw_text.strip()

        # Strip <think>/<thinking> blocks
        text = re.sub(r'<think(?:ing)?>[\s\S]*?</think(?:ing)?>', '', text, flags=re.IGNORECASE)

        # Extract from markdown code fences
        code_block_match = re.search(r'```(?:json)?\s*\n?(\{[\s\S]*?\})\s*\n?```', text)
        if code_block_match:
            text = code_block_match.group(1)

        # Find all { ... } blocks
        json_candidates = []
        brace_depth = 0
        start_idx = None
        for i, ch in enumerate(text):
            if ch == '{':
                if brace_depth == 0:
                    start_idx = i
                brace_depth += 1
            elif ch == '}':
                brace_depth -= 1
                if brace_depth == 0 and start_idx is not None:
                    json_candidates.append(text[start_idx:i+1])
                    start_idx = None

        score_keys = {'correctness', 'completeness', 'clarity', 'depth', 'usefulness'}

        for candidate in json_candidates:
            try:
                cleaned = re.sub(r',\s*}', '}', candidate)
                cleaned = re.sub(r',\s*]', ']', cleaned)
                parsed = json.loads(cleaned)
                if isinstance(parsed, dict):
                    found_keys = score_keys.intersection(set(parsed.keys()))
                    if len(found_keys) >= 3:
                        scores = {}
                        for key in score_keys:
                            val = parsed.get(key, 0)
                            try:
                                val = float(val)
                            except (ValueError, TypeError):
                                val = 0.0
                            scores[key] = max(0.0, min(10.0, val))
                        justification = parsed.get('brief_justification', '')
                        if not isinstance(justification, str):
                            justification = str(justification)
                        scores['brief_justification'] = justification
                        return scores
            except json.JSONDecodeError:
                continue

        # Regex fallback for inline scores
        scores = {}
        for key in score_keys:
            pattern = rf'{key}\W*[:=]\s*([\d]+(?:\.\d+)?)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                val = float(match.group(1))
                scores[key] = max(0.0, min(10.0, val))

        if len(scores) >= 3:
            for key in score_keys:
                if key not in scores:
                    scores[key] = 0.0
            scores['brief_justification'] = ''
            return scores

        raise ValueError(
            f"Could not extract scores. "
            f"Found {len(scores)} of 5 keys. "
            f"Text preview: {text[:200]}"
        )

    async def _judge_single(
        self, 
        judge_key: str, 
        respondent_key: str,
        question: str,
        response: str
    ) -> JudgmentScore:
        """Have one model judge another model's response"""
        judge_config = self._get_model_config(judge_key)
        judge_name = judge_config.get("display_name", judge_key)
        judge_model_id = judge_config.get("model_id", judge_key)
        judge_provider = judge_config.get("provider", "openrouter")
        
        respondent_name = self._get_model_display_name(respondent_key)
        
        # Don't let models judge themselves
        if judge_key == respondent_key:
            return JudgmentScore(
                judge_key=judge_key,
                judge_name=judge_name,
                respondent_key=respondent_key,
                respondent_name=respondent_name,
                correctness=0,
                completeness=0,
                clarity=0,
                depth=0,
                usefulness=0,
                weighted_score=0,
                brief_justification="Self-judgment excluded",
                error="self_judgment_excluded"
            )
        
        user_prompt = JUDGE_USER_PROMPT_TEMPLATE.format(
            question=question,
            response=response
        )
        
        try:
            if judge_provider == "openrouter":
                if not self.openrouter:
                    raise ValueError("OpenRouter API key not configured")
                judgment_text, _, _ = await self.openrouter.generate(
                    model_id=judge_model_id,
                    prompt=user_prompt,
                    system_prompt=JUDGE_SYSTEM_PROMPT,
                    max_tokens=JUDGMENT_PARAMS["max_tokens"],
                    temperature=JUDGMENT_PARAMS["temperature"]
                )
            elif judge_provider == "xai":
                if not self.xai:
                    raise ValueError("xAI API key not configured")
                judgment_text, _, _ = await self.xai.generate(
                    model_id=judge_model_id,
                    prompt=user_prompt,
                    system_prompt=JUDGE_SYSTEM_PROMPT,
                    max_tokens=JUDGMENT_PARAMS["max_tokens"],
                    temperature=JUDGMENT_PARAMS["temperature"]
                )
            else:
                raise ValueError(f"Unknown provider: {judge_provider}")
            
            # Parse judgment using robust parser
            try:
                scores = self._parse_judgment_json(judgment_text)
            except ValueError as parse_err:
                return JudgmentScore(
                    judge_key=judge_key,
                    judge_name=judge_name,
                    respondent_key=respondent_key,
                    respondent_name=respondent_name,
                    correctness=0,
                    completeness=0,
                    clarity=0,
                    depth=0,
                    usefulness=0,
                    weighted_score=0,
                    brief_justification="",
                    error=f"parse_failed: {str(parse_err)}"
                )
            
            # Calculate weighted score
            weights = SCORING["criteria"]
            weighted_score = (
                scores.get("correctness", 0) * weights["correctness"]["weight"] +
                scores.get("completeness", 0) * weights["completeness"]["weight"] +
                scores.get("clarity", 0) * weights["clarity"]["weight"] +
                scores.get("depth", 0) * weights["depth"]["weight"] +
                scores.get("usefulness", 0) * weights["usefulness"]["weight"]
            )
            
            return JudgmentScore(
                judge_key=judge_key,
                judge_name=judge_name,
                respondent_key=respondent_key,
                respondent_name=respondent_name,
                correctness=scores.get("correctness", 0),
                completeness=scores.get("completeness", 0),
                clarity=scores.get("clarity", 0),
                depth=scores.get("depth", 0),
                usefulness=scores.get("usefulness", 0),
                weighted_score=round(weighted_score, 2),
                brief_justification=scores.get("brief_justification", "")
            )
            
        except Exception as e:
            return JudgmentScore(
                judge_key=judge_key,
                judge_name=judge_name,
                respondent_key=respondent_key,
                respondent_name=respondent_name,
                correctness=0,
                completeness=0,
                clarity=0,
                depth=0,
                usefulness=0,
                weighted_score=0,
                brief_justification="",
                error=str(e)
            )
    

    def _collect_model_metadata(self, models):
        """Collect provider and model metadata for eval output."""
        metadata = {}
        for model_key in models:
            config = self._get_model_config(model_key)
            metadata[model_key] = {
                "display_name": config.get("display_name", model_key),
                "model_id": config.get("model_id", "unknown"),
                "provider": config.get("provider", "unknown"),
                "context_window": config.get("context_window", 0),
                "parameters": config.get("parameters", "unknown"),
                "quantization": "unknown - API provider controls quantization",
                "inference_settings": {
                    "generation_temperature": GENERATION_PARAMS["temperature"],
                    "generation_max_tokens": GENERATION_PARAMS["max_tokens"],
                    "judgment_temperature": JUDGMENT_PARAMS["temperature"],
                    "judgment_max_tokens": JUDGMENT_PARAMS["max_tokens"],
                }
            }
        return metadata

    async def run_evaluation(
        self, 
        question: str, 
        question_id: str = None,
        category: str = "meta_alignment"
    ) -> EvaluationResult:
        """Run a complete 10×10 evaluation with category-specific models"""
        
        # Set category context
        self._current_category = category
        
        evaluation_id = f"EVAL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        timestamp = datetime.now().isoformat()
        
        # Get category-specific models
        active_models = get_active_models_for_category(category)
        category_info = get_category_info(category)
        
        print(f"\n{'='*60}")
        print(f"🔮 MULTIVAC V5 EVALUATION")
        print(f"{'='*60}")
        print(f"ID: {evaluation_id}")
        print(f"Category: {category_info['display_name']}")
        print(f"Question: {question[:80]}...")
        print(f"Models: {len(active_models)} ({category}-optimized pool)")
        print(f"{'='*60}\n")
        
        # Show model pool
        print("📋 Model Pool:")
        for i, model_key in enumerate(active_models, 1):
            config = self._get_model_config(model_key)
            print(f"   {i:2}. {config.get('display_name', model_key)} ({config.get('provider', '?')})")
        print()
        
        # PHASE 1: Generate responses from all models
        print("📝 PHASE 1: Generating responses...")
        generation_tasks = [
            self._generate_single(model_key, question)
            for model_key in active_models
        ]
        responses = await asyncio.gather(*generation_tasks)
        
        successful_responses = [r for r in responses if not r.error]
        failed_responses = [r for r in responses if r.error]
        
        print(f"   ✓ {len(successful_responses)}/{len(responses)} responses generated")
        if failed_responses:
            print(f"   ⚠️  {len(failed_responses)} failures:")
            for r in failed_responses:
                print(f"      - {r.model_name}: {r.error[:40]}...")
        print()
        
        # PHASE 2: 10×10 Judgment Matrix
        print("⚖️  PHASE 2: Running 10×10 judgment matrix...")
        
        judgment_tasks = []
        for judge_key in active_models:
            for resp in successful_responses:
                judgment_tasks.append(
                    self._judge_single(
                        judge_key=judge_key,
                        respondent_key=resp.model_key,
                        question=question,
                        response=resp.response
                    )
                )
        
        # Run judgments in batches to avoid rate limits
        batch_size = 20
        all_judgments = []
        total_judgments = len(judgment_tasks)
        
        for i in range(0, total_judgments, batch_size):
            batch = judgment_tasks[i:i+batch_size]
            batch_results = await asyncio.gather(*batch)
            all_judgments.extend(batch_results)
            
            completed = min(i + batch_size, total_judgments)
            print(f"   ✓ {completed}/{total_judgments} judgments completed")
            
            # Small delay between batches to avoid rate limits
            if i + batch_size < total_judgments:
                await asyncio.sleep(1)
        
        # Filter out self-judgments and errors for stats
        valid_judgments = [j for j in all_judgments if not j.error]
        error_judgments = [j for j in all_judgments if j.error and j.error != "self_judgment_excluded"]
        
        print(f"   ✓ {len(valid_judgments)} valid judgments")
        if error_judgments:
            print(f"   ⚠️  {len(error_judgments)} judgment errors")
        print()
        
        # PHASE 3: Compute rankings and meta-analysis
        print("📊 PHASE 3: Computing rankings and meta-analysis...")
        rankings = self._compute_rankings(valid_judgments, active_models)
        meta_analysis = self._compute_meta_analysis(all_judgments, active_models)
        model_metadata = self._collect_model_metadata(active_models)
        
        result = EvaluationResult(
            evaluation_id=evaluation_id,
            timestamp=timestamp,
            question_id=question_id or evaluation_id,
            question_text=question,
            category=category,
            models_used=active_models,
            responses=[asdict(r) for r in responses],
            judgments=[asdict(j) for j in all_judgments],
            rankings=rankings,
            meta_analysis=meta_analysis
        )
        
        # Save results
        self._save_results(result)
        # Save model metadata alongside results
        metadata_path = self.outputs_path / result.evaluation_id / "model_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(model_metadata, f, indent=2)
        self._update_tracker(result)
        
        # Print summary
        self._print_summary(result)
        
        print(f"\n✅ Evaluation complete: {evaluation_id}")
        
        return result
    
    def _compute_rankings(
        self, 
        judgments, 
        models
    ):
        """
        Compute final rankings from judgment matrix.
        
        80% RULE: A model must have valid scores from at least 80% of
        possible judges to appear in aggregate rankings.
        """
        
        max_possible_judges = len(models) - 1
        min_required_judges = max(1, int(max_possible_judges * 0.80))
        
        # Aggregate scores per model
        model_scores = defaultdict(list)
        model_judges = defaultdict(set)
        
        for j in judgments:
            if j.weighted_score > 0:
                model_scores[j.respondent_key].append(j.weighted_score)
                model_judges[j.respondent_key].add(j.judge_key)
        
        # Calculate average scores
        rankings = {}
        for model_key in models:
            scores = model_scores.get(model_key, [])
            unique_judges = len(model_judges.get(model_key, set()))
            meets_threshold = unique_judges >= min_required_judges
            
            if scores and meets_threshold:
                rankings[model_key] = {
                    "display_name": self._get_model_display_name(model_key),
                    "average_score": round(sum(scores) / len(scores), 2),
                    "score_count": len(scores),
                    "unique_judges": unique_judges,
                    "min_required_judges": min_required_judges,
                    "min_score": round(min(scores), 2),
                    "max_score": round(max(scores), 2),
                    "std_dev": round(self._std_dev(scores), 2),
                    "meets_threshold": True
                }
            elif scores and not meets_threshold:
                rankings[model_key] = {
                    "display_name": self._get_model_display_name(model_key),
                    "average_score": round(sum(scores) / len(scores), 2),
                    "score_count": len(scores),
                    "unique_judges": unique_judges,
                    "min_required_judges": min_required_judges,
                    "min_score": round(min(scores), 2),
                    "max_score": round(max(scores), 2),
                    "std_dev": round(self._std_dev(scores), 2),
                    "meets_threshold": False,
                    "insufficient_data": True,
                    "note": f"Only {unique_judges}/{min_required_judges} required judges"
                }
            else:
                rankings[model_key] = {
                    "display_name": self._get_model_display_name(model_key),
                    "average_score": 0,
                    "score_count": 0,
                    "unique_judges": 0,
                    "min_required_judges": min_required_judges,
                    "meets_threshold": False,
                    "error": "no_valid_scores"
                }
        
        # Rank ONLY models meeting the 80% threshold
        rankable = sorted(
            [(k, v) for k, v in rankings.items() if v.get("meets_threshold", False)],
            key=lambda x: x[1].get("average_score", 0),
            reverse=True
        )
        
        for rank, (model_key, data) in enumerate(rankable, 1):
            rankings[model_key]["rank"] = rank
        
        for model_key, data in rankings.items():
            if "rank" not in data:
                data["rank"] = None
        
        return rankings
    def _compute_meta_analysis(
        self, 
        judgments: list[JudgmentScore], 
        models: list[str]
    ) -> dict:
        """Compute meta-analysis: judge strictness, agreement rates, etc."""
        
        # Judge strictness (average score given)
        judge_scores_given = defaultdict(list)
        for j in judgments:
            if j.weighted_score > 0:
                judge_scores_given[j.judge_key].append(j.weighted_score)
        
        judge_strictness = {}
        for model_key in models:
            scores = judge_scores_given.get(model_key, [])
            if scores:
                judge_strictness[model_key] = {
                    "display_name": self._get_model_display_name(model_key),
                    "average_score_given": round(sum(scores) / len(scores), 2),
                    "judgments_made": len(scores)
                }
        
        # Sort by strictness (lower = stricter)
        sorted_judges = sorted(
            judge_strictness.items(),
            key=lambda x: x[1].get("average_score_given", 10)
        )
        
        for rank, (model_key, data) in enumerate(sorted_judges, 1):
            judge_strictness[model_key]["strictness_rank"] = rank
        
        return {
            "judge_strictness": judge_strictness,
            "strictest_judge": sorted_judges[0][0] if sorted_judges else None,
            "most_lenient_judge": sorted_judges[-1][0] if sorted_judges else None,
            "total_judgments": len(judgments),
            "valid_judgments": len([j for j in judgments if j.weighted_score > 0]),
            "self_judgments_excluded": len([j for j in judgments if j.error == "self_judgment_excluded"]),
            "category": self._current_category,
            "model_pool_size": len(models)
        }
    
    def _std_dev(self, values: list[float]) -> float:
        """Calculate standard deviation"""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5
    
    def _print_summary(self, result: EvaluationResult):
        """Print a quick summary of results"""
        
        print(f"\n{'─'*60}")
        print("📊 RESULTS SUMMARY")
        print(f"{'─'*60}")
        
        # Sort by rank
        sorted_rankings = sorted(
            result.rankings.items(),
            key=lambda x: x[1].get("rank") or 999
        )
        
        print(f"\n{'Rank':<6} {'Model':<30} {'Score':<8} {'±':<6}")
        print(f"{'─'*6} {'─'*30} {'─'*8} {'─'*6}")
        
        for model_key, data in sorted_rankings:
            if "error" not in data:
                rank = data.get('rank', '?')
                name = data.get('display_name', model_key)[:28]
                score = data.get('average_score', 0)
                std = data.get('std_dev', 0)
                
                # Emoji for top 3
                emoji = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "  ")
                print(f"{emoji}{rank:<4} {name:<30} {score:<8.2f} {std:<6.2f}")
    
    def _save_results(self, result: EvaluationResult):
        """Save evaluation results to JSON and Markdown"""
        
        # Create output directory for this evaluation
        eval_dir = self.outputs_path / result.evaluation_id
        eval_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        json_path = eval_dir / "results.json"
        with open(json_path, "w") as f:
            json.dump(asdict(result), f, indent=2)
        
        # Save Markdown report
        md_path = eval_dir / "report.md"
        with open(md_path, "w") as f:
            f.write(self._generate_markdown_report(result))
        
        print(f"   📁 Results saved to: {eval_dir}")
    
    def _generate_markdown_report(self, result: EvaluationResult) -> str:
        """Generate a human-readable Markdown report"""
        
        category_info = get_category_info(result.category)
        
        lines = [
            f"# Multivac Evaluation Report",
            f"",
            f"**Evaluation ID:** {result.evaluation_id}",
            f"**Timestamp:** {result.timestamp}",
            f"**Category:** {category_info['display_name']}",
            f"**Model Pool:** {len(result.models_used)} {result.category}-optimized models",
            f"",
            f"## Question",
            f"",
            f"{result.question_text}",
            f"",
            f"---",
            f"",
            f"## Rankings",
            f"",
            f"| Rank | Model | Score | Min | Max | Std Dev |",
            f"|------|-------|-------|-----|-----|---------|",
        ]
        
        # Sort by rank
        sorted_rankings = sorted(
            result.rankings.items(),
            key=lambda x: x[1].get("rank") or 999
        )
        
        for model_key, data in sorted_rankings:
            if "error" not in data:
                lines.append(
                    f"| {data['rank']} | {data['display_name']} | "
                    f"{data['average_score']:.2f} | {data['min_score']:.2f} | "
                    f"{data['max_score']:.2f} | {data['std_dev']:.2f} |"
                )
        
        lines.extend([
            f"",
            f"---",
            f"",
            f"## Meta Analysis",
            f"",
            f"### Judge Strictness",
            f"",
            f"| Rank | Judge | Avg Score Given |",
            f"|------|-------|-----------------|",
        ])
        
        sorted_judges = sorted(
            result.meta_analysis["judge_strictness"].items(),
            key=lambda x: x[1].get("strictness_rank", 999)
        )
        
        for model_key, data in sorted_judges:
            lines.append(
                f"| {data['strictness_rank']} | {data['display_name']} | "
                f"{data['average_score_given']:.2f} |"
            )
        
        lines.extend([
            f"",
            f"**Strictest Judge:** {result.meta_analysis.get('strictest_judge', 'N/A')}",
            f"**Most Lenient Judge:** {result.meta_analysis.get('most_lenient_judge', 'N/A')}",
            f"**Total Judgments:** {result.meta_analysis.get('total_judgments', 0)}",
            f"**Valid Judgments:** {result.meta_analysis.get('valid_judgments', 0)}",
            f"",
            f"---",
            f"",
            f"## Model Pool",
            f"",
            f"Models selected for **{category_info['display_name']}** evaluation:",
            f"",
        ])
        
        for i, model_key in enumerate(result.models_used, 1):
            config = get_model_config(result.category, model_key)
            lines.append(f"{i}. **{config.get('display_name', model_key)}** ({config.get('provider', '?')})")
        
        lines.extend([
            f"",
            f"---",
            f"",
            f"## Model Responses",
            f"",
        ])
        
        # Add individual responses
        for resp in result.responses:
            if not resp.get("error"):
                lines.extend([
                    f"### {resp['model_name']}",
                    f"",
                    f"**Generation Time:** {resp['generation_time_ms']}ms",
                    f"**Tokens:** {resp['tokens_used']}",
                    f"",
                    f"```",
                    (resp['response'] or "")[:2000] + ("..." if len(resp.get('response') or "") > 2000 else ""),
                    f"```",
                    f"",
                ])
        
        lines.extend([
            f"---",
            f"",
            f"*Generated by The Multivac V5*",
            f"*https://themultivac.com*"
        ])
        
        return "\n".join(lines)
    
    def _update_tracker(self, result: EvaluationResult):
        """Update the persistent evaluation tracker"""
        
        # Load existing tracker or create new
        if self.tracker_path.exists():
            with open(self.tracker_path, "r") as f:
                tracker = json.load(f)
        else:
            tracker = {
                "version": "5.1",
                "created": datetime.now().isoformat(),
                "evaluations": [],
                "model_stats": {},
                "category_stats": {}
            }
        
        # Add this evaluation
        eval_summary = {
            "evaluation_id": result.evaluation_id,
            "timestamp": result.timestamp,
            "question_id": result.question_id,
            "question_preview": result.question_text[:100],
            "category": result.category,
            "models_used": result.models_used,
            "rankings_summary": {
                k: {"rank": v["rank"], "score": v["average_score"]}
                for k, v in result.rankings.items()
                if "rank" in v
            }
        }
        
        tracker["evaluations"].append(eval_summary)
        tracker["last_updated"] = datetime.now().isoformat()
        
        # Update cumulative model stats
        for model_key, data in result.rankings.items():
            if "average_score" in data and data["average_score"] > 0:
                if model_key not in tracker["model_stats"]:
                    tracker["model_stats"][model_key] = {
                        "display_name": data["display_name"],
                        "total_evaluations": 0,
                        "total_score": 0,
                        "rank_history": [],
                        "categories": []
                    }
                
                tracker["model_stats"][model_key]["total_evaluations"] += 1
                tracker["model_stats"][model_key]["total_score"] += data["average_score"]
                tracker["model_stats"][model_key]["rank_history"].append(data["rank"])
                tracker["model_stats"][model_key]["average_score"] = round(
                    tracker["model_stats"][model_key]["total_score"] / 
                    tracker["model_stats"][model_key]["total_evaluations"],
                    2
                )
                if result.category not in tracker["model_stats"][model_key]["categories"]:
                    tracker["model_stats"][model_key]["categories"].append(result.category)
        
        # Update category stats
        category = result.category
        if category not in tracker["category_stats"]:
            tracker["category_stats"][category] = {"count": 0, "evaluations": []}
        tracker["category_stats"][category]["count"] += 1
        tracker["category_stats"][category]["evaluations"].append(result.evaluation_id)
        
        # Save tracker
        with open(self.tracker_path, "w") as f:
            json.dump(tracker, f, indent=2)
        
        print(f"   📊 Tracker updated: {len(tracker['evaluations'])} total evaluations")


# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="The Multivac V5 - AI Model Evaluation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python multivac.py --question "Explain quicksort" --category code
  python multivac.py --question-id CODE-001
  python multivac.py --list-models --category reasoning
  python multivac.py --interactive
        """
    )
    
    parser.add_argument(
        "--question", "-q",
        type=str,
        help="Question to evaluate"
    )
    
    parser.add_argument(
        "--question-id", "-id",
        type=str,
        help="Use a pre-defined question by ID (e.g., CODE-001)"
    )
    
    parser.add_argument(
        "--category", "-c",
        type=str,
        default="meta_alignment",
        choices=list_all_categories(),
        help="Question category (determines model pool)"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--list-questions",
        action="store_true",
        help="List all available pre-defined questions"
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List models for a category (use with --category)"
    )
    
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List all categories and their model pools"
    )
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_categories:
        print(get_category_summary())
        return
    
    if args.list_models:
        category = args.category
        info = get_category_info(category)
        models = get_active_models_for_category(category)
        model_dict = get_models_for_category(category)
        
        print(f"\n📂 {info['display_name'].upper()}")
        print(f"   {info['description']}\n")
        print(f"{'#':<4} {'Model':<30} {'Provider':<12} {'Context':<10}")
        print(f"{'─'*4} {'─'*30} {'─'*12} {'─'*10}")
        
        for model_key in models:
            config = model_dict.get(model_key, {})
            rank = config.get("category_rank", "?")
            name = config.get("display_name", model_key)[:28]
            provider = config.get("provider", "?")
            context = config.get("context_window", 0)
            context_str = f"{context//1000}K" if context else "?"
            print(f"{rank:<4} {name:<30} {provider:<12} {context_str:<10}")
        return
    
    if args.list_questions:
        from questions import get_question_count, QUESTIONS
        print("\n📋 Available Questions:\n")
        for category, count in get_question_count().items():
            print(f"\n{category.upper()} ({count} questions):")
            for q in QUESTIONS[category]:
                print(f"  • {q['id']}: {q['title']}")
        return
    
    engine = MultivacEngine()
    
    if args.question_id:
        q = get_question_by_id(args.question_id)
        if not q:
            print(f"❌ Question not found: {args.question_id}")
            return
        question = q["question"]
        category = q["category"]
        question_id = q["id"]
    elif args.question:
        question = args.question
        category = args.category
        question_id = None
    elif args.interactive:
        print("\n🔮 MULTIVAC V5 - Interactive Mode\n")
        print("Available categories:", ", ".join(list_all_categories()))
        question = input("\nEnter your question:\n> ")
        category = input(f"\nCategory [{args.category}]:\n> ").strip() or args.category
        question_id = None
    else:
        parser.print_help()
        return
    
    # Run evaluation
    asyncio.run(engine.run_evaluation(
        question=question,
        question_id=question_id,
        category=category
    ))


if __name__ == "__main__":
    main()
