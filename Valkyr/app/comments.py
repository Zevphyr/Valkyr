from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db


class Comment(db.Model):
    _Digit = 6

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    author = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship(
        'Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()
        prefix = self.parent.path + '.' if self.parent else ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._Digit)
        db.session.commit()

    def level(self):
        return len(self.path) // self._Digit - 1


""" Obtaining a unique id that increments automatically to use in the path;
obtains the id assigned by the database requiring that the comment is saved twice."""

# db.create_all()
# c1 = Comment(text='example1', author='user1')
# c2 = Comment(text='example2', author='user2')
# c11 = Comment(text='example3', author='user3', parent=c1)
# c12 = Comment(text='example4', author='user4', parent=c1)
# c111 = Comment(text='example5', author='user5', parent=c11)
# c21 = Comment(text='example6', author='user6', parent=c2)
# for comment in [c1, c2, c11, c12, c111, c21]:
#     comment.save()

# for comment in Comment.query.order_by(Comment.path):
#     print('{}{}: {}'.format('  ' * comment.level(), comment.author, comment.text))


"""  Not sure how to go about this further...
class Vote(db.Model):
    def change_vote(vote):
        for comment in Comment.query.filter(Comment.path.like(self.path + '%')):
            self.thread_vote = vote
            db.session.add(self)
        db.session.commit()

"""