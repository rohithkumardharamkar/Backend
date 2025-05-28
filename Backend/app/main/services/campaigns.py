from flask import jsonify
from app.main.models.campaigns import Campaigns
from app.main.models.users import Users
from utils.initdb import db
from utils import send_email,campaign_message
from sqlalchemy.exc import SQLAlchemyError
from app.main.models.ngo import NGO
from app.main.models.payments import Payments
from app.main.models.Likes import Likes
from datetime import date
from sqlalchemy import func
from sqlalchemy import func, cast, Integer
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime





#Add the Campaigns
def add_campaigns(data):
    try:
        name,location,description,category,ngo_id,urgency,target_amount,date=data.get('campaign_name'),data.get('campaign_location'),data.get('campaign_description'),data.get('campaign_category'),data.get('ngo_id'),data.get('urgent'),data.get("target_amount"),data.get('campaign_date')
        print(name)
        c_data=Campaigns.query.filter_by(campaign_name=name).first()
        if c_data:
            if c_data.is_deleted:
                return {"message":"Campaign is  completed an its deleted"},404
            else:
                return {"message":"Campaign is already present"},409
        print(name,location)
        campaign_data=Campaigns(campaign_name=name,campaign_location=location,campaign_description=description,campaign_category=category,ngo_id=ngo_id,campaign_urgency=urgency,target_amount=target_amount,c_date=date)
        print(campaign_data)
        db.session.add(campaign_data)
        db.session.commit()
        user_data=Users.query.all()
        result=[]
        for el in user_data:
            result.append(el.user_email)
        subject='New Campaign Added'
        # send_email(subject=subject,recipients=result,body=campaign_message(name,location,description))
        return {"message":"Campaign Added"},201
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500
    

    
#Get the campaigsns by name and the campaign id

def get_campaigns(campaign_id,campaign_name,ngo_id):
    try:
        if campaign_id:
            data=Campaigns.query.filter_by(campaign_id=campaign_id).first()
            if not data or data.is_deleted:
                return {"message":"No Details Found"},404
            print('d1')
            ngo_id=data.ngo_id
            print('d2')
            print('debug-1')
            el=NGO.query.filter_by(ngo_id=ngo_id).first()
            print(el)
            print('debug-2')
            campaign_data={"campaign_name":data.campaign_name,"campaign_location":data.campaign_location,"campaign_description":data.campaign_description}
            ngo_owner_data=Users.query.filter_by(user_id=el.user_id).first()
            ngo_data={"name":el.ngo_name,"mission":el.ngo_mission,"address":el.ngo_location,"owner_detals":{"name":ngo_owner_data.user_name,"email":ngo_owner_data.user_email,"gender":getattr(ngo_owner_data.user_gender,"value",""),"created_at":ngo_owner_data.created_at,"updated_at":ngo_owner_data.updated_at,"mobile":ngo_owner_data.user_mobile} }
            return {"campaign_data":campaign_data,"ngo":ngo_data,"ngo_admin":ngo_owner_data}
        elif campaign_name:
            data=Campaigns.query.filter_by(campaign_name=campaign_name).first()
            print(data)
            if not data or data.is_deleted:
                return {"message":"No Details Found"},404
            ngo_id=data.ngo_id
            print('debug-1')
            print(ngo_id)
            print('debug-2')
            el=NGO.query.filter_by(ngo_id=ngo_id).first()
            print('debug-3')
            campaign_data={"campaign_name":data.campaign_name,"campaign_location":data.campaign_location,"date":data.c_data,"campaign_descriptiom":data.campaign_location}
            ngo_owner_data=Users.query.filter_by(user_id=el.user_id).first()
            print(ngo_owner_data)
            print('debug-4')
            ngo_data={"name":el.ngo_name,"mission":el.ngo_mission,"address":el.ngo_location,"owner_detals":{"name":ngo_owner_data.user_name,"email":ngo_owner_data.user_email,"gender":getattr(ngo_owner_data.user_gender,"value",""),"mobile":ngo_owner_data.user_mobile} }
            print(ngo_data)
            print('debug-5')
            return {"campaign_data":{campaign_data},"ngo":{ngo_data},"ngo_admin":{ngo_owner_data}}
        elif ngo_id:
            data=Campaigns.query.filter_by(ngo_id=ngo_id).all()
            print(data)
            r=[]
            for el in data:
                ngo_id=NGO.query.get(el.ngo_id)
                if el.is_deleted:
                    continue
                ngo_data=NGO.query.filter_by(ngo_id=ngo_id.ngo_id).first()
                n_data={"ngo_name":ngo_data.ngo_name,"ngo_id":ngo_data.ngo_id}
                total_likes = db.session.query(func.sum(cast(Likes.is_liked, Integer))).filter_by(campaign_id=el.campaign_id).scalar() or 0
                p=Payments.query.filter_by(campaign_id=el.campaign_id).all()
                total_amount = db.session.query(func.sum(Payments.payment_amount)).filter_by(campaign_id=el.campaign_id).scalar()
                # likes=db.session.query(func.sum(Campaigns.li))
                r.append({"campaign_id":str(el.campaign_id),"campain_name":el.campaign_name,"campaign_location":el.campaign_location,"category":el.campaign_category,"amount":el.target_amount, "ngo":{"name":ngo_data.ngo_name,"ngo_status":str(ngo_data.ngo_status),"location":ngo_data.ngo_location,"isVerified":ngo_data.is_verified,"ngo_blacklist":ngo_data.ngo_blacklisted},"raise_amount":total_amount,"likes":total_likes})
           
            return {'r':r},200
        else:
            data=Campaigns.query.all()
            print(data)
            r=[]
            for el in data:
                ngo_id=NGO.query.get(el.ngo_id)
                if el.is_deleted:
                    continue
                ngo_data=NGO.query.filter_by(ngo_id=ngo_id.ngo_id).first()
                n_data={"ngo_name":ngo_data.ngo_name,"ngo_id":ngo_data.ngo_id}
                total_likes = db.session.query(func.sum(cast(Likes.is_liked, Integer))).filter_by(campaign_id=el.campaign_id).scalar() or 0
                p=Payments.query.filter_by(campaign_id=el.campaign_id).all()
                total_amount = db.session.query(func.sum(Payments.payment_amount)).filter_by(campaign_id=el.campaign_id).scalar()
                # likes=db.session.query(func.sum(Campaigns.li))
                r.append({"campaign_id":str(el.campaign_id),"campain_name":el.campaign_name,"campaign_location":el.campaign_location,"category":el.campaign_category,"amount":el.target_amount, "ngo":{"name":ngo_data.ngo_name,"ngo_status":str(ngo_data.ngo_status),"location":ngo_data.ngo_location,"isVerified":ngo_data.is_verified,"ngo_blacklist":ngo_data.ngo_blacklisted},"raise_amount":total_amount,"likes":total_likes})
           
            return {'r':r},200

    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500
    



