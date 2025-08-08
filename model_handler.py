# model_handler.py
from dotenv import load_dotenv
load_dotenv()

import os
import requests
import json
from prompts import get_prompt

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

# Try to import sentence-transformers optionally (heavy dependency)
HAS_SIMILARITY = False
try:
    from sentence_transformers import SentenceTransformer, util
    similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
    HAS_SIMILARITY = True
except Exception:
    # sentence-transformers (and its deps like torch) are not installed.
    # We'll skip semantic similarity checks if not available.
    similarity_model = None
    HAS_SIMILARITY = False


def _call_gemini(prompt: str, timeout: int = 30):
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    response = None
    try:
        response = requests.post(GEMINI_ENDPOINT, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        # Be defensive about JSON structure
        data = response.json()
        candidate = data.get("candidates", [{}])[0]
        content = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
        return content.strip()
    except requests.RequestException as re:
        msg = f"❌ Request error: {str(re)}"
        # include some raw response if available
        raw = ""
        try:
            raw = response.text if response is not None else "No response"
        except Exception:
            raw = "No response"
        return f"{msg}\n\nRaw response: {raw}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"


def _semantic_similarity_score(text1: str, text2: str) -> float:
    """
    Returns cosine similarity score (0.0 - 1.0). Requires sentence-transformers.
    If the library is not available, returns 1.0 (no-op).
    """
    if not HAS_SIMILARITY or similarity_model is None:
        return 1.0
    try:
        emb1 = similarity_model.encode(text1, convert_to_tensor=True)
        emb2 = similarity_model.encode(text2, convert_to_tensor=True)
        score = util.cos_sim(emb1, emb2).item()
        # clamp
        if score is None:
            return 0.0
        return float(score)
    except Exception:
        return 0.0


def generate_response(input_text: str, mode: str, target_lang: str = None, enable_semantic_check: bool = False):
    """
    Generate a response from Gemini using prompts.get_prompt.
    enable_semantic_check: if True and sentence-transformers is installed, checks semantic similarity and appends a warning if similarity < threshold.
    """
    prompt = get_prompt(mode, input_text, target_lang)

    output = _call_gemini(prompt)

    # Optional semantic similarity check (only if explicitly enabled and library available)
    if enable_semantic_check and HAS_SIMILARITY:
        try:
            score = _semantic_similarity_score(input_text, output)
            # Use a reasonable threshold (e.g., 0.70). Adjust as needed.
            threshold = 0.70
            if score < threshold:
                output = output + f"\n\n⚠️ Note: Semantic similarity score = {score:.2f}. The output may not fully preserve the original meaning."
        except Exception:
            # don't let similarity check break the response
            pass

    return output
