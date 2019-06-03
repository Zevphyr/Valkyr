from flask import render_template, Flask, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app.forms import RegistrationForm, LoginForm
from app.Upload.upload import allowed_file, secure_filename
from app import app, bcrypt, db

@app.route('/')
@app.route('/index')
def index():
    # need to change this to acquire the user from the login form username data
    user = {'username': 'user'}
    return render_template('index.html', title='Home', user=user)


""" The index() function imports a in-built function that comes with the Flask framework called render_template(). /
This function takes a template filename and a variable list of template arguments and returns the same template, \
but with all the placeholders in it replaced with actual values. """


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
    # if the current user data matches with our database then it will redirect to home (will display log out route)
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        # hash password when form is submitted and create user instance
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # add and commit to database
        db.session.add(user)
        db.session.commit()
        # flash a message that says they have successfully registered
        flash('You have successfully made an account. You are now able to log in!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if the current user data matches with our database then it will redirect to home (will display log out route)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # check database for username and password
        # create user variable to filter by the username that the user inputted (if there isn't one then it will return None)
        user = User.query.filter_by(username=form.username.data).first()
        # create a conditional that checks if the user exists and that the password verifies with that they have in the base
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # log the user in and make sure you import the login_user function from flask_login and pass in the remember argument as the second argument
            login_user(user, remember=form.remember.data)
            # redirect the logged in user to the page they were trying to access before
            next_page = request.args.get('next')
            # redirect us to the next page route if the next_page is not None 
            # else it will just erdirect us to the home page
            return redirect(next_page) if next_page else(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
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

# implement an account info in navigation pane
# implement a check in place so the user is told to log in before they access the account page
@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')