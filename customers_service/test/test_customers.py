import pytest
from customers import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_customer(client):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "password": "securepassword",
        "age": 30,
        "address": "123 Elm Street",
        "gender": "M",
        "marital_status": "Single",
        "wallet_balance": 100.0
    }
    response = client.post('/customers/register', json=data)
    assert response.status_code == 201

@patch('database.customers_db.get_customers')
def test_get_customers(mock_get_customers, client):
    mock_get_customers.return_value = [{"username": "johndoe", "wallet_balance": 100.0}]
    response = client.get('/customers')
    assert response.status_code == 200
    assert response.json == [{"username": "johndoe", "wallet_balance": 100.0}]
