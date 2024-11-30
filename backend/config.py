"""
数据库配置指南
-------------
重要提示:
- 切换数据库"只需"修改 SQLALCHEMY_DATABASE_URI,其他代码无需更改
- 生产环境部署时请修改密钥配置(SECRET_KEY和JWT_SECRET_KEY)

1. 配置数据库连接
   只需要修改 SQLALCHEMY_DATABASE_URI 配置项,选择一种数据库并设置连接信息:

   MySQL格式:
   'mysql+pymysql://用户名:密码@主机地址:端口/数据库名'
   例如: 'mysql+pymysql://root:123456@localhost:3306/mydb'

   SQLite格式:
   'sqlite:///本地文件路径'
   例如: 'sqlite:///app.db'

   PostgreSQL格式:
   'postgresql://用户名:密码@主机地址:端口/数据库名'
   例如: 'postgresql://user:pass@localhost:5432/mydb'

2. 安装数据库驱动
   根据选择的数据库安装对应的Python驱动包:

   MySQL:
   pip install pymysql

   PostgreSQL:
   pip install psycopg2

   SQLite:
   无需安装(Python内置)

3. 连接池配置
   - SQLALCHEMY_POOL_SIZE: 连接池大小(默认5)
   - SQLALCHEMY_POOL_TIMEOUT: 连接超时时间(默认10秒)
   - SQLALCHEMY_POOL_RECYCLE: 连接自动回收时间(默认2小时)
   注意:这些配置仅对MySQL/PostgreSQL等数据库有效,SQLite不使用连接池

"""


# import os

# # 获取当前文件所在目录的绝对路径
# basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """配置类: 包含应用的所有配置项
    
    数据库配置说明:
    ----------------
    SQLALCHEMY_DATABASE_URI: 数据库连接URL,格式如下:
        MySQL: 'mysql+pymysql://用户名:密码@主机地址:端口/数据库名'
        SQLite: 'sqlite:///本地文件路径'
        PostgreSQL: 'postgresql://用户名:密码@主机地址:端口/数据库名'
        
    示例:
    - MySQL: 'mysql+pymysql://root:123456@localhost:3306/mydb'
    - SQLite: f'sqlite:///{os.path.join(basedir, "app.db")}'
    - PostgreSQL: 'postgresql://user:pass@localhost:5432/mydb'
    
    其他数据库配置项:
    ----------------
    - SQLALCHEMY_TRACK_MODIFICATIONS: 是否追踪对象修改
    - SQLALCHEMY_POOL_SIZE: 连接池大小
    - SQLALCHEMY_POOL_TIMEOUT: 连接超时时间
    - SQLALCHEMY_POOL_RECYCLE: 自动回收连接的时间
    """
    
    # ========== 数据库配置 ==========
    # 选择一种数据库配置并取消注释:
    
    # MySQL配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123321@localhost/employee_system'
    
    # SQLite配置 
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "app.db")}'
    
    # PostgreSQL配置
    # SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost:5432/employee_system'
    
    # 禁用 SQLAlchemy 的 FSADeprecationWarning 警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ========== 数据库连接池配置 ==========
    # 这些配置对 SQLite 不起作用,仅适用于 MySQL、PostgreSQL 等数据库
    SQLALCHEMY_POOL_SIZE = 10  # 连接池最大连接数
    SQLALCHEMY_POOL_TIMEOUT = 30  # 连接超时时间(秒)
    SQLALCHEMY_POOL_RECYCLE = 3600  # 自动回收连接的时间(秒)
    
    # ========== 安全配置 ==========
    # 用于各种加密操作的密钥
    # SECRET_KEY = 'your_secret_key'  # Flask的密钥
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # JWT的密钥
    """
    密钥配置指南
    -----------

    两种Web请求认证机制:
    1. 传统网页表单提交 (需要SECRET_KEY)
    - 场景: 用户通过浏览器填写HTML表单并提交
    - 示例: 
        <form action="/login" method="POST">
        <input type="text" name="username">
        <input type="password" name="password">
        <button type="submit">登录</button>
        </form>
    - 需要CSRF保护防止跨站请求伪造攻击
    
    2. API接口调用 (需要JWT_SECRET_KEY)
    - 场景: 前端通过AJAX/fetch调用后端API
    - 示例:
        fetch('/api/login', {
        headers: { 
            'Authorization': 'Bearer xxx',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: 'user', password: '123'})
        })
    - 使用JWT令牌进行身份验证

    本项目配置建议:
    --------------
    因为本项目是纯后端API服务:
    ✅ 只需保留 JWT_SECRET_KEY
    ❌ 可以删除 SECRET_KEY (因为不处理表单提交)

    JWT密钥配置:
    -----------
    1. 开发环境:
    JWT_SECRET_KEY = 'dev_jwt_key_xxx'  # 使用简单密钥即可
    
    2. 生产环境:
    # 通过环境变量配置,不要写在代码中
    JWT_SECRET_KEY = os.environ.get('FLASK_JWT_SECRET_KEY')
    
    3. 生成安全密钥:
    # 在终端执行:
    python -c 'import secrets; print(secrets.token_hex(32))'
    """
    
    
    #关于 Web开发方式对比 ：传统表单提交 vs API接口调用
    """
    1. 传统表单提交方式：
        浏览器 -> Web服务器 -> 模板引擎 -> HTML页面
        特点：
            - 前端: HTML表单 + 服务端渲染页面
            - 后端: 处理表单请求 + 返回完整HTML
            - 页面跳转: 整页刷新
            - 安全: CSRF保护
            - 适用: 内容管理系统、企业后台等传统网站
        示例：
        <!-- 前端 -->
        <form action="/users" method="POST">
        <input name="username">
        <button>提交</button>
        </form>

        <!-- 后端 Python/Flask -->
        @app.route('/users', methods=['POST'])
        def create_user():
            # 处理表单数据
            return render_template('success.html')
    2. API接口调用方式：
        前端应用 <-> API服务器 <-> 数据
        特点：
            - 前端: 单页面应用(React/Vue等)
            - 后端: 只提供API接口
            - 数据交换: JSON格式
            - 页面更新: 局部刷新
            - 安全: JWT认证
            - 适用: 移动应用、现代Web应用
        示例：
        // 前端 AJAX/fetch 调用后端API
        fetch('/api/users', {
        headers: { 
            'Authorization': 'Bearer xxx',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: 'user', password: '123'})
        })
        // 后端 Python/Flask 提供API接口
        @app.route('/api/users', methods=['POST'])
        @jwt_required
        def create_user():
            # 处理JSON数据
            return jsonify({'message': 'success'})
    
    目前大多数新项目都采用API方式，因为:
    - 前后端职责清晰
    - 多端复用API
    - 用户体验更好
    - 扩展性更强
    """