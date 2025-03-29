# ui/dashboard.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from database import create_connection

class Dashboard(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setFixedSize(700, 400)
        self.user_id = user_id
        self.layout = QVBoxLayout()

        self.stats_label = QLabel("Your Quiz Statistics")
        self.refresh_btn = QPushButton("Refresh Stats")
        self.refresh_btn.clicked.connect(self.load_stats)

        self.layout.addWidget(self.stats_label)
        self.layout.addWidget(self.refresh_btn)
        self.setLayout(self.layout)

        self.load_stats()

    def load_stats(self):
        conn = create_connection()
        if not conn:
            QMessageBox.warning(self, "Error", "Could not connect to database.")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), SUM(is_correct) FROM user_answers WHERE user_id = %s", (self.user_id,))
            total, correct = cursor.fetchone()
            total = total or 0
            correct = correct or 0
            percent = (correct / total * 100) if total > 0 else 0
            self.stats_label.setText(
                f"Total Questions Answered: {total}\nCorrect Answers: {correct}\nAccuracy: {percent:.2f}%"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load stats: {e}")
        finally:
            cursor.close()
            conn.close()
