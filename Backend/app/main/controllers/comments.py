from app.main.dto.Comments import CommentsDTO
from app.main.services.comments import Comments
from flask import jsonify,request
from flask_restx import Resource
from app.main.services.comments import campaign_commented,get_comments_by_campaigns,group_by_comments,remove_comment
comment_route=CommentsDTO.api

@comment_route.route('/')
class Comments(Resource):
    def post(self):
        data=request.get_json()
        response,status=Comments(data)
        return response,status
    def delete(self):
        comment_id=request.args.get('comment_id')
        response,status=remove_comment(comment_id)
        return response,status
    def get(self):
        campaign_id=request.args.get('campaign_id')
        response,status=get_comments_by_campaigns(campaign_id)
        return response,status
    
@comment_route.route('/campaigns')
class CommentCampaign(Resource):
    def get(self):
        response,status=group_by_comments()
        return response,status