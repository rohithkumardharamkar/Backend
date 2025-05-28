from flask import Flask,current_app
from utils.initdb import db
from app.main.models.users import Users
from app.main.models.ngo import NGO
from app.main.models.blogs import Blogs
from app.main.models.campaigncategory import CampaignsCategories
from app.main.models.campaigns import Campaigns
from app.main.models.campaigncategory import CampaignsCategories
from app.main.models.favoriteNgos import FavoriteNGO
from app.main.models.comments import Comments
from app.main.models.beneficiaries import Beneficiaries
from app.main.models.Likes import Likes
from app.main.models.newsletter import NewsLetter
from app.main.models.payments import Payments
from app.main.models.scholarship import Scholarship
# from authlib.integrations.flask_client import OAuth
from app.main.config.api_keys import init_oauth
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.main.controllers import blueprint  
from utils.extension import mail

def create_app():
    app=Flask(__name__)
    CORS(app)
    app.config.from_object('app.main.config.app_config')
    app.config.from_object('app.main.config.mail_config')
    app.secret_key='Rohith_Kumar'
    print("connected to database")
    db.init_app(app)
    mail.init_app(app)
    init_oauth(app)
    app.register_blueprint(blueprint)

    with app.app_context():
        db.create_all()
        print('tables created')
    return app



















# GOOGLE_CLIENT_ID='1057264778733-s6qtht4qro8tct21qrv5if55ko5scdf8.apps.googleusercontent.com'
# GOOGLE_SERVER_ID='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'

# app=create_app()

# oauth=OAuth(app)
# google=oauth.register(
#     name='google',
#     client_id=GOOGLE_CLIENT_ID,
#     client_secret=GOOGLE_SERVER_ID,
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope':'openid profile email'}
# )


app=create_app()