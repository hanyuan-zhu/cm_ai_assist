
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


