from app.main.dto.users import UserDTO
from app.main.services.users import get_users_updated, add_user,delete_user,login,get_users_registered,get_all_users,send_otp,google,google_auth,logout,rolechange
from utils.gemini import ai
from flask import request,jsonify
from flask_restx import Resource
user_route=UserDTO.api


@user_route.route("/")
class UserController(Resource):
    def post(self):
        data=request.get_json()
        print('im here')
        return add_user(data)
        # return response
    
    def get(self):
        user_email=request.args.get('user_email')
        user_l=request.args.get('limit')
        response=get_all_users(user_email,user_l)
        print(response)
        print(type(response))
        return jsonify(response)
    def patch(self):
        email=request.args.get('email')
        response,status=delete_user(email)
        return response,status

    

@user_route.route("/login")
class UserLogin(Resource):
    def post(self):
        data=request.get_json()
        response,status=login(data)
        return response,status

@user_route.route("/registered")
class UsersRegistered(Resource):
    try:
        def get(self):
            limit=request.args.get('limit')
            response,status=get_users_registered(limit)
            return response,status
    except Exception as e:
        print(e)
        
@user_route.route('/updated')
class UserUpdated(Resource):
    def get(self):
        limit=request.args.get('limit')
        response,status=get_users_updated(limit)
        return response,status


@user_route.route('/sendotp')
class OtpSend(Resource):
    def post(self):
        data=request.get_json()
        email=data.get('email')
        print('first',email)
        response=send_otp(email)
        return response
    

@user_route.route('/chat')
class Chat(Resource):
    def post(self):
        print('d1')
        data=request.get_json()
        print('d2')
        print(data)
        print('d3')
        q=data['question']
        print('d4')
        print(q)
        result=ai(q)
        return result

@user_route.route('/login/google')
class GoogleLogin(Resource):
    def get(self):
        print('22')
        response = google()
        return response


@user_route.route('/auth/login')
class GoogleCallback(Resource):
    def get(self):
        print('1')
        return google_auth()
    


@user_route.route('/logout')
class Logout(Resource):
    def get(self):
        return logout()
    

@user_route.route('/rolechange')
class RollChange(Resource):
    def patch(self):
        print('ty1')
        data=request.get_json()
        print('t2')
        return rolechange(data)

