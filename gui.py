import tkinter as tk
from tkinter import messagebox, ttk

from auth import login_user, register_user
from inventory import add_product, update_product, delete_product, get_low_stock
from sales import get_sales_summary, record_sale
from db import connect_db


def start_gui():
    root = tk.Tk()
    root.title("Inventory Login")
    root.geometry("300x250")

    tk.Label(root, text="Username").pack(pady=5)
    username = tk.Entry(root)
    username.pack()

    tk.Label(root, text="Password").pack(pady=5)
    password = tk.Entry(root, show="*")
    password.pack()

    def handle_login():
        if login_user(username.get(), password.get()):
            root.destroy()
            open_dashboard()
        else:
            tk.Label(root, text="❌ Login failed").pack()

    def handle_register():
        if register_user(username.get(), password.get()):
            tk.Label(root, text="✅ Registered successfully").pack()
        else:
            tk.Label(root, text="❌ Registration failed").pack()

    tk.Button(root, text="Login", command=handle_login).pack(pady=10)
    tk.Button(root, text="Register", command=handle_register).pack()

    root.mainloop()


def open_dashboard():
    dash = tk.Tk()
    dash.title("Inventory Dashboard")
    dash.geometry("900x550")

    # --- Input Fields ---
    tk.Label(dash, text="Product Name").grid(row=0, column=0)
    name_entry = tk.Entry(dash)
    name_entry.grid(row=0, column=1)

    tk.Label(dash, text="Quantity").grid(row=1, column=0)
    qty_entry = tk.Entry(dash)
    qty_entry.grid(row=1, column=1)

    tk.Label(dash, text="Price").grid(row=2, column=0)
    price_entry = tk.Entry(dash)
    price_entry.grid(row=2, column=1)

    # --- Sale Quantity ---
    tk.Label(dash, text="Sale Qty").grid(row=3, column=0)
    sale_qty_entry = tk.Entry(dash)
    sale_qty_entry.grid(row=3, column=1)

    # --- Product Table ---
    tree = ttk.Treeview(dash, columns=("ID", "Name", "Qty", "Price"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Qty", text="Quantity")
    tree.heading("Price", text="Price")
    tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    def load_products():
        for row in tree.get_children():
            tree.delete(row)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products")
        for row in cur.fetchall():
            tree.insert("", "end", values=row)

    load_products()

    def on_tree_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, 'values')
            name_entry.delete(0, tk.END)
            qty_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            sale_qty_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            qty_entry.insert(0, values[2])
            price_entry.insert(0, values[3])

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # --- Add Product ---
    def add_product_btn():
        name = name_entry.get()
        try:
            qty = int(qty_entry.get())
            price = float(price_entry.get())
            add_product(name, qty, price)
            messagebox.showinfo("Success", "Product added!")
            load_products()
        except:
            messagebox.showerror("Error", "Invalid input!")

    # --- Update Product ---
    def update_product_btn():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a product to update.")
            return
        values = tree.item(selected, 'values')
        product_id = values[0]
        try:
            name = name_entry.get()
            qty = int(qty_entry.get())
            price = float(price_entry.get())
            update_product(product_id, name, qty, price)
            messagebox.showinfo("Success", "Product updated!")
            load_products()
        except:
            messagebox.showerror("Error", "Invalid input.")

    # --- Delete Product ---
    def delete_product_btn():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a product to delete.")
            return
        values = tree.item(selected, 'values')
        product_id = values[0]
        confirm = messagebox.askyesno("Confirm", f"Delete product '{values[1]}'?")
        if confirm:
            delete_product(product_id)
            messagebox.showinfo("Deleted", "Product deleted.")
            load_products()

    # --- Record Sale ---
    def record_sale_btn():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a product to record sale.")
            return
        values = tree.item(selected, 'values')
        product_id = values[0]
        product_name = values[1]
        available_qty = int(values[2])

        try:
            sale_qty = int(sale_qty_entry.get())
            if sale_qty <= 0:
                raise ValueError
            if sale_qty > available_qty:
                messagebox.showerror("Error", "Not enough stock.")
                return

            # Record the sale
            record_sale(product_id, product_name, sale_qty)

            # Update inventory
            update_product(product_id, product_name, available_qty - sale_qty, float(values[3]))

            messagebox.showinfo("Success", "Sale recorded and stock updated.")
            sale_qty_entry.delete(0, tk.END)
            load_products()
        except:
            messagebox.showerror("Error", "Enter a valid sale quantity.")

    # --- Low Stock ---
    def show_low_stock():
        items = get_low_stock()
        if not items:
            messagebox.showinfo("Low Stock", "All items are sufficiently stocked.")
        else:
            msg = "\n".join([f"{x[1]} (Qty: {x[2]})" for x in items])
            messagebox.showwarning("Low Stock Items", msg)

    # --- Sales Summary ---
    def show_sales_summary():
        data = get_sales_summary()
        if not data:
            messagebox.showinfo("Sales", "No sales data.")
        else:
            msg = "\n".join([f"{x[0]} - Sold: {x[1]}" for x in data])
            messagebox.showinfo("Sales Summary", msg)

    # --- Buttons ---
    tk.Button(dash, text="Add Product", command=add_product_btn).grid(row=4, column=0, pady=10)
    tk.Button(dash, text="Update Product", command=update_product_btn).grid(row=4, column=1)
    tk.Button(dash, text="Delete Product", command=delete_product_btn).grid(row=4, column=2)
    tk.Button(dash, text="Record Sale", command=record_sale_btn).grid(row=4, column=3)

    tk.Button(dash, text="Show Low Stock", command=show_low_stock).grid(row=6, column=0)
    tk.Button(dash, text="Show Sales Summary", command=show_sales_summary).grid(row=6, column=1)

    dash.mainloop()
