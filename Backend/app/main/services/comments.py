from flask import jsonify
from app.main.models.Likes import Likes
from app.main.models.campaigns import Campaigns
from app.main.models.users import Users
from app.main.models.comments import Comments
from utils.initdb import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

#comment the camapign
def campaign_commented(data):
    try:
        user_id=data.get('user_id')
        campaign_id=data.get('campaign_id')
        comment=data.get('comment')
        if not all([user_id,campaign_id,comment]):
            return jsonify({"message":"All Fields are requireed"}),400
        campaign_cl=Comments(user_id=user_id,campaign_id=campaign_id,comment=comment)
        db.session.add(campaign_cl)
        db.session.commit()
        return jsonify({"message":"Your Commment Saved"}),200
    except SQLAlchemyError as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500




#Get all Campaigns comment by Campaigns
def get_comments_by_campaigns(campaign_id):
    try:
        data=Campaigns.query.filter_by(campaign_id=campaign_id).first()
        if not data:
            return jsonify({"message":"Invalid"}),404
        campaign_data=Comments.query.filter_by(campaign_id=campaign_id).all()
        result=[]
        for el in campaign_data:
            if el.is_deleted:
                continue
            user_details=Users.query.filter_by(user_id=el.user_id).first()
            result.append({"name":user_details.user_name,"datetime":el.created_at,"campaign_id":campaign_id,"comment":el.comment})
        return jsonify({"comments":result}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    


#remove the comments
def remove_comment(comment_id):
    try:
        data=Comments.query.filter_by(comment_id=comment_id).first()
        if data:
            setattr(data,'is_deleted',True)
            db.session.commit()
            return jsonify({"message":"Comment Removed"}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
        



#Group the Comment by the campaign_id
def group_by_comments():
    try:
        data=db.session.query(Campaigns.campaign_id,func.count(Campaigns.campaign_id)).group_by(Campaigns.campaign_id).all()
        if not data:
            return jsonify({"message":"No Details found"}),404
        return jsonify({"message":data})
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500