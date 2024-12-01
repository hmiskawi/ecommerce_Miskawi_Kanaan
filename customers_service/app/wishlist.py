from flask import Flask, request, jsonify
from flask_cors import CORS
from shared.decorators import login_required, admin_required
from database.wishlist_db import create_wishlist_table, insert_wish, delete_wish, get_wishes, notify_abandoned_wishlist

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/customers/wishlist/add', methods=['POST'])
@login_required
def api_add_wish():
    """
    Adds a product to a customer's wishlist.

    :return: JSON response with the added wish details or an error message.
    :rtype: flask.Response
    """
    try:
        wish = request.get_json()
        response = insert_wish(wish)
        return jsonify(response), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/customers/wishlist/remove/<customer_id>/<product_id>', methods=['DELETE'])
@login_required
def api_remove_wish(customer_id, product_id):
    """
    Removes a product from a customer's wishlist.

    :param customer_id: ID of the customer.
    :type customer_id: int
    :param product_id: ID of the product to remove.
    :type product_id: int
    :return: JSON response indicating the result of the operation.
    :rtype: flask.Response
    """
    try:
        response = delete_wish(customer_id, product_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/customers/wishlist/<customer_id>', methods=['GET'])
@login_required
def api_get_wishes(customer_id):
    """
    Retrieves all wishlist items for a customer.

    :param customer_id: ID of the customer.
    :type customer_id: int
    :return: JSON response with a list of wishlist items.
    :rtype: flask.Response
    """
    try:
        response = get_wishes(customer_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/customers/wishlist/notify/<customer_id>', methods=['POST'])
@admin_required
def api_notify_customer(customer_id):
    """
    Notifies a customer about abandoned wishlist items.

    :param customer_id: ID of the customer to notify.
    :type customer_id: int
    :return: JSON response indicating the result of the notification process.
    :rtype: flask.Response
    """
    try:
        notify_abandoned_wishlist(customer_id)
        return jsonify({"message": "Notification sent successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    """
    Initializes the wishlist table and starts the Flask application.
    """
    create_wishlist_table()
    app.run(debug=True)
