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
logger = logging.getLogger("SalesService")

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

@app.route('/sales/products', methods=['GET'])
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
