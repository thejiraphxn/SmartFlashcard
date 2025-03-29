# ui/register_page.py
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from auth import register_user, validate_credentials

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setFixedSize(700, 550)

        self.firstname_input = QLineEdit()
        self.lastname_input = QLineEdit()
        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()

        self.firstname_input.setPlaceholderText("First Name")
        self.lastname_input.setPlaceholderText("Last Name")
        self.username_input.setPlaceholderText("Username")
        self.email_input.setPlaceholderText("Email")
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.firstname_input)
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.lastname_input)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_btn)
        self.setLayout(layout)

    def register(self):
        firstname = self.firstname_input.text().strip()
        lastname = self.lastname_input.text().strip()
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()

        valid, msg = validate_credentials(username, password, email, firstname, lastname)
        if not valid:
            self._show_message(False, msg)
            return

        success, message = register_user(username, password, email, firstname, lastname)
        if success:
            self.firstname_input.clear()    
            self.lastname_input.clear()
            self.username_input.clear()
            self.email_input.clear()
            self.password_input.clear()
            self.hide()
        self._show_message(success, message)
        

    def _show_message(self, success, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Success" if success else "Error")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information if success else QMessageBox.Warning)
        msg_box.exec()
