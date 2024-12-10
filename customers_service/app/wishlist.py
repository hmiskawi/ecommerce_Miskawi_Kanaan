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

@app.route('/customers/wishlist/add', methods=['POST'])
@profile_function
@profile
def api_add_wish():
    """
    Add a product to the customer’s wishlist.

    Request Body:
        dict: JSON containing customer_id and product_id.

    Returns:
        Response: JSON confirmation of the wish being added.
    """
    wish = request.get_json()
    try:
        logger.info("Adding wish: %s", wish)
        response = requests.post(f"{DATABASE_SERVICE_URL}/customers/wishlist/add", json=wish)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error adding wish: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers/wishlist/remove/<customer_id>/<product_id>', methods=['DELETE'])
@profile_function
@profile
def api_remove_wish(customer_id, product_id):
    """
    Remove a product from the customer’s wishlist.

    Args:
        customer_id (str): The ID of the customer.
        product_id (str): The ID of the product to be removed.

    Returns:
        Response: JSON confirmation of the wish being removed.
    """
    try:
        logger.info("Removing wish for customer %s, product %s", customer_id, product_id)
        response = requests.delete(f"{DATABASE_SERVICE_URL}/customers/wishlist/remove/{customer_id}/{product_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error removing wish: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers/wishlist/<customer_id>', methods=['GET'])
def api_get_wishes(customer_id):
    """
    Get all wishlist items for a customer.

    Args:
        customer_id (str): The ID of the customer.

    Returns:
        Response: JSON list of products in the customer's wishlist.
    """
    try:
        logger.info("Fetching wishlist for customer: %s", customer_id)
        response = requests.get(f"{DATABASE_SERVICE_URL}/customers/wishlist/{customer_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching wishlist: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/customers/wishlist/notify/<customer_id>', methods=['POST'])
@profile_function
@profile
def api_notify_customer(customer_id):
    """
    Notify the customer about abandoned wishlist items.

    Args:
        customer_id (str): The ID of the customer to notify.

    Returns:
        Response: JSON confirmation of the notification.
    """
    try:
        logger.info("Notifying customer %s about abandoned wishlist items", customer_id)
        response = requests.post(f"{DATABASE_SERVICE_URL}/customers/wishlist/notify/{customer_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error notifying customer: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Wishlist Service")
    app.run(host="0.0.0.0", port=5001, debug=True)
