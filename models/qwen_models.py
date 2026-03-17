"""
Multivac V5.1 - Project Qwen Model Pool
All available Qwen models on OpenRouter, March 2026
"""

MODELS = {
    "qwen3_235b_a22b": {"model_id": "qwen/qwen3-235b-a22b-instruct-2507", "display_name": "Qwen 3 235B-A22B", "provider": "openrouter", "category_rank": 6, "context_window": 262000, "active": False},
    "qwen35_9b": {"model_id": "qwen/qwen3.5-9b", "display_name": "Qwen 3.5 9B", "provider": "openrouter", "category_rank": 1, "context_window": 256000, "active": True},
    "qwen3_8b": {"model_id": "qwen/qwen3-8b", "display_name": "Qwen 3 8B", "provider": "openrouter", "category_rank": 2, "context_window": 32768, "active": True},
    "qwen35_flash": {"model_id": "qwen/qwen3.5-flash", "display_name": "Qwen 3.5 Flash", "provider": "openrouter", "category_rank": 3, "context_window": 1000000, "active": False},
    "qwen3_32b": {"model_id": "qwen/qwen3-32b", "display_name": "Qwen 3 32B", "provider": "openrouter", "category_rank": 4, "context_window": 41000, "active": True},
    "qwen3_coder_next": {"model_id": "qwen/qwen3-coder-next", "display_name": "Qwen 3 Coder Next", "provider": "openrouter", "category_rank": 5, "context_window": 262000, "active": True},
    "qwen35_35b_a3b": {"model_id": "qwen/qwen3.5-35b-a3b", "display_name": "Qwen 3.5 35B-A3B", "provider": "openrouter", "category_rank": 6, "context_window": 262000, "active": True},
    "qwen35_27b": {"model_id": "qwen/qwen3.5-27b", "display_name": "Qwen 3.5 27B", "provider": "openrouter", "category_rank": 7, "context_window": 262000, "active": True},
    "qwen35_122b_a10b": {"model_id": "qwen/qwen3.5-122b-a10b", "display_name": "Qwen 3.5 122B-A10B", "provider": "openrouter", "category_rank": 8, "context_window": 262000, "active": True},
    "qwen35_plus": {"model_id": "qwen/qwen3.5-plus-2026-02-15", "display_name": "Qwen 3.5 Plus", "provider": "openrouter", "category_rank": 9, "context_window": 1000000, "active": False},
    "qwen35_397b_a17b": {"model_id": "qwen/qwen3.5-397b-a17b", "display_name": "Qwen 3.5 397B-A17B", "provider": "openrouter", "category_rank": 10, "context_window": 262000, "active": True},
}

CATEGORY_INFO = {"name": "qwen", "display_name": "Project Qwen", "description": "All Qwen models across 3 generations"}

def get_active_models():
    return [k for k, v in sorted(MODELS.items(), key=lambda x: x[1]["category_rank"]) if v.get("active", True)]
