from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import ChangeRequest
from modules.employee import Employee
# from modules.company import Company, Project
from extensions import db
from .schemas import ChangeSchema
from datetime import datetime

# 创建 ChangeSchema 实例，用于序列化和反序列化 ChangeRequest 对象
change_schema = ChangeSchema()
changes_schema = ChangeSchema(many=True)

# 创建请求解析器（Request Parser），用于解析请求参数
parser = reqparse.RequestParser()
parser.add_argument('type', required=True, help='类型是必需的 (Type is required)')
parser.add_argument('employee_id', required=True, type=int)
parser.add_argument('from_company_id', type=int)
parser.add_argument('to_company_id', type=int)
parser.add_argument('from_project_id', type=int)
parser.add_argument('to_project_id', type=int)
parser.add_argument('effective_date', required=True, type=lambda x: datetime.strptime(x, '%Y-%m-%d').date())

class PendingChangesResource(Resource):
    """
    PendingChangesResource 类，用于处理获取待确认变动名单的请求

        处理 GET 请求，返回待确认变动名单

        工作流程:
        1. 使用 JWT 认证确保请求合法
        2. 查询状态为 '待确认' 的变动请求
        3. 使用 ChangeSchema 将查询结果序列化为 JSON 格式
        4. 返回序列化数据和 200 状态码
    """
    @jwt_required()
    def get(self):
        try:
            changes = ChangeRequest.query.filter_by(status='待确认').all()
            return {'changes': changes_schema.dump(changes)}, 200
        except Exception as e:
            return {'message': f'获取待确认变动名单时出错: {str(e)}'}, 500
 
class EmployeeTransferResource(Resource):
    """
    员工调岗资源类（Employee Transfer Resource Class）
    
    主要功能：
    - 处理员工调岗申请
    - 创建调岗变动记录
    - 返回处理结果
    
    """

    @jwt_required()  # JWT令牌（token）验证装饰器（decorator）
    def put(self, id):
        """
        处理PUT请求，创建员工调岗申请
        
        参数（Parameters）:
        - id: 员工ID（从URL路径获取）
        
        """
        
        # 1. 创建参数解析器（argument parser）
        """
        参数解析器的作用：
        - 验证请求数据的完整性
        - 确保所有必需字段都存在
        - 提供清晰的错误提示
        """
        parser = reqparse.RequestParser()
        parser.add_argument('new_company', required=True, help='新公司ID是必需的')
        parser.add_argument('new_project', required=True, help='新项目ID是必需的')
        parser.add_argument('effective_date', required=True, help='生效日期是必需的')
        
        # 2. 解析请求参数
        """
        解析请求参数：
        - 从HTTP请求体中提取数据
        - 转换为Python对象便于处理
        """
        args = parser.parse_args()
        user_id = get_jwt_identity()  # 获取当前用户ID
        
        # 3. 查询员工信息
        """
        数据库查询（Database Query）：
        - 使用Employee模型类查询指定ID的员工
        - 如果找不到员工，返回404错误
        """
        employee = Employee.query.get(id)
        if not employee:
            return {'message': '未找到员工'}, 404
        
        try:
            # 4. 创建调岗变动请求（Change Request）
            """
            变动请求记录包含：
            - 变动类型：'调岗'
            - 员工信息：employee_id
            - 原公司和项目：from_company_id, from_project_id
            - 新公司和项目：to_company_id, to_project_id
            - 生效日期：effective_date
            - 状态：'待确认'
            """
            change = ChangeRequest(
                type='调岗',
                employee_id=employee.id,
                from_company_id=employee.company_id,
                to_company_id=args['new_company'],
                from_project_id=employee.project_id,
                to_project_id=args['new_project'],
                effective_date=datetime.strptime(args['effective_date'], '%Y-%m-%d').date(),
                status='待确认',
                creator_id=user_id  # 添加创建者ID
            )
            
            # 5. 保存到数据库
            db.session.add(change)
            db.session.commit()
            
            # 6. 返回成功响应
            return {
                "success": True,
                "message": "调岗申请已提交"
            }, 200
        
        except Exception as e:
            # 错误处理
            return {
                "message": f"提交调岗申请时出错: {str(e)}"
            }, 500

