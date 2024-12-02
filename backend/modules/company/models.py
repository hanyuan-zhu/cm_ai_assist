from extensions import db
from sqlalchemy import Column
from sqlalchemy.orm import relationship
class Company(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), unique=True, nullable=False)
    projects = relationship('Project', backref='company', lazy=True)
    employees = relationship('Employee', back_populates='company', lazy=True)

class Project(db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(64), unique=True, nullable=False)
    company_id = Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    employees = relationship('Employee', back_populates='project', lazy=True)

"""
backref 和 back_populates 都用于定义 SQLAlchemy 中的双向关系，但它们有一些不同之处：

- backref:
backref 是一个快捷方式，它会自动在关联的模型中创建一个反向引用。
使用 backref 时，只需要在一个模型中定义，SQLAlchemy 会自动在另一个模型中创建反向引用。
例如：
class Parent(db.Model):
    id = Column(db.Integer, primary_key=True)
    children = relationship('Child', backref='parent')

class Child(db.Model):
    id = Column(db.Integer, primary_key=True)
    parent_id = Column(db.Integer, db.ForeignKey('parent.id'))
在上面的例子中，Parent 模型中的 children 关系使用了 backref，因此 Child 模型中会自动有一个 parent 属性。


- back_populates:
back_populates 需要在两个模型中都定义，明确指定双向关系。
使用 back_populates 时，需要在两个模型中都定义关系，并且在每个模型中指向对方的关系属性。
例如：
class Parent(db.Model):
    id = Column(db.Integer, primary_key=True)
    children = relationship('Child', back_populates='parent')

class Child(db.Model):
    id = Column(db.Integer, primary_key=True)
    parent_id = Column(db.Integer, db.ForeignKey('parent.id'))
    parent = relationship('Parent', back_populates='children')
在上面的例子中，Parent 模型中的 children 关系和 Child 模型中的 parent 关系使用了 back_populates，明确指定了双向关系。


"""