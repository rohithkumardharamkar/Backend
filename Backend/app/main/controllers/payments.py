from flask_restx import Resource
from app.main.dto.payments import Payment
from flask import request
from app.main.services.payments import add_to_payment,get_payments_by_campaign_id,get_payments_by_last_n_days,get_payments_count_by_user_id,get_payments_sum_by_user_id

payment_route=Payment.api


@payment_route.route('')
class Payments(Resource):
    def post(self):
        data=request.get_json()
        response,status=add_to_payment(data)
        return response,status
    def get(self):
        limit=request.args.get('l')
        response,status=get_payments_by_last_n_days(limit)
        return response,status
        
        


@payment_route.route('/users')
class PaymentUsers(Resource):
    def get(self):
        response,status=get_payments_sum_by_user_id()
        return response,status

@payment_route.route('/campaigns')
class PaymentCampaigns(Resource):
    def get(self):
        response,status=get_payments_by_campaign_id()
        return response,status


@payment_route.route('/topdonors')
class TopDoners(Resource):
    def get(self):
        response,status=get_payments_sum_by_user_id()
        return response,status

        

