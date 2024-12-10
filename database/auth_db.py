import sqlite3

def connect_to_db():
    conn = sqlite3.connect('ecommerce.db')
    return conn

def create_users_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
            );
        ''')
        conn.commit()
        print('Users table created successfully.')
    except:
        print('An error occured while creating the users table.')
    finally:
        conn.close()