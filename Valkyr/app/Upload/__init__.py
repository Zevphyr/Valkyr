from flask import Blueprint

bp = Blueprint('uploads', __name__)

# This import is at the bottom to avoid circular dependencies.
from Valkyr.app.Upload import upload