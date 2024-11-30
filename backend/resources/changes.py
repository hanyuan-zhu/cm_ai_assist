from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.change_request import ChangeRequest
from backend.models.employee import Employee
from backend.models.company import Company
from backend.models.project import Project
from backend.extensions import db
from schemas.change_schema import ChangeSchema
import datetime

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

    方法:
    - get: 处理 GET 请求，返回待确认变动名单
    """
    @jwt_required()
    def get(self):
        """
        处理 GET 请求，返回待确认变动名单

        工作流程:
        1. 使用 JWT 认证确保请求合法
        2. 查询状态为 '待确认' 的变动请求
        3. 使用 ChangeSchema 将查询结果序列化为 JSON 格式
        4. 返回序列化数据和 200 状态码
        """
        changes = ChangeRequest.query.filter_by(status='待确认').all()
        return changes_schema.dump(changes), 200

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