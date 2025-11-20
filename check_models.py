import google.generativeai as gen_ai
import os
from dotenv import load_dotenv

# Load your API key from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: API Key not found in .env file.")
else:
    gen_ai.configure(api_key=api_key)

    print("--- LIST OF AVAILABLE MODELS ---")
    try:
        # Loop through models and find ones that generate text
        for model in gen_ai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(model.name)
    except Exception as e:
        print(f"Connection Error: {e}")