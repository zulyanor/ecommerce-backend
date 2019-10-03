from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_claims, jwt_required
from flask_bcrypt import Bcrypt
from blueprints import app

# import user model
from ..user.model import User

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)
bcrypt = Bcrypt(app)

class CreateTokenResource(Resource):

    """
    class to create token for user that log in
    """

    def post(self):

        '''
        method to create the token
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)

        data = parser.parse_args()

        '''to check the username and password in the database'''
        user_query = User.query.filter_by(username = data['username']).first()
        
        if user_query == None:
            return {'Status':'User Not Found'}, 404
        
        if not bcrypt.check_password_hash(user_query.password, data['password']):
            return {'Status':'Invalid Password'}, 401
        
        '''response field to be inserted into jwt claims'''
        user_data = marshal(user_query, User.jwt_response_fields)

        token = create_access_token(identity = user_query.username, user_claims = user_data)

        return {'token':token, 'message':'Login Success'}, 200

api.add_resource(CreateTokenResource, '')