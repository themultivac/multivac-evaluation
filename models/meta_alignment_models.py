"""
Multivac V5.1 - Meta & Alignment Model Pool
Updated: March 15, 2026
Model Version: V2 (March 2026 frontier models)

Previous version backed up to: models_backup_v1/
"""

MODELS = {
    "claude_opus_46": {
        "model_id": "anthropic/claude-opus-4.6",
        "display_name": "Claude Opus 4.6",
        "provider": "openrouter",
        "category_rank": 1,
        "context_window": 200000,
        "strengths": ["alignment", "robustness", "nuanced ethics"],
        "active": True
    },
    "gpt_5_4": {
        "model_id": "openai/gpt-5.4",
        "display_name": "GPT-5.4",
        "provider": "openrouter",
        "category_rank": 2,
        "context_window": 1000000,
        "strengths": ["instruction following", "safety", "steerable"],
        "active": True
    },
    "gemini_31_pro": {
        "model_id": "google/gemini-3.1-pro-preview",
        "display_name": "Gemini 3.1 Pro",
        "provider": "openrouter",
        "category_rank": 3,
        "context_window": 1050000,
        "strengths": ["depth", "interpretability", "factual QA"],
        "active": True
    },
    "claude_sonnet_46": {
        "model_id": "anthropic/claude-sonnet-4.6",
        "display_name": "Claude Sonnet 4.6",
        "provider": "openrouter",
        "category_rank": 4,
        "context_window": 1000000,
        "strengths": ["fact-based tracking", "tool orchestration"],
        "active": True
    },
    "deepseek_v4": {
        "model_id": "deepseek/deepseek-chat-v3-0324",
        "display_name": "DeepSeek V3",
        "provider": "openrouter",
        "category_rank": 5,
        "context_window": 164000,
        "strengths": ["agentic tool-use", "compliance"],
        "active": True
    },
    "grok_420": {
        "model_id": "x-ai/grok-4.20",
        "display_name": "Grok 4.20",
        "provider": "openrouter",
        "category_rank": 6,
        "context_window": 2000000,
        "strengths": ["real-world grounding", "configurable reasoning"],
        "active": True
    },
    "gpt_oss_120b": {
        "model_id": "openai/gpt-oss-120b",
        "display_name": "GPT-OSS-120B",
        "provider": "openrouter",
        "category_rank": 7,
        "context_window": 131000,
        "strengths": ["open-weight transparency", "full chain-of-thought"],
        "active": True
    },
    "mimo_v2_flash": {
        "model_id": "xiaomi/mimo-v2-flash",
        "display_name": "MiMo-V2-Flash",
        "provider": "openrouter",
        "category_rank": 8,
        "context_window": 262000,
        "strengths": ["hybrid-thinking toggle", "open-source"],
        "active": True
    },
    "minimax_m25": {
        "model_id": "minimax/minimax-m2.5",
        "display_name": "MiniMax M2.5",
        "provider": "openrouter",
        "category_rank": 9,
        "context_window": 197000,
        "strengths": ["competitive alignment at low cost"],
        "active": True
    },
    "gemini_3_flash": {
        "model_id": "google/gemini-3-flash-preview",
        "display_name": "Gemini 3 Flash Preview",
        "provider": "openrouter",
        "category_rank": 10,
        "context_window": 1050000,
        "strengths": ["configurable thinking", "reliability"],
        "active": True
    },
}

# Category metadata
CATEGORY_INFO = {
    "name": "meta_alignment",
    "display_name": "Meta & Alignment",
    "description": "AI safety, sycophancy, honesty, dual-use knowledge, and self-awareness",
    "model_count": 10,
    "version": "v2_march2026"
}

def get_active_models():
    """Return list of active model keys in rank order"""
    return [k for k, v in sorted(MODELS.items(), key=lambda x: x[1].get("category_rank", 99)) if v.get("active", True)]
