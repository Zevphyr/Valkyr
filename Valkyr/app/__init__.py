from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

# Imports the Upload blueprint
from app.Upload import bp as upload_bp
app.register_blueprint(upload_bp)

from app.Upload.upload import UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# crf token for login and register (set an environment variable using secrets.token_hex(16))
# create a database first with db.create_all() before you start registering users 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# login is the name of our route 
# when a user who isn't logged in is trying to go their account page, it will redirect them to the login route
# saying "Please log in to access this page."
login_manager.login_view = 'login'
# color of log in flash message 
login_manager.login_message_category = 'info'

from app import routes
