from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.employee import Employee
from backend.models.company import Company
from backend.models.project import Project
from backend.extensions import db
from schemas.employee_schema import EmployeeSchema
import datetime

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help='Name is required.')
parser.add_argument('position', required=True, help='Position is required.')
parser.add_argument('hire_date', required=True, help='Hire date is required.', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date())
parser.add_argument('company_id', type=int)
parser.add_argument('project_id', type=int)

class ActiveEmployeesResource(Resource):
    @jwt_required()
    def get(self):
        employees = Employee.query.filter(Employee.status.in_(['在岗', '待岗'])).all()
        return employees_schema.dump(employees), 200

class AddEmployeeResource(Resource):
    @jwt_required()
    def post(self):
        args = parser.parse_args()
        user_id = get_jwt_identity()
        company = Company.query.get(args['company_id'])
        if not company:
            return {'message': 'Company not found'}, 404
        project = Project.query.get(args['project_id']) if args['project_id'] else None
        if project and project.company_id != args['company_id']:
            return {'message': 'Project does not belong to the specified company'}, 400
        employee = Employee(
            name=args['name'],
            position=args['position'],
            hire_date=args['hire_date'],
            status='待岗',
            company_id=args['company_id'],
            project_id=args['project_id'],
            creator_id=user_id
        )
        db.session.add(employee)
        db.session.commit()
        return employee_schema.dump(employee), 201