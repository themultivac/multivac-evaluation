"""
Multivac V5 - Code Category Models
Top 10 models optimized for programming/coding tasks
Based on OpenRouter Programming rankings
"""

MODELS = {
    # #1 Programming - xAI's dedicated coding model
    "grok_code_fast": {
        "model_id": "x-ai/grok-code-fast-1",
        "display_name": "Grok Code Fast 1",
        "provider": "openrouter",
        "category_rank": 1,
        "context_window": 256000,
        "strengths": ["agentic coding", "fast reasoning", "visible traces"]
    },
    
    # #2 Programming - Anthropic flagship
    "claude_opus": {
        "model_id": "anthropic/claude-opus-4.5",
        "display_name": "Claude Opus 4.5",
        "provider": "openrouter",
        "category_rank": 2,
        "context_window": 200000,
        "strengths": ["complex software engineering", "agentic workflows", "long-horizon tasks"]
    },
    
    # #3 Programming - Google's fast thinking model
    "gemini_3_flash": {
        "model_id": "google/gemini-3-flash-preview",
        "display_name": "Gemini 3 Flash Preview",
        "provider": "openrouter",
        "category_rank": 3,
        "context_window": 1050000,
        "strengths": ["agentic workflows", "coding assistance", "tool use"]
    },
    
    # #5 Programming - Anthropic workhorse
    "claude_sonnet": {
        "model_id": "anthropic/claude-sonnet-4.5",
        "display_name": "Claude Sonnet 4.5",
        "provider": "openrouter",
        "category_rank": 5,
        "context_window": 1000000,
        "strengths": ["SWE-bench verified", "code security", "specification adherence"]
    },
    
    # #6 Programming - Google flagship
    "gemini_3_pro": {
        "model_id": "google/gemini-3-pro-preview",
        "display_name": "Gemini 3 Pro Preview",
        "provider": "openrouter",
        "category_rank": 6,
        "context_window": 1050000,
        "strengths": ["agentic coding", "SWE-Bench Verified", "Terminal-Bench 2.0"]
    },
    
    # #8 Programming - MiniMax lightweight
    "minimax_m2": {
        "model_id": "minimax/minimax-m2.1",
        "display_name": "MiniMax M2.1",
        "provider": "openrouter",
        "category_rank": 8,
        "context_window": 197000,
        "strengths": ["Multi-SWE-Bench", "SWE-Bench Multilingual", "efficient"]
    },
    
    # #9 Programming - Z.AI flagship
    "glm_4_7": {
        "model_id": "z-ai/glm-4.7",
        "display_name": "GLM 4.7",
        "provider": "openrouter",
        "category_rank": 9,
        "context_window": 203000,
        "strengths": ["programming", "complex agent tasks", "front-end aesthetics"]
    },
    
    # DeepSeek - Strong open-source coder
    "deepseek_v3": {
        "model_id": "deepseek/deepseek-v3.2",
        "display_name": "DeepSeek V3.2",
        "provider": "openrouter",
        "category_rank": 10,
        "context_window": 164000,
        "strengths": ["reasoning", "agentic tool-use", "GPT-5 class reasoning"]
    },
    
    # OpenAI dedicated coding model
    "gpt_codex": {
        "model_id": "openai/gpt-5.2-codex",
        "display_name": "GPT-5.2-Codex",
        "provider": "openrouter",
        "category_rank": 11,
        "context_window": 400000,
        "strengths": ["agentic coding", "long execution", "code review"]
    },
    
    # Grok direct API for diversity
    "grok_direct": {
        "model_id": "grok-3",
        "display_name": "Grok 3 (Direct)",
        "provider": "xai",
        "category_rank": 12,
        "context_window": 131072,
        "strengths": ["real-time knowledge", "code generation"]
    }
}

def get_active_models() -> list[str]:
    """Return list of active model keys for this category"""
    # Return top 10 by category rank
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
    "name": "code",
    "display_name": "Programming & Code",
    "description": "Models optimized for software engineering, debugging, code review, and agentic coding tasks",
    "evaluation_focus": ["correctness", "efficiency", "best practices", "security", "maintainability"]
}
