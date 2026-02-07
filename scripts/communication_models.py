"""
Multivac V5 - Communication Category Models
Top 10 models optimized for marketing, translation, writing, and interpersonal tasks
Based on OpenRouter Marketing/Translation/Roleplay rankings
"""

MODELS = {
    # #1 Marketing - Google lightweight
    "gemini_2_5_flash_lite": {
        "model_id": "google/gemini-2.5-flash-lite",
        "display_name": "Gemini 2.5 Flash-Lite",
        "provider": "openrouter",
        "category_rank": 1,
        "context_window": 1050000,
        "strengths": ["marketing", "fast responses", "cost-efficient"]
    },
    
    # #2 - ByteDance Seed (replacing Gemini 2.0 Flash which has API issues)
    "seed_1_6_flash": {
        "model_id": "bytedance-seed/seed-1.6-flash",
        "display_name": "Seed 1.6 Flash",
        "provider": "openrouter",
        "category_rank": 2,
        "context_window": 262000,
        "strengths": ["multimodal", "deep thinking", "fast"]
    },
    
    # #2 Marketing - Google workhorse
    "gemini_2_5_flash": {
        "model_id": "google/gemini-2.5-flash",
        "display_name": "Gemini 2.5 Flash",
        "provider": "openrouter",
        "category_rank": 3,
        "context_window": 1050000,
        "strengths": ["marketing copy", "nuanced context handling"]
    },
    
    # #3 Translation - OpenAI open-weight
    "gpt_oss_120b": {
        "model_id": "openai/gpt-oss-120b",
        "display_name": "GPT-OSS-120B",
        "provider": "openrouter",
        "category_rank": 4,
        "context_window": 131000,
        "strengths": ["translation", "general-purpose", "chain-of-thought"]
    },
    
    # #4 Marketing, #4 Roleplay - xAI
    "grok_4_1_fast": {
        "model_id": "x-ai/grok-4.1-fast",
        "display_name": "Grok 4.1 Fast",
        "provider": "openrouter",
        "category_rank": 5,
        "context_window": 2000000,
        "strengths": ["marketing", "customer support", "conversational"]
    },
    
    # #1 Roleplay - DeepSeek for creative
    "deepseek_v3": {
        "model_id": "deepseek/deepseek-v3.2",
        "display_name": "DeepSeek V3.2",
        "provider": "openrouter",
        "category_rank": 6,
        "context_window": 164000,
        "strengths": ["roleplay", "creative writing", "character consistency"]
    },
    
    # #8 Translation - Z.AI
    "glm_4_7": {
        "model_id": "z-ai/glm-4.7",
        "display_name": "GLM 4.7",
        "provider": "openrouter",
        "category_rank": 7,
        "context_window": 203000,
        "strengths": ["translation", "natural conversation", "multilingual"]
    },
    
    # Anthropic - Strong writing quality
    "claude_sonnet": {
        "model_id": "anthropic/claude-sonnet-4.5",
        "display_name": "Claude Sonnet 4.5",
        "provider": "openrouter",
        "category_rank": 8,
        "context_window": 1000000,
        "strengths": ["writing quality", "tone consistency", "brand voice"]
    },
    
    # Anthropic flagship - Nuanced communication
    "claude_opus": {
        "model_id": "anthropic/claude-opus-4.5",
        "display_name": "Claude Opus 4.5",
        "provider": "openrouter",
        "category_rank": 9,
        "context_window": 200000,
        "strengths": ["nuanced writing", "editorial quality", "persuasion"]
    },
    
    # Mistral Creative - Experimental creative model
    "mistral_small_creative": {
        "model_id": "mistralai/mistral-small-creative",
        "display_name": "Mistral Small Creative",
        "provider": "openrouter",
        "category_rank": 10,
        "context_window": 33000,
        "strengths": ["creative writing", "narrative generation", "character dialogue"]
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
    "name": "communication",
    "display_name": "Communication & Writing",
    "description": "Models optimized for marketing copy, translation, creative writing, and interpersonal communication",
    "evaluation_focus": ["clarity", "tone appropriateness", "persuasiveness", "cultural sensitivity", "engagement"]
}
