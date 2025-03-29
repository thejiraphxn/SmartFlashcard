# ui/flashcard_set_selector.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox
from database import create_connection
from PySide6.QtWidgets import QListWidgetItem


class FlashcardSetSelector(QWidget):
    def __init__(self, user_id, start_quiz_callback):
        super().__init__()
        self.setWindowTitle("Select Flashcard Set")
        self.setFixedSize(700, 400)
        self.user_id = user_id
        self.start_quiz_callback = start_quiz_callback
        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.load_sets()

        self.start_btn = QPushButton("Start Quiz")
        self.start_btn.clicked.connect(self.select_set)

        self.layout.addWidget(QLabel("Available Flashcard Sets:"))
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.start_btn)
        self.setLayout(self.layout)

    def load_sets(self):
        conn = create_connection()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flashcard_sets ORDER BY id DESC")
            sets = cursor.fetchall()
            print("sets",sets)
            for row in sets:
                item = QListWidgetItem(f"{row[2]}")
                item.setData(256, row[0])
                self.list_widget.addItem(item)
        finally:
            cursor.close()
            conn.close()

    def select_set(self):
        selected = self.list_widget.currentItem()
        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a flashcard set.")
            return
        
        flashcard_set_id = selected.data(256)  # 256 = Qt.UserRole
        self.start_quiz_callback(flashcard_set_id)
