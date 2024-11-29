from flask import Flask, request, jsonify
from flask_cors import CORS 
from shared.decorators import login_required, admin_required
from database.inventory_db import create_inventory_table, insert_product, update_product, delete_product, get_products, get_product_by_id, get_category_products

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Add a new product to the inventory
@app.route('/inventory/add', methods=['POST'])
@admin_required
def api_add_product():
    product = request.get_json()
    return jsonify(insert_product(product))

# Update details of a product
@app.route('/inventory/update', methods=['PUT'])
@admin_required
def api_update_product():
    product = request.get_json()
    return jsonify(update_product(product))

# Delete a product from the inventory
@app.route('/inventory/delete/<product_id>', methods=['DELETE'])
@admin_required
def api_delete_product(product_id):
    return jsonify(delete_product(product_id))

# Get a list of all available products
@app.route('/inventory', methods=['GET'])
@admin_required
def api_get_products():
    return jsonify(get_products())

# Get full details of a specific product
@app.route('/inventory/<product_id>', methods=['GET'])
@admin_required
def api_get_product_by_id(product_id):
    return jsonify(get_product_by_id(product_id))

# Get a list of all products in a specific category
@app.route('/inventory/categories/<category>', methods=['GET'])
@admin_required
def api_get_products_by_category(category):
    return jsonify(get_category_products(category))

if __name__ == "__main__":
    create_inventory_table()
    app.run(debug=True)