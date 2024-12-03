import pytest
from app.auth import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_signup_success(client):
    response = client.post('/signup', json={
        'username': 'test_user',
        'password': 'test_password',
        'role': 'customer'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User test_user created successfully!'

def test_signup_missing_fields(client):
    response = client.post('/signup', json={'username': 'test_user'})
    assert response.status_code == 400
    assert response.json['message'] == 'All fields are required!'

def test_login_success(client):
    client.post('/signup', json={
        'username': 'test_user',
        'password': 'test_password',
        'role': 'customer'
    })
    response = client.post('/login', json={
        'username': 'test_user',
        'password': 'test_password'
    })
    assert response.status_code == 200
    assert response.json['message'].startswith('Welcome')

def test_login_failure(client):
    response = client.post('/login', json={
        'username': 'wrong_user',
        'password': 'wrong_password'
    })
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid credentials!'
