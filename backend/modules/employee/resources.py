from flask import request # 用于debug log
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Employee
from modules.company import Company,Project
from extensions import db
from .schemas import EmployeeSchema
from datetime import datetime  # 修正datetime导入

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


class ActiveEmployeesResource(Resource):
    """
        处理GET请求，返回在岗和待岗员工列表

        工作流程:
        1. 使用JWT认证确保请求合法
        2. 查询状态为'在岗'或'待岗'的员工
        3. 使用EmployeeSchema将查询结果序列化为JSON格式
        4. 返回序列化数据和200状态码
    """
    @jwt_required()
    def get(self):
        try:
            employees = Employee.query.filter(Employee.status.in_(['在岗', '待岗'])).all()
            return {'employees': employees_schema.dump(employees)}, 200
        except Exception as e:
            return {'message': f'获取在岗员工列表时出错 (Error retrieving active employees list): {str(e)}'}, 500

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help='Name is required.')
parser.add_argument('position', required=True, help='Position is required.')
parser.add_argument('hire_date', required=True, help='Hire date is required.', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date())


class AddEmployeeResource(Resource):
    @jwt_required()
    def post(self):
        try:
            # 打印请求数据
            print("Request data:", request.get_json())
            
            args = parser.parse_args()
            
            # 打印解析后的参数
            print(f"Parsed args: {args}")
            
            user_id = get_jwt_identity()
            
            # 打印用户ID
            print(f"User ID: {user_id}")
            
            # 创建新员工对象
            employee = Employee(
                name=args['name'],
                position=args['position'],
                hire_date=args['hire_date'],  # 使用解析后的日期字段
                status='待岗',
                creator_id=user_id
            )
            
            # 将新员工对象添加到数据库会话
            db.session.add(employee)
            db.session.commit()
            
            # 返回新员工对象的序列化数据，结构与GET /api/active-employees一致
            return {'employee': employee_schema.dump(employee)}, 201
        
        except Exception as e:
            # 打印错误信息
            print(f"Error: {str(e)}")
            # 返回错误响应
            return {'message': f'添加员工时出错 (Error adding employee): {str(e)}'}, 500