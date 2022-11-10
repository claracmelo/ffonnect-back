from flask import Flask, jsonify 
from flask_login import LoginManager

import os

from dotenv import load_dotenv
load_dotenv() # takes the environment variables from .env

from resources.members import members 
from resources.user import user
import models
from flask_cors import CORS

DEBUG=True 
PORT=os.environ.get("PORT")

app = Flask(__name__) 
app.secret_key = os.environ.get("APP_SECRET")
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except:
        return None

CORS(members, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(members, url_prefix='/api/v1/members')
app.register_blueprint(user, url_prefix='/api/v1/user')

if __name__ == '__main__':
    models.initialize() 
    app.run(debug=DEBUG, port=PORT)