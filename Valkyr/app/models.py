from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


# Decorator: user.loader is for reloading the user from the user id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# add the UserMixin class into User class so that it inherits the methods and attributes from it 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # default image for user profile picture (static/profile_pic/default.jpg)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # find all posts by one user, referencing Post model
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    data = db.Column(db.LargeBinary)
    filename = db.Column(db.String(20))

    # referencing user.id in User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.user_id}', '{self.filename}')"