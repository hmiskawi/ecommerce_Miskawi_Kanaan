import unittest
from unittest.mock import patch, MagicMock
from app import app  # Import your Flask app

class TestCustomerAPI(unittest.TestCase):
    def setUp(self):
        # Configure Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.insert_customer')
    @patch('shared.decorators.login_required', lambda f: f)  # Mock login_required
    def test_register_customer(self, mock_insert_customer):
        # Mocking the database method
        mock_insert_customer.return_value = {"success": True, "message": "Customer registered"}
        
        # Sending a POST request
        response = self.app.post('/customers/register', json={
            "username": "test_user",
            "email": "test@example.com",
            "wallet": 100
        })
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True, "message": "Customer registered"})
        mock_insert_customer.assert_called_once_with({
            "username": "test_user",
            "email": "test@example.com",
            "wallet": 100
        })

    @patch('app.delete_customer')
    @patch('shared.decorators.admin_required', lambda f: f)  # Mock admin_required
    def test_delete_customer(self, mock_delete_customer):
        # Mocking the database method
        mock_delete_customer.return_value = {"success": True, "message": "Customer deleted"}
        
        # Sending a DELETE request
        response = self.app.delete('/customers/delete/1')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True, "message": "Customer deleted"})
        mock_delete_customer.assert_called_once_with("1")

    @patch('app.update_customer')
    @patch('shared.decorators.login_required', lambda f: f)
    def test_update_customer(self, mock_update_customer):
        # Mocking the database method
        mock_update_customer.return_value = {"success": True, "message": "Customer updated"}
        
        # Sending a PUT request
        response = self.app.put('/customers/update', json={
            "id": 1,
            "username": "updated_user",
            "email": "updated@example.com"
        })
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True, "message": "Customer updated"})
        mock_update_customer.assert_called_once_with({
            "id": 1,
            "username": "updated_user",
            "email": "updated@example.com"
        })

    @patch('app.get_customers')
    @patch('shared.decorators.admin_required', lambda f: f)
    def test_get_customers(self, mock_get_customers):
        # Mocking the database method
        mock_get_customers.return_value = [
            {"id": 1, "username": "user1", "email": "user1@example.com"},
            {"id": 2, "username": "user2", "email": "user2@example.com"}
        ]
        
        # Sending a GET request
        response = self.app.get('/customers')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"id": 1, "username": "user1", "email": "user1@example.com"},
            {"id": 2, "username": "user2", "email": "user2@example.com"}
        ])
        mock_get_customers.assert_called_once()

    @patch('app.update_customer_wallet')
    @patch('shared.decorators.admin_required', lambda f: f)
    def test_charge_customer(self, mock_update_customer_wallet):
        # Mocking the database method
        mock_update_customer_wallet.return_value = {"success": True, "message": "Wallet updated"}
        
        # Sending a POST request
        response = self.app.post('/customers/test_user/charge/50')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True, "message": "Wallet updated"})
        mock_update_customer_wallet.assert_called_once_with("test_user", 50)

    @patch('app.update_customer_wallet')
    @patch('shared.decorators.admin_required', lambda f: f)
    def test_deduct_customer(self, mock_update_customer_wallet):
        # Mocking the database method
        mock_update_customer_wallet.return_value = {"success": True, "message": "Wallet updated"}
        
        # Sending a POST request
        response = self.app.post('/customers/test_user/deduct/30')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"success": True, "message": "Wallet updated"})
        mock_update_customer_wallet.assert_called_once_with("test_user", -30)

if __name__ == '__main__':
    unittest.main()
