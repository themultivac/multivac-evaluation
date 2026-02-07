"""
Multivac V5 - Reasoning Category Models
Top 10 models optimized for reasoning, logic, and scientific thinking
Based on OpenRouter Science/Trivia/Academia rankings
"""

MODELS = {
    # #1 Science, #1 Trivia, #1 Academia - Xiaomi's MoE powerhouse
    "mimo_v2_flash": {
        "model_id": "xiaomi/mimo-v2-flash",
        "display_name": "MiMo-V2-Flash",
        "provider": "openrouter",
        "category_rank": 1,
        "context_window": 262000,
        "strengths": ["reasoning", "hybrid-thinking", "IMO/IOI gold-medal level"]
    },
    
    # #2 Science - Google's thinking model
    "gemini_3_flash": {
        "model_id": "google/gemini-3-flash-preview",
        "display_name": "Gemini 3 Flash Preview",
        "provider": "openrouter",
        "category_rank": 2,
        "context_window": 1050000,
        "strengths": ["configurable reasoning", "multi-turn", "near Pro-level reasoning"]
    },
    
    # #3 Science - Anthropic workhorse
    "claude_sonnet": {
        "model_id": "anthropic/claude-sonnet-4.5",
        "display_name": "Claude Sonnet 4.5",
        "provider": "openrouter",
        "category_rank": 3,
        "context_window": 1000000,
        "strengths": ["real-world agents", "extended autonomous operation"]
    },
    
    # #4 Science - DeepSeek reasoning
    "deepseek_v3": {
        "model_id": "deepseek/deepseek-v3.2",
        "display_name": "DeepSeek V3.2",
        "provider": "openrouter",
        "category_rank": 4,
        "context_window": 164000,
        "strengths": ["GPT-5 class reasoning", "2025 IMO gold", "2025 IOI gold"]
    },
    
    # #7 Science - Anthropic flagship
    "claude_opus": {
        "model_id": "anthropic/claude-opus-4.5",
        "display_name": "Claude Opus 4.5",
        "provider": "openrouter",
        "category_rank": 5,
        "context_window": 200000,
        "strengths": ["frontier reasoning", "structured reasoning", "execution reliability"]
    },
    
    # #10 Science - Google flagship
    "gemini_3_pro": {
        "model_id": "google/gemini-3-pro-preview",
        "display_name": "Gemini 3 Pro Preview",
        "provider": "openrouter",
        "category_rank": 6,
        "context_window": 1050000,
        "strengths": ["GPQA Diamond", "MathArena Apex", "STEM problem solving"]
    },
    
    # Google's workhorse with thinking
    "gemini_2_5_flash": {
        "model_id": "google/gemini-2.5-flash",
        "display_name": "Gemini 2.5 Flash",
        "provider": "openrouter",
        "category_rank": 7,
        "context_window": 1050000,
        "strengths": ["advanced reasoning", "mathematics", "scientific tasks"]
    },
    
    # OpenAI open-weight reasoner
    "gpt_oss_120b": {
        "model_id": "openai/gpt-oss-120b",
        "display_name": "GPT-OSS-120B",
        "provider": "openrouter",
        "category_rank": 8,
        "context_window": 131000,
        "strengths": ["high-reasoning", "configurable reasoning depth", "chain-of-thought"]
    },
    
    # AllenAI thinking model
    "olmo_think": {
        "model_id": "allenai/olmo-3.1-32b-think",
        "display_name": "Olmo 3.1 32B Think",
        "provider": "openrouter",
        "category_rank": 9,
        "context_window": 66000,
        "strengths": ["deep reasoning", "multi-step logic", "open-source transparency"]
    },
    
    # Grok direct for real-time reasoning
    "grok_direct": {
        "model_id": "grok-3",
        "display_name": "Grok 3 (Direct)",
        "provider": "xai",
        "category_rank": 10,
        "context_window": 131072,
        "strengths": ["real-time knowledge", "reasoning"]
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
    "name": "reasoning",
    "display_name": "Reasoning & Logic",
    "description": "Models optimized for logical reasoning, scientific thinking, mathematics, and complex problem solving",
    "evaluation_focus": ["logical validity", "step-by-step reasoning", "mathematical accuracy", "scientific rigor"]
}
