"""
app.py - Flask应用程序的入口文件

这个模块负责创建和配置Flask应用实例。它使用"工厂模式"来创建应用，
这种方式允许我们轻松创建多个应用实例（如测试环境和生产环境）。

工厂模式类比：
- 就像开连锁餐厅，每家分店（应用实例）可能需要不同的配置
- create_app() 就像是标准化的"开店指南"
- 可以根据需要创建不同配置的应用实例
"""

from flask import Flask  # Flask是Web框架,用于创建Web应用
from config import Config  # 导入配置文件,包含数据库URL等设置
from extensions import db, api, jwt  # 导入需要的Flask扩展
from resources import initialize_routes  # 导入API路由初始化函数

def create_app():
    """
    创建并配置Flask应用实例的工厂函数
    
    工作流程：
    1. 创建Flask应用实例（相当于获取"营业执照"）
    2. 加载配置（设置应用的各种参数）
    3. 初始化扩展（添加额外功能）
    4. 注册路由（设置API端点）
    5. 准备数据库（创建必要的表）
    
    Flask应用实例的核心功能：
    - config: 配置管理（如app.config.from_object()）
    - init_app(): 扩展初始化接口
    - route(): 路由注册
    - app_context(): 应用上下文管理
    
    返回:
        Flask: 配置完成的Flask应用实例
    """
    # 创建Flask应用实例 
    app = Flask(__name__)
    """
    创建app对象后，它就具备了以下内置功能：

    1. 配置管理能力:
    app.config.from_object(Config)  # 可以加载配置
    app.config['DEBUG'] = True      # 可以直接设置配置

    2. 扩展插件集成能力:
    app.register_blueprint(...)     # 可以注册蓝图
    db.init_app(app)               # 可以初始化数据库
    jwt.init_app(app)              # 可以添加JWT认证

    3. 路由管理能力:
    @app.route('/hello')           # 可以注册路由
    def hello():
        return 'Hello World'

    4. 上下文管理能力:
    with app.app_context():        # 可以创建应用上下文
        db.create_all()

    这就像Flask给了app对象一个"工具箱":
    - config: 用来存放各种设置
    - init_app(): 用来让各种插件和app关联
    - route(): 用来设置URL路径
    - app_context(): 用来管理应用的运行环境
    """
    # 关于 __name__ 变量的说明
    """
    关于 __name__ 变量的说明：

    1. 特殊变量的定义：
    - __name__ 是Python的一个内置"魔法变量"（双下划线变量）
    - 它会根据文件的执行方式动态变化

    2. __name__ 的两种值：
    - 直接运行文件时：__name__ == "__main__"
    - 作为模块导入时：__name__ == "模块名"

    3. 在Flask中的作用：
    - 帮助Flask定位应用根目录
    - 用于查找模板和静态文件
    - 协助调试和错误追踪
    
    示例：
    如果这个文件叫 app.py：
    - 直接运行 python app.py 时：__name__ == "__main__"
    - 被其他文件导入时：__name__ == "app"

    这就像给应用一个"身份证"，让Flask知道：
    - 谁在运行这个应用
    - 从哪里查找资源文件
    - 如何正确显示错误信息
    """
    
    # 从Config对象加载配置
    # 可以设置数据库URL、密钥等重要参数
    app.config.from_object(Config)
    
    """
    Flask应用上下文(Application Context)详细说明

    什么是上下文？
    想象你在一个大型办公楼里工作：
    - 上下文就像是你的办公室环境
    - 不同部门(应用)有不同的门禁卡(配置)和办公用品(资源)
    - 你需要在正确的办公室里才能使用该部门的资源

    with app.app_context(): 具体做什么：
    1. 进入办公室：
    - 刷门禁卡进入特定办公室(创建应用上下文)
    - 获得使用办公设备的权限(访问应用资源的权限)

    2. 工作过程：
    - 可以使用办公室里的所有设备(应用的所有资源)
    - 比如打印机(数据库)、文件柜(配置)等

    3. 离开办公室：
    - 自动关灯、锁门(清理资源)
    - 交还临时使用的设备(释放资源)

    实际例子：
    """
    """
    # 错误示例 - 没有上下文
    db.create_all()  # ❌ 报错：RuntimeError: No application context

    # 正确示例 - 使用上下文
    with app.app_context():    # 创建一个安全的工作环境
        db.create_all()       # ✅ 在正确的环境中创建数据库表
    """ 
    """
    为什么需要上下文？

    1. 安全性：
    - 确保操作在正确的应用环境中执行
    - 防止意外访问错误的资源

    2. 资源管理：
    - 自动管理资源的分配和释放
    - 防止资源泄露

    3. 多应用支持：
    - Flask可以同时运行多个应用
    - 上下文帮助区分当前是哪个应用在工作

    常见使用场景：
    """
    """
    # 1. 数据库操作
    with app.app_context():
        # 创建新用户
        new_user = User(username="张三")
        db.session.add(new_user)
        db.session.commit()

    # 2. 访问配置
    with app.app_context():
        # 获取配置信息
        secret_key = app.config['SECRET_KEY']

    # 3. 后台任务
    def background_job():
        with app.app_context():
            # 在这里执行需要应用上下文的操作
            process_data()
    """
    """
    注意事项：

    1. 在Flask路由函数中不需要手动创建上下文：
    @app.route('/')
    def index():
        # Flask自动处理上下文
        return 'Hello'

    2. 在测试中经常需要上下文：
    def test_something():
        with app.app_context():
            # 执行测试代码

    3. 错误处理：
    try:
        with app.app_context():
            # 你的代码
    except RuntimeError as e:
        print("上下文错误:", str(e))
    """    
    
    # 初始化各种Flask扩展
    # 这些扩展为应用添加额外功能：
    db.init_app(app)   # SQLAlchemy：数据库操作能力
    api.init_app(app)  # Flask-RESTful：REST API支持
    jwt.init_app(app)  # JWT：用户认证功能
    
    # 注册所有API路由
    # 设置所有的API端点（URLs）
    initialize_routes(api)
    
    # 创建所有数据库表
    # 使用应用上下文确保在正确的环境中创建表
    with app.app_context():
        db.create_all()
    
    return app

# 当直接运行此文件时（而不是作为模块导入时）
if __name__ == '__main__':
    app = create_app()  # 使用工厂函数创建应用实例
    app.run(debug=True)  # 以调试模式运行服务器
    # debug=True 允许:
    # - 代码修改后自动重启
    # - 显示详细的错误信息
    # 注意：生产环境中应禁用debug模式