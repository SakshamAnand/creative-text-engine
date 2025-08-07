from dotenv import load_dotenv
load_dotenv()

import os
import requests
from prompts import get_prompt
from sentence_transformers import SentenceTransformer, util

similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
def generate_response(input_text, mode, target_lang=None):
    prompt = get_prompt(mode, input_text, target_lang)

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

        # ✅ Optional: semantic similarity check
        if mode in ["translate", "rephrase", "formal", "casual"]:
            sim = util.cos_sim(
                similarity_model.encode(input_text, convert_to_tensor=True),
                similarity_model.encode(output, convert_to_tensor=True)
            ).item()
            if sim < 0.75:
                output += "\n\n⚠️ Warning: Output meaning may differ from input."

        return output

    except Exception as e:
        return f"❌ Error: {str(e)}\n\nRaw response: {response.text if response else 'No response'}"
