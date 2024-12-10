import cProfile
import pstats
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

DATABASE_SERVICE_URL = "http://database:5000"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InventoryService")


def profile_function(func):
    """
    A decorator to profile the execution time of a function using cProfile.
    """
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()

        # Save stats to a stream
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Print top 10 cumulative time functions

        logger.info("Profiling results:\n%s", stream.getvalue())
        return result
    return wrapper

@app.route('/health', methods=['GET'])
@profile_function
@profile
def health_check():
    logger.info("Health check requested")
    return jsonify({"status": "healthy"}), 200

@app.route('/customers/register', methods=['POST'])
@profile_function
@profile
def api_register_customer():
    """
    Register a new customer with full details.

    Request Body:
        dict: JSON containing customer details (e.g., name, username, wallet balance).

    Returns:
        Response: JSON confirmation of the customer registration.
    """
    customer = request.get_json()
    try:
        logger.info("Registering customer: %s", customer)
        response = requests.post(f"{DATABASE_SERVICE_URL}/customers/register", json=customer)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error registering customer: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers/delete/<customer_id>', methods=['DELETE'])
@profile_function
@profile
def api_delete_customer(customer_id):
    """
    Delete a customer by their ID.

    Args:
        customer_id (str): ID of the customer to delete.

    Returns:
        Response: JSON confirmation of the customer deletion.
    """
    try:
        logger.info("Deleting customer with ID: %s", customer_id)
        response = requests.delete(f"{DATABASE_SERVICE_URL}/customers/delete/{customer_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error deleting customer: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers/update', methods=['PUT'])
def api_update_customer():
    """
    Update customer details (partial or full updates).

    Request Body:
        dict: JSON containing updated customer details.

    Returns:
        Response: JSON confirmation of the update.
    """
    customer = request.get_json()
    try:
        logger.info("Updating customer: %s", customer)
        response = requests.put(f"{DATABASE_SERVICE_URL}/customers/update", json=customer)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error updating customer: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers', methods=['GET'])
@profile_function
@profile
def api_get_customers():
    """
    Get a list of all customers.

    Returns:
        Response: JSON list of customers.
    """
    try:
        logger.info("Fetching all customers")
        response = requests.get(f"{DATABASE_SERVICE_URL}/customers")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching customers: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers/username/<username>', methods=['GET'])
@profile_function
@profile
def api_get_customer_by_username(username):
    """
    Get details of a specific customer by username.

    Args:
        username (str): The username of the customer to fetch.

    Returns:
        Response: JSON with customer details.
    """
    try:
        logger.info("Fetching customer by username: %s", username)
        response = requests.get(f"{DATABASE_SERVICE_URL}/customers/username/{username}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching customer by username: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers/id/<customer_id>', methods=['GET'])
def api_get_customer_by_id(customer_id):
    """
    Get details of a specific customer by their ID.

    Args:
        customer_id (str): The customer ID to fetch.

    Returns:
        Response: JSON with customer details.
    """
    try:
        logger.info("Fetching customer by ID: %s", customer_id)
        response = requests.get(f"{DATABASE_SERVICE_URL}/customers/id/{customer_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching customer by ID: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers/<username>/charge/<amount>', methods=['POST'])
@profile_function
@profile
def api_charge_customer(username, amount):
    """
    Add funds to the customer's wallet.

    Args:
        username (str): The username of the customer.
        amount (int): The amount to add to the wallet.

    Returns:
        Response: JSON with wallet update confirmation.
    """
    try:
        logger.info("Charging customer %s with amount: %s", username, amount)
        response = requests.post(f"{DATABASE_SERVICE_URL}/customers/{username}/charge/{amount}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error charging customer: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers/<username>/deduct/<amount>', methods=['POST'])
@profile_function
@profile
def api_deduct_customer(username, amount):
    """
    Deduct funds from the customer's wallet.

    Args:
        username (str): The username of the customer.
        amount (int): The amount to deduct from the wallet.

    Returns:
        Response: JSON with wallet update confirmation.
    """
    try:
        logger.info("Deducting amount %s from customer %s wallet", amount, username)
        response = requests.post(f"{DATABASE_SERVICE_URL}/customers/{username}/deduct/{amount}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error deducting from customer wallet: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    """
    Starts the Customer Service on port 5001.
    """
    logger.info("Starting Customer Service")
    app.run(host="0.0.0.0", port=5001, debug=True)
