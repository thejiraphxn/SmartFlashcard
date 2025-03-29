from ui.login_page import LoginWindow
from PySide6.QtWidgets import QApplication
import sys

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     login = LoginWindow()
#     login.show()
#     sys.exit(app.exec())
    
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # ✅ โหลด QSS ฉ่ำ ๆ ที่นี่!
    try:
        with open("ui/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"[QSS ERROR] {e}")

    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

