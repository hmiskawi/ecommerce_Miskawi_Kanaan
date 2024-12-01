from flask import Flask, request, jsonify
from flask_cors import CORS
from shared.decorators import login_required, admin_required
from database.sales_db import (
    create_sales_table,
    insert_sale,
    display_goods,
    display_good_detail,
    display_customer_sales,
)
from marshmallow import Schema, fields, ValidationError
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SaleSchema(Schema):
    """
    Schema for validating sale data.

    Attributes:
        customer_id (int): The ID of the customer making the purchase.
        product_id (int): The ID of the product being purchased.
        quantity (int): The quantity of the product being purchased.
        total_price (float): The total price of the purchase.
    """
    customer_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    total_price = fields.Float(required=True)

sale_schema = SaleSchema()

@app.route('/sales/products', methods=['GET'])
def api_get_products():
    """
    Retrieves a list of all products available for sale.

    :return: JSON response with product names and prices.
    :rtype: flask.Response
    """
    try:
        products = display_goods()
        return jsonify(products), 200
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return jsonify({"error": "Failed to retrieve products"}), 500

@app.route('/sales/products/<int:product_id>', methods=['GET'])
def api_get_product_detail(product_id):
    """
    Retrieves detailed information about a specific product.

    :param product_id: ID of the product to retrieve.
    :type product_id: int
    :return: JSON response with product details.
    :rtype: flask.Response
    """
    try:
        product = display_good_detail(product_id)
        return jsonify(product), 200
    except Exception as e:
        logger.error(f"Error fetching product details: {e}")
        return jsonify({"error": "Failed to retrieve product details"}), 500

@app.route('/sales/purchase', methods=['POST'])
@login_required
def api_process_sale():
    """
    Processes a sale.

    :return: JSON response with the sale details or an error message.
    :rtype: flask.Response
    """
    try:
        sale = sale_schema.load(request.get_json())
        response = insert_sale(sale)
        if not response:
            return jsonify({"error": "Purchase failed. Check balance or stock availability."}), 400
        return jsonify(response), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logger.error(f"Error processing sale: {e}")
        return jsonify({"error": "Failed to process sale"}), 500

@app.route('/sales/history/<int:customer_id>', methods=['GET'])
@admin_required
def api_purchase_history(customer_id):
    """
    Retrieves the purchase history for a specific customer.

    :param customer_id: ID of the customer whose history is being retrieved.
    :type customer_id: int
    :return: JSON response with the customer's purchase history.
    :rtype: flask.Response
    """
    try:
        sales = display_customer_sales(customer_id)
        return jsonify(sales), 200
    except Exception as e:
        logger.error(f"Error fetching purchase history: {e}")
        return jsonify({"error": "Failed to retrieve purchase history"}), 500

if __name__ == "__main__":
    """
    Initializes the sales table and starts the Flask application.
    """
    create_sales_table()
    app.run(debug=True)
