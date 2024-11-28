import sqlite3
from flask import Flask, request, jsonify, session
from flask_cors import CORS 
from werkzeug.security import generate_password_hash, check_password_hash
from database.auth_db import connect_to_db, create_users_table

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Sign-up Endpoint
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"message": "All fields are required!"}), 400

    if role not in ['admin', 'customer']:
        return jsonify({"message": "Role must be either 'admin' or 'customer'"}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    try:
        with connect_to_db() as conn:
            conn.execute('INSERT INTO Users (username, password, role) VALUES (?, ?, ?)',(username, hashed_password, role))
            conn.commit()
        return jsonify({"message": f"User {username} created successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "User already exists!"}), 400

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    with connect_to_db() as conn:
        user = conn.execute('SELECT * FROM Users WHERE username = ?',(username,)).fetchone()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials!"}), 401

    session['user_id'] = user['id']
    session['role'] = user['role']

    return jsonify({"message": f"Welcome {username}!", "role": user['role']}), 200

# Logout Endpoint
@app.route('/logout', methods=['POST'])
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('role', None)
        return jsonify({"message": "Logged out successfully!"}), 200

    return jsonify({"message": "No user is logged in!"}), 400

if __name__ == '__main__':
    create_users_table()
    app.run(debug=True)
