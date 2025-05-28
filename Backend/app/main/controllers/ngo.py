from app.main.services.ngos import add_ngo,delete_ngo,get_ngo_owner_details,ngo_status_change,blacklist_ngo,get_ngo_registered,get_ngo_updated,get_ngo_by_user_id
from app.main.dto.ngos import NgoDTO
from flask import jsonify,request
from flask_restx import Resource




ngo_route=NgoDTO.api
@ngo_route.route("/")
class NGO(Resource):
    def post(self):
        data=request.get_json()
        response,data=add_ngo(data)
        return response,data
    def delete(self):
        name=request.args.get('name')
        response,data=delete_ngo(name)
        return response,data
    def get(self):
        name=request.args.get('name') 
        location=request.args.get('location')
        status=request.args.get('status')
        ngo_status=request.args.get('ngo_status')
        response,data=get_ngo_owner_details(name,location,status,ngo_status)
        return response,data
    def patch(self):
        data=request.get_json()
        response,status=ngo_status_change(data)
        return response,status




@ngo_route.route('/blacklisted')
class BlacklistedNgo(Resource):
    def post(self):
        id=request.args.get('id')
        response,data=blacklist_ngo(id)
        return response,data
    



@ngo_route.route('/registerd')
class RegisteredNGO(Resource):
    def get(self):
        limit=request.args.get('limit')
        response,data=get_ngo_registered(limit)
        return response,data






@ngo_route.route("/updated")
class UpdatedNGO(Resource):
    def get(self):
        limit=request.args.get('limit')
        response,data=get_ngo_updated(limit)
        return response,data
    





    

@ngo_route.route('/details')
class NGODetails(Resource):
    def post(self):
        data=request.get_json()
        response=get_ngo_by_user_id(data)
        return response
