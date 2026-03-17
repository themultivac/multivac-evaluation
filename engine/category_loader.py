"""
Multivac V5 - Category Model Loader
Dynamically loads the appropriate model pool based on question category
"""

from typing import Optional
import importlib

# Category to module mapping
CATEGORY_MODULES = {
    "code": "code_models",
    "qwen": "qwen_models",  # Project Qwen - all Qwen models
    "reasoning": "reasoning_models",
    "analysis": "analysis_models",
    "communication": "communication_models",
    "meta_alignment": "meta_alignment_models",
    "slm": "slm_models",  # Small Language Models (<48B)
    # Aliases
    "programming": "code_models",
    "science": "reasoning_models",
    "finance": "analysis_models",
    "writing": "communication_models",
    "alignment": "meta_alignment_models",
    "edge_cases": "meta_alignment_models",  # Edge cases use alignment pool
    "small": "slm_models",  # Alias for SLM
    "open": "slm_models",   # Alias for open-weight focus
}

# Default fallback category
DEFAULT_CATEGORY = "meta_alignment"

# Cache for loaded modules
_module_cache = {}


def get_category_module(category: str):
    """Load and return the appropriate category module"""
    
    # Normalize category name
    category = category.lower().strip()
    
    # Get module name (with fallback)
    module_name = CATEGORY_MODULES.get(category, CATEGORY_MODULES[DEFAULT_CATEGORY])
    
    # Return cached module if available
    if module_name in _module_cache:
        return _module_cache[module_name]
    
    # Import module dynamically
    try:
        module = importlib.import_module(module_name)
        _module_cache[module_name] = module
        return module
    except ImportError as e:
        print(f"⚠️  Warning: Could not load {module_name}, falling back to meta_alignment")
        fallback = importlib.import_module("meta_alignment_models")
        _module_cache[module_name] = fallback
        return fallback


def get_models_for_category(category: str) -> dict:
    """Get the MODELS dict for a category"""
    module = get_category_module(category)
    # Handle both MODELS and SLM_MODELS naming conventions
    if hasattr(module, 'MODELS'):
        return module.MODELS
    elif hasattr(module, 'SLM_MODELS'):
        return module.SLM_MODELS
    else:
        return {}


def get_active_models_for_category(category: str) -> list[str]:
    """Get active model keys for a category"""
    module = get_category_module(category)
    # Handle both naming conventions
    if hasattr(module, 'get_active_models'):
        return module.get_active_models()
    elif hasattr(module, 'get_active_slm_models'):
        return module.get_active_slm_models()
    else:
        # Fallback: filter active models manually
        models = get_models_for_category(category)
        return [k for k, v in models.items() if v.get("active", False)]


def get_model_display_name(category: str, model_key: str) -> str:
    """Get display name for a model in a category"""
    module = get_category_module(category)
    # Handle both naming conventions
    if hasattr(module, 'get_model_display_name'):
        return module.get_model_display_name(model_key)
    elif hasattr(module, 'get_slm_display_name'):
        return module.get_slm_display_name(model_key)
    else:
        # Fallback
        models = get_models_for_category(category)
        return models.get(model_key, {}).get("display_name", model_key)


def get_model_config(category: str, model_key: str) -> dict:
    """Get full config for a model in a category"""
    module = get_category_module(category)
    # Handle both naming conventions
    if hasattr(module, 'get_model_config'):
        return module.get_model_config(model_key)
    elif hasattr(module, 'get_slm_model_config'):
        return module.get_slm_model_config(model_key)
    else:
        # Fallback
        models = get_models_for_category(category)
        return models.get(model_key, {})


def get_category_info(category: str) -> dict:
    """Get metadata about a category"""
    module = get_category_module(category)
    # Handle both naming conventions
    if hasattr(module, 'CATEGORY_INFO'):
        return module.CATEGORY_INFO
    elif hasattr(module, 'SLM_CATEGORY_INFO'):
        return module.SLM_CATEGORY_INFO
    else:
        # Fallback
        return {
            "name": category,
            "display_name": category.title(),
            "description": f"{category} evaluation pool"
        }


def list_all_categories() -> list[str]:
    """List all available categories (excluding aliases)"""
    return ["code", "reasoning", "analysis", "communication", "meta_alignment", "slm", "qwen"]


def get_category_summary() -> str:
    """Get a formatted summary of all categories and their models"""
    
    lines = [
        "=" * 60,
        "MULTIVAC V5 - CATEGORY MODEL POOLS",
        "=" * 60,
        ""
    ]
    
    for category in list_all_categories():
        try:
            info = get_category_info(category)
            models = get_active_models_for_category(category)
            model_dict = get_models_for_category(category)
            
            lines.append(f"📂 {info.get('display_name', category).upper()}")
            lines.append(f"   {info.get('description', 'No description')}")
            lines.append("")
            
            for model_key in models:
                config = model_dict.get(model_key, {})
                provider = config.get("provider", "unknown")
                rank = config.get("category_rank", "?")
                name = config.get('display_name', model_key)
                params = config.get('parameters', '')
                if params:
                    lines.append(f"   #{rank:2} {name} [{params}] ({provider})")
                else:
                    lines.append(f"   #{rank:2} {name} ({provider})")
            
            lines.append("")
        except Exception as e:
            lines.append(f"📂 {category.upper()}")
            lines.append(f"   ⚠️ Error loading: {e}")
            lines.append("")
    
    return "\n".join(lines)


# Quick test
if __name__ == "__main__":
    print(get_category_summary())
    
    print("\n" + "=" * 60)
    print("Testing category loading:")
    print("=" * 60)
    
    for cat in list_all_categories():
        try:
            models = get_active_models_for_category(cat)
            print(f"\n{cat}: {len(models)} models")
            for m in models[:3]:
                print(f"  - {get_model_display_name(cat, m)}")
        except Exception as e:
            print(f"\n{cat}: ⚠️ Error - {e}")
