from app.main.dto.campaigncategory import CampaignCategoryDTO
from app.main.services.campaign_category import add_campaign_category
from flask import request
from flask_restx import Resource


category_route=CampaignCategoryDTO.api

@category_route.route('/')
class Category(Resource):
    def post(self):
        data=request.get_json()
        response,status=add_campaign_category(data)
        return response,status

