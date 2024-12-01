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

def create_users_table():
    """
    Creates the Users table in the database if it does not already exist.
    """
    try:
        with get_db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('admin', 'customer'))
                );
            ''')
            conn.commit()
            logger.info('Users table created successfully.')
    except Exception as e:
        logger.error(f"Failed to create users table: {e}")
