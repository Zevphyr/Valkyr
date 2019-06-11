from flask import Flask, redirect, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from app import db



@app.route('/')
def index():
    return render_template('index.html')


# These next two routes don't work right out the box and just serve as rough example how it \
# would look
@app.route('/messages')
def messages():
    result = db.get('/messages', None)
    return render_template('list.html', messages=result)


@app.route('/submit_message', methods=['POST'])
def submit_message():
    message = {'body': request.form['message'],
               'who': request.form['who']}
    db.post('/messages', message)
    return redirect(url_for('messages'))
