from flask import Blueprint
from flask_restx import Api
from app.main.controllers.users import user_route
from app.main.controllers.scholarships import scholarship_route
from app.main.controllers.payments import payment_route
from app.main.controllers.ngo import ngo_route
from app.main.controllers.likes import liked_route
from app.main.controllers.comments import comment_route
from app.main.controllers.campaigns import campaign_route
from app.main.controllers.campaigncategories import category_route
from app.main.controllers.beneficiaries import beneciary_route

blueprint=Blueprint('api',__name__)

api=Api(blueprint,title='Altrusys apis',version='1.0',description='atrusys web apis')

api.add_namespace(user_route)
api.add_namespace(scholarship_route)
api.add_namespace(payment_route)
api.add_namespace(ngo_route)
api.add_namespace(liked_route)
api.add_namespace(comment_route)
api.add_namespace(campaign_route)
api.add_namespace(category_route)
api.add_namespace(beneciary_route)