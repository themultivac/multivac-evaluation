"""
Multivac V5 - Analysis Category Models
Top 10 models optimized for data analysis, finance, and academic research
Based on OpenRouter Finance/Academia/Legal rankings
"""

MODELS = {
    # #1 Finance, #1 Academia - Xiaomi MoE
    "mimo_v2_flash": {
        "model_id": "xiaomi/mimo-v2-flash",
        "display_name": "MiMo-V2-Flash",
        "provider": "openrouter",
        "category_rank": 1,
        "context_window": 262000,
        "strengths": ["finance", "academia", "hybrid-thinking"]
    },
    
    # #2 Finance, #3 Academia - Google thinking
    "gemini_3_flash": {
        "model_id": "google/gemini-3-flash-preview",
        "display_name": "Gemini 3 Flash Preview",
        "provider": "openrouter",
        "category_rank": 2,
        "context_window": 1050000,
        "strengths": ["financial analysis", "research", "multimodal understanding"]
    },
    
    # #2 Academia - Google workhorse
    "gemini_2_5_flash": {
        "model_id": "google/gemini-2.5-flash",
        "display_name": "Gemini 2.5 Flash",
        "provider": "openrouter",
        "category_rank": 3,
        "context_window": 1050000,
        "strengths": ["academic tasks", "mathematics", "built-in thinking"]
    },
    
    # #3 Finance, #6 Academia - OpenAI open-weight
    "gpt_oss_120b": {
        "model_id": "openai/gpt-oss-120b",
        "display_name": "GPT-OSS-120B",
        "provider": "openrouter",
        "category_rank": 4,
        "context_window": 131000,
        "strengths": ["financial analysis", "academic reasoning", "structured output"]
    },
    
    # #4 Academia - DeepSeek
    "deepseek_v3": {
        "model_id": "deepseek/deepseek-v3.2",
        "display_name": "DeepSeek V3.2",
        "provider": "openrouter",
        "category_rank": 5,
        "context_window": 164000,
        "strengths": ["research synthesis", "data analysis", "long-context"]
    },
    
    # #5 Academia - Anthropic workhorse
    "claude_sonnet": {
        "model_id": "anthropic/claude-sonnet-4.5",
        "display_name": "Claude Sonnet 4.5",
        "provider": "openrouter",
        "category_rank": 6,
        "context_window": 1000000,
        "strengths": ["financial analysis", "research agents", "specification adherence"]
    },
    
    # #9 Academia - Anthropic flagship
    "claude_opus": {
        "model_id": "anthropic/claude-opus-4.5",
        "display_name": "Claude Opus 4.5",
        "provider": "openrouter",
        "category_rank": 7,
        "context_window": 200000,
        "strengths": ["autonomous research", "multi-step planning", "spreadsheet manipulation"]
    },
    
    # #1 Legal - Strong for formal analysis
    "gpt_oss_legal": {
        "model_id": "openai/gpt-oss-120b",
        "display_name": "GPT-OSS-120B (Legal)",
        "provider": "openrouter",
        "category_rank": 8,
        "context_window": 131000,
        "strengths": ["legal analysis", "formal reasoning", "document review"]
    },
    
    # Google flagship for deep analysis
    "gemini_3_pro": {
        "model_id": "google/gemini-3-pro-preview",
        "display_name": "Gemini 3 Pro Preview",
        "provider": "openrouter",
        "category_rank": 9,
        "context_window": 1050000,
        "strengths": ["multimodal analytics", "research synthesis", "factual QA"]
    },
    
    # Grok for real-time financial data
    "grok_4_1_fast": {
        "model_id": "x-ai/grok-4.1-fast",
        "display_name": "Grok 4.1 Fast",
        "provider": "openrouter",
        "category_rank": 10,
        "context_window": 2000000,
        "strengths": ["real-time data", "financial research", "2M context"]
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
    "name": "analysis",
    "display_name": "Analysis & Research",
    "description": "Models optimized for data analysis, financial modeling, academic research, and document review",
    "evaluation_focus": ["accuracy", "thoroughness", "citation quality", "analytical depth", "insight generation"]
}
