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
    def a_wrapper(*args, **kwargs):
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
    return a_wrapper

@app.route('/health', methods=['GET'])
@profile_function
@profile
def health_check():
    logger.info("Health check requested")
    return jsonify({"status": "healthy"}), 200

# Add @profile_function to other endpoints for profiling
@app.route('/inventory', methods=['GET'])
@profile_function
def api_get_products():
    try:
        logger.info("Fetching all products")
        response = requests.get(f"{DATABASE_SERVICE_URL}/inventory")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching products: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/inventory/add', methods=['POST'])
@profile_function
@profile
def api_add_product():
    """
    Add a new product to the inventory.

    Request:
        JSON object containing:
            - name (str): Product name.
            - category (str): Product category.
            - price (float): Product price.
            - description (str): Product description.
            - stock_count (int): Available stock count.

    Returns:
        Response: JSON with confirmation message or error details.
    """
    product = request.get_json()
    try:
        logger.info("Adding a new product: %s", product)
        response = requests.post(f"{DATABASE_SERVICE_URL}/inventory/add", json=product)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error adding product: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/inventory/update', methods=['PUT'])
def api_update_product():
    """
    Update details of an existing product.

    Request:
        JSON object containing:
            - product_id (int): ID of the product to update.
            - name (str): Updated product name.
            - category (str): Updated category.
            - price (float): Updated price.
            - description (str): Updated description.
            - stock_count (int): Updated stock count.

    Returns:
        Response: JSON with confirmation message or error details.
    """
    product = request.get_json()
    try:
        logger.info("Updating product: %s", product)
        response = requests.put(f"{DATABASE_SERVICE_URL}/inventory/update", json=product)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error updating product: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/inventory/delete/<product_id>', methods=['DELETE'])
def api_delete_product(product_id):
    """
    Delete a product from the inventory.

    Args:
        product_id (int): ID of the product to delete.

    Returns:
        Response: JSON with confirmation message or error details.
    """
    try:
        logger.info("Deleting product with ID: %s", product_id)
        response = requests.delete(f"{DATABASE_SERVICE_URL}/inventory/delete/{product_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error deleting product: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/inventory/<product_id>', methods=['GET'])
def api_get_product_by_id(product_id):
    """
    Get details of a specific product.

    Args:
        product_id (int): ID of the product to fetch.

    Returns:
        Response: JSON object with product details (e.g., name, price, description).
    """
    try:
        logger.info("Fetching product details for ID: %s", product_id)
        response = requests.get(f"{DATABASE_SERVICE_URL}/inventory/{product_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching product details: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/inventory/categories/<category>', methods=['GET'])
def api_get_products_by_category(category):
    """
    Get a list of products in a specific category.

    Args:
        category (str): The category to filter products by.

    Returns:
        Response: JSON list of products in the specified category.
    """
    try:
        logger.info("Fetching products in category: %s", category)
        response = requests.get(f"{DATABASE_SERVICE_URL}/inventory/categories/{category}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching products by category: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    """
    Starts the Inventory Service on port 5002.
    """
    logger.info("Starting Inventory Service")
    app.run(host="0.0.0.0", port=5002, debug=True)
