import requests
import os
from dotenv import load_dotenv

load_dotenv()


def summarize_text(text: str) -> str:
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    API_KEY = os.getenv("GEMINI_API_KEY")

    if not API_KEY:
        raise ValueError("API key for Gemini AI is not set")

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"Summarize the following text:\n{text}"}]}]
    }

    response = requests.post(f"{API_URL}?key={API_KEY}", json=payload, headers=headers)
    response_data = response.json()

    if "candidates" in response_data and response_data["candidates"]:
        return response_data["candidates"][0]["content"]["parts"][0]["text"]

    return "Summarization failed"
