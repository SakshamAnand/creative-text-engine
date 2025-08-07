from dotenv import load_dotenv
load_dotenv()

import os
import requests
from prompts import get_prompt

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
def generate_text(input_text, mode, target_lang=None):
    # 🔗 Build the final prompt from prompts.py
    prompt = get_prompt(mode, input_text, target_lang)

    # Prepare Gemini payload
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Call the Gemini API
    try:
        response = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return output.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}\n\nRaw response: {response.text if response else 'No response'}"
