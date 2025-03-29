# ai_title_generator.py
import requests

OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"

def generate_title(text: str) -> str:
    prompt = (
        "From the following text, suggest a short and clear title for a flashcard set."
        "Respond with only the title."
        f"Text:{text}"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "temperature": 0.5,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_BASE_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip().replace('"', '')
    except Exception as e:
        print(f"[AI TITLE ERROR] {e}")
        return "Untitled Set"
