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
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), nullable=False)
    position = Column(db.String(64))
    hire_date = Column(db.Date)
    status = Column(db.String(16), default='待岗')
    company_id = Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    project_id = Column(db.Integer, db.ForeignKey('project.id'))
    creator_id = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 关系定义，用于访问关联的Company和Project对象
    company = relationship("Company", back_populates="employees")
    project = relationship("Project", back_populates="employees")