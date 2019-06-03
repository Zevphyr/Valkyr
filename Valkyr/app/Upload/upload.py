import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from pathlib import Path


home = (Path.home())
UPLOAD_FOLDER = Path(home.joinpath('Desktop', 'git', 'collab_website', 'media'))
ALLOWED_EXTENSIONS = {'mp4', '3gp', 'wmv', 'ogg', 'mp3', 'wav', 'mpg', 'avi'}  # A set for allowed file extensions


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



