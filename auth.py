import sqlite3
import hashlib
import secrets
from typing import Optional

DB_PATH = "users.db"

def _get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT, salt TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS user_data (username TEXT, key TEXT, value TEXT, PRIMARY KEY(username,key))")
    return conn

def _hash_password(password: str, salt: str) -> str:
    # Use SHA-256 for demonstration (not as secure as bcrypt)
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

def register_user(username: str, password: str) -> bool:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if cur.fetchone():
        return False
    salt = secrets.token_hex(16)
    pw_hash = _hash_password(password, salt)
    cur.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)", (username, pw_hash, salt))
    conn.commit()
    return True

def authenticate_user(username: str, password: str) -> bool:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if not row:
        return False
    pw_hash, salt = row
    return pw_hash == _hash_password(password, salt)

def save_user_data(username: str, key: str, value: str):
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO user_data (username, key, value) VALUES (?, ?, ?)", (username, key, value))
    conn.commit()

def load_user_data(username: str, key: str) -> Optional[str]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT value FROM user_data WHERE username = ? AND key = ?", (username, key))
    row = cur.fetchone()
    return row[0] if row else None