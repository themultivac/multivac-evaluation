"""
Multivac V5.1 - Communication & Writing Model Pool
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
        "strengths": ["nuanced writing", "editorial quality", "persuasion"],
        "active": True
    },
    "gpt_5_4": {
        "model_id": "openai/gpt-5.4",
        "display_name": "GPT-5.4",
        "provider": "openrouter",
        "category_rank": 2,
        "context_window": 1000000,
        "strengths": ["professional writing", "audience adaptation"],
        "active": True
    },
    "claude_sonnet_46": {
        "model_id": "anthropic/claude-sonnet-4.6",
        "display_name": "Claude Sonnet 4.6",
        "provider": "openrouter",
        "category_rank": 3,
        "context_window": 1000000,
        "strengths": ["writing quality", "tone consistency"],
        "active": True
    },
    "gemini_31_pro": {
        "model_id": "google/gemini-3.1-pro",
        "display_name": "Gemini 3.1 Pro",
        "provider": "openrouter",
        "category_rank": 4,
        "context_window": 1050000,
        "strengths": ["multilingual", "content creation"],
        "active": True
    },
    "grok_420": {
        "model_id": "x-ai/grok-4.20",
        "display_name": "Grok 4.20",
        "provider": "openrouter",
        "category_rank": 5,
        "context_window": 2000000,
        "strengths": ["marketing", "customer support"],
        "active": True
    },
    "deepseek_v4": {
        "model_id": "deepseek/deepseek-v4",
        "display_name": "DeepSeek V4",
        "provider": "openrouter",
        "category_rank": 6,
        "context_window": 164000,
        "strengths": ["creative writing", "character consistency"],
        "active": True
    },
    "gpt_oss_120b": {
        "model_id": "openai/gpt-oss-120b",
        "display_name": "GPT-OSS-120B",
        "provider": "openrouter",
        "category_rank": 7,
        "context_window": 131000,
        "strengths": ["translation", "general-purpose communication"],
        "active": True
    },
    "mimo_v2_flash": {
        "model_id": "xiaomi/mimo-v2-flash",
        "display_name": "MiMo-V2-Flash",
        "provider": "openrouter",
        "category_rank": 8,
        "context_window": 262000,
        "strengths": ["multilingual", "efficient communication"],
        "active": True
    },
    "mistral_small_creative": {
        "model_id": "mistralai/mistral-small-creative",
        "display_name": "Mistral Small Creative",
        "provider": "openrouter",
        "category_rank": 9,
        "context_window": 33000,
        "strengths": ["creative writing", "narrative generation"],
        "active": True
    },
    "seed_16_flash": {
        "model_id": "bytedance-seed/seed-1.6-flash",
        "display_name": "Seed 1.6 Flash",
        "provider": "openrouter",
        "category_rank": 10,
        "context_window": 262000,
        "strengths": ["multimodal", "fast communication"],
        "active": True
    },
}

# Category metadata
CATEGORY_INFO = {
    "name": "communication",
    "display_name": "Communication & Writing",
    "description": "Technical writing, persuasion, cross-cultural communication, and UX copy",
    "model_count": 10,
    "version": "v2_march2026"
}

def get_active_models():
    """Return list of active model keys in rank order"""
    return [k for k, v in sorted(MODELS.items(), key=lambda x: x[1].get("category_rank", 99)) if v.get("active", True)]
