from utils.initdb import db
from manage import create_app
from flask_cors import CORS


app=create_app()
CORS(app,supports_credentials=True)

if __name__=="__main__":
    app.run(debug=True,port=4000)





