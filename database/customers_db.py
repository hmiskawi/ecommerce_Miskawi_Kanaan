import sqlite3
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def connect_to_db():
    """
    Establishes a connection to the SQLite database.

    :return: SQLite connection object.
    :rtype: sqlite3.Connection
    """
    return sqlite3.connect('ecommerce.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

@contextmanager
def get_db_connection():
    """
    Provides a context-managed database connection.

    :yield: SQLite connection object.
    :rtype: sqlite3.Connection
    """
    conn = connect_to_db()
    try:
        yield conn
    finally:
        conn.close()

def create_customers_table():
    """
    Creates the Customers table in the database if it does not already exist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Customers (
                    customer_id INTEGER PRIMARY KEY NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    age INTEGER,
                    address TEXT,
                    gender TEXT CHECK(gender IN ('M', 'F', 'O')),
                    marital_status TEXT CHECK(marital_status IN ('Single', 'Married', 'Other')),
                    wallet_balance REAL DEFAULT 0.0
                );
            ''')
            conn.commit()
            print('Customers table created successfully.')
    except Exception as e:
        logger.error(f"Failed to create customers table: {e}")

def insert_customer(customer):
    """
    Inserts a new customer into the Customers table.

    :param customer: A dictionary containing the customer's details.
    :type customer: dict
    :return: The inserted customer's details.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO Customers 
                (first_name, last_name, username, password, age, address, gender, marital_status, wallet_balance) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer['first_name'], customer['last_name'], customer['username'], customer['password'], 
                customer['age'], customer.get('address'), customer.get('gender'), 
                customer.get('marital_status'), customer.get('wallet_balance', 0.0)
            ))
            conn.commit()
            return get_customer_by_id(cur.lastrowid)
    except Exception as e:
        logger.error(f"Insertion failed: {e}")
        return {"error": "Failed to insert customer"}

def update_customer(customer):
    """
    Updates a customer's details in the database.

    :param customer: A dictionary containing the updated details of the customer.
    :type customer: dict
    :return: The updated customer's details.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE Customers 
                SET first_name = ?, last_name = ?, username = ?, password = ?, 
                    age = ?, address = ?, gender = ?, marital_status = ?, wallet_balance = ? 
                WHERE customer_id = ?
            ''', (
                customer['first_name'], customer['last_name'], customer['username'], customer['password'], 
                customer['age'], customer.get('address'), customer.get('gender'), 
                customer.get('marital_status'), customer.get('wallet_balance', 0.0), customer["customer_id"]
            ))
            conn.commit()
            return get_customer_by_id(customer["customer_id"])
    except Exception as e:
        logger.error(f"Update failed: {e}")
        return {"error": "Failed to update customer"}

def delete_customer(customer_id):
    """
    Deletes a customer from the database.

    :param customer_id: ID of the customer to be deleted.
    :type customer_id: int
    :return: A message indicating the success or failure of the operation.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM Customers WHERE customer_id = ?", (customer_id,))
            conn.commit()
            return {"status": "Customer deleted successfully"}
    except Exception as e:
        logger.error(f"Deletion failed: {e}")
        return {"error": "Cannot delete customer"}

def get_customers():
    """
    Retrieves all customers from the database.

    :return: A list of customers.
    :rtype: list
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Customers")
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch customers: {e}")
        return []

def get_customer_by_id(customer_id):
    """
    Retrieves a customer by their ID.

    :param customer_id: ID of the customer to retrieve.
    :type customer_id: int
    :return: The customer's details or an empty dictionary if not found.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Customers WHERE customer_id = ?", (customer_id,))
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception as e:
        logger.error(f"Failed to fetch customer by ID: {e}")
        return {}

def get_customer_by_username(username):
    """
    Retrieves a customer by their username.

    :param username: Username of the customer to retrieve.
    :type username: str
    :return: The customer's details or an empty dictionary if not found.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Customers WHERE username = ?", (username,))
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception as e:
        logger.error(f"Failed to fetch customer by username: {e}")
        return {}

def update_customer_wallet(username, amount):
    """
    Updates a customer's wallet balance.

    :param username: The username of the customer.
    :type username: str
    :param amount: The amount to adjust in the wallet (positive to add, negative to deduct).
    :type amount: float
    :return: The updated customer's details or an error message.
    :rtype: dict
    """
    try:
        customer = get_customer_by_username(username)
        if not customer:
            return {"error": "Customer not found"}
        new_balance = customer["wallet_balance"] + amount
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE Customers SET wallet_balance = ? WHERE username = ?", (new_balance, username))
            conn.commit()
            return get_customer_by_id(customer["customer_id"])
    except Exception as e:
        logger.error(f"Wallet update failed: {e}")
        return {"error": "Failed to update wallet"}
