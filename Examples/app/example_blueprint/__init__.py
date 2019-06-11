from flask import Blueprint

bp = Blueprint('example', __name__)

from app.example_blueprint import example