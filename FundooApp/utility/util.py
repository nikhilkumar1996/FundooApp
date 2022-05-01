import os
from user.model import User
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from email.message import EmailMessage
import smtplib
import jwt
from dotenv import load_dotenv
load_dotenv()


token_dict = {}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers.get('access-token')
        if not token:
            return jsonify(message='Token is missing!')
        try:
            data = jwt.decode(token, str(os.environ.get('SECRET_KEY')), algorithms=["HS256"])
            current_user = User.objects.filter(email=data['Email']).first()
            print(current_user)
            user = {'user': current_user}
            print(user)
        except:
            return jsonify(message='Token is invalid')

        return f(*args, **user)

    return decorated


def get_token(email):
    token = jwt.encode({'Email': email, 'Exp': str(datetime.utcnow() + timedelta(seconds=600))},
                       str(os.getenv('SECRET_KEY')))
    return token


def access_token(log_id):
    token = jwt.encode({'LogId': log_id, 'Exp': str(datetime.utcnow() + timedelta(seconds=600))},
                       str(os.getenv('SECRET_KEY')))
    return token


def account_activation_link(email, token, name):
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    msg = EmailMessage()
    msg['Subject'] = 'Activate Account'
    msg['From'] = email_address
    msg['To'] = email
    msg.set_content(f"Hello {name}, \n Click the Link to activate your account "
                    f"http://127.0.0.1:5000/activate_email?activate={token}")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    server.send_message(msg)


def reset_password_link(email, token, name):
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    msg = EmailMessage()
    msg['Subject'] = 'Reset Password'
    msg['From'] = email_address
    msg['To'] = email
    msg.set_content(f"Hello {name}, \n Click the Link to Reset your Password "
                    f"http://127.0.0.1:5000/reset_password?reset={token}")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    server.send_message(msg)


