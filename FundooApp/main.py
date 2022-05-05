import os
from flask import Flask
from flask_restful import Api
from user.api import UserLogin, Registration, ForgotPassword, ActivateEmail, ResetPassword
from notes.api import NotesOperations, PinNotes, TrashNote, GetLabels
from label.api import LabelOperations
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
api.add_resource(PinNotes, '/pin_notes')
api.add_resource(TrashNote, '/trash_notes')
api.add_resource(LabelOperations, '/labels')
api.add_resource(GetLabels, '/get_labels')

if __name__ == '__main__':
    app.run(debug=True)