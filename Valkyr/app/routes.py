from flask import render_template, Flask, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app.models import User, Post, load_user
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, UploadForm
from werkzeug.utils import secure_filename
from app import app, bcrypt, db
import secrets, os
from PIL import Image


@app.route('/')
@app.route('/index')
def index():
    # retreive all the posts from our database
    posts = Post.query.all()
    user = {'username': 'user'}
    return render_template('index.html', title='Home', user=user, posts=posts)


""" The index() function imports a in-built function that comes with the Flask framework called render_template(). /
This function takes a template filename and a variable list of template arguments and returns the same template, \
but with all the placeholders in it replaced with actual values. """


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash password when form is submitted and create user instance
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully made an account. You are now able to log in!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        # check database for username and password
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # redirect the logged in user to the page they were trying to access before
            next_page = request.args.get('next')
            # redirect us to the next page route if the next_page is not None 
            # else it will redirect us to the home page
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Register', form=form)


ALLOWED_EXTENSIONS = {'mp4', '3gp', 'wmv', 'ogg', 'mp3', 'wav', 'mpg', 'avi', 'png'}  # A set for allowed file extensions


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
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

            newFile = Post(title=file.filename, data=file.read(), description=form.description.data,  user_id=current_user.id)
            db.session.add(newFile)
            db.session.commit()

        if form.validate_on_submit():
            flash('Your post has been created!')
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('upload.html', title='Upload', form=form)


# route for single post (/upload/1 . . . /upload/2)
@app.route('/upload/<int:post_id>')
def upload(post_id):
    # fetch post if it exists by id
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    # randomize name to avoid duplicates
    random_hex = secrets.token_hex(8)
    # split picture file name and concatenate using the random hex and the file extension
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # get full path where image will be saved
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)
    # resize picture with PIL module
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
    

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('account'))
    # prefill the fields on account page
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # set an image_file variable
    image_file = url_for('static', filename='profile_pic/'+ current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.errorhandler(404)
def error_page_not_found(error):
    # error_code = 404
    # error_message = "Sorry, page not found!"
    return render_template('Errors/404.html'), 404