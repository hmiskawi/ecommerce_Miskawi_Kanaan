from flask import Flask, request, jsonify
from flask_cors import CORS
from shared.decorators import login_required, admin_required
from database.inventory_db import (
    create_inventory_table,
    insert_product,
    update_product,
    delete_product,
    get_products,
    get_product_by_id,
    get_category_products,
)
from marshmallow import Schema, fields, ValidationError
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductSchema(Schema):
    """
    Schema for validating product data.

    Attributes:
        name (str): The name of the product.
        category (str): The category of the product ('Food', 'Clothes', 'Accessories', 'Electronics').
        price (float): The price of the product.
        description (str): A description of the product.
        stock_count (int): The stock count for the product.
    """
    name = fields.Str(required=True)
    category = fields.Str(required=True, validate=lambda c: c in ['Food', 'Clothes', 'Accessories', 'Electronics'])
    price = fields.Float(required=True)
    description = fields.Str(required=False)
    stock_count = fields.Int(required=True)

product_schema = ProductSchema()

@app.route('/inventory/add', methods=['POST'])
@admin_required
def api_add_product():
    """
    Adds a new product to the inventory.

    :return: JSON response with the added product details or an error message.
    :rtype: flask.Response
    """
    try:
        product = product_schema.load(request.get_json())
        response = insert_product(product)
        return jsonify(response), 201
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logger.error(f"Error adding product: {e}")
        return jsonify({"error": "Failed to add product"}), 500

@app.route('/inventory/update', methods=['PUT'])
@admin_required
def api_update_product():
    """
    Updates an existing product's details.

    :return: JSON response with the updated product details or an error message.
    :rtype: flask.Response
    """
    try:
        product = product_schema.load(request.get_json(), partial=True)
        response = update_product(product)
        return jsonify(response), 200
    except ValidationError as e:
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        return jsonify({"error": "Failed to update product"}), 500

@app.route('/inventory/delete/<product_id>', methods=['DELETE'])
@admin_required
def api_delete_product(product_id):
    """
    Deletes a product from the inventory.

    :param product_id: ID of the product to be deleted.
    :type product_id: int
    :return: JSON response indicating the result of the operation.
    :rtype: flask.Response
    """
    try:
        response = delete_product(product_id)
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        return jsonify({"error": "Failed to delete product"}), 500

@app.route('/inventory', methods=['GET'])
@admin_required
def api_get_products():
    """
    Retrieves all available products in the inventory.

    :return: JSON response with a list of products.
    :rtype: flask.Response
    """
    try:
        response = get_products()
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        return jsonify({"error": "Failed to retrieve products"}), 500

@app.route('/inventory/<product_id>', methods=['GET'])
@admin_required
def api_get_product_by_id(product_id):
    """
    Retrieves the details of a specific product.

    :param product_id: ID of the product to retrieve.
    :type product_id: int
    :return: JSON response with the product's details.
    :rtype: flask.Response
    """
    try:
        response = get_product_by_id(product_id)
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error retrieving product: {e}")
        return jsonify({"error": "Failed to retrieve product"}), 500

@app.route('/inventory/categories/<category>', methods=['GET'])
@admin_required
def api_get_products_by_category(category):
    """
    Retrieves all products within a specific category.

    :param category: The category of the products.
    :type category: str
    :return: JSON response with a list of products in the category.
    :rtype: flask.Response
    """
    try:
        response = get_category_products(category)
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error retrieving category products: {e}")
        return jsonify({"error": "Failed to retrieve category products"}), 500

if __name__ == "__main__":
    """
    Initializes the inventory table and starts the Flask application.
    """
    create_inventory_table()
    app.run(debug=True)
