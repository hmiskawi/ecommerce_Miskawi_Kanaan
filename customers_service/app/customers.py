from flask import Flask, request, jsonify
from flask_cors import CORS 
from shared.decorators import login_required, admin_required
from database.customers_db import create_customers_table, insert_customer, update_customer, delete_customer, get_customers, get_customer_by_id, get_customer_by_username, update_customer_wallet

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200
    
# Register a new customer with full details
@app.route('/customers/register', methods=['POST'])
@login_required
def api_register_customer():
    customer = request.get_json()
    return jsonify(insert_customer(customer))

# Delete a customer by their ID
@app.route('/customers/delete/<customer_id>', methods=['DELETE'])
@admin_required
def api_delete_customer(customer_id):
    return jsonify(delete_customer(customer_id))

# Update customer details (partial or full updates)
@app.route('/customers/update', methods=['PUT'])
@login_required
def api_update_customer():
    customer = request.get_json()
    return jsonify(update_customer(customer))

# Get a list of all customers
@app.route('/customers', methods=['GET'])
@admin_required
def api_get_customers():
    return jsonify(get_customers())

# Get details of a specific customer by username
@app.route('/customers/username/<username>', methods=['GET'])
@admin_required
def api_get_customer_by_username(username):
    return jsonify(get_customer_by_username(username))

# Get details of a specific customer by id
@app.route('/customers/id/<customer_id>', methods=['GET'])
@admin_required
def api_get_customer_by_id(customer_id):
    return jsonify(get_customer_by_id(customer_id))

# Add funds to the customer’s wallet
@app.route('/customers/<username>/charge/<amount>', methods=['POST'])
@admin_required
def api_charge_customer(username, amount):
    return jsonify(update_customer_wallet(username, int(amount)))

# Deduct funds from the customer’s wallet
@app.route('/customers/<username>/deduct/<amount>', methods=['POST'])
@admin_required
def api_deduct_customer(username, amount):
    neg_amount = -(int(amount))
    return jsonify(update_customer_wallet(username, neg_amount))

if __name__ == "__main__":
    create_customers_table()
    app.run(debug=True)
