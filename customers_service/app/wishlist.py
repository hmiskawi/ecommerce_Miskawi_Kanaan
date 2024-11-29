from flask import Flask, request, jsonify
from flask_cors import CORS 
from shared.decorators import login_required, admin_required
from database.wishlist_db import create_wishlist_table, insert_wish, delete_wish, get_wishes, notify_abandoned_wishlist

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Add a product to the customer’s wishlist
@app.route('/customers/wishlist/add', methods=['POST'])
@login_required
def api_add_wish():
    wish = request.get_json()
    return jsonify(insert_wish(wish))

# Remove a product from the customer’s wishlist
@app.route('/customers/wishlist/remove/<customer_id>/<product_id>', methods=['DELETE'])
@login_required
def api_remove_wish(customer_id, product_id):
    return jsonify(delete_wish(customer_id, product_id))

# Get all wishlist items for a customer
@app.route('/customers/wishlist/<customer_id>', methods=['GET'])
@login_required
def api_get_wishes(customer_id):
    return jsonify(get_wishes(customer_id))

# Notify the customer about abandoned wishlist items
@app.route('customers/wishlist/notify/<customer_id>', methods=['POST'])
@admin_required
def api_notify_customer(customer_id):
    return jsonify(notify_abandoned_wishlist(customer_id))

if __name__ == "__main__":
    create_wishlist_table()
    app.run(debug=True)