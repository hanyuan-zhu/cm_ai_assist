from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(64), unique=True, nullable=False)
    password = Column(db.String(128), nullable=False)
    # 关系
    employees = relationship('Employee', backref='creator', lazy=True)
    change_requests = relationship('ChangeRequest', backref='creator', lazy=True)