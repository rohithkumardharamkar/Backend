from flask_restx import Namespace
class LikesDTO:
    api=Namespace('likes',description="user liked to campaigns operations")