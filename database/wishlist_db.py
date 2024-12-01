import sqlite3
from datetime import datetime, timedelta
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

def create_wishlist_table():
    """
    Creates the Wishes table in the database if it does not already exist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Wishes (
                    wish_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES Inventory(product_id),
                    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
                );
            ''')
            conn.commit()
            print('Wishlist table created successfully.')
    except Exception as e:
        logger.error(f"Failed to create wishlist table: {e}")

def insert_wish(wish):
    """
    Inserts a new wish into the Wishes table.

    :param wish: A dictionary containing the wish details.
    :type wish: dict
    :return: The inserted wish details.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO Wishes (customer_id, product_id, quantity) 
                VALUES (?, ?, ?)
            ''', (wish['customer_id'], wish['product_id'], wish['quantity']))
            conn.commit()
            return get_wish_by_id(cur.lastrowid)
    except Exception as e:
        logger.error(f"Insertion failed: {e}")
        return {"error": "Failed to insert wish"}

def delete_wish(customer_id, product_id):
    """
    Deletes a wish from the Wishes table.

    :param customer_id: ID of the customer.
    :type customer_id: int
    :param product_id: ID of the product to delete.
    :type product_id: int
    :return: A message indicating the success or failure of the operation.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.execute('''
                DELETE FROM Wishes WHERE customer_id = ? AND product_id = ?
            ''', (customer_id, product_id))
            conn.commit()
            return {"status": "Wish removed from wishlist"}
    except Exception as e:
        logger.error(f"Deletion failed: {e}")
        return {"error": "Cannot remove wish"}

def get_wishes(customer_id):
    """
    Retrieves all wishlist items for a customer.

    :param customer_id: ID of the customer.
    :type customer_id: int
    :return: A list of wishlist items.
    :rtype: list
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('SELECT * FROM Wishes WHERE customer_id = ?', (customer_id,))
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch wishes: {e}")
        return []

def get_wish_by_id(wish_id):
    """
    Retrieves a wish by its ID.

    :param wish_id: ID of the wish to retrieve.
    :type wish_id: int
    :return: The wish details or an empty dictionary if not found.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('SELECT * FROM Wishes WHERE wish_id = ?', (wish_id,))
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception as e:
        logger.error(f"Failed to fetch wish by ID: {e}")
        return {}

def notify_abandoned_wishlist(customer_id):
    """
    Notifies a customer about abandoned wishlist items older than a threshold.

    :param customer_id: ID of the customer to notify.
    :type customer_id: int
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            abandoned_threshold = datetime.now() - timedelta(days=7)
            cur.execute('''
                SELECT * FROM Wishes WHERE customer_id = ? AND added_at < ?
            ''', (customer_id, abandoned_threshold))
            abandoned_wishes = cur.fetchall()

            if not abandoned_wishes:
                logger.info(f"No abandoned wishlist items found for customer {customer_id}.")
                return

            for wish in abandoned_wishes:
                logger.info(f"Notification: Customer {wish['customer_id']}, "
                            f"your wish for product {wish['product_id']} (quantity: {wish['quantity']}) "
                            f"added on {wish['added_at']} is still in your wishlist. Consider purchasing!")
    except Exception as e:
        logger.error(f"Failed to process abandoned wishlist notification: {e}")
