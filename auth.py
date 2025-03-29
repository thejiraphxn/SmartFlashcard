import re
import bcrypt
from database import create_connection

def validate_credentials(username: str, password: str, email: str, firstname: str, lastname: str):
    if not all([username, password, email, firstname, lastname]):
        return False, "All fields are required."
    if len(username) < 4:
        return False, "Username must be at least 4 characters."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain a digit."
    if not re.search(r"[!@#$%^&*()_+{}:\";'\\[\],.<>/?]", password):
        return False, "Password must contain a special character."
    if not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Invalid email format."
    if not firstname.isalpha() or not lastname.isalpha():
        return False, "First and last name must contain only letters."
    return True, "Valid"

def register_user(username: str, password: str, email: str, firstname: str, lastname: str):
    conn = create_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "Username already exists."

        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "Email already registered."

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, firstname, lastname) VALUES (%s, %s, %s, %s, %s)",
            (username, hashed_pw, email, firstname, lastname)
        )
        conn.commit()
        return True, "Registration successful."
    except Exception as e:
        return False, f"Registration failed: {e}"
    finally:
        cursor.close()
        conn.close()


def login_user(username: str, password: str):
    conn = create_connection()
    if not conn:
        return False, "Database connection failed.", None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if not result:
            return False, "Invalid username or password.", None

        user_id = result[0]
        stored_hash = result[1].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True, "Login successful.", user_id
        else:
            return False, "Invalid username or password.", None
    except Exception as e:
        return False, f"Login failed: {e}", None
    finally:
        cursor.close()
        conn.close()

