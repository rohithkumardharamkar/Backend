from sqlalchemy import func
from app.main.models.payments import Payments
from flask import jsonify
from app.main.models.users import Users
from app.main.models.campaigns import Campaigns
# from utils.send_email import send_email
from utils.initdb import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timedelta
from app.main.models.ngo import NGO

#Add Payments
def add_to_payment(data):
    campaign_id,user_id,payment_type,amount=data.get('campaign_id'),data.get('user_id'),data.get('paymentType'),data.get('amount')
    if not campaign_id or not user_id or not payment_type or not amount:
        return {"message":"All Fields are Required"},400
    user_data=Users.query.filter_by(user_id=user_id).first()
    campaign_data=Campaigns.query.filter_by(campaign_id=campaign_id).first()
    if not user_data:
        return {"message":"User DEtails Not Found"},404
    if not campaign_data:
        return {"message":"No Campaigns are Found"},404
    email=user_data.user_email
    payment_data=Payments(campaign_id=campaign_id,user_id=user_id,payment_type=payment_type,payment_amount=amount)
    # send_email(subject='Thank you for the Contribution',recipients=[email],body='Amout Rs 20000 payed for the campaigns thank you for your  contribution')
    db.session.add(payment_data)
    db.session.commit()
    return {"message":"Payment Successfull"},201



#group by sum of amount
def get_payments_sum_by_user_id():
    try:
        data=db.session.query(Payments.user_id,func.sum(Payments.amount)).group_by(Payments.user_id).all()
        if len(data)==0:
            return jsonify({"message":"No Payments Found"}),404
        return jsonify({"message":data}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    

    
#group by how many times he paid the amount  to find the most recuuring donor 
def get_payments_count_by_user_id():
    try:
        data=db.session.query(Payments.user_id,func.count(Payments.user_id)).group_by(Payments.user_id).all()
        if not data:
            return jsonify({"message":"No Paymets Found"}),404
        return jsonify({"message":data}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
 
    
#get total amount by the campaign_id
def get_payments_by_campaign_id():
    try:
        data=db.session.query(Payments.user_id,Payments.campaign_id,func.count(Payments.campaign_id,Payments.campaign_id)).group_by(Payments.user_id).all()
        if not data:
            return jsonify({"message":"No Details Found"}),404
        return jsonify({"message":"data"}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"INternal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500



#Get THe payments in last n days
def get_payments_by_last_n_days(limit,campaign_id):
    try:
        if l:
            l=limit or 0
            n=datetime.utcnow()-timedelta(days=int(l))
            payments_data=Payments.query.filter_by(Payments.created_at<=n).all()
            if not payments_data:
                return jsonify({"message":f'No Payments Found in last {l} days'}),200
            return jsonify({"message":payments_data}),200
        elif campaign_id:
            payments_data=Payments.query.filter_by(campaign_id=campaign_id).all()
            print(payments_data)
            return {"message":"jhjhhjhjhjj"}

    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"mesage":"Internal Sever error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    



#get payments by campaign_id
def get_by_campaign_id(campaign_id):
    try:
        print(campaign_id)
        p_data=Payments.query.filter_by(campaign_id=campaign_id).all()
        result=[]
        for el in p_data:
            user_data=Users.query.filter_by(user_id=el.user_id).first()
            result.append({'payment':{'id':str(el.payment_id),'amount':el.payment_amount,'type':el.payment_type},'users':{'name':user_data.user_name,'email':user_data.user_email,'gender':user_data.user_gender,'mobile':user_data.user_mobile}})
        return {"data":result}



    except SQLAlchemyError as e:
        print(e)
        return {"message":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500





    
def get_by_user_id(user_id):
    try:
        print('d1',user_id)
        user_payments=Payments.query.filter_by(user_id=user_id).all()
        result=[]
        for el in user_payments:
            cam_data=Campaigns.query.filter_by(campaign_id=el.campaign_id).first()
            ngo_data=NGO.query.filter_by(ngo_id=cam_data.ngo_id).first()
            c_d={'id':str(cam_data.campaign_id),'name':cam_data.campaign_name,'location':cam_data.campaign_location,'category':cam_data.campaign_category}
            print('nd',cam_data.ngo_id)
            n_d={'id':str(ngo_data.ngo_id),'name':ngo_data.ngo_name,'location':ngo_data.ngo_location}
            p_d={'id':str(el.payment_id),'mode':el.payment_type,'amount':el.payment_amount}
            result.append({'ngo':n_d,'campaign':c_d,'payments':p_d})
        return {"data":result},200
    except SQLAlchemyError as e:
        print(e)
        return {"messgae":"Internal Server Error"},500
    except Exception as e:
        print(e)
        return {"message":"Internal Server Error"},500






