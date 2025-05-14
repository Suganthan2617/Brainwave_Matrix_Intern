from db import connect_db
import datetime

def record_sale(product_id, quantity_sold):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO sales (product_id, quantity_sold, sale_date) VALUES (?, ?, ?)", 
                (product_id, quantity_sold, datetime.datetime.now().isoformat()))
    cur.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", 
                (quantity_sold, product_id))
    conn.commit()

def get_sales_summary():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""SELECT p.name, SUM(s.quantity_sold) as total_sold 
                   FROM sales s JOIN products p ON s.product_id = p.id 
                   GROUP BY s.product_id""")
    return cur.fetchall()
