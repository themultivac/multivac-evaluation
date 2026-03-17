#!/usr/bin/env python3
"""
Model Discovery Script for Multivac V5
Run this to find available models on OpenRouter
"""

import os
import httpx
import json
import sys

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_all_models():
    """Fetch all available models from OpenRouter"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = httpx.get(
        "https://openrouter.ai/api/v1/models",
        headers=headers
    )
    response.raise_for_status()
    return response.json()["data"]

def search_models(query: str):
    """Search for models matching a query"""
    models = get_all_models()
    query_lower = query.lower()
    
    matches = [
        m for m in models 
        if query_lower in m["id"].lower() or query_lower in m.get("name", "").lower()
    ]
    
    return matches

def print_model_info(model):
    """Pretty print model information"""
    print(f"\n{'='*60}")
    print(f"ID: {model['id']}")
    print(f"Name: {model.get('name', 'N/A')}")
    print(f"Context: {model.get('context_length', 'N/A')}")
    print(f"Input Price: ${model.get('pricing', {}).get('prompt', 'N/A')}/token")
    print(f"Output Price: ${model.get('pricing', {}).get('completion', 'N/A')}/token")

def main():
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not set")
        sys.exit(1)
    
    # Search terms for models we want
    search_terms = [
        "claude",
        "gpt-4o",
        "o1",
        "gemini",
        "llama",
        "deepseek",
        "mistral",
        "command",
        "grok"
    ]
    
    print("\n🔍 OPENROUTER MODEL DISCOVERY")
    print("="*60)
    
    all_models = get_all_models()
    print(f"\nTotal models available: {len(all_models)}")
    
    for term in search_terms:
        matches = search_models(term)
        if matches:
            print(f"\n\n{'#'*60}")
            print(f"# SEARCH: {term.upper()}")
            print(f"# Found: {len(matches)} models")
            print(f"{'#'*60}")
            
            # Show top 5 most relevant
            for model in matches[:5]:
                print(f"\n  📦 {model['id']}")
                context = model.get('context_length', 'N/A')
                print(f"     Context: {context}")
    
    # Print recommended config
    print("\n\n" + "="*60)
    print("📋 RECOMMENDED MODEL IDS FOR config.py:")
    print("="*60)
    
    # Find best matches for our needs
    recommendations = {}
    
    for model in all_models:
        mid = model['id'].lower()
        
        # Claude
        if 'claude' in mid and 'sonnet' in mid and '4' in mid:
            if 'claude-sonnet' not in recommendations:
                recommendations['claude-sonnet'] = model['id']
        if 'claude' in mid and 'opus' in mid:
            if 'claude-opus' not in recommendations:
                recommendations['claude-opus'] = model['id']
        
        # GPT
        if mid == 'openai/gpt-4o':
            recommendations['gpt-4o'] = model['id']
        if mid == 'openai/o1':
            recommendations['o1'] = model['id']
        
        # Gemini
        if 'gemini' in mid and ('2.0' in mid or '2-' in mid or 'pro' in mid):
            if 'gemini' not in recommendations:
                recommendations['gemini'] = model['id']
        
        # Llama
        if 'llama' in mid and ('4' in mid or '3.3' in mid or '70b' in mid):
            if 'llama' not in recommendations:
                recommendations['llama'] = model['id']
        
        # DeepSeek
        if 'deepseek' in mid and ('v3' in mid or 'chat' in mid):
            if 'deepseek' not in recommendations:
                recommendations['deepseek'] = model['id']
        
        # Mistral
        if 'mistral' in mid and 'large' in mid:
            if 'mistral' not in recommendations:
                recommendations['mistral'] = model['id']
        
        # Cohere
        if 'command' in mid and ('plus' in mid or 'r-plus' in mid):
            if 'cohere' not in recommendations:
                recommendations['cohere'] = model['id']
    
    for name, model_id in recommendations.items():
        print(f"  {name}: \"{model_id}\"")
    
    print("\n" + "="*60)
    print("Copy these IDs to your config.py MODELS dictionary")
    print("="*60)

if __name__ == "__main__":
    main()
