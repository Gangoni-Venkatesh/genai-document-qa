import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv(override=True)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not found!")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Explain RAG in two simple sentences."
    )

    print("\nGEMINI CONNECTION SUCCESSFUL!")
    print("--------------------------------")
    print(response.text)

except Exception as e:
    print("\nGEMINI CONNECTION FAILED!")
    print("--------------------------------")
    print(type(e).__name__)
    print(str(e)[:1500])