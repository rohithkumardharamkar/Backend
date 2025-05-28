# utils/email_utils.py

from flask_mail import Message,Mail
from flask import current_app
from utils.extension import mail
# from app import mail  # This imports the `mail` object from app/__init__.py

def send_email(subject, recipients, body):
    try:
        print('debug-1')
        msg = Message(subject,sender='rohithkumardharamkar@gmail.com',recipients=recipients)
        print('debug-2')
        msg.body = body
        mail.send(msg)
        print('debug-3')
        return True
    except Exception as e:
        current_app.logger.exception("Failed to send email")
        return False
