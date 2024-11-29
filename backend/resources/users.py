from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from schemas.user_schema import UserSchema

user_schema = UserSchema()

class UserMeResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': '未找到用户 (User not found)'}, 404
        return user_schema.dump(user), 200