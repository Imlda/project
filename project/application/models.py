from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.String(256), default="default.jpg")
    likes = db.relationship("Like", backref="user", lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

class PokemonPost(db.Model):
    __tablename__ = "pokemon_posts"
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    image_url = db.Column(db.String(256), nullable=False)
    post_date = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.relationship("Like", backref="pokemon_post", lazy=True)

    def like(self, user):
        if not self.is_liked_by(user):
            like = Like(user_id=user.id, pokemon_post_id=self.id)
            db.session.add(like)
            db.session.commit()

    def unlike(self, user):
        like = Like.query.filter_by(user_id=user.id, pokemon_post_id=self.id).first()
        if like:
            db.session.delete(like)
            db.session.commit()

    def is_liked_by(self, user):
        return Like.query.filter_by(user_id=user.id, pokemon_post_id=self.id).count() > 0

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pokemon_post_id = db.Column(db.Integer, db.ForeignKey('pokemon_posts.id'), nullable=False)
    like_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
 