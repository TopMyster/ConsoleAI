import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()

def ask():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        return

    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Ask Gemini: ")
    
    if not prompt.strip():
        return

    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={"system_instruction": "Answer in at most 20 words. Be concise."}
        )
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ask()
