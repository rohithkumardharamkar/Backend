from flask import jsonify
from app.main.models.scholarship import Scholarship
from app.main.models.users import Users
from app.main.models.ngo import NGO
from utils.initdb import db
from sqlalchemy.exc import SQLAlchemyError



#Scholarship Apply
def scholarship_apply(data):
    try:
        user_id=data.get('user_id')
        ngo_id=data.get('ngo_id')
        if not user_id or not ngo_id:
            return jsonify({"message":"User Id or Ngo Id is missing"}),404
        scholarship_data=Scholarship(user_id=user_id,ngo_id=ngo_id)
        db.session.add(scholarship_data)
        db.session.commit()
        return jsonify({"message":"Thank you,We will reveive your application"}),201
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500   
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    


#Get all Applications
def get_scholarships():
    try:
        data=Scholarship.query.all()
        result=[]
        for el in data:
            if el.is_deleted:
                continue
            user_data=Users.query.filter_by(user_id=el.user_id).first()
            ngo_data=NGO.query.filter_by(ngo_id=el.ngo_id).first()
            result.append({"ngo_name":ngo_data.ngo_name,"ngo_location":ngo_data.ngo_location,"applicant_name":user_data.user_name,"applicant_email":user_data.user_email,"applicant_mobile":user_data.user_mobile,"applicant_gender":getattr(user_data.user_gender,"value","")})
        return jsonify({"applications":result})
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal SErver Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500



#Delete the Application
def delete_scholarship(scholarship_id):
    try:
        data=Scholarship.query.filter_by(scholarship_id=scholarship_id).first()
        if not data:
            return jsonify({"message":"Invalid Action"}),404
        setattr(data,'is_deleted',True)
        db.session.commit()
        return jsonify({"message":"Application is Deleted"}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.close()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    


#approve the scholarship
def approve_scholarship(scholarship_id):
    try:
        applicant_data=Scholarship.query.filter_by(scholarship_id=scholarship_id).first()
        if applicant_data is None:
            return jsonify({"message":"No Detals Found"}),404
        if applicant_data.approved==True:
            return jsonify({"message":"Scholarship is already Approved"}),200
        applicant_data.approved=not applicant_data.approved
        db.session.commit()
        return jsonify({"message":f"Scholarship status :{applicant_data.approved}"}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.close()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500











