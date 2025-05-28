from flask_restx import Namespace
class UserDTO:
    api = Namespace("users", description="User Related operations")