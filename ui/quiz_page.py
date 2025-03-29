# ui/quiz_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QButtonGroup, QRadioButton
from database import create_connection

class QuizPage(QWidget):
    def __init__(self, flashcards, user_id, flashcard_ids=None):
        super().__init__()
        self.setWindowTitle("Flashcard Quiz")
        self.setFixedSize(700, 400)
        self.flashcards = flashcards
        self.flashcard_ids = flashcard_ids or list(range(1, len(flashcards)+1))
        self.user_id = user_id
        self.current_index = 0
        self.selected_option = None

        self.layout = QVBoxLayout()
        self.question_label = QLabel()
        self.option_buttons = QButtonGroup(self)
        self.layout.addWidget(self.question_label)
        for key in ["A", "B", "C", "D"]:
            btn = QRadioButton()
            self.option_buttons.addButton(btn, ord(key))
            self.layout.addWidget(btn)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.submit_answer)
        
        self.layout.addWidget(self.submit_btn)

        self.setLayout(self.layout)
        self.load_question()

    def load_question(self):
        if self.current_index >= len(self.flashcards):
            QMessageBox.information(self, "Done", "You have completed the quiz.")
            self.close()
            return

        card = self.flashcards[self.current_index]
        self.question_label.setText(card["question"])
        for i, key in enumerate(["A", "B", "C", "D"]):
            btn = self.option_buttons.buttons()[i]
            btn.setText(f"{key}: {card['options'][key]}")
            btn.setChecked(False)

    def submit_answer(self):
        selected_btn = self.option_buttons.checkedButton()
        if not selected_btn:
            QMessageBox.warning(self, "Error", "Please select an option.")
            return

        selected_text = selected_btn.text()[0]
        correct = self.flashcards[self.current_index]["answer"]
        is_correct = selected_text == correct
        flashcard_id = self.flashcard_ids[self.current_index]

        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO user_answers (user_id, flashcard_id, selected_option, is_correct) VALUES (%s, %s, %s, %s)",
                    (self.user_id, flashcard_id, selected_text, is_correct)
                )
                conn.commit()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", str(e))
            finally:
                cursor.close()
                conn.close()

        self.current_index += 1
        self.load_question()
