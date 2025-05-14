import hashlib
from db import connect_db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                    (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", 
                (username, hash_password(password)))
    return cur.fetchone() is not None
