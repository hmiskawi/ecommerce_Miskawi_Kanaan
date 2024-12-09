import pytest
from wishlist import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('database.wishlist_db.insert_wish')
def test_api_add_wish(mock_insert_wish, client):
    mock_insert_wish.return_value = {"message": "Wish added successfully."}
    wish_data = {"customer_id": 1, "product_id": 42, "quantity": 1}
    response = client.post('/customers/wishlist/add', json=wish_data)
    assert response.status_code == 201
    assert response.json == {"message": "Wish added successfully."}

@patch('database.wishlist_db.delete_wish')
def test_api_remove_wish(mock_delete_wish, client):
    mock_delete_wish.return_value = {"message": "Wish removed successfully."}
    response = client.delete('/customers/wishlist/remove/1/42')
    assert response.status_code == 200
    assert response.json == {"message": "Wish removed successfully."}

@patch('database.wishlist_db.get_wishes')
def test_api_get_wishes(mock_get_wishes, client):
    mock_get_wishes.return_value = [{"product_id": 42, "quantity": 1}]
    response = client.get('/customers/wishlist/1')
    assert response.status_code == 200
    assert response.json == [{"product_id": 42, "quantity": 1}]

@patch('database.wishlist_db.notify_abandoned_wishlist')
def test_api_notify_customer(mock_notify, client):
    mock_notify.return_value = None
    response = client.post('/customers/wishlist/notify/1')
    assert response.status_code == 200
    assert response.json == {"message": "Notification sent successfully."}
