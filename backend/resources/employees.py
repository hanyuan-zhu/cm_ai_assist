from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.employee import Employee
from models.company import Company
from models.project import Project
from models.change_request import ChangeRequest  # 新增导入
from extensions import db
from schemas.employee_schema import EmployeeSchema
from schemas.change_schema import ChangeSchema  # 新增导入
from datetime import datetime  # 修正datetime导入

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help='Name is required.')
parser.add_argument('position', required=True, help='Position is required.')
parser.add_argument('hire_date', required=True, help='Hire date is required.', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date())

class ActiveEmployeesResource(Resource):
    """
    ActiveEmployeesResource类，用于处理获取在岗和待岗员工列表的请求

    方法:
    - get: 处理GET请求，返回在岗和待岗员工列表
    """
    @jwt_required()
    def get(self):
        """
        处理GET请求，返回在岗和待岗员工列表

        工作流程:
        1. 使用JWT认证确保请求合法
        2. 查询状态为'在岗'或'待岗'的员工
        3. 使用EmployeeSchema将查询结果序列化为JSON格式
        4. 返回序列化数据和200状态码
        """
        employees = Employee.query.filter(Employee.status.in_(['在岗', '待岗'])).all()
        return employees_schema.dump(employees), 200

class AddEmployeeResource(Resource):
    @jwt_required()
    def post(self):
        args = parser.parse_args()
        user_id = get_jwt_identity()
        
        # 创建新员工对象
        # 刚入职的员工，只需要提供姓名，岗位和入职时间，默认待岗，所以这里没有公司和项目信息。
        employee = Employee(
            name=args['name'],
            position=args['position'],
            hire_date=args['hire_date'],
            status='待岗',
            creator_id=user_id
        )
        
        # 将新员工对象添加到数据库会话
        db.session.add(employee)
        db.session.commit()
        
        # 返回新员工对象的序列化数据
        return employee_schema.dump(employee), 201
    
    
class EmployeeTransferResource(Resource):
    """
    员工调岗资源类（Employee Transfer Resource Class）
    
    主要功能：
    - 处理员工调岗申请
    - 创建调岗变动记录
    - 返回处理结果
    
    工作流程类比：
    - 就像员工提交调岗申请表：
      * 填写当前部门和目标部门
      * 注明预期生效日期
      * 提交给人事部门审批
    """

    @jwt_required()  # JWT令牌（token）验证装饰器（decorator）
    def put(self, id):
        """
        处理PUT请求，创建员工调岗申请
        
        参数（Parameters）:
        - id: 员工ID（从URL路径获取）
        
        返回（Returns）:
        - 成功：{'success': True, 'message': '调岗申请已提交'}, 200
        - 失败：{'message': '未找到员工'}, 404
        """
        
        # 1. 创建参数解析器（argument parser）
        """
        参数解析器的作用：
        - 验证请求数据的完整性
        - 确保所有必需字段都存在
        - 提供清晰的错误提示
        """
        parser = reqparse.RequestParser()
        parser.add_argument('newCompany', required=True, help='新公司ID是必需的')
        parser.add_argument('newProject', required=True, help='新项目ID是必需的')
        parser.add_argument('effectiveDate', required=True, help='生效日期是必需的')
        
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
            to_company_id=args['newCompany'],
            from_project_id=employee.project_id,
            to_project_id=args['newProject'],
            effective_date=datetime.strptime(args['effectiveDate'], '%Y-%m-%d').date(),
            status='待确认',
            creator_id=user_id  # 添加创建者ID
        )
        
        # 5. 保存到数据库
        """
        数据库事务（Database Transaction）：
        - add()：将变动请求添加到数据库会话
        - commit()：提交更改到数据库
        """
        db.session.add(change)
        db.session.commit()
        
        # 6. 返回成功响应
        return {'success': True, 'message': '调岗申请已提交'}, 200

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
        parser.add_argument('resignDate', required=True, help='离职日期是必需的')
        
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
            effective_date=datetime.strptime(args['resignDate'], '%Y-%m-%d').date(),
            status='待确认',
            creator_id=user_id  # 添加创建者ID

        )
        
        # 5. 保存到数据库
        """
        保存变动请求：
        - 将新建的变动请求添加到数据库会话
        - 提交变更到数据库
        """
        db.session.add(change)
        db.session.commit()
        
        # 6. 返回成功响应
        return {'success': True, 'message': '离职申请已提交'}, 200

"""
使用示例（Usage Examples）：

1. 提交调岗申请：
PUT /api/employees/1/transfer
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "newCompany": 2,
    "newProject": 3,
    "effectiveDate": "2024-03-20"
}

2. 提交离职申请：
PUT /api/employees/1/resign
Content-Type: application/json
Authorization: Bearer <JWT_TOKEN>

{
    "resignDate": "2024-04-01"
}
"""