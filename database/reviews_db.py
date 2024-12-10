import sqlite3

def connect_to_db():
    conn = sqlite3.connect('ecommerce.db')
    return conn

def create_reviews_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Reviews (
            review_id INTEGER PRIMARY KEY NOT NULL,
            customer_id INT NOT NULL,
            product_id INT NOT NULL,
            rating INT CHECK (rating BETWEEN 1 AND 5),
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES Inventory(product_id)
        );
        ''')
        conn.commit()
        print('Reviews table created successfully.')
    except:
        print('An error occured while creating the reviews table.')
    finally:
        conn.close()

def create_moderation_table():
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Moderate (
            review_id INTEGER PRIMARY KEY NOT NULL,
            customer_id INT NOT NULL,
            product_id INT NOT NULL,
            rating INT CHECK (rating BETWEEN 1 AND 5),
            comment TEXT,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES Inventory(product_id)
        );
        ''')
        conn.commit()
        print('Moderation table created successfully.')
    except:
        print('An error occured while creating the moderation table.')
    finally:
        conn.close()


def approve_review(review):
    inserted_review = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Reviews (customer_id, product_id, rating, comment) VALUES (?, ?, ?, ?)", (review['customer_id'], review['product_id'], review['rating'], review['comment']))
        conn.commit()
        inserted_review = get_review_by_id(cur.lastrowid)
    except:
        print("Insertion failed.")
        conn().rollback()
    finally:
        conn.close()
    return inserted_review

def reject_review(review):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Moderate WHERE review_id = ?",(review['review_id'],))
        conn.commit()
        message["status"] = "Unposted review deleted successfully"
    except:
        print("Deletion failed.")
        conn.rollback()
        message["status"] = "Cannot delete unposted review"
    finally:
        conn.close()
    return message

def update_review(review):
    updated_review = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Reviews SET customer_id = ?, product_id = ?, rating = ?, comment = ? WHERE review_id = ?", (review['customer_id'], review['product_id'], review['rating'], review['comment'], review['review_id']))
        conn.commit()
        updated_review = get_review_by_id(review["review_id"])
    except:
        print("Update failed.")
        conn.rollback()
        updated_review = {}
    finally:
        conn.close() 
    return updated_review

def delete_review(review_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Reviews WHERE review_id = ?",(review_id,))
        conn.commit()
        message["status"] = "Review deleted successfully"
    except:
        print("Deletion failed.")
        conn.rollback()
        message["status"] = "Cannot delete review"
    finally:
        conn.close()
    return message

def get_product_reviews(product_id):
    reviews = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Reviews WHERE product_id = ?", (product_id,))
        rows = cur.fetchall()
        for i in rows:
            review = {}
            review["customer_id"] = i["customer_id"]
            review["product_id"] = i["product_id"]
            review["rating"] = i["rating"]
            review["comment"] = i["comment"]
            review["review_id"] = i["review_id"]
            reviews.append(review)
    except:
        print(f"Failed to fetch all reviews for product: {product_id}.")
        reviews = []
    return reviews

def get_customer_reviews(customer_id):
    reviews = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Reviews WHERE customer_id = ?", (customer_id,))
        rows = cur.fetchall()
        for i in rows:
            review = {}
            review["customer_id"] = i["customer_id"]
            review["product_id"] = i["product_id"]
            review["rating"] = i["rating"]
            review["comment"] = i["comment"]
            review["review_id"] = i["review_id"]
            reviews.append(review)
    except:
        print(f"Failed to fetch all reviews by customer: {customer_id}.")
        reviews = []
    return reviews

def get_review_by_id(review_id):
    review = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Reviews WHERE review_id = ?",(review_id,))
        row = cur.fetchone()
        review["review_id"] = row["review_id"]
        review["customer_id"] = row["customer_id"]
        review["product_id"] = row["product_id"]
        review["rating"] = row["rating"]
        review["comment"] = row["comment"]
    except:
        print(f"Failed to fetch review with id: {review_id}")
        review = {}
    return review

def get_moderate_by_id(review_id):
    review = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Moderate WHERE review_id = ?",(review_id,))
        row = cur.fetchone()
        review["review_id"] = row["review_id"]
        review["customer_id"] = row["customer_id"]
        review["product_id"] = row["product_id"]
        review["rating"] = row["rating"]
        review["comment"] = row["comment"]
    except:
        print(f"Failed to fetch unposted review with id: {review_id}")
        review = {}
    return review

def submit_review(review):
    submitted_review = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Moderate (customer_id, product_id, rating, comment) VALUES (?, ?, ?, ?)", (review['customer_id'], review['product_id'], review['rating'], review['comment']))
        conn.commit()
        submitted_review = get_moderate_by_id(cur.lastrowid)
    except:
        print("Insertion failed.")
        conn().rollback()
    finally:
        conn.close()
    return submitted_review
