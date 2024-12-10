import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# Base URL for the database service
DATABASE_SERVICE_URL = "http://database:5000"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("InventoryService")

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.

    Returns:
        Response: JSON indicating the health status of the service.
        Example: {"status": "healthy"}
    """
    logger.info("Health check requested")
    return jsonify({"status": "healthy"}), 200

@app.route('/inventory/add', methods=['POST'])
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

@app.route('/inventory', methods=['GET'])
def api_get_products():
    """
    Get a list of all products in the inventory.

    Returns:
        Response: JSON list of products with details (e.g., name, price, stock).
    """
    try:
        logger.info("Fetching all products")
        response = requests.get(f"{DATABASE_SERVICE_URL}/inventory")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching products: %s", str(e))
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
