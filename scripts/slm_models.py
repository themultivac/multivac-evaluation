"""
Multivac V5 - Small Language Model (SLM) Pool
<48B Parameter Models - Community Requested Evaluation

Based on Reddit feedback requesting coverage for smaller, 
open-weight models that can run on consumer hardware.

UPDATED: Fixed model IDs for OpenRouter compatibility
"""

# ============================================================
# SLM MODEL POOL (<48B Parameters)
# ============================================================

SLM_MODELS = {
    # Qwen 3 Series
    "qwen3_32b": {
        "model_id": "qwen/qwen3-32b",
        "display_name": "Qwen 3 32B",
        "provider": "openrouter",
        "parameters": "32B",
        "context_window": 32768,
        "category_rank": 1,
        "active": True,
        "notes": "Alibaba's latest, strong reasoning"
    },
    
    # Kimi K2.5 - FIXED with correct ID
    "kimi_k25": {
        "model_id": "moonshotai/kimi-k2.5",
        "display_name": "Kimi K2.5",
        "provider": "openrouter",
        "parameters": "32B active / 1T MoE",
        "context_window": 262144,
        "category_rank": 2,
        "active": True,
        "notes": "Latest Kimi, native multimodal, visual coding"
    },
    
    # Gemma 3
    "gemma3_27b": {
        "model_id": "google/gemma-3-27b-it",
        "display_name": "Gemma 3 27B",
        "provider": "openrouter",
        "parameters": "27B",
        "context_window": 8192,
        "category_rank": 3,
        "active": True,
        "notes": "Google's efficient open model"
    },
    
    # Devstral - Mistral's coding model
    "devstral": {
        "model_id": "mistralai/devstral-small",
        "display_name": "Devstral Small",
        "provider": "openrouter",
        "parameters": "24B",
        "context_window": 32768,
        "category_rank": 4,
        "active": True,
        "notes": "Mistral's dedicated coding model"
    },
    
    # Llama 3.1 70B
    "llama3_70b": {
        "model_id": "meta-llama/llama-3.1-70b-instruct",
        "display_name": "Llama 3.1 70B",
        "provider": "openrouter",
        "parameters": "70B",
        "context_window": 131072,
        "category_rank": 5,
        "active": True,
        "notes": "Meta's flagship open model"
    },
    
    # Granite 4.0 - FIXED with correct ID
    "granite": {
        "model_id": "ibm-granite/granite-4.0-h-micro",
        "display_name": "Granite 4.0 Micro",
        "provider": "openrouter",
        "parameters": "Micro",
        "context_window": 128000,
        "category_rank": 6,
        "active": True,
        "notes": "IBM's latest enterprise-focused model"
    },
    
    # Qwen 3 8B
    "qwen3_8b": {
        "model_id": "qwen/qwen3-8b",
        "display_name": "Qwen 3 8B",
        "provider": "openrouter",
        "parameters": "8B",
        "context_window": 32768,
        "category_rank": 7,
        "active": True,
        "notes": "Efficient small Qwen"
    },
    
    # Llama 3.1 8B
    "llama3_8b": {
        "model_id": "meta-llama/llama-3.1-8b-instruct",
        "display_name": "Llama 3.1 8B",
        "provider": "openrouter",
        "parameters": "8B",
        "context_window": 131072,
        "category_rank": 8,
        "active": True,
        "notes": "Meta's efficient 8B model"
    },
    
    # Mistral Nemo
    "mistral_nemo": {
        "model_id": "mistralai/mistral-nemo",
        "display_name": "Mistral Nemo 12B",
        "provider": "openrouter",
        "parameters": "12B",
        "context_window": 131072,
        "category_rank": 9,
        "active": True,
        "notes": "Mistral's efficient 12B"
    },
    
    # Phi-4
    "phi4": {
        "model_id": "microsoft/phi-4",
        "display_name": "Phi-4 14B",
        "provider": "openrouter",
        "parameters": "14B",
        "context_window": 16384,
        "category_rank": 10,
        "active": True,
        "notes": "Microsoft's reasoning-focused small model"
    },
}

# ============================================================
# CATEGORY INFO
# ============================================================

CATEGORY_INFO = {
    "name": "slm",
    "display_name": "Small Language Models (<48B)",
    "description": "Open-weight models that can run on consumer hardware",
    "day": "Special",
    "focus": "Efficiency, accessibility, local deployment"
}

# Alias for compatibility
SLM_CATEGORY_INFO = CATEGORY_INFO

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_active_models() -> list[str]:
    """Return list of active SLM model keys"""
    return [k for k, v in SLM_MODELS.items() if v.get("active", False)]

# Alias for compatibility
def get_active_slm_models() -> list[str]:
    return get_active_models()

def get_model_config(model_key: str) -> dict:
    """Get config for a specific SLM model"""
    return SLM_MODELS.get(model_key, {})

# Alias for compatibility  
def get_slm_model_config(model_key: str) -> dict:
    return get_model_config(model_key)

def get_model_display_name(model_key: str) -> str:
    """Get display name for an SLM model"""
    return SLM_MODELS.get(model_key, {}).get("display_name", model_key)

# Alias for compatibility
def get_slm_display_name(model_key: str) -> str:
    return get_model_display_name(model_key)

# Export MODELS for category_loader compatibility
MODELS = SLM_MODELS

def list_slm_models():
    """Print all SLM models"""
    print(f"\n{'='*60}")
    print("📱 SMALL LANGUAGE MODEL POOL (<48B Parameters)")
    print(f"{'='*60}\n")
    
    for key, config in SLM_MODELS.items():
        status = "✓" if config.get("active") else "✗"
        print(f"{status} {config['display_name']:<25} | {config['parameters']:<20} | {config['model_id']}")
    
    print(f"\nTotal: {len(SLM_MODELS)} models")
    print(f"Active: {len(get_active_models())} models\n")


if __name__ == "__main__":
    list_slm_models()
