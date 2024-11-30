# 项目目录结构

- 需求文档.md
- API.md
- backend/
  - app.py: Flask应用的入口文件，包含应用的创建和配置。
  - config.py: 配置文件，包含数据库URI、密钥等配置信息。
  - extensions.py: 扩展文件，初始化Flask扩展（如SQLAlchemy、Flask-RESTful、JWT等）。
  - models/
    - __init__.py: 初始化文件，导入所有模型。
    - change_request.py: 变动请求模型，定义了员工调岗、离职等变动请求的表结构。
    - company.py: 公司模型，定义了公司的表结构。
    - employee.py: 员工模型p，定义了员工的表结构。
    - project.py: 项目模型，定义了项目的表结构。
    - user.py: 用户模型，定义了用户的表结构。
  - resources/
    - __init__.py: 初始化文件，导入并初始化所有资源。
    - auth.py: 认证资源，包含登录、注册和登出功能。
    - changes.py: 变动资源，包含获取待确认变动、批准变动、拒绝变动等功能。
    - companies.py: 公司资源，包含获取公司列表、获取公司项目列表等功能。
    - employees.py: 员工资源，包含获取在岗员工列表、添加新员工等功能。
    - users.py: 用户资源，包含获取当前登录用户信息的功能。
  - schemas/
    - __init__.py: 初始化文件，导入所有模式。
    - change_schema.py: 变动模式，定义了变动请求的序列化和反序列化规则。
    - company_schema.py: 公司模式，定义了公司的序列化和反序列化规则。
    - employee_schema.py: 员工模式，定义了员工的序列化和反序列化规则。
    - project_schema.py: 项目模式，定义了项目的序列化和反序列化规则。
    - user_schema.py: 用户模式，定义了用户的序列化和反序列化规则。
  - tests/
    - test_api.py: API测试文件，包含对各个API的测试用例。
- README.md

## 目录说明

### models 目录
模型文件，定义了数据库表结构和ORM模型。
### resources 目录
资源文件，定义了API的路由和处理逻辑。
### schemas 目录
模式文件，定义了数据序列化（serialization）和反序列化（deserialization）的模式。

## 作用说明

在Web应用中，数据的传输通常以JSON格式进行。为了确保数据的格式和内容符合预期，我们需要对数据进行序列化（serialization）和反序列化（deserialization）。`schemas` 目录中的文件就是用来定义这些规则的。

- **序列化（serialization）**：将Python对象（Python objects）转换为JSON格式，以便传输。
- **反序列化（deserialization）**：将JSON格式的数据转换为Python对象，以便处理。

类比：
- 就像是数据的“翻译官”，在Python对象和JSON数据之间进行转换。
- 确保数据在传输过程中保持一致性和完整性。

#### SQLAlchemy ORM 和 Marshmallow 序列化/反序列化

##### SQLAlchemy ORM

SQLAlchemy 是一个对象关系映射（ORM，Object-Relational Mapping）库，它的**主要作用**是<u>**将数据库表（database tables）映射为 Python 对象**</u>，使得我们可以用面向对象的方式操作数据库。

- **数据库表（database tables）**：存储在数据库中的数据结构。
- **Python 对象（Python objects）**：在 Python 代码中使用的类（classes）和实例（instances）。

SQLAlchemy ORM 的作用是将数据库表和 Python 类关联起来，使得我们可以通过操作 Python 对象来操作数据库表。

例如，在 `models/user.py` 中定义的 `User` 模型（model）：

```python
from backend.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
```

这个 `User` 类对应数据库中的 `users` 表。我们可以通过创建 `User` 类的实例来插入数据，通过查询 `User` 类来获取数据。

#### Marshmallow 序列化/反序列化
Marshmallow 是一个用于对象序列化（serialization）和反序列化（deserialization）的库。它的**主要作用**是将<u>**Python 对象转换为 JSON 格式（序列化）**</u>，以及将 JSON 格式的数据转换为 Python 对象（反序列化）。
###### 序列化
目的：将**后端的Python对象转换为JSON格式，以便通过HTTP协议传输给前端**。 使用场景：当后端需要将数据发送给前端时，例如返回用户信息、列表数据等。 示例：将一个 User 对象转换为JSON格式的字符串。

```python
from backend.schemas import user_schema

user = User(username="zhang_san", password="my_password123")
user_data = user_schema.dump(user)
# user_data 现在是一个字典，可以转换为JSON格式
# {"id": 1, "username": "zhang_san"}
```

###### 反序列化
目的：将前端发送的JSON格式数据转换为后端的Python对象，以便进行处理和存储。 使用场景：当后端接收到前端发送的数据时，例如用户注册、登录等操作。 示例：将一个JSON格式的字符串转换为 User 对象。


```python
from backend.schemas import user_schema

json_data = '{"username": "zhang_san", "password": "my_password123"}'
user_data = user_schema.loads(json_data)
user = User(**user_data)
```


