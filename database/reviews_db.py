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

def create_reviews_table():
    """
    Creates the Reviews and Moderate tables in the database if they do not already exist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Reviews (
                    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                    FOREIGN KEY (product_id) REFERENCES Inventory(product_id)
                );
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Moderate (
                    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
                    FOREIGN KEY (product_id) REFERENCES Inventory(product_id)
                );
            ''')
            conn.commit()
            logger.info('Reviews and Moderation tables created successfully.')
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")

def submit_review(review):
    """
    Submits a review for moderation.

    :param review: A dictionary containing review details.
    :type review: dict
    :return: Submitted review details or an empty dictionary on failure.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO Moderate (customer_id, product_id, rating, comment)
                VALUES (?, ?, ?, ?)
            ''', (review['customer_id'], review['product_id'], review['rating'], review['comment']))
            conn.commit()
            return get_moderation_review_by_id(cur.lastrowid)
    except Exception as e:
        logger.error(f"Failed to submit review: {e}")
        return {}

def approve_review(review_id):
    """
    Approves a review and moves it from the Moderate table to the Reviews table.

    :param review_id: The ID of the review to approve.
    :type review_id: int
    :return: The approved review details or an empty dictionary on failure.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Moderate WHERE review_id = ?", (review_id,))
            review = cur.fetchone()
            if not review:
                logger.error(f"Review {review_id} not found for approval.")
                return {}

            cur.execute('''
                INSERT INTO Reviews (customer_id, product_id, rating, comment)
                VALUES (?, ?, ?, ?)
            ''', (review['customer_id'], review['product_id'], review['rating'], review['comment']))
            cur.execute("DELETE FROM Moderate WHERE review_id = ?", (review_id,))
            conn.commit()
            return get_review_by_id(cur.lastrowid)
    except Exception as e:
        logger.error(f"Failed to approve review: {e}")
        return {}

def reject_review(review_id):
    """
    Rejects a review and deletes it from the Moderate table.

    :param review_id: The ID of the review to reject.
    :type review_id: int
    :return: A status message indicating success or failure.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Moderate WHERE review_id = ?", (review_id,))
            conn.commit()
            return {"message": "Review rejected and deleted successfully."}
    except Exception as e:
        logger.error(f"Failed to reject review: {e}")
        return {"error": "Failed to reject review"}

def get_review_by_id(review_id):
    """
    Retrieves a review by its ID from the Reviews table.

    :param review_id: The ID of the review to retrieve.
    :type review_id: int
    :return: Review details or an empty dictionary if not found.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Reviews WHERE review_id = ?", (review_id,))
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception as e:
        logger.error(f"Failed to fetch review by ID: {e}")
        return {}

def get_moderation_review_by_id(review_id):
    """
    Retrieves a review by its ID from the Moderate table.

    :param review_id: The ID of the review to retrieve.
    :type review_id: int
    :return: Review details or an empty dictionary if not found.
    :rtype: dict
    """
    try:
        with get_db_connection() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM Moderate WHERE review_id = ?", (review_id,))
            row = cur.fetchone()
            return dict(row) if row else {}
    except Exception as e:
        logger.error(f"Failed to fetch moderated review by ID: {e}")
        return {}
