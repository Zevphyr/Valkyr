from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Imports the Upload blueprint
from app.Upload import bp as upload_bp
app.register_blueprint(upload_bp)

from app.Upload.upload import UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# crf token for login and register (set an environment variable using secrets.token_hex(16))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from app import routes
