from flask import Flask, jsonify, after_this_request
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

# Deja added
if os.environ.get('FLASK_ENV') != 'development':
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='None',
)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except:
        return None

CORS(members, origins=['https://ffonnect.herokuapp.com','http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['https://ffonnect.herokuapp.com','http://localhost:3000'], supports_credentials=True)

app.register_blueprint(members, url_prefix='/api/v1/members')
app.register_blueprint(user, url_prefix='/api/v1/user')


@app.before_request # use this decorator to cause a function to run before reqs
def before_request():
    print()
    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)

if __name__ == '__main__':
    models.initialize() 
    app.run(debug=DEBUG, port=PORT)

if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()