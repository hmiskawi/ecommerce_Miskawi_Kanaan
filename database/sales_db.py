import sqlite3
from customers_db import update_customer_wallet
from inventory_db import get_product_by_id

def connect_to_db():
    conn = sqlite3.connect('ecommerce.db')
    return conn

def create_sales_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Sales (
                sale_id INTEGER PRIMARY KEY NOT NULL,
                customer_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL,
                total_price DECIMAL(10, 2),
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                FOREIGN KEY (product_id) REFERENCES Inventory(product_id)
            );
        ''')
        conn.commit()
        print('Sales table created successfully.')
    except:
        print('An error occured while creating the sales table.')
    finally:
        conn.close()

def product_sold(product_id):
    updated_product = {}
    try:
        product = get_product_by_id(product_id)
        conn = connect_to_db()
        cur = conn.cursor()
        new_stock_count = product["stock_count"] - 1
        cur.execute("UPDATE Inventory SET stock_count = ? WHERE product_id = ?", (new_stock_count, product['product_id']))
        conn.commit()
        updated_product = get_product_by_id(product["product_id"])
    except:
        print("Update failed.")
        conn.rollback()
        updated_product = {}
    finally:
        conn.close() 
    return updated_product

def insert_sale(sale):
    inserted_sale = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT wallet_balance, username FROM Customers WHERE customer_id = ?", (sale["customer_id"]))
        cur.commit()
        row = cur.fetchone()
        customer_balance = row["wallet_balance"]
        customer_username = row["username"]
        cur.execute("SELECT quantity FROM Inventory WHERE product_id = ?", (sale["product_id"]))
        cur.commit()
        row = cur.fetchone()
        quantity = row["quantity"]
        if customer_balance >= sale["total_price"] and quantity >= sale["quantity"]:
            cur.execute("INSERT INTO Sales (customer_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?)", (sale['customer_id'], sale['product_id'], sale['quantity'], sale['total_price']) )
            conn.commit()
            amount = sale["total_price"]
            update_customer_wallet(customer_username, -amount)
            product_sold(sale["product_id"])
            inserted_sale = get_sale_by_id(cur.lastrowid)
        else:
            inserted_sale = {}
            print("Customer does not have enough balance, or the product is out of stock.")
    except:
        print("Insertion failed.")
        conn().rollback()
    finally:
        conn.close()
    return inserted_sale

def update_sale(sale):
    updated_sale = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Sales SET customer_id = ?, product_id = ?, quantity = ?, total_price = ?, order_date = ? WHERE sale_id = ?", (sale['customer_id'], sale['product_id'], sale['quantity'], sale['total_price'], sale['order_date'], sale['sale_id']))
        conn.commit()
        updated_sale = get_sale_by_id(sale["sale_id"])
    except:
        print("Update failed.")
        conn.rollback()
        updated_sale = {}
    finally:
        conn.close() 
    return updated_sale

def delete_sale(sale_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Sales WHERE sale_id = ?",(sale_id,))
        conn.commit()
        message["status"] = "Sale deleted successfully"
    except:
        print("Deletion failed.")
        conn.rollback()
        message["status"] = "Cannot delete sale"
    finally:
        conn.close()
    return message

def get_sales():
    sales = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Sales")
        rows = cur.fetchall()
        for i in rows:
            sale = {}
            sale["sale_id"] = i["sale_id"]
            sale["customer_id"] = i["customer_id"]
            sale["product_id"] = i["product_id"]
            sale["quantity"] = i["quantity"]
            sale["total_price"] = i["total_price"]
            sale["order_date"] = i["order_date"]
            sales.append(sale)
    except:
        print("Failed to fetch all sales.")
        sales = []
    return sales

def get_sale_by_id(sale_id):
    sale = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Sales WHERE sale_id = ?",(sale_id,))
        row = cur.fetchone()
        sale["sale_id"] = row["sale_id"]
        sale["customer_id"] = row["customer_id"]
        sale["product_id"] = row["product_id"]
        sale["quantity"] = row["quantity"]
        sale["total_price"] = row["total_price"]
        sale["order_date"] = row["order_date"]
    except:
        print(f"Failed to fetch sale with id: {sale_id}")
        sale = {}
    return sale

def display_goods():
    products = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Inventory")
        rows = cur.fetchall()
        for i in rows:
            product = {}
            product["name"] = i["name"]
            product["price"] = i["price"]
            products.append(product)
    except:
        print("Failed to fetch all products.")
        products = []
    return products

def display_good_detail(product_id):
    product = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Inventory WHERE product_id = ?",(product_id,))
        row = cur.fetchone()
        product["product_id"] = row["product_id"]
        product["name"] = row["name"]
        product["category"] = row["category"]
        product["price"] = row["price"]
        product["description"] = row["description"]
        product["stock_count"] = row["stock_count"]
    except:
        print(f"Failed to fetch product with id: {product_id}")
        product = {}
    return product

def display_customer_sales(customer_id):
    sales = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Sales WHERE customer_id = ?", (customer_id))
        rows = cur.fetchall()
        for i in rows:
            sale = {}
            sale["sale_id"] = i["sale_id"]
            sale["customer_id"] = i["customer_id"]
            sale["product_id"] = i["product_id"]
            sale["quantity"] = i["quantity"]
            sale["total_price"] = i["total_price"]
            sale["order_date"] = i["order_date"]
            sales.append(sale)
    except:
        print(f"Failed to fetch all sales of customer: {customer_id}.")
        sales = []
    return sales