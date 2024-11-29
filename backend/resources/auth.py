from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,get_jwt
from backend.models.user import User
from backend.extensions import db, jwt_blacklist

"""
用户认证模块详细说明

主要功能：
1. 用户注册
2. 用户登录
3. 用户登出

工作流程类比：
- 就像加入一个会员系统：
  * 注册 = 填写会员申请表
  * 登录 = 刷会员卡进入
  * 登出 = 离开时交还临时权限
"""

# 创建请求解析器
"""
reqparse的作用：
1. 验证请求数据：确保必要的字段都存在
2. 清理数据：去除不需要的字段
3. 统一格式：将不同来源的数据转换为标准格式

类比：
- 就像收银员检查顾客填写的表格：
  * required=True：必填项不能空着
  * help：告诉顾客哪里填错了
"""

parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help='用户名是必需的 (Username is required)')
parser.add_argument('password', required=True, help='密码是必需的 (Password is required).')
class LoginResource(Resource):
    def post(self):
        # 解析请求参数
        """
        1. 解析请求参数：
           - 使用 reqparse 解析请求中的 `username` 和 `password` 参数
           - 如果缺少必需字段会自动返回错误
        """
        args = parser.parse_args()
        
        # 查询用户
        """
        2. 查询用户：
           - 使用 SQLAlchemy 查询数据库中是否存在该用户名的用户
        """
        user = User.query.filter_by(username=args['username']).first()
        
        # 验证密码
        """
        3. 验证密码：
           - 检查用户是否存在并且密码是否匹配
        """
        if user and user.password == args['password']:
            
            # 生成JWT token
            """
            简单的说：
            #1 JWT token = JWT token ( Header, Payload, Signature)
            #2 Signature = HMACSHA256(Header, Payload, JWT_SECRET_KEY) 
            HMACSHA256是一种加密算法，用于生成签名
            JWT_SECRET_KEY是一个密钥，保存在服务器端（config.py)。

            所以显而易见，服务器有JWT_SECRET_KEY（客户端没有），所以，可以通过#2快速验证（客户端无法伪造JWT token）。
            
            
            4. 生成JWT token：
            - 使用 `create_access_token` 生成JWT token
            - `identity` 参数为用户的ID
            - `create_access_token` 函数会根据配置的 `JWT_SECRET_KEY` 对用户ID进行加密，生成一个JWT token。
            - JWT token 由三部分组成：
                1. Header：包含令牌类型（JWT）和签名算法（如HS256）。
                2. Payload：包含用户的身份信息（如用户ID）和其他声明（如过期时间）。
                3. Signature：使用 `JWT_SECRET_KEY` 对Header和Payload进行签名，确保令牌的完整性和真实性。
            - 生成过程：
                1. Header 和 Payload 使用 Base64 编码。
                2. 使用 `JWT_SECRET_KEY` 对编码后的 Header 和 Payload 进行签名。
                3. 将 Header、Payload 和 Signature 用点（`.`）连接起来，形成最终的JWT token。
            """
            token = create_access_token(identity=user.id)
            
            # 返回响应
            """
            5. 返回响应：
            - 返回包含JWT token和用户信息的响应
            - 响应内容包括：
                1. `token`：生成的JWT token。
                2. `user`：用户信息，包括用户ID和用户名。
            - 示例响应：
                {
                    'token': '<JWT token>',
                    'user': {
                        'id': user.id,
                        'username': user.username
                    }
                }
            """
            return {'token': token, 'user': {'id': user.id, 'username': user.username}}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

class RegisterResource(Resource):
    """
    用户注册资源
    
    工作流程：
    1. 接收注册请求（POST方法）
    2. 验证用户提供的信息
    3. 创建新用户记录
    4. 保存到数据库
    5. 返回注册结果
    
    就像填写新会员申请表：
    - 确保信息完整
    - 创建会员档案
    - 存入会员系统
    - 通知申请结果
    """

    def post(self):
        """
        处理用户注册请求
        
        以下有步骤说明：
        """
    
        # 获取并验证用户提供的数据
        """
        1. parser.parse_args()：
           - 检查并提取请求中的用户名和密码
           - 如果缺少必需字段会自动返回错误
        """

        args = parser.parse_args()
        
        try:
            # 检查用户名是否已存在
            """
            为什么要检查用户名：
            1. 防止重复注册
            2. 保证用户名的唯一性
            3. 提供明确的错误提示
            """
            if User.query.filter_by(username=args['username']).first():
                return {
                    'success': False,
                    'message': '用户名已存在 (Username already exists)'
                }, 400
            
            # 创建新用户
            """
            2. User()创建新用户：
            - 根据提供的信息创建用户对象
            - 此时用户还未保存到数据库
            """
            user = User(
                username=args['username'],
                password=args['password']  # 注意：实际应用中应该加密存储
            )
            
            # 保存到数据库
            """
            3. db.session.add()：
            - 将新用户添加到数据库会话
            - 类似购物车，先添加但还未付款
            4. db.session.commit()：
            - 提交更改到数据库
            - 相当于真正付款，变更永久保存
            """
            """
            数据库会话管理：
            1. add(): 将对象加入session（暂存）
            2. commit(): 提交所有变更（永久保存）
            3. 出错时自动回滚（撤销所有变更）
            """
            db.session.add(user)
            db.session.commit()
            
            """
            返回值：
            - success: 注册是否成功
            - message: 结果说明
            - HTTP状态码201: 表示资源创建成功
            """
            
            return {
                'success': True,
                'message': '用户注册成功 (User registered successfully)',
                'user': {
                    'id': user.id,
                    'username': user.username
                }
            }, 201
            
        except Exception as e:
            """
            错误处理：
            1. 回滚数据库会话
            2. 返回错误信息
            3. 使用500状态码表示服务器错误
            """
            db.session.rollback()
            return {
                'success': False,
                'message': f'注册过程中出错 (Error during registration): {str(e)}'
            }, 500

    """
    使用示例：

    1. 发送注册请求：
    POST /api/auth/register
    Content-Type: application/json

    {
        "username": "zhang_san",
        "password": "my_password123"
    }

    2. 成功响应：
    {
        "success": true,
        "message": "用户注册成功",
        "user": {
            "id": 1,
            "username": "zhang_san"
        }
    }

    3. 用户名已存在：
    {
        "success": false,
        "message": "用户名已存在"
    }
    """


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        jwt_blacklist.add(jti)
        return {'success': True, 'message': 'Logged out successfully'}, 200