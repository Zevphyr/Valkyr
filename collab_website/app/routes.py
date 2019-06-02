from flask import render_template, Flask, flash, request, redirect, url_for
from flask_login import logout_user
from app.forms import RegistrationForm, LoginForm
from app.Upload.upload import allowed_file, secure_filename
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'user'}
    return render_template('index.html', title='Home', user=user)


""" The index() function imports a in-built function that comes with the Flask framework called render_template(). /
This function takes a template filename and a variable list of template arguments and returns the same template, \
but with all the placeholders in it replaced with actual values. """


# TODO: Need to set up user authentication

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html', title='Register', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
        return render_template('upload.html', title='Upload', form=form)


@app.route('/logout')
def logout():
    logout_user()
return redirect(url_for('index'))


