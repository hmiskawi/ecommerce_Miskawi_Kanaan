import sqlite3

def connect_to_db():
    conn = sqlite3.connect('ecommerce.db')
    return conn

def create_customers_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            age INTEGER,
            address TEXT,
            gender ENUM('M', 'F', 'O'),
            marital_status ENUM('Single', 'Married', 'Other'),
            wallet_balance DECIMAL(10, 2) DEFAULT 0.0,
            );
        ''')
        conn.commit()
        print('Customers table created successfully.')
    except:
        print('An error occured while creating the customers table.')
    finally:
        conn.close()

def insert_customer(customer):
    inserted_customer = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Customers (first_name, last_name, username, password, age, address, gender, marital_status, wallet_balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (customer['first_name'], customer['last_name'], customer['username'], customer['password'], customer['age'], customer['address'], customer['gender'], customer['marital_status'], customer['wallet_balance']) )
        conn.commit()
        inserted_customer = get_customer_by_id(cur.lastrowid)
    except:
        print("Insertion failed.")
        conn().rollback()
    finally:
        conn.close()
    return inserted_customer

def update_customer(customer):
    updated_customer = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Customers SET first_name = ?, last_name = ?, username = ?, password=?, age = ?, address = ?, gender = ?, marital_status = ?, wallet_balance = ? WHERE customer_id=?", (customer['first_name'], customer['last_name'], customer['username'], customer['password'], customer['age'], customer['address'], customer['gender'], customer['marital_status'], customer['wallet_balance'], customer["user_id"],))
        conn.commit()
        updated_customer = get_customer_by_id(customer["customer_id"])
    except:
        print("Update failed.")
        conn.rollback()
        updated_customer = {}
    finally:
        conn.close() 
    return updated_customer

def delete_customer(customer_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Customers WHERE customer_id = ?",(customer_id,))
        conn.commit()
        message["status"] = "Customer deleted successfully"
    except:
        print("Deletion failed.")
        conn.rollback()
        message["status"] = "Cannot delete customer"
    finally:
        conn.close()
    return message

def get_customers():
    customers = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Customers")
        rows = cur.fetchall()
        for i in rows:
            customer = {}
            customer["customer_id"] = i["customer_id"]
            customer["first_name"] = i["first_name"]
            customer["last_name"] = i["last_name"]
            customer["username"] = i["username"]
            customer["password"] = i["password"]
            customer["age"] = i["age"]
            customer["address"] = i["address"]
            customer["gender"] = i["gender"]
            customer["marital_status"] = i["marital_status"]
            customer["wallet_balance"] = i["wallet_balance"]
            customers.append(customer)
    except:
        print("Failed to fetch all customers.")
        customers = []
    return customers

def get_customer_by_id(customer_id):
    customer = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Customers WHERE customer_id = ?",(customer_id,))
        row = cur.fetchone()
        customer["customer_id"] = ["customer_id"]
        customer["first_name"] = ["first_name"]
        customer["last_name"] = ["last_name"]
        customer["username"] = ["username"]
        customer["password"] = ["password"]
        customer["age"] = ["age"]
        customer["address"] = ["address"]
        customer["gender"] = ["gender"]
        customer["marital_status"] = ["marital_status"]
        customer["wallet_balance"] = ["wallet_balance"]
    except:
        print(f"Failed to fetch customer with id: {customer_id}")
        customer = {}
    return customer

def get_customer_by_username(customer_username):
    customer = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Customers WHERE username = ?",(customer_username,))
        row = cur.fetchone()
        customer["customer_id"] = ["customer_id"]
        customer["first_name"] = ["first_name"]
        customer["last_name"] = ["last_name"]
        customer["username"] = ["username"]
        customer["password"] = ["password"]
        customer["age"] = ["age"]
        customer["address"] = ["address"]
        customer["gender"] = ["gender"]
        customer["marital_status"] = ["marital_status"]
        customer["wallet_balance"] = ["wallet_balance"]
    except:
        print(f"Failed to fetch customer with username: {customer_username}")
        customer = {}
    return customer

def update_customer_wallet(username, amount):
    updated_customer = {}
    customer = get_customer_by_username(username)
    balance = customer["wallet_balance"] + amount
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Customers SET wallet_balance = ? WHERE username = ?", (balance, username))
        conn.commit()
        updated_customer = get_customer_by_id(customer["customer_id"])
    except:
        print("Wallet update failed.")
        conn.rollback()
        updated_customer = {}
    finally:
        conn.close()
    return updated_customer