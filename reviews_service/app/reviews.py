import cProfile
import pstats
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

DATABASE_SERVICE_URL = "http://database:5000"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InventoryService")


def profile_function(func):
    """
    A decorator to profile the execution time of a function using cProfile.
    """
    def u_wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()

        # Save stats to a stream
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Print top 10 cumulative time functions

        logger.info("Profiling results:\n%s", stream.getvalue())
        return result
    return u_wrapper

@app.route('/health', methods=['GET'])
@profile_function
def health_check():
    logger.info("Health check requested")
    return jsonify({"status": "healthy"}), 200

@app.route('/reviews/submit', methods=['POST'])
@profile
@profile_function
def api_submit_review():
    """
    Submit a review for a product.

    The submitted review is stored in a moderation table for admin approval.

    Request:
        JSON object containing:
            - customer_id (int): ID of the customer submitting the review.
            - product_id (int): ID of the product being reviewed.
            - rating (int): Rating score (1-5).
            - comment (str): Review comment.

    Returns:
        Response: JSON with confirmation message or error details.
    """
    review = request.get_json()
    try:
        logger.info("Submitting a review: %s", review)
        response = requests.post(f"{DATABASE_SERVICE_URL}/reviews/submit", json=review)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error submitting review: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/reviews/update', methods=['PUT'])
@profile
@profile_function
def api_update_review():
    """
    Update an existing review.

    Request:
        JSON object containing:
            - review_id (int): ID of the review to update.
            - customer_id (int): ID of the customer who submitted the review.
            - product_id (int): ID of the product being reviewed.
            - rating (int): Updated rating score (1-5).
            - comment (str): Updated review comment.

    Returns:
        Response: JSON with confirmation message or error details.
    """
    review = request.get_json()
    try:
        logger.info("Updating a review: %s", review)
        response = requests.put(f"{DATABASE_SERVICE_URL}/reviews/update", json=review)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error updating review: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/reviews/delete/<review_id>', methods=['DELETE'])
@profile
@profile_function
def api_delete_review(review_id):
    """
    Delete a specific review.

    Args:
        review_id (int): ID of the review to delete.

    Returns:
        Response: JSON with confirmation message or error details.
    """
    try:
        logger.info("Deleting review with ID: %s", review_id)
        response = requests.delete(f"{DATABASE_SERVICE_URL}/reviews/delete/{review_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error deleting review: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/reviews/product/<product_id>', methods=['GET'])
def api_get_product_reviews(product_id):
    """
    Get all reviews for a specific product.

    Args:
        product_id (int): ID of the product to fetch reviews for.

    Returns:
        Response: JSON list of reviews for the specified product.
    """
    try:
        logger.info("Fetching reviews for product ID: %s", product_id)
        response = requests.get(f"{DATABASE_SERVICE_URL}/reviews/product/{product_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching product reviews: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/reviews/customer/<customer_id>', methods=['GET'])
def api_get_customer_reviews(customer_id):
    """
    Get all reviews submitted by a specific customer.

    Args:
        customer_id (int): ID of the customer to fetch reviews for.

    Returns:
        Response: JSON list of reviews submitted by the customer.
    """
    try:
        logger.info("Fetching reviews for customer ID: %s", customer_id)
        response = requests.get(f"{DATABASE_SERVICE_URL}/reviews/customer/{customer_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching customer reviews: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/reviews/approve', methods=['POST'])
@profile
@profile_function
def api_approve_review():
    """
    Approve a submitted review.

    Request:
        JSON object containing:
            - review_id (int): ID of the review to approve.

    Returns:
        Response: JSON with confirmation message or error details.
    """
    review = request.get_json()
    try:
        logger.info("Approving a review: %s", review)
        response = requests.post(f"{DATABASE_SERVICE_URL}/reviews/approve", json=review)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error approving review: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/reviews/reject/<review_id>', methods=['DELETE'])
def api_reject_review(review_id):
    """
    Reject (flag) a review.

    Args:
        review_id (int): ID of the review to reject.

    Returns:
        Response: JSON with confirmation message or error details.
    """
    try:
        logger.info("Rejecting review with ID: %s", review_id)
        response = requests.delete(f"{DATABASE_SERVICE_URL}/reviews/reject/{review_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error rejecting review: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/reviews/<review_id>', methods=['GET'])
def api_get_specific_review(review_id):
    """
    Get details of a specific review.

    Args:
        review_id (int): ID of the review to fetch.

    Returns:
        Response: JSON object with review details (e.g., rating, comment).
    """
    try:
        logger.info("Fetching details for review ID: %s", review_id)
        response = requests.get(f"{DATABASE_SERVICE_URL}/reviews/{review_id}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching review details: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    """
    Starts the Reviews Service on port 5003.
    """
    logger.info("Starting Reviews Service")
    app.run(host="0.0.0.0", port=5003, debug=True)
