import sqlite3
from datetime import datetime, timedelta

def connect_to_db():
    conn = sqlite3.connect('ecommerce.db')
    return conn

def create_wishlist_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Wishes (
            wish_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES Inventory(product_id),
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            );
        ''')
        conn.commit()
        print('Wishlist table created successfully.')
    except:
        print('An error occured while creating the wishlist table.')
    finally:
        conn.close()

def insert_wish(wish):
    inserted_wish = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Wishes (customer_id, product_id, quantity) VALUES (?, ?, ?)", (wish['customer_id'], wish["product_id"], wish["quantity"]) )
        conn.commit()
        inserted_wish = get_wish_by_id(cur.lastrowid)
    except:
        print("Insertion failed.")
        conn().rollback()
    finally:
        conn.close()
    return inserted_wish

def delete_wish(customer_id, product_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Wishes WHERE customer_id = ? AND product_id = ?",(customer_id,product_id))
        conn.commit()
        message["status"] = "Wish removed from wishlist"
    except:
        print("Deletion failed.")
        conn.rollback()
        message["status"] = "Cannot remove wish"
    finally:
        conn.close()
    return message

def get_wishes(customer_id):
    wishes = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Wishes WHERE customer_id = ?", (customer_id))
        rows = cur.fetchall()
        for i in rows:
            wish = {}
            wish["wish_id"] = i["wish_id"]
            wish["customer_id"] = i["customer_id"]
            wish["product_id"] = i["product_id"]
            wish["quantity"] = i["quantity"]
            wish["added_at"] = i["added_at"]
            wishes.append(wish)
    except:
        print("Failed to fetch all wishes.")
        wishes = []
    return wishes

def get_wish_by_id(wish_id):
    wish = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Wishes WHERE wish_id = ?",(wish_id,))
        row = cur.fetchone()
        wish["wish_id"] = row["wish_id"]
        wish["customer_id"] = row["customer_id"]
        wish["product_id"] = row["product_id"]
        wish["quantity"] = row["quantity"]
        wish["added_at"] = row["added_at"]
    except:
        print(f"Failed to fetch wish with id: {wish_id}")
        product = {}
    return product


def notify_abandoned_wishlist(customer_id):
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        abandoned_threshold = datetime.now() - timedelta(days=7)

        cur.execute("SELECT * FROM Wishes WHERE customer_id = ? AND added_at < ?", (customer_id, abandoned_threshold))

        abandoned_wishes = cur.fetchall()

        if not abandoned_wishes:
            print(f"No abandoned wishlist items found for customer {customer_id}.")
            return

        for wish in abandoned_wishes:
            print(f"Notification: Customer {wish['customer_id']}, "
                  f"your wish for product {wish['product_id']} (quantity: {wish['quantity']}) "
                  f"added on {wish['added_at']} is still in your wishlist. Consider purchasing!")

    except Exception as e:
        print(f"Failed to process abandoned wishlist notification: {e}")
    finally:
        conn.close()