from flask import jsonify,url_for,session,redirect
from flask_bcrypt import Bcrypt
from app.main.models.users import Users
from utils.validation import validate_email,validate_mobile,validate_password
from utils.initdb import db
from utils import registration_message
from datetime import datetime,timedelta
from sqlalchemy.exc import SQLAlchemyError
from utils.update_message import update_message
from flask_mail import Mail,Message
from utils.email_utils import send_email
from utils import registration_message
from utils.gemini import ai
from app.main.config.api_keys import oauth
from flask import session

bcrypt=Bcrypt()






#ADDING USERS==OK
def add_user(data):
    try:
        name,email,mobile,password,gender,role=data.get('user_name'),data.get('user_email'),data.get('user_mobile'),data.get('user_password'),data.get('user_gender'),data.get('user_role')
        required_fields={"user_name":name,"user_email":email,"user_password":password}
        missing_fields=[k for k,v in required_fields.items() if not v]
        if missing_fields:
            return {"message":f"{','.join(missing_fields)} are required"},400
        if not validate_email(email):
            return {"message":"Invalid email-id"},400
        check=Users.query.filter_by(user_email=email).first()
        if check:
            return {"message":"User Already Exists Login with your password"},409
        if mobile and not validate_mobile(mobile):
            return {"message":"Invalid mobile number"},400
        if not validate_password(password):
            print('password is in valid')
            return {"message":"Password must be greater than 8 charachters  with one uppercase,lowercase and Special Chracters"},400
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        user_details=Users(user_name=name,user_email=email,user_mobile=mobile,user_password=hashed_password,user_gender=gender,user_role=role)
        db.session.add(user_details)
        db.session.commit()
        subject,recep='Registration Successfull',email
        # print(email)
        # body = registration_message(name)
        # print(subject,body)
        send_email(subject='Account Added',recipients=[email],body=f'Account addedd')
        return {"message":"User Details are added"}, 201
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        print('eerr1')
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        print('e2222')
        return {"message":"Internal Server Error"},500





#GET ALL USERS AND BY EMAIL ALSO==OK
def get_all_users(email,l):
    try:
        print("e1:",email)
        if email:
            data=Users.query.filter_by(user_email=email).first()
            print("e2",email)
            print(data)
            
            if not data:
                return {"message":"User Details not Found"},404
            user_data={"user_id":data.user_id,"user_name":data.user_name,"user_email":data.user_email,"user_gender":getattr(data.user_gender,"value",""),"user_role":getattr(data.user_role,"value",""),"created_at":data.created_at,"updated_at":data.updated_at,"user_mobile":data.user_mobile}
            return {"user_data":user_data},200
        else:
            data=Users.query.limit(l).all() if l else Users.query.all()
            result=[]
            for el in data:
                if el.is_deleted:
                    continue
                user_data={"user_id":el.user_id,"name":el.user_name,"email":el.user_email,"gender":getattr(el.user_gender,"value",""),"role":getattr(el.user_role,"value",""),"created_at":el.created_at,"updated_at":el.updated_at,"mobile":el.user_mobile}
                result.append(user_data)
            return {"users":result},200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"messaage":"Internal Server Error"},500






#DELETE THE USER==OK
def delete_user(email):
    try:
        data=Users.query.filter_by(user_email=email).first()
        if not data:
            return {"message":"No User Found"},404
        setattr(data,'is_deleted',True)
        db.session.commit()
        return {"message":"User Details are deleted"},200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500





#GET REGISTERED USERS IN LAST N DAYS==OK
def get_users_registered(limit):
    try:
        l=int(limit) if limit else 5
        print(l)
        n= datetime.utcnow()-timedelta(days=int(l))
        user_data=Users.query.filter(Users.created_at>=n).all()
        if not user_data:
            return {"message":"No Users Found"},404
        result=[]
        for el in user_data:
            if el.is_deleted:
                continue
            result.append({"name":el.user_name,"email":el.user_email,"role":getattr(el.user_role,"value",""),"gender":getattr(el.user_gender,"value",""),"mobile":el.user_mobile})
        return {"users":result},200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500




