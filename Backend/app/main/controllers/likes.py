from app.main.dto.likes import LikesDTO
from app.main.services.likes import campaign_liked
from flask import jsonify,request
from flask_restx import Resource
liked_route=LikesDTO.api

@liked_route.route("")
class Likes(Resource):
    def post(self):
        data=request.get_json()
        response=campaign_liked(data)
        return response
    
