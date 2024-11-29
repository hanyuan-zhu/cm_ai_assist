from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager

# 初始化SQLAlchemy对象
"""
SQLAlchemy 是一个ORM（对象关系映射）库：
- ORM的作用是将数据库表映射为Python对象
- 使得我们可以用面向对象的方式操作数据库

类比：
- 就像是数据库和Python之间的翻译官
- 我们用Python的语言告诉它要做什么
- 它帮我们翻译成数据库能理解的语言
"""
db = SQLAlchemy()

# 初始化Flask-RESTful API对象
"""
Flask-RESTful 是一个扩展，用于快速构建REST API：
- 提供了资源(Resource)的概念
- 使得我们可以用类的方式定义API端点

类比：
- 就像是API的管理者
- 我们定义好每个资源的行为
- 它帮我们处理请求和响应
"""
api = Api()

# 初始化JWT管理器
"""
Flask-JWT-Extended 是一个扩展，用于处理JWT认证：
- 提供了生成和验证JWT的功能
- 使得我们可以轻松地为API添加认证机制

类比：
- 就像是门禁系统
- 我们定义好谁可以进出
- 它帮我们检查每个人的通行证
"""
jwt = JWTManager()
jwt_blacklist = set()