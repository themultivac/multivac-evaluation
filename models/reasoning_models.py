"""
Multivac V5.1 - Reasoning & Logic Model Pool
Updated: March 15, 2026
Model Version: V2 (March 2026 frontier models)

Previous version backed up to: models_backup_v1/
"""

MODELS = {
    "gemini_31_pro": {
        "model_id": "google/gemini-3.1-pro",
        "display_name": "Gemini 3.1 Pro",
        "provider": "openrouter",
        "category_rank": 1,
        "context_window": 1050000,
        "strengths": ["13/16 benchmark leader", "GPQA Diamond"],
        "active": True
    },
    "deepseek_v4": {
        "model_id": "deepseek/deepseek-v4",
        "display_name": "DeepSeek V4",
        "provider": "openrouter",
        "category_rank": 2,
        "context_window": 164000,
        "strengths": ["1T/32B MoE", "mathematical reasoning"],
        "active": True
    },
    "claude_opus_46": {
        "model_id": "anthropic/claude-opus-4.6",
        "display_name": "Claude Opus 4.6",
        "provider": "openrouter",
        "category_rank": 3,
        "context_window": 200000,
        "strengths": ["frontier reasoning", "structured reasoning"],
        "active": True
    },
    "gpt_5_4": {
        "model_id": "openai/gpt-5.4",
        "display_name": "GPT-5.4",
        "provider": "openrouter",
        "category_rank": 4,
        "context_window": 1000000,
        "strengths": ["unified routing architecture", "expert-level reasoning"],
        "active": True
    },
    "grok_420": {
        "model_id": "x-ai/grok-4.20",
        "display_name": "Grok 4.20",
        "provider": "openrouter",
        "category_rank": 5,
        "context_window": 2000000,
        "strengths": ["four-agent parallel processing", "extended thinking"],
        "active": True
    },
    "claude_sonnet_46": {
        "model_id": "anthropic/claude-sonnet-4.6",
        "display_name": "Claude Sonnet 4.6",
        "provider": "openrouter",
        "category_rank": 6,
        "context_window": 1000000,
        "strengths": ["real-world agents", "extended autonomous operation"],
        "active": True
    },
    "mimo_v2_flash": {
        "model_id": "xiaomi/mimo-v2-flash",
        "display_name": "MiMo-V2-Flash",
        "provider": "openrouter",
        "category_rank": 7,
        "context_window": 262000,
        "strengths": ["reasoning", "hybrid-thinking", "IMO/IOI gold-medal level"],
        "active": True
    },
    "gpt_oss_120b": {
        "model_id": "openai/gpt-oss-120b",
        "display_name": "GPT-OSS-120B",
        "provider": "openrouter",
        "category_rank": 8,
        "context_window": 131000,
        "strengths": ["open-weight reasoning", "configurable depth"],
        "active": True
    },
    "gemini_25_flash": {
        "model_id": "google/gemini-2.5-flash",
        "display_name": "Gemini 2.5 Flash",
        "provider": "openrouter",
        "category_rank": 9,
        "context_window": 1050000,
        "strengths": ["advanced reasoning", "built-in thinking"],
        "active": True
    },
    "minimax_m25": {
        "model_id": "minimax/minimax-m2.5",
        "display_name": "MiniMax M2.5",
        "provider": "openrouter",
        "category_rank": 10,
        "context_window": 197000,
        "strengths": ["competitive reasoning at low cost"],
        "active": True
    },
}

# Category metadata
CATEGORY_INFO = {
    "name": "reasoning",
    "display_name": "Reasoning & Logic",
    "description": "Logical reasoning, mathematical proof, paradoxes, and decision theory",
    "model_count": 10,
    "version": "v2_march2026"
}

def get_active_models():
    """Return list of active model keys in rank order"""
    return [k for k, v in sorted(MODELS.items(), key=lambda x: x[1].get("category_rank", 99)) if v.get("active", True)]
