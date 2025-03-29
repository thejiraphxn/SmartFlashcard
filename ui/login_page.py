# ui/login_page.py
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from auth import login_user
from ui.main_window import MainWindow
from ui.register_page import RegisterWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(700, 400)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setText("Jiraphon123");
        

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setText("0980656183Jj#");

        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)
        self.setLayout(layout)

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.open_register_window)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            self._show_message(False, "Please fill in all fields.")
            return
        success, message, user_id = login_user(username, password)
        
        # self._show_message(success, message)
        if success:
            self.hide()
            self.main_window = MainWindow(user_id=user_id)
            self.main_window.show()

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def _show_message(self, success, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Success" if success else "Error")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information if success else QMessageBox.Warning)
        msg_box.exec()


