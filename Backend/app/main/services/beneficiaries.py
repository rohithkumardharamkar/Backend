from flask import jsonify
from app.main.models.beneficiaries import Beneficiaries
from app.main.models.ngo import NGO
from utils.initdb import db
from sqlalchemy.exc import SQLAlchemyError


def add_to_beneficiary(data):
    try:
        ngo_id=data.get('ngo_id')
        beneficiary_name=data.get('beneficiary_name')
        beneficiary_address=data.get('beneficiary_address')

        if not all([ngo_id, beneficiary_name, beneficiary_address]):
            return jsonify({"message":"All fields are required"}),400
        beneficiary_data=Beneficiaries(ngo_id=ngo_id,beneficiary_name=beneficiary_name,beneficiary_address=beneficiary_address)
        db.session.add(beneficiary_data)
        db.session.commit()
        return jsonify({"message":"Beneficiary details added"}),200

    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500





# Get all beneficiaries
def get_beneficiaries():
    try:
        data =Beneficiaries.query.all()  
        result=[]
        for el in data:
            ngo_data=NGO.query.get(el.ngo_id)
            result.append({"name": el.beneficiary_name,"address":el.beneficiary_address,"ngo_data":ngo_data})     
        return jsonify({"beneficiaries":result}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    




# Get beneficiaries by NGO
def get_beneficiaries_by_ngo(ngo_id):
    try:
        data=Beneficiaries.query.filter_by(ngo_id=ngo_id).all()  
        result=[]
        for el in data:
            result.append({"name":el.beneficiary_name,"address":el.beneficiary_address})
        return jsonify({"data":result}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
