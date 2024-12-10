from auth_db import create_users_table
from customers_db import create_customers_table
from inventory_db import create_inventory_table
from reviews_db import create_reviews_table, create_moderation_table
from sales_db import create_sales_table
from wishlist_db import create_wishlist_table

def initialize_database():
    create_customers_table()
    create_inventory_table()
    create_reviews_table()
    create_moderation_table()
    create_sales_table()
    create_wishlist_table()
    create_users_table()

from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = 'ecommerce.db'

def connect_to_db():
    return sqlite3.connect(DATABASE)

@app.route('/customers', methods=['POST'])
def api_insert_customer():
    data = request.get_json()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Customers (first_name, last_name, username, password, age, address, gender, marital_status, wallet_balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['first_name'], data['last_name'], data['username'], data['password'], data['age'], data['address'], data['gender'], data['marital_status'], data['wallet_balance']))
        conn.commit()
        return jsonify({"message": "Customer added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def api_delete_customer(customer_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM Customers WHERE customer_id = ?", (customer_id,))
        conn.commit()
        return jsonify({"message": "Customer deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/customers/<int:customer_id>', methods=['GET'])
def api_get_customer_by_id(customer_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Customers WHERE customer_id = ?", (customer_id,))
        row = cur.fetchone()
        if row:
            customer = {
                "customer_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "username": row[3],
                "password": row[4],
                "age": row[5],
                "address": row[6],
                "gender": row[7],
                "marital_status": row[8],
                "wallet_balance": row[9],
            }
            return jsonify(customer), 200
        return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/customers', methods=['GET'])
def api_get_customers():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Customers")
        rows = cur.fetchall()
        customers = [
            {
                "customer_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "username": row[3],
                "password": row[4],
                "age": row[5],
                "address": row[6],
                "gender": row[7],
                "marital_status": row[8],
                "wallet_balance": row[9],
            }
            for row in rows
        ]
        return jsonify(customers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/customers/<username>', methods=['GET'])
def api_get_customer_by_username(username):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Customers WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            customer = {
                "customer_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "username": row[3],
                "password": row[4],
                "age": row[5],
                "address": row[6],
                "gender": row[7],
                "marital_status": row[8],
                "wallet_balance": row[9],
            }
            return jsonify(customer), 200
        return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/customers/<username>/wallet', methods=['POST'])
def api_update_customer_wallet(username):
    data = request.get_json()
    amount = data.get("amount", 0)
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT wallet_balance FROM Customers WHERE username = ?", (username,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Customer not found"}), 404
        new_balance = row[0] + amount
        cur.execute("UPDATE Customers SET wallet_balance = ? WHERE username = ?", (new_balance, username))
        conn.commit()
        return jsonify({"message": "Wallet updated successfully!", "new_balance": new_balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/inventory', methods=['POST'])
def api_insert_product():
    data = request.get_json()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Inventory (name, category, price, description, stock_count)
            VALUES (?, ?, ?, ?, ?)
        """, (data['name'], data['category'], data['price'], data['description'], data['stock_count']))
        conn.commit()
        return jsonify({"message": "Product added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/inventory/<int:product_id>', methods=['PUT'])
def api_update_product(product_id):
    data = request.get_json()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Inventory
            SET name = ?, category = ?, price = ?, description = ?, stock_count = ?
            WHERE product_id = ?
        """, (data['name'], data['category'], data['price'], data['description'], data['stock_count'], product_id))
        conn.commit()
        return jsonify({"message": "Product updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/inventory/<int:product_id>', methods=['DELETE'])
def api_delete_product(product_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM Inventory WHERE product_id = ?", (product_id,))
        conn.commit()
        return jsonify({"message": "Product deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/inventory', methods=['GET'])
def api_get_products():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Inventory")
        rows = cur.fetchall()
        products = [
            {
                "product_id": row[0],
                "name": row[1],
                "category": row[2],
                "price": row[3],
                "description": row[4],
                "stock_count": row[5],
            }
            for row in rows
        ]
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/inventory/<int:product_id>', methods=['GET'])
def api_get_product_by_id(product_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Inventory WHERE product_id = ?", (product_id,))
        row = cur.fetchone()
        if row:
            product = {
                "product_id": row[0],
                "name": row[1],
                "category": row[2],
                "price": row[3],
                "description": row[4],
                "stock_count": row[5],
            }
            return jsonify(product), 200
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/inventory/categories/<string:category>', methods=['GET'])
def api_get_products_by_category(category):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Inventory WHERE category = ?", (category,))
        rows = cur.fetchall()
        products = [
            {
                "product_id": row[0],
                "name": row[1],
                "category": row[2],
                "price": row[3],
                "description": row[4],
                "stock_count": row[5],
            }
            for row in rows
        ]
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/sales/products', methods=['GET'])
def api_get_products_for_sale():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT name, price FROM Inventory")
        rows = cur.fetchall()
        products = [{"name": row[0], "price": row[1]} for row in rows]
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/sales/products/<int:product_id>', methods=['GET'])
def api_get_product_detail(product_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Inventory WHERE product_id = ?", (product_id,))
        row = cur.fetchone()
        if row:
            product = {
                "product_id": row[0],
                "name": row[1],
                "category": row[2],
                "price": row[3],
                "description": row[4],
                "stock_count": row[5],
            }
            return jsonify(product), 200
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/sales', methods=['POST'])
def api_insert_sale():
    data = request.get_json()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Sales (customer_id, product_id, quantity, total_price)
            VALUES (?, ?, ?, ?)
        """, (data['customer_id'], data['product_id'], data['quantity'], data['total_price']))
        conn.commit()
        return jsonify({"message": "Sale processed successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/sales/history/<int:customer_id>', methods=['GET'])
def api_get_customer_sales_history(customer_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Sales WHERE customer_id = ?", (customer_id,))
        rows = cur.fetchall()
        sales = [
            {
                "sale_id": row[0],
                "customer_id": row[1],
                "product_id": row[2],
                "quantity": row[3],
                "total_price": row[4],
                "order_date": row[5],
            }
            for row in rows
        ]
        return jsonify(sales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/reviews', methods=['POST'])
def api_submit_review():
    data = request.get_json()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Moderate (customer_id, product_id, rating, comment)
            VALUES (?, ?, ?, ?)
        """, (data['customer_id'], data['product_id'], data['rating'], data['comment']))
        conn.commit()
        return jsonify({"message": "Review submitted for moderation."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/reviews/<int:review_id>', methods=['PUT'])
def api_update_review(review_id):
    data = request.get_json()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Reviews
            SET customer_id = ?, product_id = ?, rating = ?, comment = ?
            WHERE review_id = ?
        """, (data['customer_id'], data['product_id'], data['rating'], data['comment'], review_id))
        conn.commit()
        return jsonify({"message": "Review updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def api_delete_review(review_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM Reviews WHERE review_id = ?", (review_id,))
        conn.commit()
        return jsonify({"message": "Review deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/reviews/product/<int:product_id>', methods=['GET'])
def api_get_product_reviews(product_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Reviews WHERE product_id = ?", (product_id,))
        rows = cur.fetchall()
        reviews = [
            {
                "review_id": row[0],
                "customer_id": row[1],
                "product_id": row[2],
                "rating": row[3],
                "comment": row[4],
                "created_at": row[5],
                "updated_at": row[6],
            }
            for row in rows
        ]
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/reviews/customer/<int:customer_id>', methods=['GET'])
def api_get_customer_reviews(customer_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Reviews WHERE customer_id = ?", (customer_id,))
        rows = cur.fetchall()
        reviews = [
            {
                "review_id": row[0],
                "customer_id": row[1],
                "product_id": row[2],
                "rating": row[3],
                "comment": row[4],
                "created_at": row[5],
                "updated_at": row[6],
            }
            for row in rows
        ]
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/reviews/approve', methods=['POST'])
def api_approve_review():
    data = request.get_json()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Reviews (customer_id, product_id, rating, comment)
            VALUES (?, ?, ?, ?)
        """, (data['customer_id'], data['product_id'], data['rating'], data['comment']))
        conn.commit()
        return jsonify({"message": "Review approved and added."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/reviews/reject/<int:review_id>', methods=['DELETE'])
def api_reject_review(review_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM Moderate WHERE review_id = ?", (review_id,))
        conn.commit()
        return jsonify({"message": "Review rejected and removed."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/wishlist', methods=['POST'])
def api_add_to_wishlist():
    data = request.get_json()
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Wishes (customer_id, product_id, quantity)
            VALUES (?, ?, ?)
        """, (data['customer_id'], data['product_id'], data['quantity']))
        conn.commit()
        return jsonify({"message": "Wish added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/wishlist/<int:customer_id>/<int:product_id>', methods=['DELETE'])
def api_remove_from_wishlist(customer_id, product_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Wishes WHERE customer_id = ? AND product_id = ?
        """, (customer_id, product_id))
        conn.commit()
        return jsonify({"message": "Wish removed successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/wishlist/<int:customer_id>', methods=['GET'])
def api_get_wishlist(customer_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM Wishes WHERE customer_id = ?
        """, (customer_id,))
        rows = cur.fetchall()
        wishes = [
            {
                "wish_id": row[0],
                "customer_id": row[1],
                "product_id": row[2],
                "quantity": row[3],
                "added_at": row[4],
            }
            for row in rows
        ]
        return jsonify(wishes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/wishlist/notify/<int:customer_id>', methods=['POST'])
def api_notify_abandoned_wishlist(customer_id):
    try:
        conn = connect_to_db()
        cur = conn.cursor()

        # Notify about items added more than 7 days ago
        cur.execute("""
            SELECT * FROM Wishes
            WHERE customer_id = ? AND added_at < datetime('now', '-7 days')
        """, (customer_id,))
        rows = cur.fetchall()

        if not rows:
            return jsonify({"message": "No abandoned wishlist items found."}), 200

        notifications = []
        for row in rows:
            notifications.append(
                f"Customer {row[1]}, your wish for product {row[2]} (quantity: {row[3]}) "
                f"added on {row[4]} is still in your wishlist. Consider purchasing!"
            )

        return jsonify({"notifications": notifications}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/auth/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"message": "All fields are required!"}), 400

    if role not in ['admin', 'customer']:
        return jsonify({"message": "Role must be either 'admin' or 'customer'"}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    try:
        conn = connect_to_db()
        conn.execute("""
            INSERT INTO Users (username, password, role) VALUES (?, ?, ?)
        """, (username, hashed_password, role))
        conn.commit()
        return jsonify({"message": f"User {username} created successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "User already exists!"}), 400
    finally:
        conn.close()

@app.route('/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE username = ?", (username,))
        user = cur.fetchone()

        if not user or not check_password_hash(user['password'], password):
            return jsonify({"message": "Invalid credentials!"}), 401

        return jsonify({"message": f"Welcome {username}!", "role": user['role']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/auth/logout', methods=['POST'])
def api_logout():
    return jsonify({"message": "Logout functionality is client-side in this setup."}), 200


if __name__ == '__main__':
    initialize_database()
    print("Database initialized successfully!")
    app.run(host='0.0.0.0', port=5000)
