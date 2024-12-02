from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Employee
from modules.company import Company,Project
from extensions import db
from .schemas import EmployeeSchema
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
    
   