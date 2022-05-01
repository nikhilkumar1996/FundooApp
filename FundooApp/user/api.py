import os
import jwt
from flask import request, json
from flask_restful import Resource
from utility.util import get_token, account_activation_link, reset_password_link
from .model import User
from dotenv import load_dotenv
load_dotenv()


class UserLogin(Resource):
    def get(self):
        """
        API used to get User Registered
        :param request: EmailId and Password
        :return: Token is generated if user is registered
        """
        email_entered = request.args.get("Email")
        password = request.args.get("Password")
        details = User.objects.filter(email=email_entered).first()
        if details:
            if password == details.password:
                token = get_token(email_entered)
                return {"message": token}, 201
            else:
                return {"message": "Entered Wrong Password"}, 404
        else:

            return {"message": "User doesnt Exist"}, 404


class Registration(Resource):
    def post(self):
        """
        API used to create a User Info
        :param request: UserName,EmailID,PhoneNo,Password
        :return:User is registered and Activation Link is sent to the User EmailId
        """
        data = User.objects()
        record = json.loads(request.data)
        details = User(name=record['Name'],
                       email=record['Email'],
                       phone_no=record['PhoneNo'],
                       password=record['Password'])
        for user in data:
            if user.name == details.name:
                return {"message": "User Already Exists"}, 409
        for user in data:
            if user.email == details.email:
                return {"message": "Email Already Exists"}, 409
        details.save()
        token = get_token(details.email)
        account_activation_link(details.email, token, details.name)
        return {"message": "User Added Check your registered mail id to activate account"}, 201


class ActivateEmail(Resource):
    def get(self):
        """
        This API Activates the User Account after verifying the User by Token Header
        :param request:token required decorator for verifying User Info
        :return: Account is Active
        """
        token = request.args.get("activate")
        payload = jwt.decode(token, str(os.getenv('SECRET_KEY')), algorithms=["HS256"])
        data = User.objects.filter(email=payload['Email']).first()
        if data:
            data.is_active = True
            data.save()
            return {'message': 'Your account is active'}, 204
        else:
            return{"message": "User is missing"}, 404


class ForgotPassword(Resource):
    def get(self):
        """
        This API is used to send reset_password_link to the User Account Email
        :param request:Email_Id
        :return: Link Send to the User Email
        """
        id_email = request.args.get('Email')
        details = User.objects.filter(email=id_email).first()
        if details:
            token = get_token(details.email)
            reset_password_link(details.email, token, details.name)
            return {"message": "Link Sent to Email"}, 200
        else:
            return {"message": "Wrong Credentials Provided"}, 404


class ResetPassword(Resource):
    def patch(self):
        """
        This API reset the password after token is generated and reset link is send after using Forget Password API
        :param request:token required decorator,User Password to be changed
        :return:Password changed successfully
        """
        record = json.loads(request.data)
        user = User(password=record["Password"])
        token = request.args.get("reset")
        payload = jwt.decode(token, str(os.getenv('SECRET_KEY')), algorithms=["HS256"])
        data = User.objects.filter(email=payload['Email']).first()
        if not data:
            return {"message": "No User Found"}, 404
        if data.password == user.password:
            return {"message": "You typed same Password"}, 409
        if data.is_active:
            data.update(password=record['Password'])
            return {"message": "Password Changed Successfully"}, 204
        else:
            return{"message": "User Already Active"}, 409














