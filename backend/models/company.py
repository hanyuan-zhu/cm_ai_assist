from backend.models import db
from sqlalchemy import Column
from sqlalchemy.orm import relationship
class Company(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), unique=True, nullable=False)
    projects = relationship('Project', backref='company', lazy=True)
    employees = relationship('Employee', backref='company', lazy=True)