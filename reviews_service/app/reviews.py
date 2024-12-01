from flask import Flask, request, jsonify
from flask_cors import CORS
from database.reviews_db import (
    create_reviews_table,
    submit_review,
    approve_review,
    reject_review,
    get_review_by_id,
)
from shared.decorators import login_required, admin_required
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/reviews/submit', methods=['POST'])
@login_required
def api_submit_review():
    """
    Submits a review for moderation.

    :return: JSON response with the review details or an error message.
    :rtype: flask.Response
    """
    try:
        review = request.get_json()
        response = submit_review(review)
        return jsonify(response), 201
    except Exception as e:
        logger.error(f"Error submitting review: {e}")
        return jsonify({"error": "Failed to submit review"}), 500

@app.route('/reviews/approve/<int:review_id>', methods=['POST'])
@admin_required
def api_approve_review(review_id):
    """
    Approves a review and moves it to the main Reviews table.

    :param review_id: The ID of the review to approve.
    :type review_id: int
    :return: JSON response with the approved review details or an error message.
    :rtype: flask.Response
    """
    try:
        response = approve_review(review_id)
        if not response:
            return jsonify({"error": "Review not found or approval failed"}), 404
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error approving review: {e}")
        return jsonify({"error": "Failed to approve review"}), 500

@app.route('/reviews/reject/<int:review_id>', methods=['DELETE'])
@admin_required
def api_reject_review(review_id):
    """
    Rejects a review and removes it from the moderation queue.

    :param review_id: The ID of the review to reject.
    :type review_id: int
    :return: JSON response indicating success or failure.
    :rtype: flask.Response
    """
    try:
        response = reject_review(review_id)
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error rejecting review: {e}")
        return jsonify({"error": "Failed to reject review"}), 500

@app.route('/reviews/<int:review_id>', methods=['GET'])
@login_required
def api_get_review(review_id):
    """
    Retrieves a specific review.

    :param review_id: The ID of the review to retrieve.
    :type review_id: int
    :return: JSON response with the review details or an error message.
    :rtype: flask.Response
    """
    try:
        review = get_review_by_id(review_id)
        return jsonify(review), 200
    except Exception as e:
        logger.error(f"Error fetching review: {e}")
        return jsonify({"error": "Failed to retrieve review"}), 500

if __name__ == "__main__":
    create_reviews_table()
    app.run(debug=True)
