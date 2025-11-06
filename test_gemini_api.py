#!/usr/bin/env python3
"""Test Google Generative AI library for video support (alternative to Vertex AI)."""

import google.generativeai as genai
import os

# Use the API key from the working demo
API_KEY = "AIzaSyA_SIvs6tGlusHJ_82CaPfiHJp50ySsSCQ"

print("Testing Google Generative AI library...")
print(f"API Key: {API_KEY[:20]}...")

genai.configure(api_key=API_KEY)

print("\n📋 Listing available models:")
print("-" * 60)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"   Methods: {', '.join(model.supported_generation_methods)}")
        if hasattr(model, 'input_token_limit'):
            print(f"   Input token limit: {model.input_token_limit}")

        # Check if model supports video
        supports_video = False
        if hasattr(model, 'supported_inputs'):
            supports_video = 'video/*' in model.supported_inputs or 'video' in str(model.supported_inputs).lower()

        print(f"   Video support: {'✅ YES' if supports_video else '❌ No'}")
        print()

print("\n" + "="*60)
print("🔍 Looking for video-capable models...")
print("="*60)

# Look specifically for Gemini 1.5 models that support video
for model in genai.list_models():
    model_name = model.name.lower()
    if '1.5' in model_name or 'flash' in model_name or 'pro' in model_name:
        print(f"\n📹 Found: {model.name}")
        print(f"   Display name: {model.display_name if hasattr(model, 'display_name') else 'N/A'}")
        print(f"   Description: {model.description if hasattr(model, 'description') else 'N/A'}")
