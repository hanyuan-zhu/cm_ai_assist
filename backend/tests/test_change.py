import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
import pytest
from modules.company import Company, Project
import json

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

@pytest.fixture(scope='module')
def initialize_data(app):
    """
    初始化测试数据库中的公司和项目数据。
    从 backend/data/initial_data.json 加载数据。
    """
    with app.app_context():
        # 定义初始数据的路径
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'initial_data.json')
        if not os.path.exists(data_path):
            pytest.fail(f"初始数据文件未找到: {data_path}")
        
        # 加载 initial_data.json 文件
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 添加公司和项目数据到数据库
        for company_data in data['companies']:
            company = Company(name=company_data['name'])
            db.session.add(company)
            db.session.commit()
            
            for project_data in company_data['projects']:
                project = Project(name=project_data['name'], company_id=company.id)
                db.session.add(project)
            db.session.commit()

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

def test_get_pending_changes(client, auth_headers, initialize_data):
    """
    测试获取待确认变动名单的API接口。
    发送GET请求到 /api/pending-changes，并验证响应。
    """
    response = client.get('/api/pending-changes', headers=auth_headers)
    print(response.data)  # 打印响应数据
    assert response.status_code == 200
    assert 'changes' in response.json

def test_submit_transfer_request(client, auth_headers, initialize_data):
    """
    测试提交员工调岗申请的API接口。
    先添加一个员工，然后发送PUT请求到 /api/pending-changes/{id}/transfer，并验证响应。
    """
    # 先添加一个员工
    new_employee = {
        'name': '测试员工',
        'position': '开发工程师',
        'efffective_date': '2023-10-01'
    }
    add_response = client.post('/api/employees', json=new_employee, headers=auth_headers)
    assert add_response.status_code == 201
    employee_id = add_response.json['employee']['id']

    # 发起调岗申请
    transfer_request = {
        'new_company': '1',  # 假设初始化数据中有公司ID为1的公司
        'new_project': '1',  # 假设初始化数据中有项目ID为1的项目
        'effective_date': '2023-10-01'
    }
    response = client.put(f'/api/pending-changes/{employee_id}/transfer', json=transfer_request, headers=auth_headers)
    print(response.data)  # 打印响应数据
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == '调岗申请已提交'

def test_submit_resign_request(client, auth_headers, initialize_data):
    """
    测试提交员工离职申请的API接口。
    先添加一个员工，然后发送PUT请求到 /api/pending-changes/{id}/resign，并验证响应。
    """
    # 先添加一个员工
    new_employee = {
        'name': '测试员工',
        'position': '开发工程师',
        'efffective_date': '2023-10-01'
    }
    add_response = client.post('/api/employees', json=new_employee, headers=auth_headers)
    assert add_response.status_code == 201
    employee_id = add_response.json['employee']['id']

    # 发起离职申请
    resign_request = {
        'resign_date': '2023-11-01'
    }
    response = client.put(f'/api/pending-changes/{employee_id}/resign', json=resign_request, headers=auth_headers)
    print(response.data)  # 打印响应数据
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == '离职申请已提交'

def test_approve_change_request(client, auth_headers, initialize_data):
    """
    测试确认变动申请的API接口。
    先添加一个员工并发起调岗申请，然后发送PUT请求到 /api/pending-changes/{id}/approve，并验证响应。
    """
    # 先添加一个员工
    new_employee = {
        'name': '测试员工',
        'position': '开发工程师',
        'efffective_date': '2023-10-01'
    }
    add_response = client.post('/api/employees', json=new_employee, headers=auth_headers)
    assert add_response.status_code == 201
    employee_id = add_response.json['employee']['id']

    # 发起调岗申请
    transfer_request = {
        'new_company': '1',  # 假设初始化数据中有公司ID为1的公司
        'new_project': '1',  # 假设初始化数据中有项目ID为1的项目
        'effective_date': '2023-10-01'
    }
    transfer_response = client.put(f'/api/pending-changes/{employee_id}/transfer', json=transfer_request, headers=auth_headers)
    assert transfer_response.status_code == 200

    # 确认变动申请
    response = client.put(f'/api/pending-changes/{employee_id}/approve', headers=auth_headers)
    print(response.data)  # 打印响应数据
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == '变更请求已批准 (Change request approved)'

def test_reject_change_request(client, auth_headers, initialize_data):
    """
    测试拒绝变动申请的API接口。
    先添加一个员工并发起调岗申请，然后发送PUT请求到 /api/pending-changes/{id}/reject，并验证响应。
    """
    # 先添加一个员工
    new_employee = {
        'name': '测试员工',
        'position': '开发工程师',
        'efffective_date': '2023-10-01'
    }
    add_response = client.post('/api/employees', json=new_employee, headers=auth_headers)
    assert add_response.status_code == 201
    employee_id = add_response.json['employee']['id']

    # 发起调岗申请
    transfer_request = {
        'new_company': '1',  # 假设初始化数据中有公司ID为1的公司
        'new_project': '1',  # 假设初始化数据中有项目ID为1的项目
        'effective_date': '2023-10-01'
    }
    transfer_response = client.put(f'/api/pending-changes/{employee_id}/transfer', json=transfer_request, headers=auth_headers)
    assert transfer_response.status_code == 200

    # 拒绝变动申请
    response = client.put(f'/api/pending-changes/{employee_id}/reject', headers=auth_headers)
    print(response.data)  # 打印响应数据
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == '变更请求已拒绝 (Change request rejected)'