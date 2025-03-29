# flashcard.py
import json

def parse_flashcards(json_text):
    try:
        flashcards = json.loads(json_text)
        parsed = []
        for card in flashcards:
            if all(k in card for k in ["question", "options", "answer"]):
                parsed.append({
                    "question": card["question"],
                    "options": card["options"],
                    "answer": card["answer"].strip().upper()
                })
        return parsed
    except Exception as e:
        print(f"[PARSE ERROR] {e}")
        return []
