import os
from flask import Flask
from flask_restful import Api
from user.api import UserLogin, Registration, ForgotPassword, ActivateEmail, ResetPassword
from notes.api import NotesOperations
from db.database import connect_db
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET KEY'] = os.getenv('SECRET_KEY')
api = Api(app)

connect_db()

api.add_resource(UserLogin, '/login')
api.add_resource(Registration, '/register')
api.add_resource(ActivateEmail, '/activate_email')
api.add_resource(ForgotPassword, '/forgot_password')
api.add_resource(ResetPassword, '/reset_password')
api.add_resource(NotesOperations, '/notes')

if __name__ == '__main__':
    app.run(debug=True)