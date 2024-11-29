from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.models.user import User
from backend.extensions import db

parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help='Username is required.')
parser.add_argument('password', required=True, help='Password is required.')

class LoginResource(Resource):
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user and user.password == args['password']:
            token = create_access_token(identity=user.id)
            return {'token': token, 'user': {'id': user.id, 'username': user.username}}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

class RegisterResource(Resource):
    def post(self):
        args = parser.parse_args()
        user = User(username=args['username'], password=args['password'])
        db.session.add(user)
        db.session.commit()
        return {'success': True, 'message': 'User registered successfully'}, 201

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        # 可以在此处添加JWT黑名单逻辑
        return {'success': True, 'message': 'Logged out successfully'}, 200