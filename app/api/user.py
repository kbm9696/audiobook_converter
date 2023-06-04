import requests
from flask import jsonify, request, abort
from flask_api import status
from flask_restful import Resource
from dba.userdba import UserDba, Users
import schemas
import dba.utils
from utils.validation import validate_user_credentials

headers = {
    'content-type': 'application/json',
    'Accept': 'application/json'
}


class UsersApi(Resource):
    def __init__(self):
        pass

    @validate_user_credentials
    def get(self):
        try:
            resp = {}
            user_dba = UserDba()
            user_data = user_dba.get_all_users()
            print('user_data', user_data)
            resp = {
                'description': 'Users Collections',
                'details': user_data
            }
            resp = jsonify(resp)
            resp.status_code = 200
            return resp

        except Exception as e:
            print(f'Got Exception in Get method of Users:{e}')
            resp = {
                'error': f'Got Exception in Get method of Users:{e}'
            }
            resp = jsonify(resp)
            resp.status_code = 400
            return resp

    def post(self):
        resp = {}
        try:
            res_boby = request.get_json()
            validation_status = dba.utils.schema_validation(res_boby, schemas.USER_POST)
            if validation_status is not None:
                print('Validation failed for the given data', validation_status.message)
                response = {'error': 'Validation failed', 'message': str(validation_status.message)}
                resp = jsonify(response)
                resp.status_code = 400
                return resp
            user_details = Users()
            user_details.user_id = res_boby.get('user-id')
            user_details.user_name = res_boby.get('username')
            user_details.password = res_boby.get('password')
            user_details.premium_user = res_boby.get('premium-user')
            user_dba = UserDba()
            user_dba.add(user_details)
            resp = jsonify({})
            resp.status_code = 204
            return resp

        except Exception as e:
            print(f'error in post func of user {e}')


class UserApi(Resource):
    def __init__(self):
        pass

    @validate_user_credentials
    def get(self, uid):
        try:
            resp = {}
            user_dba = UserDba()
            user_data = user_dba.get_by_userid(uid)
            if not bool(user_data):
                resp = {
                    "message": "resource not found"
                }
                resp = jsonify(resp)
                resp.status_code = 404
                return resp
            print('user_data', user_data)
            resp = user_data
            resp = jsonify(resp)
            resp.status_code = 200
            return resp

        except Exception as e:
            print(f'Got Exception in Get method of Users:{e}')
            resp = {
                'error': f'Got Exception in Get method of Users:{e}'
            }
            resp = jsonify(resp)
            resp.status_code = 400
            return resp

    @validate_user_credentials
    def patch(self, uid):
        resp = {}
        try:
            data = request.get_json()
            validation_status = dba.utils.schema_validation(data, schemas.USER_PATCH)
            if validation_status is not None:
                print('Validation failed for the given data', validation_status.message)
                response = {'error': 'Validation failed', 'message': str(validation_status.message)}
                resp = jsonify(response)
                resp.status_code = 400
                return resp
            user_dba = UserDba()
            ret = user_dba.update_data(uid, data)
            if len(ret):
                resp['error'] = ret
            resp = jsonify(resp)
            resp.status_code = 401
            return resp
        except Exception as e:
            print(f'Got Exception in patch handler:{e}')
            resp['error'] = f'Got Exception in patch handler:{e}'
            resp = jsonify(resp)
            resp.status_code = 400
            return resp
