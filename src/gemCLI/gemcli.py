import os
import sys
from dotenv import load_dotenv
from google import genai
import speech_recognition as sr

load_dotenv()

voice_mode = False # Change to False to use text oode instead of voice
max_words = 20 # Change if you'd like

def gemini_voice():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        return

    r = sr.Recognizer()

    with sr.Microphone() as s:
        print("Gemini is Listening...")
        audio = r.listen(s)

    client = genai.Client(api_key=api_key)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=text,
            config={"system_instruction": f"Answer in at most {max_words}. Be concise."},
        )
        print("Gemini:", response.text)
    except Exception as e:
        print(f"Error: {e}")


def gemini_text():
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
            config={"system_instruction": f"Answer in at most {max_words}. Be concise."}
        )
        print("Gemini:", response.text)
    except Exception as e:
        print(f"Error: {e}")


def gemini():
    if voice_mode:
        gemini_voice()
    else:
        gemini_text()


if __name__ == "__main__":
    gemini()