class EmployeeResignResource(Resource):
    """
    员工离职资源类（Employee Resignation Resource Class）
    
    主要功能：
    - 处理员工离职申请
    - 创建离职变动记录
    - 返回处理结果
    
    工作流程类比：
    - 就像员工提交离职申请表：
      * 注明预计离职日期
      * 提交给人事部门审批
    """

    @jwt_required()
    def put(self, id):
        """
        处理PUT请求，创建员工离职申请
        
        参数（Parameters）:
        - id: 员工ID（从URL路径获取）
        
        返回（Returns）:
        - 成功：{'success': True, 'message': '离职申请已提交'}, 200
        - 失败：{'message': '未找到员工'}, 404
        """
        
        # 1. 创建参数解析器
        parser = reqparse.RequestParser()
        parser.add_argument('resign_date', required=True, help='离职日期是必需的')
        
        # 2. 解析请求参数
        args = parser.parse_args()
        user_id = get_jwt_identity()  # 获取当前用户ID

        
        # 3. 查询员工信息
        """
        查询数据库中的员工记录：
        - 使用员工ID查询
        - 验证员工是否存在
        """
        employee = Employee.query.get(id)
        if not employee:
            return {'message': '未找到员工'}, 404
        
        try:
            # 4. 创建离职变动请求
            """
            创建离职变动记录：
            - 记录当前员工所属公司和项目
            - 设置变动类型为'离职'
            - 记录预计离职日期
            - 初始状态设为'待确认'
            """
            change = ChangeRequest(
                type='离职',
                employee_id=employee.id,
                from_company_id=employee.company_id,
                from_project_id=employee.project_id,
                effective_date=datetime.strptime(args['resign_date'], '%Y-%m-%d').date(),
                status='待确认',
                creator_id=user_id  # 添加创建者ID
            )
            
            # 5. 保存到数据库
            db.session.add(change)
            db.session.commit()
            
            # 6. 返回成功响应
            return {'success': True, 'message': '离职申请已提交'}, 200
        
        except Exception as e:
            # 错误处理
            return {
                "message": f"提交离职申请时出错: {str(e)}"
            }, 500

class ApproveChangeResource(Resource):
    """
    ApproveChangeResource 类，用于处理确认变动申请的请求

    方法:
    - put: 处理 PUT 请求，确认变动申请
    """
    @jwt_required()
    def put(self, id):
        """
        处理 PUT 请求，确认变动申请

        参数:
        - id: 变动请求 ID（从 URL 路径获取）

        返回:
        - 成功：{'success': True, 'message': '变更请求已批准 (Change request approved)'}, 200
        - 失败：{'message': '未找到变更请求 (Change request not found)'}, 404
        - 失败：{'message': '变更请求已处理 (Change request already processed)'}, 400

        工作流程:
        1. 使用 JWT 认证确保请求合法
        2. 查询指定 ID 的变动请求
        3. 如果变动请求不存在，返回 404 错误
        4. 如果变动请求状态不是 '待确认'，返回 400 错误
        5. 更新变动请求状态为 '已确认'
        6. 根据变动类型更新员工信息
        7. 提交数据库事务
        8. 返回成功响应
        """
        change = ChangeRequest.query.get(id)
        if not change:
            return {'message': '未找到变更请求 (Change request not found)'}, 404
        if change.status != '待确认':
            return {'message': '变更请求已处理 (Change request already processed)'}, 400
        
        # 更新变动请求状态为已确认
        change.status = '已确认'
        
        # 更新员工信息
        employee = Employee.query.get(change.employee_id)
        if change.type == '调岗':
            employee.company_id = change.to_company_id
            employee.project_id = change.to_project_id
            employee.hire_date = change.effective_date  # 更新 hire_date 为 effective_date
        elif change.type == '离职':
            employee.status = '离职'
            employee.hire_date = change.effective_date  # 更新 hire_date 为 effective_date
        
        # 提交数据库事务
        db.session.commit()
        
        return {'success': True, 'message': '变更请求已批准 (Change request approved)'}, 200

class RejectChangeResource(Resource):
    """
    RejectChangeResource 类，用于处理拒绝变动申请的请求

    方法:
    - put: 处理 PUT 请求，拒绝变动申请
    """
    @jwt_required()
    def put(self, id):
        """
        处理 PUT 请求，拒绝变动申请

        参数:
        - id: 变动请求 ID（从 URL 路径获取）

        返回:
        - 成功：{'success': True, 'message': '变更请求已拒绝 (Change request rejected)'}, 200
        - 失败：{'message': '未找到变更请求 (Change request not found)'}, 404
        - 失败：{'message': '变更请求已处理 (Change request already processed)'}, 400

        工作流程:
        1. 使用 JWT 认证确保请求合法
        2. 查询指定 ID 的变动请求
        3. 如果变动请求不存在，返回 404 错误
        4. 如果变动请求状态不是 '待确认'，返回 400 错误
        5. 更新变动请求状态为 '已拒绝'
        6. 提交数据库事务
        7. 返回成功响应
        """
        change = ChangeRequest.query.get(id)
        if not change:
            return {'message': '未找到变更请求 (Change request not found)'}, 404
        if change.status != '待确认':
            return {'message': '变更请求已处理 (Change request already processed)'}, 400
        
        # 更新变动请求状态为已拒绝
        change.status = '已拒绝'
        
        # 提交数据库事务
        db.session.commit()
        
        return {'success': True, 'message': '变更请求已拒绝 (Change request rejected)'}, 200