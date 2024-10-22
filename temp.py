import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import hashlib
import os
from PIL import Image, ImageTk
import datetime

class UserType:
    ADMIN = "admin"
    DB = "db"
    USER = "user"
    MANAGEMENT = "management"

class POSSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced POS System")
        self.master.geometry("1024x768")

        # Initialize database
        self.conn = sqlite3.connect('pos_database.db')
        self.cursor = self.conn.cursor()
        
        # Create necessary tables if they don't exist
        self.create_tables()

        # Set up login screen
        self.setup_login()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                            (id INTEGER PRIMARY KEY, name TEXT, price REAL, category TEXT, 
                             quantity INTEGER, icon_path TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales
                            (id INTEGER PRIMARY KEY, date TEXT, total REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, user_type TEXT)''')
        self.conn.commit()

    def setup_login(self):
        self.login_frame = ttk.Frame(self.master)
        self.login_frame.pack(padx=20, pady=20)

        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="e", pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=1, pady=10)
        ttk.Button(self.login_frame, text="Create Account", command=self.show_create_account).grid(row=3, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = self.cursor.fetchone()

        if user:
            self.current_user = {"id": user[0], "username": user[1], "user_type": user[3]}
            self.login_frame.destroy()
            self.setup_gui()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show_create_account(self):
        self.create_account_window = tk.Toplevel(self.master)
        self.create_account_window.title("Create Account")
        self.create_account_window.geometry("300x250")

        ttk.Label(self.create_account_window, text="Username:").pack(pady=5)
        self.new_username_entry = ttk.Entry(self.create_account_window)
        self.new_username_entry.pack(pady=5)

        ttk.Label(self.create_account_window, text="Password:").pack(pady=5)
        self.new_password_entry = ttk.Entry(self.create_account_window, show="*")
        self.new_password_entry.pack(pady=5)

        ttk.Label(self.create_account_window, text="User Type:").pack(pady=5)
        self.user_type_var = tk.StringVar()
        user_type_combo = ttk.Combobox(self.create_account_window, textvariable=self.user_type_var)
        user_type_combo['values'] = [UserType.ADMIN, UserType.DB, UserType.USER, UserType.MANAGEMENT]
        user_type_combo.pack(pady=5)

        ttk.Label(self.create_account_window, text="Secret Key:").pack(pady=5)
        self.secret_key_entry = ttk.Entry(self.create_account_window, show="*")
        self.secret_key_entry.pack(pady=5)

        ttk.Button(self.create_account_window, text="Create Account", command=self.create_account).pack(pady=10)
    def setup_add_tab(self):
        self.add_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_frame, text="Add Item")

        # Item Name
        ttk.Label(self.add_frame, text="Item Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.new_item_name = ttk.Entry(self.add_frame)
        self.new_item_name.grid(row=0, column=1, padx=10, pady=5)

        # Quantity
        ttk.Label(self.add_frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.new_item_quantity = ttk.Entry(self.add_frame)
        self.new_item_quantity.grid(row=1, column=1, padx=10, pady=5)

        # Price Each
        ttk.Label(self.add_frame, text="Price Each:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.new_item_price = ttk.Entry(self.add_frame)
        self.new_item_price.grid(row=2, column=1, padx=10, pady=5)

        # Category
        ttk.Label(self.add_frame, text="Category:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.new_item_category = ttk.Entry(self.add_frame)
        self.new_item_category.grid(row=3, column=1, padx=10, pady=5)

        # Icon
        ttk.Label(self.add_frame, text="Icon:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.icon_button = ttk.Button(self.add_frame, text="Select Icon", command=self.select_icon)
        self.icon_button.grid(row=4, column=1, padx=10, pady=5)

        self.icon_label = ttk.Label(self.add_frame, text="No icon selected")
        self.icon_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Add Item Button
        ttk.Button(self.add_frame, text="Add Item", command=self.add_new_item).grid(row=6, column=0, columnspan=2, padx=10, pady=20)

        self.icon_path = None


    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        user_type = self.user_type_var.get()
        secret_key = self.secret_key_entry.get()

        if not all([username, password, user_type, secret_key]):
            messagebox.showerror("Error", "All fields are required")
            return

        if secret_key != "665171":
            messagebox.showerror("Error", "Invalid secret key")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            self.cursor.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",
                                (username, hashed_password, user_type))
            self.conn.commit()
            messagebox.showinfo("Success", "Account created successfully")
            self.create_account_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    
            

    def setup_sales_tab(self):
        # Product list
        self.product_frame = ttk.Frame(self.sales_frame)
        self.product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.product_tree = ttk.Treeview(self.product_frame, columns=('Name', 'Price', 'Quantity'))
        self.product_tree.heading('Name', text='Name')
        self.product_tree.heading('Price', text='Price')
        self.product_tree.heading('Quantity', text='Quantity')
        self.product_tree.pack(fill=tk.BOTH, expand=True)

        self.load_products()

        # Cart
        self.cart_frame = ttk.Frame(self.sales_frame)
        self.cart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.cart_tree = ttk.Treeview(self.cart_frame, columns=('Name', 'Price', 'Quantity'))
        self.cart_tree.heading('Name', text='Name')
        self.cart_tree.heading('Price', text='Price')
        self.cart_tree.heading('Quantity', text='Quantity')
        self.cart_tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        ttk.Button(self.cart_frame, text="Add to Cart", command=self.add_to_cart).pack(pady=5)
        ttk.Button(self.cart_frame, text="Remove from Cart", command=self.remove_from_cart).pack(pady=5)
        ttk.Button(self.cart_frame, text="Process Sale", command=self.process_sale).pack(pady=5)

        # Total
        self.total_var = tk.StringVar()
        self.total_var.set("Total: $0.00")
        ttk.Label(self.cart_frame, textvariable=self.total_var).pack(pady=10)

    def setup_inventory_tab(self):
        ttk.Button(self.inventory_frame, text="Add New Item", command=self.show_add_item_window).pack(pady=10)

        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=('Name', 'Price', 'Category', 'Quantity'))
        self.inventory_tree.heading('Name', text='Name')
        self.inventory_tree.heading('Price', text='Price')
        self.inventory_tree.heading('Category', text='Category')
        self.inventory_tree.heading('Quantity', text='Quantity')
        self.inventory_tree.pack(fill=tk.BOTH, expand=True)

        self.load_inventory()

    def setup_reports_tab(self):
        ttk.Button(self.reports_frame, text="Generate Sales Report", command=self.generate_sales_report).pack(pady=10)
        ttk.Button(self.reports_frame, text="Generate Inventory Report", command=self.generate_inventory_report).pack(pady=10)

    def setup_user_management_tab(self):
        ttk.Button(self.user_management_frame, text="Add User", command=self.show_create_account).pack(pady=5)
        ttk.Button(self.user_management_frame, text="Edit User", command=self.edit_user).pack(pady=5)
        ttk.Button(self.user_management_frame, text="Delete User", command=self.delete_user).pack(pady=5)

    def show_add_item_window(self):
        self.add_item_window = tk.Toplevel(self.master)
        self.add_item_window.title("Add New Item")
        self.add_item_window.geometry("400x500")

        ttk.Label(self.add_item_window, text="Item Name:").pack(pady=5)
        self.item_name_entry = ttk.Entry(self.add_item_window)
        self.item_name_entry.pack(pady=5)

        ttk.Label(self.add_item_window, text="Price Each:").pack(pady=5)
        self.item_price_entry = ttk.Entry(self.add_item_window)
        self.item_price_entry.pack(pady=5)

        ttk.Label(self.add_item_window, text="Category:").pack(pady=5)
        self.item_category_entry = ttk.Entry(self.add_item_window)
        self.item_category_entry.pack(pady=5)

        ttk.Label(self.add_item_window, text="Quantity:").pack(pady=5)
        self.item_quantity_entry = ttk.Entry(self.add_item_window)
        self.item_quantity_entry.pack(pady=5)

        ttk.Button(self.add_item_window, text="Select Icon", command=self.select_icon).pack(pady=10)

        self.icon_label = ttk.Label(self.add_item_window, text="No icon selected")
        self.icon_label.pack(pady=5)

        ttk.Button(self.add_item_window, text="Add Item", command=self.add_item).pack(pady=10)

        self.icon_path = None

    def select_icon(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            self.icon_path = file_path
            self.icon_label.config(text=f"Icon selected: {os.path.basename(file_path)}")

    def add_item(self):
        name = self.item_name_entry.get()
        price = self.item_price_entry.get()
        category = self.item_category_entry.get()
        quantity = self.item_quantity_entry.get()

        if not all([name, price, category, quantity]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and Quantity must be an integer")
            return

        if self.icon_path:
            icon_dir = "item_icons"
            if not os.path.exists(icon_dir):
                os.makedirs(icon_dir)
            new_icon_path = os.path.join(icon_dir, f"{name}_{os.path.basename(self.icon_path)}")
            Image.open(self.icon_path).save(new_icon_path)
        else:
            new_icon_path = None

        try:
            self.cursor.execute("""
                INSERT INTO products (name, price, category, quantity, icon_path)
                VALUES (?, ?, ?, ?, ?)
            """, (name, price, category, quantity, new_icon_path))
            self.conn.commit()
            messagebox.showinfo("Success", "Item added successfully")
            self.add_item_window.destroy()
            self.load_inventory()
            self.load_products()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    def add_new_item(self):
        name = self.new_item_name.get()
        quantity = self.new_item_quantity.get()
        price = self.new_item_price.get()
        category = self.new_item_category.get()

        if not all([name, quantity, price, category]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and Quantity must be an integer")
            return

        if self.icon_path:
            icon_dir = "item_icons"
            if not os.path.exists(icon_dir):
                os.makedirs(icon_dir)
            new_icon_path = os.path.join(icon_dir, f"{name}_{os.path.basename(self.icon_path)}")
            Image.open(self.icon_path).save(new_icon_path)
        else:
            new_icon_path = None

        try:
            self.cursor.execute("""
                INSERT INTO products (name, price, category, quantity, icon_path)
                VALUES (?, ?, ?, ?, ?)
            """, (name, price, category, quantity, new_icon_path))
            self.conn.commit()
            messagebox.showinfo("Success", "Item added successfully")
            
            # Clear the fields after successful addition
            self.new_item_name.delete(0, tk.END)
            self.new_item_quantity.delete(0, tk.END)
            self.new_item_price.delete(0, tk.END)
            self.new_item_category.delete(0, tk.END)
            self.icon_path = None
            self.icon_label.config(text="No icon selected")

            self.load_inventory()
            self.load_products()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    def load_products(self):
        self.product_tree.delete(*self.product_tree.get_children())
        self.cursor.execute("SELECT name, price, quantity FROM products")
        for product in self.cursor.fetchall():
            self.product_tree.insert('', 'end', values=product)
    def select_icon(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            self.icon_path = file_path
            self.icon_label.config(text=f"Icon selected: {os.path.basename(file_path)}")
    def load_inventory(self):
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        self.cursor.execute("SELECT name, price, category, quantity FROM products")
        for product in self.cursor.fetchall():
            self.inventory_tree.insert('', 'end', values=product)

    def add_to_cart(self):
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to add to cart")
            return

        item = self.product_tree.item(selected_item)['values']
        self.cart_tree.insert('', 'end', values=item)
        self.update_total()

    def remove_from_cart(self):
        selected_item = self.cart_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to remove from cart")
            return

        self.cart_tree.delete(selected_item)
        self.update_total()

    def update_total(self):
        total = sum(float(self.cart_tree.item(item)['values'][1]) for item in self.cart_tree.get_children())
        self.total_var.set(f"Total: ${total:.2f}")

    def process_sale(self):
        if not self.cart_tree.get_children():
            messagebox.showerror("Error", "Cart is empty")
            return

        total = sum(float(self.cart_tree.item(item)['values'][1]) * int(self.cart_tree.item(item)['values'][2]) 
                    for item in self.cart_tree.get_children())
        
        # Record the sale
        sale_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO sales (date, total) VALUES (?, ?)", (sale_date, total))
        sale_id = self.cursor.lastrowid

        # Update inventory
        for item in self.cart_tree.get_children():
            name, price, quantity = self.cart_tree.item(item)['values']
            self.cursor.execute("UPDATE products SET quantity = quantity - ? WHERE name = ?", (quantity, name))

        self.conn.commit()

        # Clear the cart
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        self.update_total()
        self.load_products()
        self.load_inventory()

        messagebox.showinfo("Success", f"Sale processed successfully. Total: ${total:.2f}")

    def generate_sales_report(self):
        self.cursor.execute("SELECT date, total FROM sales ORDER BY date DESC")
        sales = self.cursor.fetchall()

        report = "Sales Report\n\n"
        report += "Date\t\t\tTotal\n"
        report += "-" * 40 + "\n"

        for sale in sales:
            report += f"{sale[0]}\t${sale[1]:.2f}\n"

        total_sales = sum(sale[1] for sale in sales)
        report += f"\nTotal Sales: ${total_sales:.2f}"

        self.show_report(report, "Sales Report")

    def generate_inventory_report(self):
        self.cursor.execute("SELECT name, price, category, quantity FROM products ORDER BY category, name")
        products = self.cursor.fetchall()

        report = "Inventory Report\n\n"
        report += "Name\t\tPrice\tCategory\tQuantity\n"
        report += "-" * 60 + "\n"

        for product in products:
            report += f"{product[0][:15]:<15}\t${product[1]:<7.2f}{product[2]:<15}\t{product[3]}\n"

        total_value = sum(product[1] * product[3] for product in products)
        report += f"\nTotal Inventory Value: ${total_value:.2f}"

        self.show_report(report, "Inventory Report")

    def show_report(self, report, title):
        report_window = tk.Toplevel(self.master)
        report_window.title(title)
        report_window.geometry("600x400")

        report_text = tk.Text(report_window, wrap=tk.WORD)
        report_text.pack(fill=tk.BOTH, expand=True)

        report_text.insert(tk.END, report)
        report_text.config(state=tk.DISABLED)

    def edit_user(self):
        # This is a placeholder for user editing functionality
        messagebox.showinfo("Info", "User editing functionality not implemented yet")

    def delete_user(self):
        # This is a placeholder for user deletion functionality
        messagebox.showinfo("Info", "User deletion functionality not implemented yet")
    
    def setup_gui(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        if self.current_user["user_type"] in [UserType.ADMIN, UserType.USER]:
            self.sales_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.sales_frame, text="Sales")
            self.setup_sales_tab()

        if self.current_user["user_type"] in [UserType.ADMIN, UserType.DB]:
            self.inventory_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.inventory_frame, text="Inventory")
            self.setup_inventory_tab()
            self.setup_add_tab()

        if self.current_user["user_type"] in [UserType.ADMIN, UserType.MANAGEMENT]:
            self.reports_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.reports_frame, text="Reports")
            self.setup_reports_tab()

        if self.current_user["user_type"] == UserType.ADMIN:
            self.user_management_frame = ttk.Frame(self.notebook)
            self.notebook.add(self.user_management_frame, text="User Management")
            self.setup_user_management_tab()
            self.setup_inventory_tab()
            self.setup_add_tab()
            self.setup_reports_tab()
            self.setup_sales_tab()
if __name__ == "__main__": 
    root = tk.Tk()
    pos = POSSystem(root)
    root.mainloop()