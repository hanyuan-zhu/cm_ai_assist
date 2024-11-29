from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.change_request import ChangeRequest
from backend.models.employee import Employee
from backend.models.company import Company
from backend.models.project import Project
from backend.extensions import db
from schemas.change_schema import ChangeSchema
import datetime
change_schema = ChangeSchema()
changes_schema = ChangeSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument('type', required=True, help='Type is required.')
parser.add_argument('employee_id', required=True, type=int)
parser.add_argument('from_company_id', type=int)
parser.add_argument('to_company_id', type=int)
parser.add_argument('from_project_id', type=int)
parser.add_argument('to_project_id', type=int)
parser.add_argument('effective_date', required=True, type=lambda x: datetime.strptime(x, '%Y-%m-%d').date())

class PendingChangesResource(Resource):
    @jwt_required()
    def get(self):
        changes = ChangeRequest.query.filter_by(status='待确认').all()
        return changes_schema.dump(changes), 200

class ApproveChangeResource(Resource):
    @jwt_required()
    def put(self, id):
        change = ChangeRequest.query.get(id)
        if not change:
            return {'message': 'Change request not found'}, 404
        if change.status != '待确认':
            return {'message': 'Change request already processed'}, 400
        # 处理变动逻辑
        change.status = '已确认'
        db.session.commit()
        return {'success': True, 'message': 'Change request approved'}, 200

class RejectChangeResource(Resource):
    @jwt_required()
    def put(self, id):
        change = ChangeRequest.query.get(id)
        if not change:
            return {'message': 'Change request not found'}, 404
        if change.status != '待确认':
            return {'message': 'Change request already processed'}, 400
        change.status = '已拒绝'
        db.session.commit()
        return {'success': True, 'message': 'Change request rejected'}, 200