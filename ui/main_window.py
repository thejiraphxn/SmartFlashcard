# ui/main_window.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from ui.dashboard import Dashboard
from ui.flashcard_set_selector import FlashcardSetSelector
from ui.quiz_page import QuizPage
from pdf_reader import extract_text_from_pdf
from flashcard import parse_flashcards
from ai_engine import generate_flashcards
from flashcard_saver import save_flashcards_to_db
from database import create_connection


class MainWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Smart Flashcard")
        self.setFixedSize(700, 400)
        self.user_id = user_id
        self.layout = QVBoxLayout()

        self.dashboard_btn = QPushButton("View Dashboard")
        self.flashcard_btn = QPushButton("Select Flashcard Set")
        self.upload_btn = QPushButton("Upload PDF & Generate Flashcards")

        self.dashboard_btn.clicked.connect(self.open_dashboard)
        self.flashcard_btn.clicked.connect(self.open_flashcard_selector)
        self.upload_btn.clicked.connect(self.upload_pdf)

        self.layout.addWidget(self.dashboard_btn)
        self.layout.addWidget(self.flashcard_btn)
        self.layout.addWidget(self.upload_btn)
        self.setLayout(self.layout)

    def open_dashboard(self):
        self.dashboard = Dashboard(self.user_id)
        self.dashboard.show()

    def open_flashcard_selector(self):
        self.selector = FlashcardSetSelector(self.user_id, self.launch_quiz)
        self.selector.show()

    def upload_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if not file_path:
            return
        try:
            text = extract_text_from_pdf(file_path)
            ai_response = generate_flashcards(text)
            flashcards = parse_flashcards(ai_response)
            if not flashcards:
                QMessageBox.warning(self, "No Flashcards", "AI did not return valid flashcards.")
                return

            flashcard_ids, msg = save_flashcards_to_db(flashcards, self.user_id, pdf_path=file_path)
            print("Flashcard IDs saved to DB:", flashcard_ids)

            self.quiz = QuizPage(flashcards, self.user_id, flashcard_ids=flashcard_ids)
            self.quiz.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate flashcards: {e}")


    def launch_quiz(self, flashcard_set_id):
        conn = create_connection()
        if not conn:
            QMessageBox.critical(self, "Error", "Cannot connect to the database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flashcards WHERE set_id = %s", (flashcard_set_id,))
            rows = cursor.fetchall()

            if not rows:
                QMessageBox.information(self, "Info", "No flashcards found for this user.")
                return

            flashcards = []
            flashcard_ids = []
            for row in rows:
                flashcard_ids.append(row[0])
                flashcards.append({
                    "question": row[1],
                    "options": {
                        "A": row[2],
                        "B": row[3],
                        "C": row[4],
                        "D": row[5]
                    },
                    "answer": row[6].strip().upper()
                })

            self.quiz = QuizPage(flashcards, self.user_id, flashcard_ids=flashcard_ids)
            self.quiz.show()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            cursor.close()
            conn.close()
