from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_bcrypt import Bcrypt
from blueprints import db, app

# import user and user detail model
from ..user.model import User
from ..user_detail.model import UserDetail

import json

bp_user = Blueprint('user', __name__)
api = Api(bp_user)
bcrypt = Bcrypt(app)

##############
# Resources
##############

class UserRegisterResource(Resource):

    """
    class for register resource
    """

    def post(self):

        '''
        method to register new user
        '''
        parser = reqparse.RequestParser()
        
        '''for user table'''
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        parser.add_argument('gender', location = 'json', required = True)

        data = parser.parse_args()

        '''hashing password'''
        password_hash = bcrypt.generate_password_hash(data['password'])

        '''check if username already exist'''
        all_data = User.query.all()

        existing_username = [item.username for item in all_data]

        if data['username'] in existing_username:
            return {'Status':'User already exist'}, 422

        user = User(
            data['username'], 
            data['email'], 
            password_hash, 
            data['gender']
        )

        db.session.add(user)
        db.session.commit()

        '''get the user id from the newly created user to make row in user deetail table'''
        user_id = user.id
        user_detail = UserDetail(
            int(user_id),
            "Please Enter Your Full Name",
            "Please Enter Your Address",
            "Please Enter Your Phone Number"
        )
        db.session.add(user_detail)
        db.session.commit()

        app.logger.debug('DEBUG: %s', user)

        return marshal(user, User.response_fields), 200, {'Content-Type':'application/json'}

class UserResource(Resource):

    """
    class for user resources
    """

    @jwt_required
    def get(self, id):

        '''
        method to get single user by id
        '''
        user_query = User.query.get(id)
        user_detail_query = UserDetail.query.get(id)

        if user_query is not None:
            result =  marshal(user_query, User.view_response_fields)
            result['full_name'] = user_detail_query.full_name
            result['address'] = user_detail_query.address
            result['phone'] = user_detail_query.phone

            return result, 200, {'Content-Type' : 'application/json'}

        return {'status':'user doesn\'t exist'}, 404
    
    @jwt_required
    def put(self, id):

        '''
        method to edit user profile
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('email', location = 'json', required = False)
        parser.add_argument('password', location = 'json', required = False)
        parser.add_argument('full_name', location = 'json', required = False)
        parser.add_argument('address', location = 'json', required = False)
        parser.add_argument('phone', location = 'json', required = False)

        data = parser.parse_args()

        user_query = User.query.get(id)
        user_detail_query = UserDetail.query.get(id)

        '''for user'''
        if data['email'] is not None:
            user_query.email = data['email']
        if data['password'] is not None:
            user_query.password = bcrypt.generate_password_hash(data['paswword'])

        '''for user detail'''
        if data['full_name'] is not None:
            user_detail_query.full_name = data['full_name']
        if data['address'] is not None:
            user_detail_query.address = data['address']
        if data['phone'] is not None:
            user_detail_query.phone = data['phone']
        
        '''to save changes into database'''
        db.session.commit()

        return {'status':'edit profile success'}, 200
    
api.add_resource(UserRegisterResource, '', '/register')
api.add_resource(UserResource, '', '/<id>')