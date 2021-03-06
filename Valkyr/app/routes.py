from flask import render_template, Flask, flash, request, redirect, url_for, send_file, abort, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app.models import User, Post, load_user, Comment
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, UploadForm, CommentForm
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTP_STATUS_CODES, HTTPException
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
        flash('You have successfully made an account. You are now able to log in!', 'success')
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
            print(filename)

            newFile = Post(title=form.title.data, data=file.read(), description=form.description.data,  user_id=current_user.id, filename=filename)
            db.session.add(newFile)
            db.session.commit()

        if form.validate_on_submit():
            flash('Your post has been created!', 'success')
            return redirect(url_for('upload_file',
                                    filename=filename))

    return render_template('upload.html', title='Upload', form=form, legend='Upload')


@app.route('/upload/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # only the user who created the post can make changes; if the user is not the author of the post it will return a Forbidden error page
    if post.author != current_user:
        abort(403)
    # don't let user change the video (no video field in UploadForm())
    form = UploadForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        # commit the changes made to title and description and update post 
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('upload', post_id=post.id))

    # prepopulate the form fields if it is a GET method
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        
    return render_template('upload.html', title='Update Post', form=form, legend='Update')


@app.route('/upload/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    # if the user is the author of the post then the user can delete the post and be redirected to home page
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))


# route for single post (/upload/1 . . . /upload/2)
# included the comment.html we incorporated {% include 'comment.html' %}
@app.route('/upload/<int:post_id>', methods=['GET', 'POST'])
def upload(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).all()
    form = CommentForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            # Comment gets added to database if form is validated on submit
            comment = Comment(text=form.comment.data, user_username=current_user.username, post_id=post.id, post_title=post.title)
            db.session.add(comment)
            db.session.commit()
            flash('Comment posted!', 'success')
            return redirect(url_for('upload', post_id=post.id))
    # if the user isn't logged in it will redirect to the login page
    if current_user.is_anonymous:
        if form.validate_on_submit():
            flash('Please log in to comment', 'danger')
            return redirect(url_for('login'))
    return render_template('post.html', post=post, form=form, comments=comments)


''' TODO - delete comment '''
# @app.route('/upload/<int:post_id>/delete/<int:comment_id>', methods=['GET', 'POST'])
# def delete_comment(id):
#     comment = Comment.query.get_or_404(id)
#     post = Post.query.get_or_404(comment.post_id)
#     if comment.user_username != current_user and post.author != current_user:
#         abort(403)
#     db.session.delete(comment)
#     db.session.commit()
#     flash('The comment has been deleted!', 'success')

#     return redirect(url_for('index'))


# send video file from our media folder 
@app.route('/media/<filename>')
def send_video(filename):
		return send_from_directory('/home/joe/Desktop/site/Valkyr/app/static/media', filename)


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


# redirect the user to user page when clicking on username and show their upload information
# and comment information
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
    .order_by(Post.date_posted.desc())\
    .paginate(page=page, per_page=4)
    comments = Comment.query.filter_by(user_username=username)\
    .order_by(Comment.timestamp.desc())\
    .paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user, comments=comments)

""" 
Error Handling starts here
"""


@app.errorhandler(500)
def special_exception_handler(e):
    return render_template('Errors/500.html'), 500


@app.errorhandler(401)
def unauthorized(e):
    return render_template('Errors/401.html'), 401


@app.errorhandler(404)
def error_page_not_found(e):
    return render_template('Errors/404.html'), 404


@app.errorhandler(400)
def handle_bad_request(e):
    return render_template('Errors/400.html'), 400


@app.errorhandler(429)
def too_many_request(e):
    return render_template('Errors/429.html'), 429


"""
Error Handling ends here
"""