from flask import jsonify
from app.main.models.ngo import  NGO
from app.main.models.users import Users
from utils.initdb import db
from datetime import datetime,timedelta
from sqlalchemy.exc import SQLAlchemyError


#ADD THE NGO
def add_ngo(data):
    try:
        name,mission,status,user_id,location=data.get('ngo_name'),data.get('ngo_mission'),data.get('ngo_status'),data.get('user_id'),data.get('ngo_location')
        ngo_check=NGO.query.filter_by(ngo_name=name).first()
        if ngo_check:
            return jsonify({"message":"NGO Already Registered"}),409
        
        ngo_data=NGO(ngo_name=name,ngo_mission=mission,ngo_status=status,user_id=user_id,ngo_location=location)
        db.session.add(ngo_data)
        db.session.commit()
        return {"message":"NGO is addded"},201
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500



#DELETE THE NGO
def delete_ngo(name):
    try:
        data=NGO.query.filter_by(ngo_name=name).first()
        if data:
            setattr(data,'is_deleted',True)
            db.session.commit()
            return jsonify({"message":"NGO is Deleted"}),204
        return jsonify({"message":"NGO details not Found"}),404
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Errror"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    



#GET NGO DETAILS
def get_ngo_owner_details(name):
    try:
        if name:
            data=NGO.query.filter_by(ngo_name=name).first()
            if data is None:
                return jsonify({"message":"No Details Found"}),404
            if data.user_id is None:
                return jsonify({"message":"Invalid Input"}),401
            ngo_owner_data=Users.query.filter_by(user_id=data.user_id).first()
            if data.is_deleted:
                return jsonify({"message":"No Details Found"}),404
            data={"name":data.ngo_name,"mission":data.ngo_mission,"address":data.ngo_location,"owner_detals":{"name":ngo_owner_data.user_name,"email":ngo_owner_data.user_email,"gender":getattr(ngo_owner_data.user_gender,"value",""),"created_at":ngo_owner_data.created_at,"updated_at":ngo_owner_data.updated_at,"mobile":ngo_owner_data.user_mobile} }
        else:
            data=NGO.query.all()
            print(data)
            result=[]
            for el in data:
                result.append({"ngo_name":el.ngo_name,"ngo_mission":el.ngo_mission,"ngo_address":el.ngo_location})
            return jsonify({"ngos":result}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":'Internal Server Error'}),500   
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    





#GET NGO BY LOCATION
def get_ngo_by_location(location):
    try:
        data=NGO.query.filter_by(ngo_location=location).all()
        result=[]
        if data is None:
            return jsonify({"message":"No Details are Found"}),404
        for el in data:    
            if el.is_deleted:
                continue
            ngo_owner_data=Users.query.filter_by(user_id=el.user_id).first()
            ngo_data={"name":el.ngo_name,"mission":el.ngo_mission,"address":el.ngo_location,"owner_detals":{"name":ngo_owner_data.user_name,"email":ngo_owner_data.user_email,"gender":getattr(ngo_owner_data.user_gender,"value",""),"created_at":ngo_owner_data.created_at,"updated_at":ngo_owner_data.updated_at,"mobile":ngo_owner_data.user_mobile} }
            result.append(ngo_data)
        return jsonify({"data":result}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    








#change NGO STATUS
def ngo_status_change(data):
    try:
        ngo_id=data.get('ngo_id')
        action=data.get('status')
        ngo_data=NGO.query.filter_by(ngo_id=ngo_id).first()
        if ngo_data.is_deleted:
            return jsonify({"message":"No Details are found"}),404
        if ngo_data is None:
            return jsonify({"message":"No Details Found"}),404
        ngo_data.ngo_status=action
        db.session.commit()
        msg=f"status changed to {action}"
        return jsonify({"message":msg}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Error"}),500
    







# BLACKLISTE NGO
def blacklist_ngo(ngo_id):
    try:
        i=ngo_id
        ngo_data=NGO.query.filter_by(ngo_id=i).first()
        if ngo_data is None or ngo_data.is_deleted:
            return jsonify({"message":"NGO Details not Found"}),404
        ngo_data.ngo_blacklisted = not ngo_data.ngo_blacklisted
        t=f"NGO Blacklisted :{ngo_data.ngo_blacklisted}"
        db.session.commit()
        if ngo_data.ngo_blacklisted:
            return jsonify({"message":t})
        else:
            return jsonify({"message":"NGO is unblocked, Terms and Conditions Apply"}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500

    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500







#GET NGOS WHICH REGISTERED IN LAST N DAYS
def get_ngo_registered(limit):
    try:
        n= datetime.utcnow()-timedelta(days=int(limit))
        ngo_data=NGO.query.filter(NGO.created_at>=n).all()
        if ngo_data is None:
            return jsonify({"message":"No NGOS Found"}),404
        print(ngo_data)
        result=[]
        for el in ngo_data:
            if el.is_deleted:
                continue
            result.append({"name":el.ngo_name})
        return jsonify({"data":result}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    





#GET NGOS WHICH UPDATED IN LAST N DAYS
def get_ngo_updated(limit):
    try:
        n= datetime.utcnow()-timedelta(days=int(limit))
        ngo_data=NGO.query.filter(NGO.updated_at>=n).all()
        if ngo_data is None:
            return jsonify({"message":"No NGOS Found"}),404
        print(ngo_data)
        result=[]
        for el in ngo_data:
            if el.is_deleted:
                continue
            result.append({"name":el.ngo_name})
        return jsonify({"data":result}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500





#GET ALL BLACKLISTED NGOS







#Get the ngo by user_id
def get_ngo_by_user_id(data):
    try:
        print(data)
        data=NGO.query.filter_by(user_id=data['user_id']).first()
        print(data)
        return {"ngo":{'name':data.ngo_name,'location':data.ngo_location,'ngo_id':str(data.ngo_id)}},200
    except SQLAlchemyError as e:
        print(e)
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500







