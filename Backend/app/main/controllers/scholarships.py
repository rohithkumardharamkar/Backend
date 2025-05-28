from app.main.services.scholarships import Scholarship,scholarship_apply,get_scholarships,delete_scholarship,approve_scholarship
from app.main.dto.scholarships import ScholarshipDTO
from flask import jsonify,request
from flask_restx import Resource

scholarship_route=ScholarshipDTO.api
@scholarship_route.route("")
class Scholarships(Resource):
    def post(self):
        data=request.get_json()
        response,status=scholarship_apply(data),status
        return response,status
    def get(self):
        response,status=get_scholarships()
        return response,status
    def delete(self):
        scholarship_id=request.args.get('scholarship_id')
        response,status=delete_scholarship(scholarship_id)
        return response,status
    def patch(self):
        scholarship_id=request.args.get('scholarship_id')
        response,status=approve_scholarship(scholarship_id)
        return response,status



    





