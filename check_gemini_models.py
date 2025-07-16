import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List all available models
models = genai.list_models()

print("\n✅ Available Gemini Models:")
for model in models:
    print("-", model.name)