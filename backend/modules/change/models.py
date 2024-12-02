from extensions import db
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
    
    

"""
问题与解答汇总
问题 1: ChangeRequest model 引用了其他 modules 的 model (如 Employee, Company)，但没有导入这些 model，这样合理吗？
解答: 合理，因为:
- 避免循环导入问题
- 所有模型共享同一个 db.Model 基类
- SQLAlchemy 使用字符串引用延迟加载机制

问题 2: 所有模型来自同一基类，模型命名需要全局唯一吗？为什么可以通过字符串名称找到正确模型？
解答: 对，是的，模型名必须全局唯一，因为:
- 所有模型共享同一个 MetaData 注册表
- 通过字符串引用时，SQLAlchemy 在这个全局注册表中查找

最佳实践:
```python
# 1. 共享基类
from extensions import db
class Model(db.Model): 
    pass

# 2. 使用字符串引用关系
employee = relationship("Employee", backref="changes")

# 3. 避免循环导入
# 不要直接 import 其他模块的 model
```

"""