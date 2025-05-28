from flask import jsonify
from utils.initdb import db
from app.main.models.campaigncategory import CampaignsCategories
from sqlalchemy.exc import SQLAlchemyError


#Adding the Campaign Category
def add_campaign_category(data):
    try:
        category_name=data.get('category_name')
        print(data)
        if not category_name:
            return {"message":"Input field is Required"},400
        print('debug-1')
        c_data=CampaignsCategories.query.filter_by(category_name=data['category_name']).first()
        print('debug-2')
        print("c",c_data)
        if c_data:
            return {"message":"Category already Found"},404
        cam_data=CampaignsCategories(category_name=category_name)
        db.session.add(cam_data)
        db.session.commit()
        return {"message":"Category added"},201
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500

