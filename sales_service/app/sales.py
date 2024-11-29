from flask import Flask, request, jsonify
from flask_cors import CORS 
from shared.decorators import login_required, admin_required
from database.sales_db import create_sales_table, insert_sale, update_sale, delete_sale, get_sales, get_sale_by_id, display_goods, display_good_detail, display_customer_sales

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Get a list of all products available for sale (name, price)
@app.route('/sales/products', methods=['GET'])
def api_get_products():
    return jsonify(display_goods())

# Get detailed information about a specific product
@app.route('/sales/products/<product_id>', methods=['GET'])
def api_get_product_detail(product_id):
    return jsonify(display_good_detail(product_id))

# Process a sale
@app.route('/sales/purchase', methods=['POST'])
@login_required
def api_process_sale():
    sale = request.get_json()
    return jsonify(insert_sale(sale))

# Get the purchase history for a specific customer
@app.route('/sales/history/<customer_id>', methods=['GET'])
@admin_required
def api_purchase_history(customer_id):
    return jsonify(display_customer_sales(customer_id))

if __name__ == "__main__":
    create_sales_table()
    app.run(debug=True)