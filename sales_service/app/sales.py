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
def health_check():
    logger.info("Health check requested")
    return jsonify({"status": "healthy"}), 200

@app.route('/sales/products', methods=['GET'])
@profile
@profile_function
def api_get_products():
    """
    Get a list of all products available for sale (name, price).

    Returns:
        Response: JSON list of products with basic details (e.g., name, price).
    """
    try:
        logger.info("Fetching all products available for sale")
        response = requests.get(f"{DATABASE_SERVICE_URL}/sales/products")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching products: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/sales/products/<product_id>', methods=['GET'])
@profile
@profile_function
def api_get_product_detail(product_id):
    """
    Get detailed information about a specific product.

    Args:
        product_id (int): ID of the product to fetch details for.

    Returns:
        Response: JSON object with product details (e.g., name, price, stock).
    """
    try:
        logger.info("Fetching product details for ID: %s", product_id)
        response = requests.get(f"{DATABASE_SERVICE_URL}/sales/products/{product_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching product details: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/sales/purchase', methods=['POST'])
@profile
@profile_function
def api_process_sale():
    """
    Process a sale.

    Request:
        JSON object containing:
            - customer_id (int): ID of the customer making the purchase.
            - product_id (int): ID of the product being purchased.
            - quantity (int): Quantity of the product to purchase.
            - total_price (float): Total cost of the purchase.

    Returns:
        Response: JSON confirmation of the sale or error details.
    """
    sale = request.get_json()
    try:
        logger.info("Processing sale: %s", sale)
        response = requests.post(f"{DATABASE_SERVICE_URL}/sales/purchase", json=sale)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error processing sale: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/sales/history/<customer_id>', methods=['GET'])
@profile
@profile_function
def api_purchase_history(customer_id):
    """
    Get the purchase history for a specific customer.

    Args:
        customer_id (int): ID of the customer to fetch purchase history for.

    Returns:
        Response: JSON list of past purchases made by the customer.
    """
    try:
        logger.info("Fetching purchase history for customer ID: %s", customer_id)
        response = requests.get(f"{DATABASE_SERVICE_URL}/sales/history/{customer_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching purchase history: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    """
    Starts the Sales Service on port 5004.
    """
    logger.info("Starting Sales Service")
    app.run(host="0.0.0.0", port=5004, debug=True)
