import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
import pytest

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        db.session.begin_nested()
        yield
        db.session.rollback()

def test_register(client):
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    print(response.data)  # 打印响应数据
    assert response.status_code == 201
    assert response.json['success'] == True

def test_login(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    print(response.data)  # 打印响应数据
    assert response.status_code == 200
    assert 'token' in response.json

def test_logout(client):
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = login_response.json['token']
    response = client.post('/api/auth/logout', headers={
        'Authorization': f'Bearer {token}'
    })
    print(response.data)  # 打印响应数据
    assert response.status_code == 200
    assert response.json['success'] == True