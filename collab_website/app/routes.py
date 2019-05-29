from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'user'}
    return render_template('index.html', title='Home', user=user)


""" The index() function imports a in-built function that comes with the Flask framework called render_template(). /
This function takes a template filename and a variable list of template arguments and returns the same template, \
but with all the placeholders in it replaced with actual values. """