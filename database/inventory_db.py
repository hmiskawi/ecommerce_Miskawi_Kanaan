import sqlite3

def connect_to_db():
    conn = sqlite3.connect('ecommerce.db')
    return conn

def create_inventory_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
            product_id INTEGER PRIMARY KEY NOT NULL,
            name VARCHAR(255) NOT NULL,
            category ENUM('Food', 'Clothes', 'Accessories', 'Electronics') NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            description TEXT,
            stock_count INT DEFAULT 0
            );
        ''')
        conn.commit()
        print('Inventory table created successfully.')
    except:
        print('An error occured while creating the inventory table.')
    finally:
        conn.close()

def insert_product(product):
    inserted_product = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Inventory (name, category, price, description, stock_count) VALUES (?, ?, ?, ?, ?)", (product['name'], product['category'], product['price'], product['description'], product['stock_count']) )
        conn.commit()
        inserted_product = get_product_by_id(cur.lastrowid)
    except:
        print("Insertion failed.")
        conn().rollback()
    finally:
        conn.close()
    return inserted_product

def update_product(product):
    updated_product = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Inventory SET name = ?, category = ?, price = ?, description = ?, stock_count = ? WHERE product_id = ?", (product['name'], product['category'], product['price'], product['description'], product['stock_count'], product['product_id']))
        conn.commit()
        updated_product = get_product_by_id(product["product_id"])
    except:
        print("Update failed.")
        conn.rollback()
        updated_product = {}
    finally:
        conn.close() 
    return updated_product

def delete_product(product_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Inventory WHERE product_id = ?",(product_id,))
        conn.commit()
        message["status"] = "Product deleted successfully"
    except:
        print("Deletion failed.")
        conn.rollback()
        message["status"] = "Cannot delete product"
    finally:
        conn.close()
    return message

def get_products():
    products = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Inventory")
        rows = cur.fetchall()
        for i in rows:
            product = {}
            product["product_id"] = i["product_id"]
            product["name"] = i["name"]
            product["category"] = i["category"]
            product["price"] = i["price"]
            product["description"] = i["description"]
            product["stock_count"] = i["stock_count"]
            products.append(product)
    except:
        print("Failed to fetch all products.")
        products = []
    return products

def get_product_by_id(product_id):
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

def get_category_products(category):
    products = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Inventory WHERE category = ?", (category,))
        rows = cur.fetchall()
        for i in rows:
            product = {}
            product["product_id"] = i["product_id"]
            product["name"] = i["name"]
            product["category"] = i["category"]
            product["price"] = i["price"]
            product["description"] = i["description"]
            product["stock_count"] = i["stock_count"]
            products.append(product)
    except:
        print("Failed to fetch all products.")
        products = []
    return products