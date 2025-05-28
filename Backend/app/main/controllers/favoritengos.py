from app.main.dto.favoritengos import FavoriteNgoDTO
from app.main.services.favoritengos import favorite_ngos,get_favorite_ngo_by_user_id,unfavorite
from flask_restx import Resource
from flask import request
favorite_route=FavoriteNgoDTO.api
# @favorite_route.route("")
# class AddFavorite(Resource):
#     def post(self):
#         data=request.get_json()
#         return favorite_ngos(data)
#     def delete(self):
#         data=request.args.get('')
#     def patch(self):
        
    


