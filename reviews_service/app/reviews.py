from flask import Flask, request, jsonify
from flask_cors import CORS 

from database.reviews_db import create_reviews_table, create_moderation_table, approve_review, reject_review, update_review, delete_review, get_product_reviews, get_customer_reviews, get_review_by_id, submit_review
from decorators import login_required, admin_required

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Submit a review for a product which can be approved or denied by an admin
@app.route('/reviews/submit', methods=['POST'])
@login_required
def api_submit_review():
    review = request.get_json()
    return jsonify(submit_review(review))

# Update an existing review
@app.route('/reviews/update', methods=['PUT'])
@login_required
def api_update_review():
    review = request.get_json()
    return jsonify(update_review(review))

# Delete a specific review
@app.route('/reviews/delete/<review_id>', methods=['DELETE'])
@login_required
def api_delete_review(review_id):
    return jsonify(delete_review(review_id))

# Get all reviews for a specific product
@app.route('/reviews/product/<product_id>', methods=['GET'])
@login_required
def api_get_product_reviews(product_id):
    return jsonify(get_product_reviews(product_id))

# Get all reviews submitted by a specific customer
@app.route('/reviews/customer/<customer_id>', methods=['GET'])
@login_required
def api_get_customer_reviews(customer_id):
    return jsonify(get_customer_reviews(customer_id))

# Moderate a review (approve)
@app.route('/reviews/approve', methods=['POST'])
@admin_required
def api_approve_review():
    review = request.get_json()
    return jsonify(approve_review(review))

# Moderate a review (flag)
@app.route('/reviews/reject/<review_id>', methods=['DELETE'])
@admin_required
def api_reject_review():
    review = request.get_json()
    return jsonify(reject_review(review))

# Get details of a specific review
@app.route('/reviews/<review_id>', methods=['GET'])
@login_required
def api_get_specific_review(review_id):
    return jsonify(get_review_by_id(review_id))

if __name__ == "__main__":
    create_moderation_table()
    create_reviews_table()
    app.run(debug=True)