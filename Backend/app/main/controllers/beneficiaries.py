from app.main.dto.beneficiaries import BeneficiaryDTO
from app.main.services.beneficiaries import add_to_beneficiary,get_beneficiaries
from flask import request
from flask_restx import Resource
beneciary_route=BeneficiaryDTO.api

@beneciary_route.route("/")
class Beneficiaries(Resource):
    def post(self):
        data=request.get_json
        response,status=add_to_beneficiary(data)
        return response,status
    def get(self):
        response,status=get_beneficiaries()
        return response,status
        