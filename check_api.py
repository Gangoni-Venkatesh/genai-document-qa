import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

api_key = os.getenv("GOOGLE_API_KEY")

print("GEMINI API CONFIGURATION CHECK")
print("--------------------------------")

print("API key found:", bool(api_key))
print("API key length:", len(api_key) if api_key else 0)
print("Starts with AIza:", api_key.startswith("AIza") if api_key else False)
print("Contains spaces:", any(c.isspace() for c in api_key) if api_key else False)
print("Contains placeholder:", "YOUR_" in api_key if api_key else False)