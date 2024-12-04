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
from extensions import db, jwt,jwt_blacklist, migrate  # 导入需要的Flask扩展
from routes import initialize_routes  # 导入API路由初始化函数
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS


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
        
    # 初始化各种Flask扩展
    # 这些扩展为应用添加额外功能：
    db.init_app(app)   # SQLAlchemy：数据库操作能力
    
    # 初始化迁移
    migrate.init_app(app, db)

    jwt.init_app(app)  # JWT：用户认证功能
    
    CORS(app)  # 允许所有来源的跨域请求

    # 在此处初始化 Api 对象，直接传入 app
    api = Api(app)
    
    # 注册所有API路由
    # 设置所有的API端点（URLs）
    initialize_routes(api,app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in jwt_blacklist

    return app

# 当直接运行此文件时（而不是作为模块导入时）
if __name__ == '__main__':
    app = create_app()  # 使用工厂函数创建应用实例
    app.run(debug=True)  # 以调试模式运行服务器
    # debug=True 允许:
    # - 代码修改后自动重启
    # - 显示详细的错误信息
    # 注意：生产环境中应禁用debug模式