from backend.models import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class ChangeRequest(db.Model):
    id = Column(Integer, primary_key=True)
    type = Column(String(16), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    from_company_id = Column(Integer, ForeignKey('company.id'))
    to_company_id = Column(Integer, ForeignKey('company.id'))
    from_project_id = Column(Integer, ForeignKey('project.id'))
    to_project_id = Column(Integer, ForeignKey('project.id'))
    effective_date = Column(Date)
    status = Column(String(16), default='待确认')
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # 添加关系
    employee = relationship("Employee", backref="changes")
    from_company = relationship("Company", foreign_keys=[from_company_id])
    to_company = relationship("Company", foreign_keys=[to_company_id])
    from_project = relationship("Project", foreign_keys=[from_project_id])
    to_project = relationship("Project", foreign_keys=[to_project_id])