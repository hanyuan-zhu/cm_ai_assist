import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
import pytest

from modules.company import Company, Project


import json

# 将项目根目录添加到系统路径，以便导入模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def test_get_companies(client, initialize_data):
    """
    测试获取公司列表的API接口。
    发送GET请求到 /api/companies，并验证响应。
    """
    response = client.get('/api/companies')
    print(response.data)  # 打印响应数据
    assert response.status_code == 200
    assert 'companies' in response.json
    assert len(response.json['companies']) == 5  # 根据 initial_data.json 中的公司数量

def test_get_company_projects(client, initialize_data):
    """
    测试获取指定公司项目列表的API接口。
    使用初始化数据中的公司名称获取其项目列表。
    """
    # 获取公司列表
    companies_response = client.get('/api/companies')
    assert companies_response.status_code == 200
    companies = companies_response.json.get('companies', [])
    
    # 定义公司名称和对应的项目数量
    company_project_counts = {
        "珠海分公司": 3,
        "联嘉": 3,
        "六部": 6,
        "省建筑": 2,
        "天泽": 1
    }
    
    for company in companies:
        company_name = company['name']
        company_id = company['id']
        
        # 获取该公司的项目列表
        projects_response = client.get(f'/api/companies/{company_id}/projects')
        print(projects_response.data)  # 打印响应数据
        assert projects_response.status_code == 200
        assert 'projects' in projects_response.json
        
        # 根据 initial_data.json 中的公司名称和项目数量进行断言
        expected_project_count = company_project_counts.get(company_name, 0)
        assert len(projects_response.json['projects']) == expected_project_count