from app.main.dto.campaigns import CampaignsDTO
from app.main.services.campaigns import add_campaigns,get_campaigns_by_location, delete_campaigns,get_campaigns,get_active_campaigns,get_inactive_campaigns
from flask import request,jsonify
from flask_restx import Resource
campaign_route=CampaignsDTO.api
@campaign_route.route("/")
class Campaigns(Resource):
    def post(self):
        data=request.get_json()
        response,data=add_campaigns(data)
        return response,data
    def get(self):
        campaign_id=request.args.get('campaign_id')
        campaign_name=request.args.get('campaign_name')
        ngo_id=request.args.get('ngo_id')
        response=get_campaigns(campaign_id,campaign_name,ngo_id)
        return response
    def delete(self):
        campaign_id=request.args.get('campaign_id')
        response,status=delete_campaigns(campaign_id)
        return response,status


@campaign_route.route("/active")
class ActiveCampaigns(Resource):
    def get(self):
        response,status=get_active_campaigns()
        return response,status
@campaign_route.route("/inactive")
class InactiveCampaigns(Resource):
    def get(self):
        response,status=get_inactive_campaigns()
        return response,status
    

@campaign_route.route('/location')
class Location(Resource):
    def get(self):
        location=request.args.get('location')
        response,status=get_campaigns_by_location(location)
        return response,status
    
    