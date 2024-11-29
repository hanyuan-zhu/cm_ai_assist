from backend.models import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class Project(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), unique=True, nullable=False)
    company_id = Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employees = relationship('Employee', backref='project', lazy=True)