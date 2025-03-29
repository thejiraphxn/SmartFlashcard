# flashcard_saver.py
import uuid
from database import create_connection
from ai_title_generator import generate_title
from pdf_reader import extract_text_from_pdf

def save_flashcards_to_db(flashcards, user_id, pdf_path):
    conn = create_connection()
    if not conn:
        return [], "Database connection failed."

    try:
        cursor = conn.cursor()
        text = extract_text_from_pdf(pdf_path)
        title = generate_title(text)
        set_id = str(uuid.uuid4())

        cursor.execute(
            "INSERT INTO flashcard_sets (id, created_by, title_name) VALUES (%s, %s, %s)",
            (set_id, user_id, title)
        )

        flashcard_ids = []
        for card in flashcards:
            q = card["question"]
            a = card["options"]["A"]
            b = card["options"]["B"]
            c = card["options"]["C"]
            d = card["options"]["D"]
            correct = card["answer"]
            cursor.execute(
                "INSERT INTO flashcards (question, option_a, option_b, option_c, option_d, correct_option, created_by, set_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (q, a, b, c, d, correct, user_id, set_id)
            )
            flashcard_ids.append(cursor.lastrowid)

        conn.commit()
        return flashcard_ids, f"Flashcards saved in set: {title}"
    except Exception as e:
        return [], f"Error saving flashcards: {e}"
    finally:
        cursor.close()
        conn.close()
