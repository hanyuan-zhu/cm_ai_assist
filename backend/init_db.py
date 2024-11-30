import json
import os
from app import create_app
from models import Company, Project
from extensions import db
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.engine.url import URL, make_url
from sqlalchemy import create_engine

app = create_app()

with app.app_context():
    # 获取当前的数据库 URL
    print('当前数据库 URL：')
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    url = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
    
    # 提取数据库名称并将其从 URL 中移除
    database_name = url.database
    url = url.set(database=None)

    # 使用不含数据库名称的 URL 创建引擎
    engine = create_engine(url)
   
    # 检查数据库是否存在，如果不存在则创建它
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"数据库 '{database_name}' 已创建。")

    # 将数据库名称还原
    url = url.set(database=database_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = str(url)
   
    # 更新 SQLAlchemy 对象的配置
    db.engine.dispose()  # 释放现有连接
    db.get_engine(app, bind=None)  # 更新引擎配置
   
    # 创建所有表
    db.create_all()

    # 初始化数据
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'initial_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
   
    for company_data in data['companies']:
        company = Company(name=company_data['name'])
        db.session.add(company)
        db.session.commit()
       
        for project_data in company_data['projects']:
            project = Project(name=project_data['name'], company_id=company.id)
            db.session.add(project)
            db.session.commit()