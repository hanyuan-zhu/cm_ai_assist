from backend.models import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date

class Employee(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), nullable=False)
    position = Column(db.String(64))
    hire_date = Column(db.Date)
    status = Column(db.String(16), default='待岗')
    company_id = Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    project_id = Column(db.Integer, db.ForeignKey('project.id'))
    creator_id = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)