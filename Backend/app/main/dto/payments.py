from flask_restx import Namespace
class Payment:
    api=Namespace('payments',description='Payment related Operations')