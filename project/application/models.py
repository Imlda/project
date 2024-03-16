from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.String(256), default="default.jpg")
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.relationship("Like", backref="user", lazy=True)

class PokemonPost(db.Model):
    __tablename__ = "pokemon_posts"
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(256), nullable=False)
    image_url = db.Column(db.String(256), nullable=False)
    post_date = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.relationship("Like", backref="pokemon_post", lazy=True)

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pokemon_post_id = db.Column(db.Integer, db.ForeignKey('pokemon_posts.id'), nullable=False)
    like_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
