from authlib.integrations.flask_client import OAuth

GOOGLE_CLIENT_ID = '1057264778733-s6qtht4qro8tct21qrv5if55ko5scdf8.apps.googleusercontent.com'
GOOGLE_SERVER_ID = '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'

oauth = OAuth()  

def init_oauth(app):
    oauth.init_app(app)  

    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_SERVER_ID,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid profile email'}
    )
