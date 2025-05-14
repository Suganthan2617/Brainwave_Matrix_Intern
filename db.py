import sqlite3

def connect_db():
    conn = sqlite3.connect("inventory.db")
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    quantity INTEGER,
                    price REAL)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY,
                    product_id INTEGER,
                    quantity_sold INTEGER,
                    sale_date TEXT)""")

    conn.commit()
    return conn
