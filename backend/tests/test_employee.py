import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
import pytest

@pytest.fixture(scope='module')
def app():
    """
    创建Flask应用实例并配置为测试模式。
    初始化数据库并在测试结束后清理。
    """
    app = create_app()
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """
    创建测试客户端，用于发送HTTP请求到应用。
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    创建测试命令行运行器，用于测试Flask命令行接口。
    """
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def clean_db(app):
    """
    在每个测试之前开始一个数据库会话，
    并在测试之后回滚以保持数据库状态干净。
    """
    with app.app_context():
        db.session.begin_nested()
        yield
        db.session.rollback()

@pytest.fixture
def auth_headers(client):
    """
    注册并登录一个测试用户，获取认证头信息。
    """
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = response.json['token']
    return {
        'Authorization': f'Bearer {token}'
    }

def test_get_active_employees(client, auth_headers):
    """
    测试获取在岗及待岗员工列表的API接口。
    发送GET请求到 /api/active-employees，并验证响应。
    """
    response = client.get('/api/active-employees', headers=auth_headers)
    print(response.data)  # 打印响应数据
    assert response.status_code == 200
    assert 'employees' in response.json

def test_add_employee(client, auth_headers):
    """
    测试添加新员工的API接口。
    发送POST请求到 /api/employees，并验证响应。
    """
    new_employee = {
        'name': '测试员工',
        'position': '开发工程师',
        'efffective_date': '2023-10-01'
    }
    response = client.post('/api/employees', json=new_employee, headers=auth_headers)
    print(response.data)  # 打印响应数据
    print(response.status_code)  # 打印状态码
    assert response.status_code == 201
    assert response.json['employee']['name'] == new_employee['name']
    assert response.json['employee']['position'] == new_employee['position']
    assert response.json['employee']['efffective_date'] == new_employee['efffective_date']
    assert response.json['employee']['status'] == '待岗'