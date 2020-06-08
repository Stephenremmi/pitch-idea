from . import db
from werkzeug.security import (generate_password_hash,
                               check_password_hash)
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer,primary_key = True)
    post_title = db.Column(db.String)
    post_content = db.Column(db.String)
    posted_at = db.Column(db.DateTime,default=datetime.utcnow)
    category = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship("Comment",backref = "post_comments",lazy = "dynamic")

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user_posts(cls,id):
        posts = Post.query.filter_by(user_id = id).all()
        return posts

    @classmethod
    def get_all_posts(cls):
        return Post.query.order_by(Post.posted_at.asc()).all()

class Comment(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    posted_at = db.Column(db.DateTime,default=datetime.utcnow)
    post_id = db.Column(db.Integer,db.ForeignKey("posts.post_id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Post.query.filter_by(post_id = id).all()
        return comments

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    full_name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique = True)
    email = db.Column(db.String(255), unique = True, index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    posts = db.relationship("Post",backref = "posts",lazy = "dynamic")
    comments = db.relationship("Comment",backref = "comments",lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # string representaion to print out a row of a column, important in debugging
    def __repr__(self):
        return f'User {self.username}'



