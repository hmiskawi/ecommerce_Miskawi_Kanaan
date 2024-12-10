import unittest
from unittest.mock import patch, MagicMock
from sales import app

class TestSalesService(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch('sales.requests.get')
    def test_health_check(self, mock_get):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    @patch('sales.requests.get')
    def test_get_products(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{"name": "Product1", "price": 10.0}])
        response = self.client.get('/sales/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{"name": "Product1", "price": 10.0}])

    @patch('sales.requests.post')
    def test_process_sale(self, mock_post):
        mock_post.return_value = MagicMock(status_code=201, json=lambda: {"message": "Sale processed"})
        response = self.client.post('/sales/purchase', json={"customer_id": 1, "product_id": 1, "quantity": 2, "total_price": 20.0})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Sale processed"})

if __name__ == '__main__':
    unittest.main()
