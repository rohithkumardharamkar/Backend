# from flask_mail import Mail,Message
# from manage import app

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT']=587
# app.config['MAIL_USERNAME']='rohith431431@gmail.com'
# app.config['MAIL_PASSWORD']='aqdeqmzqhqomnjql'
# app.config['MAIL_USE_TLS']=True
# app.config['MAIL_USE_SSL']=False

# mail=Mail(app)

# def send_email(subject,recipients,body,sender=None):
#     try:
#         msg=Message(subject,sender=sender or app.config['MAIL_USERNAME'],recipients=recipients)
#         msg.body=body
#         mail.send(msg)
#         return True
#     except Exception as e:
#         return "Failed to send the email",e

