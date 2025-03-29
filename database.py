import mysql.connector
from mysql.connector import Error
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PORT = os.getenv("DB_PORT", 8889)
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "SmartFlashcard2")

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return connection
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None

def init_db():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcards (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    question TEXT NOT NULL,
                    option_a TEXT,
                    option_b TEXT,
                    option_c TEXT,
                    option_d TEXT,
                    correct_option ENUM('A','B','C','D'),
                    created_by INT,
                    FOREIGN KEY (created_by) REFERENCES users(id)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_answers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    flashcard_id INT,
                    selected_option ENUM('A','B','C','D'),
                    is_correct BOOLEAN,
                    answered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id)
                );
            """)

            connection.commit()
        except Error as e:
            print(f"[DB INIT ERROR] {e}")
        finally:
            cursor.close()
            connection.close()
