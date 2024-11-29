from backend.models import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class Employee(db.Model):
    """
    Employee模型类，表示员工信息

    属性:
    - id: 员工ID，主键
    - name: 员工姓名
    - position: 员工职位
    - hire_date: 入职日期
    - status: 员工状态（在岗、待岗、离职）
    - company_id: 所属公司ID，外键
    - project_id: 所属项目ID，外键
    - creator_id: 创建者ID，外键
    - company: 关联的Company对象
    - project: 关联的Project对象
    """
    # 定义员工ID列，主键（primary key）
    id = Column(db.Integer, primary_key=True)
    
    # 定义员工姓名列，字符串类型，不允许为空
    name = Column(db.String(64), nullable=False)
    
    # 定义员工职位列，字符串类型
    position = Column(db.String(64))
    
    # 定义入职日期列，日期类型
    hire_date = Column(db.Date)
    
    # 定义员工状态列，字符串类型，默认值为'待岗'
    status = Column(db.String(16), default='待岗')
    
    # 定义公司ID列，外键（foreign key），关联到公司表的ID列
    company_id = Column(db.Integer, db.ForeignKey('company.id'))
    
    # 定义项目ID列，外键，关联到项目表的ID列
    project_id = Column(db.Integer, db.ForeignKey('project.id'))
    
    # 定义创建者ID列，外键，关联到用户表的ID列，不允许为空
    creator_id = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 定义关系，用于访问关联的Company对象
    # back_populates参数用于双向关系，指向Company模型中的employees属性
    company = relationship("Company", back_populates="employees")
    
    # 定义关系，用于访问关联的Project对象
    # back_populates参数用于双向关系，指向Project模型中的employees属性
    project = relationship("Project", back_populates="employees")
    
"""
    关系（Relationship）说明：
    在SQLAlchemy中，关系用于在ORM层面上定义表之间的关联。关系属性允许我们在代码中方便地访问关联的对象。

    示例1： company 关系属性允许我们通过 Employee 对象访问关联的 Company 对象。
       - 定义：company = relationship("Company", back_populates="employees")
       - 作用：通过company属性，可以访问Employee对象关联的Company对象。
       - 双向关系：使用back_populates参数，指向Company模型中的employees属性，表示Company对象也可以访问关联的Employee对象。
       - 示例：
         employee = Employee.query.get(1)
         print(employee.company.name)  # 输出关联的公司名称

    示例2：
        - 假设你有以下数据：
        公司：Company(id=1, name='Company A')
        项目：Project(id=1, name='Project A', company_id=1)
        员工：Employee(id=1, name='Employee 1', company_id=1, project_id=1)

        - 访问关系属性：
        你可以通过Employee对象访问其关联的公司和项目对象：
        employee = Employee.query.get(1)
        print(employee.company.name)  # 输出: Company A
        print(employee.project.name)  # 输出: Project A

        - 序列化：
        使用EmployeeSchema序列化Employee对象时，会自动调用get_company_name和get_project_name方法：
        employee_data = employee_schema.dump(employee)
        print(employee_data)
        # 输出:
        # {
        #     'id': 1,
        #     'name': 'Employee 1',
        #     'position': None,
        #     'hire_date': None,
        #     'status': '待岗',
        #     'company_id': 1,
        #     'company_name': 'Company A',
        #     'project_id': 1,
        #     'project_name': 'Project A',
        #     'creator_id': None
        # }


    """