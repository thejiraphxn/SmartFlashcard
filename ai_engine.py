# ai_engine.py
import requests
import json

OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"

def generate_title(text: str):
    prompt = (
        "Give a short, clear, and relevant title for a flashcard set "
        "based on the following educational content:"
        f"{text[:1000]}Title:"
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
        return result.get("response", "Untitled Set").strip()
    except Exception as e:
        print(f"[AI TITLE ERROR] {e}")
        return "Untitled Set"

def generate_flashcards(text: str, num_cards: int = 5):
    prompt = (
        f"From the following text, generate {num_cards} flashcards in JSON format.\n"
        "Each flashcard must include:\n"
        "- 'question': a string\n"
        "- 'options': { 'A': ..., 'B': ..., 'C': ..., 'D': ... }\n"
        "- 'answer': one of 'A', 'B', 'C', or 'D'\n"
        "Respond ONLY with a JSON array.\n\n"
        f"Text:\n{text}"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "temperature": 0.7,
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
        return result.get("response", "")
    except Exception as e:
        print(f"[AI ERROR] {e}")
        return "[]"
