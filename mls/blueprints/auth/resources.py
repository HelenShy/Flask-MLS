from flask import Flask, Blueprint, request, jsonify
from flask_restplus import Api, Resource, reqparse, fields

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                set_access_cookies, set_refresh_cookies, unset_jwt_cookies,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,
                                current_user)

from .models import User, UserSchema
import datetime

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_api = Api(auth_blueprint)

# Namespaces
ns_users = auth_api.namespace('users', description='API endpoints for operations on single user')
ns_token = auth_api.namespace('token', description='API endpoints for operations on tokens')

# Parsers
parser = auth_api.parser()
parser.add_argument('username', type=str, help='This field cannot be blank', required=True, location='form')
parser.add_argument('password', type=str, help='This field cannot be blank', required=True, location='form')
parser.add_argument('email', type=str, help='This field cannot be blank', required=False, location='form')

parser_login = auth_api.parser()
parser_login.add_argument('username', type=str, help='This field cannot be blank', required=True, location='form')
parser_login.add_argument('password', type=str, help='This field cannot be blank', required=True, location='form')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# @ns_user.route('/hello')
# class UserRegistration(Resource):
#     @jwt_required
#     def get(self):
#         return {'message': 'Ok'}


@ns_users.route('/register')
@ns_users.expect(parser)
class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = User(
            username=data['username'],
            password=data['password'],
            email=data['email']
        )
        try:
            new_user.save()

            resp = jsonify({'register': 'True'})
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        except:
            return {'message': 'Something went wrong'}, 500


@ns_users.route('/login')
@ns_users.expect(parser_login)
class UserLogin(Resource):
    def post(self):
        data = parser_login.parse_args()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn`t exist '.format(data['username'])}
        if current_user.check_password(data['password']):
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(identity=data['username'], expires_delta=expires)
            refresh_token = create_refresh_token(identity=data['username'])
            resp = jsonify({'login': 'True'})
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp
        else:
            return {'message': 'Invalid identity or password'}


@ns_users.route('/edit')
@ns_users.expect(parser)
class UserEditMail(Resource):
    @jwt_required
    def put(self):
        data = parser.parse_args()
        resp = jsonify({'message': 'User was edited successfully'})
        if data['email'] != '':
            current_user.email = data['email']
        if data['password'] != '':
            current_user.password = User.encrypt_password(data['password'])
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
        current_user.save()
        return resp


@ns_users.route('/logout')
class UserLogoutAccess(Resource):
    @jwt_required
    def delete(self):
        resp = jsonify({'logout': 'True'})
        unset_jwt_cookies(resp)
        return resp


@ns_users.route('/<int:id>')
class UserDetails(Resource):
    @jwt_required
    def get(self, id):
        user = User.find_by_id(id)
        return user_schema.dump(user)


@ns_token.route('/refresh')
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        access_token = create_access_token(identity=get_jwt_identity())
        resp = jsonify({'refresh': 'True'})
        set_access_cookies(resp, access_token)
        return resp


@ns_users.route('')
class AllUsers(Resource):
    @jwt_required
    def get(self):
        all_users = User.all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)

    @jwt_required
    def delete(self):
        return {'message': 'Delete all users'}


