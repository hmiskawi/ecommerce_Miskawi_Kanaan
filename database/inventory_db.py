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

def create_inventory_table():
    """
    Creates the Inventory table in the database if it does not already exist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Inventory (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL CHECK(category IN ('Food', 'Clothes', 'Accessories', 'Electronics')),
                    price REAL NOT NULL,
                    description TEXT,
                    stock_count INTEGER DEFAULT 0
                );
            ''')
            conn.commit()
            logger.info('Inventory table created successfully.')
    except Exception as e:
        logger.error(f"Failed to create inventory table: {e}")

def insert_product(product):
    """
    Inserts a new product into the Inventory table.

    :param product: A dictionary containing the product details.
    :type product: dict
    :return: The inserted product details.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO Inventory (name, category, price, description, stock_count)
                VALUES (?, ?, ?, ?, ?)
            ''', (product['name'], product['category'], product['price'], product['description'], product['stock_count']))
            conn.commit()
            return get_product_by_id(cur.lastrowid)
    except Exception as e:
        logger.error(f"Insertion failed: {e}")
        return {"error": "Failed to insert product"}

def update_product(product):
    """
    Updates a product's details in the Inventory table.

    :param product: A dictionary containing the updated product details.
    :type product: dict
    :return: The updated product details.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE Inventory
                SET name = ?, category = ?, price = ?, description = ?, stock_count = ?
                WHERE product_id = ?
            ''', (product['name'], product['category'], product['price'], product['description'],
                  product['stock_count'], product['product_id']))
            conn.commit()
            return get_product_by_id(product["product_id"])
    except Exception as e:
        logger.error(f"Update failed: {e}")
        return {"error": "Failed to update product"}

def delete_product(product_id):
    """
    Deletes a product from the Inventory table.

    :param product_id: ID of the product to delete.
    :type product_id: int
    :return: A message indicating the success or failure of the operation.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM Inventory WHERE product_id = ?", (product_id,))
            conn.commit()
            return {"status": "Product deleted successfully"}
    except Exception as e:
        logger.error(f"Deletion failed: {e}")
        return {"error": "Failed to delete product"}

def get_products():
    """
    Retrieves all products from the Inventory table.

    :return: A list of products.
    :rtype: list
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Inventory")
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch products: {e}")
        return []

def get_product_by_id(product_id):
    """
    Retrieves a product by its ID.

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
        logger.error(f"Failed to fetch product by ID: {e}")
        return {}

def get_category_products(category):
    """
    Retrieves all products within a specific category.

    :param category: The category of the products.
    :type category: str
    :return: A list of products in the category.
    :rtype: list
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Inventory WHERE category = ?", (category,))
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Failed to fetch category products: {e}")
        return []
