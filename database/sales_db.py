import sqlite3
import logging
from contextlib import contextmanager
from customers_db import update_customer_wallet
from inventory_db import get_product_by_id

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

def create_sales_table():
    """
    Creates the Sales table in the database if it does not already exist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Sales (
                    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    total_price REAL NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                    FOREIGN KEY (product_id) REFERENCES Inventory(product_id)
                );
            ''')
            conn.commit()
            logger.info('Sales table created successfully.')
    except Exception as e:
        logger.error(f"Failed to create sales table: {e}")

def insert_sale(sale):
    """
    Inserts a new sale into the Sales table.

    :param sale: A dictionary containing the sale details.
    :type sale: dict
    :return: The inserted sale details or an empty dictionary on failure.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()

            # Fetch customer balance and product stock
            cur.execute('SELECT wallet_balance, username FROM Customers WHERE customer_id = ?', (sale['customer_id'],))
            customer = cur.fetchone()
            if not customer:
                logger.error("Customer not found")
                return {}

            cur.execute('SELECT stock_count, price FROM Inventory WHERE product_id = ?', (sale['product_id'],))
            product = cur.fetchone()
            if not product:
                logger.error("Product not found")
                return {}

            # Validate balance and stock
            if customer['wallet_balance'] < sale['total_price']:
                logger.error("Insufficient balance")
                return {}
            if product['stock_count'] < sale['quantity']:
                logger.error("Insufficient stock")
                return {}

            # Process sale
            cur.execute('''
                INSERT INTO Sales (customer_id, product_id, quantity, total_price)
                VALUES (?, ?, ?, ?)
            ''', (sale['customer_id'], sale['product_id'], sale['quantity'], sale['total_price']))
            conn.commit()

            # Update wallet and stock
            update_customer_wallet(customer['username'], -sale['total_price'])
            cur.execute('UPDATE Inventory SET stock_count = stock_count - ? WHERE product_id = ?', 
                        (sale['quantity'], sale['product_id']))
            conn.commit()

            return get_sale_by_id(cur.lastrowid)
    except Exception as e:
        logger.error(f"Failed to insert sale: {e}")
        return {}

def get_sale_by_id(sale_id):
    """
    Retrieves a sale by its ID.

    :param sale_id: ID of the sale to retrieve.
    :type sale_id: int
    :return: The sale details or an empty dictionary if not found.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Sales WHERE sale_id = ?", (sale_id,))
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception as e:
        logger.error(f"Failed to fetch sale by ID: {e}")
        return {}

def display_goods():
    """
    Retrieves all goods available for sale (name and price).

    :return: A list of goods.
    :rtype: list
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT name, price FROM Inventory")
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch goods: {e}")
        return []

def display_good_detail(product_id):
    """
    Retrieves detailed information about a specific product.

    :param product_id: ID of the product to retrieve.
    :type product_id: int
    :return: The product details or an empty dictionary if not found.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Inventory WHERE product_id = ?", (product_id,))
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception as e:
        logger.error(f"Failed to fetch product details: {e}")
        return {}

def display_customer_sales(customer_id):
    """
    Retrieves all sales made by a specific customer.

    :param customer_id: ID of the customer.
    :type customer_id: int
    :return: A list of sales made by the customer.
    :rtype: list
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Sales WHERE customer_id = ?", (customer_id,))
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch customer sales: {e}")
        return []
