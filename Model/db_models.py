from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    searches = db.relationship('UserSearch', backref='user', lazy=True)
    search_keywords = db.relationship('SearchKeyword', backref='user', lazy=True)

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class SearchKeyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    keywords = db.Column(db.String(256), nullable=False)
    seller_type = db.Column(db.String(50))
    seller_country = db.Column(db.String(50))
    search_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    listings = db.relationship('Listing', backref='search', lazy=True)
    user_searches = db.relationship('UserSearch', backref='search_keyword', lazy=True)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey('search_keyword.id'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)
    sales = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    industry = db.Column(db.String(100))
    platform = db.Column(db.String(100))
    last_delivery = db.Column(db.Date)
    seller_rank = db.Column(db.Integer)

class UserSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    search_id = db.Column(db.Integer, db.ForeignKey('search_keyword.id'), nullable=False)


def init_app(app):
    db.init_app(app)