# Get the active campaigns
def get_active_campaigns():
    try:
        data = Campaigns.query.filter(Campaigns.campaign_date >= datetime.utcnow()).all()
        result = []
        for el in data:
            if el.is_deleted:
                continue
            result.append({"campaign_id": el.campaign_id, "campaign_name": el.campaign_name})
        print(result)
        return {"campaigns": result}, 200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message": "Internal Server Error"}, 500
    except Exception as e:
        print(e)
        return {"message": "Internal Server Error"}, 500


# Get the inactive campaigns
def get_inactive_campaigns():
    try:
        data = Campaigns.query.filter(Campaigns.campaign_date < datetime.utcnow()).all()
        result = []
        for el in data:
            if el.is_deleted:
                continue
            result.append({"campaign_id": el.campaign_id, "campaign_name": el.campaign_name})
        return {"campaigns": result}, 200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message": "Internal Server Error"}, 500
    except Exception as e:
        print(e)
        return {"message": "Internal Server Error"}, 500


# Get campaigns by location
def get_campaigns_by_location(location):
    try:
        data = Campaigns.query.filter_by(campaign_location=location).all()
        if not data:
            return {"message": "No campaigns Found"}, 404

        result = []
        for el in data:
            if el.is_deleted:
                continue
            result.append({"campaign_name": el.campaign_name})

        return {"campaigns": result}, 200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message": "Internal Server Error"}, 500
    except Exception as e:
        print(e)
        return {"message": "Internal Server Error"}, 500


#Delete the campaigns
def delete_campaigns(campaign_id):
    try:
        campaign_details=Campaigns.query.filter_by(campaign_id=campaign_id).first()
        if campaign_details:
            setattr(campaign_details,"is_deleted",True)
            db.session.commit()
            return {"message":"Campaign is Deleted"},200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500
    




#get campaigns by ngo_id
def get_by_ngo_id(ngo_id):
    try:
        ngo_campaigns=NGO.query.filter_by(ngo_id=ngo_id).all()
        print(ngo_campaigns)
        return {"message":"2"},200
    except SQLAlchemyError as e:
        print(e)
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500
    
