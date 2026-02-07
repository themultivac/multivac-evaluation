"""
Multivac V5 - Meta Alignment Category Models
Top 10 frontier models for evaluating alignment, safety, and edge cases
Selected for general capability, nuanced reasoning, and robustness
"""

MODELS = {
    # Anthropic flagship - Best for alignment evaluation
    "claude_opus": {
        "model_id": "anthropic/claude-opus-4.5",
        "display_name": "Claude Opus 4.5",
        "provider": "openrouter",
        "category_rank": 1,
        "context_window": 200000,
        "strengths": ["alignment", "robustness to prompt injection", "nuanced ethics"]
    },
    
    # Google flagship - Strong multimodal reasoning
    "gemini_3_pro": {
        "model_id": "google/gemini-3-pro-preview",
        "display_name": "Gemini 3 Pro Preview",
        "provider": "openrouter",
        "category_rank": 2,
        "context_window": 1050000,
        "strengths": ["depth", "interpretability", "factual QA"]
    },
    
    # Anthropic workhorse - Balanced capability
    "claude_sonnet": {
        "model_id": "anthropic/claude-sonnet-4.5",
        "display_name": "Claude Sonnet 4.5",
        "provider": "openrouter",
        "category_rank": 3,
        "context_window": 1000000,
        "strengths": ["fact-based tracking", "tool orchestration", "context awareness"]
    },
    
    # OpenAI Codex - Strong reasoning
    "gpt_codex": {
        "model_id": "openai/gpt-5.2-codex",
        "display_name": "GPT-5.2-Codex",
        "provider": "openrouter",
        "category_rank": 4,
        "context_window": 400000,
        "strengths": ["steerable", "instruction following", "reasoning effort control"]
    },
    
    # OpenAI open-weight - Transparent reasoning
    "gpt_oss_120b": {
        "model_id": "openai/gpt-oss-120b",
        "display_name": "GPT-OSS-120B",
        "provider": "openrouter",
        "category_rank": 5,
        "context_window": 131000,
        "strengths": ["configurable reasoning", "full chain-of-thought access", "tool use"]
    },
    
    # Google thinking model
    "gemini_3_flash": {
        "model_id": "google/gemini-3-flash-preview",
        "display_name": "Gemini 3 Flash Preview",
        "provider": "openrouter",
        "category_rank": 6,
        "context_window": 1050000,
        "strengths": ["configurable thinking levels", "reliability", "tool use"]
    },
    
    # DeepSeek - Strong open-source reasoning
    "deepseek_v3": {
        "model_id": "deepseek/deepseek-v3.2",
        "display_name": "DeepSeek V3.2",
        "provider": "openrouter",
        "category_rank": 7,
        "context_window": 164000,
        "strengths": ["agentic tool-use", "reasoning in tool settings", "compliance"]
    },
    
    # Xiaomi - Open-source frontier
    "mimo_v2_flash": {
        "model_id": "xiaomi/mimo-v2-flash",
        "display_name": "MiMo-V2-Flash",
        "provider": "openrouter",
        "category_rank": 8,
        "context_window": 262000,
        "strengths": ["hybrid-thinking toggle", "open-source", "agent scenarios"]
    },
    
    # xAI flagship - Real-time grounding
    "grok_4_1_fast": {
        "model_id": "x-ai/grok-4.1-fast",
        "display_name": "Grok 4.1 Fast",
        "provider": "openrouter",
        "category_rank": 9,
        "context_window": 2000000,
        "strengths": ["real-world grounding", "deep research", "configurable reasoning"]
    },
    
    # Grok direct API for diversity
    "grok_direct": {
        "model_id": "grok-3",
        "display_name": "Grok 3 (Direct)",
        "provider": "xai",
        "category_rank": 10,
        "context_window": 131072,
        "strengths": ["real-time knowledge", "unfiltered perspective"]
    }
}

def get_active_models() -> list[str]:
    """Return list of active model keys for this category"""
    sorted_models = sorted(MODELS.items(), key=lambda x: x[1]["category_rank"])
    return [k for k, v in sorted_models[:10]]

def get_model_display_name(model_key: str) -> str:
    """Get display name for a model"""
    return MODELS.get(model_key, {}).get("display_name", model_key)

def get_model_config(model_key: str) -> dict:
    """Get full config for a model"""
    return MODELS.get(model_key, {})


# Category metadata
CATEGORY_INFO = {
    "name": "meta_alignment",
    "display_name": "Meta & Alignment",
    "description": "Frontier models for evaluating AI alignment, safety, edge cases, and meta-level reasoning about AI systems",
    "evaluation_focus": ["safety awareness", "ethical reasoning", "edge case handling", "robustness", "honesty"]
}
