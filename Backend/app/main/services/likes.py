from flask import jsonify
from app.main.models.Likes import Likes
from app.main.models.campaigns import Campaigns
from app.main.models.users import Users
from utils.initdb import db
from sqlalchemy.exc import SQLAlchemyError

#Like the camapign
def campaign_liked(data):
    try:
        user_id=data.get('user_id')
        campaign_id=data.get('campaign_id')
        ldata=Likes.query.filter_by(user_id=user_id,campaign_id=campaign_id).first()
        print("campaign data",ldata)


        if ldata is None:
            print('d2')
            liked=True
            if not user_id or not campaign_id:
                return {"message":"All Fields are required"},403
            campaign_cl=Likes(user_id=user_id,campaign_id=campaign_id,is_liked=liked)
            db.session.add(campaign_cl)
            db.session.commit()
        elif ldata is not None:
            print('d1')
            print(ldata.is_liked)
            print('tttttttttttttttt')
            ldata.is_liked=not ldata.is_liked
            setattr(ldata,'is_liked',ldata.is_liked)
            db.session.commit()
            return {"message":"dis liked"}
        else:
            print('d3')
            print('hhhhhhhhhhhhhhhhh')
            setattr(ldata,'is_liked',True)
            db.session.commit()
            return {"message":"disliked"}



        return {"message":"You liked this Campaign"},200
    except SQLAlchemyError as e:
        print(e)
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500


#Get all Campaigns Likes by Campaigns
def get_likes_by_campaigns(campaign_id):
    try:
        data=Campaigns.query.filter_by(campaign_id=campaign_id).first()
        if not data:
            return jsonify({"message":"Invalid"}),404
        campaign_data=Likes.query.filter_by(campaign_id=campaign_id).all()
        result=[]
        for el in campaign_data:
            if el.is_deleted:
                continue
            user_details=Users.query.filter_by(user_id=el.user_id).first()
            result.append({"name":user_details.user_name,"datetime":el.created_at,"capaign_id":campaign_id})
        return jsonify({"likes":result}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    


