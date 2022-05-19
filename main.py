import os
from flask_restful_swagger import swagger
from flask import Flask
from flask_restful import Api
from routes import all_routes
from db.database import connect_db
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET KEY'] = os.getenv('SECRET_KEY')
# api = Api(app)
api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/swagger')

connect_db()


def run_apis():
    for route in all_routes:
        api_class = route[0]
        endpoint = route[1]
        api.add_resource(api_class, endpoint)


run_apis()

if __name__ == '__main__':
    app.run(debug=True)