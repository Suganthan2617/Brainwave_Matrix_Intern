from db import connect_db

def add_product(name, quantity, price):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", 
                (name, quantity, price))
    conn.commit()

def get_low_stock(threshold=5):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE quantity <= ?", (threshold,))
    return cur.fetchall()

def update_product(pid, name, quantity, price):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?", 
                (name, quantity, price, pid))
    conn.commit()

def delete_product(pid):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