#GET USERS UPDATED THERE PROFILE IN LAST N DAYS==OK
def get_users_updated(limit):
    try:
        l=int(limit) if limit else 1
        print('debug-1')
        n= datetime.utcnow()-timedelta(days=l)
        print('debug-2')
        user_data=Users.query.filter(Users.updated_at>=n).all()
        if user_data is None:
            return {"message":"No Users Found"},404
        result=[]
        for el in user_data:
            if el.is_deleted:
                continue
            result.append({"name":el.user_name,"email":el.user_email,"role":getattr(el.user_role,"value",""),"gender":getattr(el.user_gender,"value",""),"mobile":el.user_mobile})
        return {"users":result},200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500



#LOGIN==OK
def login(data):
    try:
        user_email=data.get('user_email')
        user_password=data.get('user_password')
        print(user_email,user_password)
        if user_email is None:
            return {"message":"email is required"},400
        if user_password is None:
            return {"message":"password is required"},400
        user_data=Users.query.filter_by(user_email=user_email).first()
        print(user_data)
        if user_data is None or user_data.is_deleted:
            return {"message":"Invalid Credentials"},401
        password=user_data.user_password
        password_check=bcrypt.check_password_hash(password,user_password)
        print(password_check)
        if password_check:
            return {"message":"Success full login"},200

        return {"message":"Invalid Password"},401
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500

def send_otp(email):
    try:
        otp=7777
        print('bd1')
        print('sending email')
        print(email)
        send_email(subject='Deletee Account',recipients=[email],body=f'otp is {otp}')
        print('email is sent')
        return {"otp":otp}
    except Exception as e:
        print(e)
        return {"message":"error"}

def chat(data):
    try:
        return ai(data)
    except Exception as e:
        print(e)



        
# This is not working check them

# #UPDATE USER PASSWORD
# def update_user(data):
#     try:
#         updated_password=data.get('password')
#         user_data=Users.query.filter_by(us).first()
#         if not validate_password(updated_password):
#             return jsonify({"message":"Password must be greater than 8 charachters  with one uppercase,lowercase and Special Chracters"}),400
#         hashed_password = bcrypt.generate_password_hash(updated_password).decode('utf-8')
#         user_data.user_password = hashed_password
#         db.session.commit()
#         send_email(subject='Password has been Updated',recipients=[user_email],body=update_message(user_data.user_name))
#         return jsonify({"message":"Password is updated"}),201
#     except SQLAlchemyError as e:
#         print(e)
#         db.session.rollback()
#         return jsonify({"message":"Internal Server Error"}),500
#     except Exception as e:
#         print(e)
#         return jsonify({"message":"Internal Server Error"}),500


#This is not working check them
def google():
    print('d1')
    if 'google_token' in session:
        return redirect(url_for('api.users_user_login'))
    print('d2')
    redirect_uri = url_for('api.users_google_callback', _external=True)
    print(redirect_uri)
    print('d3')
    return oauth.google.authorize_redirect(redirect_uri)


def google_auth():
    try:
        print('2')
        token = oauth.google.authorize_access_token()
        print(token)
        print('3')
        if not token:
            return redirect(url_for('google'))  

        userinfo_endpoint = oauth.google.server_metadata.get('userinfo_endpoint')
        if not userinfo_endpoint:
            return {"message": "Google userinfo endpoint missing"}, 500

        resp = oauth.google.get(userinfo_endpoint)
        user_info = resp.json()

        email = user_info.get('email')
        name = user_info.get('given_name') or user_info.get('name')

        if not email:
            return {"message": "Email not returned by Google"}, 400

        userdata = Users.query.filter_by(user_email=email).first()

        if userdata is None:
            user = Users(user_email=email, user_name=name)
            db.session.add(user)
            db.session.commit()
        else:
            user = userdata

        session['google_token'] = token

        return { "message": "Login successful","user": {"email": email, "name": name}, "token": token}, 200

    except SQLAlchemyError as e:
        print("DB Error:", e)
        db.session.rollback()
        return {"message": "Database error"}, 500

    except Exception as e:
        print("General Error:", e)
        return {"message": "Internal server error"}, 500
    

def logout():
    session.clear()

    return {"MESSAGE":"LOGOUT"}



def rolechange(data):
    try:
        print('a1')
        print(data)
        print(data['user_id'])
        print('a2')
        user_data=Users.query.filter_by(user_id=data['user_id']).first()
        print('d1')
        print(user_data)
        print('d2')
        if user_data:
            setattr(user_data,'user_role','ngo_admin')
            db.session.commit()
            print('role change')
            return {"message":"Role change"},200

    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500




#UPDATE THE USER DETAILS


























    

        