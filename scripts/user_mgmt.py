import sqlite3
from werkzeug.security import generate_password_hash

DB_FILE = 'data/users.db'

def init_users_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    """)
    seed_users = {
        "demo": "demo_project",
        "pmr": "pmrresearch"
    }
    for name, password in seed_users.items():
        hash_str = generate_password_hash(password,
                                          method='pbkdf2:sha256',
                                          salt_length=16)
        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash) VALUES (?, ?)
                """, (name, hash_str)
            )
            print(f"User {name} created")
        except sqlite3.IntegrityError:
            print(f"User {name} already exists")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_users_db()