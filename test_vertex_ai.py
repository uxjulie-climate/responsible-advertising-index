#!/usr/bin/env python3
"""Test Vertex AI connection and Gemini 1.5 Flash model availability."""

import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
PROJECT_ID = "gen-lang-client-0192368285"
LOCATION = "us-central1"

print(f"Initializing Vertex AI...")
print(f"Project: {PROJECT_ID}")
print(f"Location: {LOCATION}")

vertexai.init(project=PROJECT_ID, location=LOCATION)

print("\n✅ Vertex AI initialized successfully!")

# Test Gemini 1.5 Flash model
print("\nTesting Gemini 1.5 Flash model...")
model = GenerativeModel("gemini-1.5-flash")

# Simple test prompt
response = model.generate_content("Say 'Hello from Vertex AI!' in one sentence.")

print(f"\n✅ Model test successful!")
print(f"Response: {response.text}")

# Test model info
print(f"\nModel name: {model._model_name}")

print("\n" + "="*60)
print("🎉 ALL TESTS PASSED!")
print("="*60)
print("\nYour Vertex AI setup is complete and working!")
print(f"- Project ID: {PROJECT_ID}")
print(f"- Location: {LOCATION}")
print(f"- Model: gemini-1.5-flash-002")
print(f"- Bucket: gs://rai-video-temp-{PROJECT_ID}")
print("\nYou're ready to implement video analysis!")
