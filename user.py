import sqlite3
from flask_login import UserMixin
from extensions import login_manager

DB_FILE = "data/users.db"

class User(UserMixin):
    def __init__(self, username):
        self.id = username

def get_user_from_db(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, password_hash
        FROM users
        WHERE username = ?
        """,
        (username,)
    )
    user_data = cursor.fetchone()
    conn.close()
    return user_data

def register_user_loader():
    @login_manager.user_loader
    def load_user(user_id):
        user_data = get_user_from_db(user_id)
        if user_data:
            return User(user_id)
        return None