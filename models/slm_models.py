"""
Multivac V5.1 - Small Language Models (<48B) Model Pool
Updated: April 3, 2026
Model Version: V3 (April 2026 - added Nemotron 3 Super, Qwen3-Next, Gemma 3n)

Changes from V2:
- Added: Nemotron 3 Super (12B active / 120B MoE, free)
- Added: Qwen3-Next 80B-A3B (3B active / 80B MoE, free)
- Added: Gemma 3n 4B (Google's mobile-optimized model)
- Removed: Phi-4 14B, Mistral Nemo 12B, Llama 3.1 8B

Previous version backed up to: models_backup_v1/
"""

MODELS = {
    "qwen3_32b": {
        "model_id": "qwen/qwen3-32b",
        "display_name": "Qwen 3 32B",
        "provider": "openrouter",
        "parameters": "32B",
        "context_window": 32768,
        "category_rank": 1,
        "active": True
    },
    "kimi_k25": {
        "model_id": "moonshotai/kimi-k2.5",
        "display_name": "Kimi K2.5",
        "provider": "openrouter",
        "parameters": "32B active / 1T MoE",
        "context_window": 262144,
        "category_rank": 2,
        "active": True
    },
    "nemotron_3_super": {
        "model_id": "nvidia/nemotron-3-super-120b-a12b:free",
        "display_name": "Nemotron 3 Super",
        "provider": "openrouter",
        "parameters": "12B active / 120B MoE",
        "context_window": 262144,
        "category_rank": 3,
        "active": True
    },
    "qwen3_next_80b": {
        "model_id": "qwen/qwen3-next-80b-a3b-instruct:free",
        "display_name": "Qwen3-Next 80B-A3B",
        "provider": "openrouter",
        "parameters": "3B active / 80B MoE",
        "context_window": 262144,
        "category_rank": 4,
        "active": True
    },
    "devstral": {
        "model_id": "mistralai/devstral-small",
        "display_name": "Devstral Small",
        "provider": "openrouter",
        "parameters": "24B",
        "context_window": 32768,
        "category_rank": 5,
        "active": True
    },
    "gemma3_27b": {
        "model_id": "google/gemma-3-27b-it",
        "display_name": "Gemma 3 27B",
        "provider": "openrouter",
        "parameters": "27B",
        "context_window": 8192,
        "category_rank": 6,
        "active": True
    },
    "llama4_scout": {
        "model_id": "meta-llama/llama-4-scout",
        "display_name": "Llama 4 Scout",
        "provider": "openrouter",
        "parameters": "17B active / 109B MoE",
        "context_window": 131072,
        "category_rank": 7,
        "active": True
    },
    "granite_40": {
        "model_id": "ibm-granite/granite-4.0-h-micro",
        "display_name": "Granite 4.0 Micro",
        "provider": "openrouter",
        "parameters": "Micro",
        "context_window": 128000,
        "category_rank": 8,
        "active": True
    },
    "gemma_3n_4b": {
        "model_id": "google/gemma-3n-e4b-it",
        "display_name": "Gemma 3n 4B",
        "provider": "openrouter",
        "parameters": "4B",
        "context_window": 32768,
        "category_rank": 9,
        "active": True
    },
    "qwen3_8b": {
        "model_id": "qwen/qwen3-8b",
        "display_name": "Qwen 3 8B",
        "provider": "openrouter",
        "parameters": "8B",
        "context_window": 32768,
        "category_rank": 10,
        "active": True
    },
}

# Category metadata
CATEGORY_INFO = {
    "name": "slm",
    "display_name": "Small Language Models (<48B)",
    "description": "Open-weight models under 48B parameters for local deployment evaluation",
    "model_count": 10,
    "version": "v3_april2026"
}

def get_active_models():
    """Return list of active model keys in rank order"""
    return [k for k, v in sorted(MODELS.items(), key=lambda x: x[1].get("category_rank", 99)) if v.get("active", True)]
