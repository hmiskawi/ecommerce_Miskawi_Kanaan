import unittest
from unittest.mock import patch, MagicMock
from inventory import app

class TestInventoryService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch('inventory.requests.get')
    def test_health_check(self, mock_get):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    @patch('inventory.requests.get')
    def test_get_products(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{"name": "Product1", "price": 10.0}])
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"name": "Product1", "price": 10.0}])

    @patch('inventory.requests.post')
    def test_add_product(self, mock_post):
        mock_post.return_value = MagicMock(status_code=201, json=lambda: {"message": "Product added"})
        response = self.client.post('/inventory/add', json={"name": "Product1", "price": 10.0, "category": "Electronics"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Product added"})

if __name__ == '__main__':
    unittest.main()
