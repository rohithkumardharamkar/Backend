from models.newsletter import NewsLetter
from flask import jsonify
from utils.initdb import db
from sqlalchemy.exc import SQLAlchemyError
from utils.send_email import send_email
from flask import request
#add the newsletter
def add_news_letter(data):
    try:
        email=data.get('email')
        name=data.get('name')
        if not email or not name:
            return jsonify({"message":"Invalid Details"}),404
        data=NewsLetter(email=email,name=name)
        db.session.add(data)
        db.session.commit()
        return jsonify({"message":"The New Newsletter is added"}),200
    except SQLAlchemyError  as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"message":"Internal Server ERror"}),500
    



#Send the NewsLettter
def send_news_letter(data):
    try:
        content=data.get('content')
        subject=data.get('subject')
        l=[]
        data=NewsLetter.query.all()
        for el in data:
            l.append(el.email)
        send_email(subject=subject,recipients=l,body=content)
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        return jsonify({"message":"Internal Server Error"}),500
    except Exception as e:
        print(e)
        return jsonify({"messgae":"Internal Server Error"}),500
