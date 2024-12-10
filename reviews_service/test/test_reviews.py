import unittest
from unittest.mock import patch, MagicMock
from reviews_service import app

class TestReviewsService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch('reviews_service.requests.get')
    def test_health_check(self, mock_get):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    @patch('reviews_service.requests.post')
    def test_submit_review(self, mock_post):
        mock_post.return_value = MagicMock(status_code=201, json=lambda: {"message": "Review submitted"})
        response = self.client.post('/reviews/submit', json={"product_id": 1, "rating": 5, "comment": "Great product!"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Review submitted"})

    @patch('reviews_service.requests.get')
    def test_get_product_reviews(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{"product_id": 1, "rating": 5, "comment": "Great product!"}])
        response = self.client.get('/reviews/product/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"product_id": 1, "rating": 5, "comment": "Great product!"}])

if __name__ == '__main__':
    unittest.main()
