from flask import jsonify
from app.main.models.favoriteNgos import FavoriteNGO
from app.main.models.ngo import NGO
from utils.initdb import db
from sqlalchemy.exc import SQLAlchemyError



#Adding Favorite Ngos
def favorite_ngos(data):
    try:
        user_id=data.get('user_id')
        ngo_id=data.get('ngo_id')
        favorite_ngos=FavoriteNGO(user_id=user_id,ngo_id=ngo_id)
        db.session.add(favorite_ngos)
        db.session.commit()
        return jsonify({"message":"Added to Favortites"}),201
    except SQLAlchemyError as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    


#Get the NGO by the user_id
def get_favorite_ngo_by_user_id(user_id):
    try:
        data=FavoriteNGO.query.filter_by( user_id=user_id).first()
        if not data:
            return jsonify({"message":"No Favorites Found"}),404
        ngo_details=NGO.query.filter_by(ngo_id=data.ngo_id).all()
        result=[]
        for el in ngo_details:
            if el.is_deleted:
                continue
            ngo_data={"name":el.ngo_name}
            result.append(ngo_data)
        return jsonify({"message":result}),200
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500
    


#Remove From Favorites
def unfavorite(favorite_id):
    try:
        data=FavoriteNGO.query.filter_by(favorite_id=favorite_id).first()
        if not data or data.is_deleted:
            return jsonify({"message":"no found"}),200
        setattr(data,'is_deleted',True)
        db.session.commit()
        return jsonify({"message":"Removed from favorites"}),200

    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server Error"}),500




