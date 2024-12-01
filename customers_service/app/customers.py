from flask import Flask, request, jsonify
from flask_cors import CORS
from shared.decorators import login_required, admin_required
from database.customers_db import (
    create_customers_table,
    insert_customer,
    update_customer,
    delete_customer,
    get_customers,
    get_customer_by_id,
    get_customer_by_username,
    update_customer_wallet,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from marshmallow import Schema, fields, ValidationError
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.getenv('CORS_ORIGIN', '*')}})

# Rate limiter
limiter = Limiter(app, key_func=get_remote_address)

# Marshmallow schema for validation
class CustomerSchema(Schema):
    """
    Schema for validating customer data.

    Attributes:
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        username (str): The username of the customer.
        password (str): The password of the customer.
        age (int): The age of the customer.
        address (str): The address of the customer.
        gender (str): The gender of the customer ('M', 'F', 'O').
        marital_status (str): The marital status of the customer ('Single', 'Married', 'Other').
        wallet_balance (float): The wallet balance of the customer.
    """
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    age = fields.Int(required=True)
    address = fields.Str(required=False)
    gender = fields.Str(validate=lambda g: g in ['M', 'F', 'O'], required=False)
    marital_status = fields.Str(validate=lambda ms: ms in ['Single', 'Married', 'Other'], required=False)
    wallet_balance = fields.Float(required=False, default=0.0)

customer_schema = CustomerSchema()

@app.route('/customers/register', methods=['POST'])
@login_required
@limiter.limit("5 per minute")
def api_register_customer():
    """
    Registers a new customer.

    :return: JSON response with the newly created customer details or an error message.
    :rtype: flask.Response
    """
    try:
        customer = customer_schema.load(request.get_json())
        response = insert_customer(customer)
        return jsonify(response), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/customers/delete/<customer_id>', methods=['DELETE'])
@admin_required
@limiter.limit("2 per minute")
def api_delete_customer(customer_id):
    """
    Deletes a customer by their ID.

    :param customer_id: ID of the customer to be deleted.
    :type customer_id: int
    :return: JSON response indicating the result of the deletion.
    :rtype: flask.Response
    """
    try:
        return jsonify(delete_customer(customer_id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/customers/update', methods=['PUT'])
@login_required
def api_update_customer():
    """
    Updates a customer's details.

    :return: JSON response with the updated customer details or an error message.
    :rtype: flask.Response
    """
    try:
        customer = customer_schema.load(request.get_json(), partial=True)
        return jsonify(update_customer(customer)), 200
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/customers', methods=['GET'])
@admin_required
def api_get_customers():
    """
    Retrieves a list of all customers.

    :return: JSON response with the list of customers or an error message.
    :rtype: flask.Response
    """
    try:
        return jsonify(get_customers()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/customers/username/<username>', methods=['GET'])
@admin_required
def api_get_customer_by_username(username):
    """
    Retrieves a customer's details by username.

    :param username: The username of the customer.
    :type username: str
    :return: JSON response with the customer's details or an error message.
    :rtype: flask.Response
    """
    try:
        return jsonify(get_customer_by_username(username)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/customers/<username>/<operation>/<amount>', methods=['POST'])
@admin_required
def api_update_wallet(username, operation, amount):
    """
    Updates a customer's wallet balance.

    :param username: The username of the customer.
    :type username: str
    :param operation: The type of operation ('charge' or 'deduct').
    :type operation: str
    :param amount: The amount to be charged or deducted.
    :type amount: float
    :return: JSON response with the updated wallet balance or an error message.
    :rtype: flask.Response
    """
    try:
        amount = float(amount)
        if operation == "deduct":
            amount = -amount
        return jsonify(update_customer_wallet(username, amount)), 200
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    """
    Initializes the customers table and starts the Flask application.
    """
    create_customers_table()
    app.run(debug=True)
