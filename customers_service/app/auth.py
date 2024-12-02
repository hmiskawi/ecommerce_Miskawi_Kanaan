from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from database.auth_db import connect_to_db, create_users_table
import logging
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/signup', methods=['POST'])
def signup():
    """
    Registers a new user.

    :return: JSON response indicating success or failure.
    :rtype: flask.Response
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"message": "All fields are required!"}), 400

    if role not in ['admin', 'customer']:
        return jsonify({"message": "Role must be 'admin' or 'customer'"}), 400

    hashed_password = generate_password_hash(password, method='sha256')

    try:
        with connect_to_db() as conn:
            conn.execute('INSERT INTO Users (username, password, role) VALUES (?, ?, ?)', (username, hashed_password, role))
            conn.commit()
        logger.info(f"User {username} registered successfully.")
        return jsonify({"message": f"User {username} created successfully!"}), 201
    except sqlite3.IntegrityError:
        logger.error("Username already exists.")
        return jsonify({"message": "User already exists!"}), 400

@app.route('/login', methods=['POST'])
def login():
    """
    Logs in an existing user.

    :return: JSON response with login status and user role.
    :rtype: flask.Response
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    with connect_to_db() as conn:
        conn.row_factory = sqlite3.Row
        user = conn.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid credentials!"}), 401

    session['user_id'] = user['id']
    session['role'] = user['role']

    logger.info(f"User {username} logged in successfully.")
    return jsonify({"message": f"Welcome {username}!", "role": user['role']}), 200

@app.route('/logout', methods=['POST'])
def logout():
    """
    Logs out the current user.

    :return: JSON response indicating logout status.
    :rtype: flask.Response
    """
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('role', None)
        logger.info("User logged out successfully.")
        return jsonify({"message": "Logged out successfully!"}), 200

    logger.warning("No user was logged in.")
    return jsonify({"message": "No user is logged in!"}), 400

if __name__ == '__main__':
    create_users_table()
    app.run(debug=True)
