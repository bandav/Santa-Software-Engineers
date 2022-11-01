# models.py

from flask_login import UserMixin
from . import db

# Relations

###CREATE TABLE gift_choice (
###gift_id integer, // FK to gifts
###user_id integer, //FK to users
###PRIMARY KEY (gift_id, user_id)
###);
gift_choice = db.Table('gift_choice', 
    db.Column('gift_id', db.Integer, db.ForeignKey('gift.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

###CREATE TABLE players (
###user_id integer, //FK to users
###game_id integer, //FK to games
###PRIMARY KEY (user_id, game_id)
###);
players = db.Table('players',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

# Tables

###CREATE TABLE users (
###user_id integer PRIMARY KEY,
###username varchar(250),
###display_name varchar(250),
###encrypted_password varchar(250)
###);

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    displayname = db.Column(db.String(250))
    gift_choice = db.relationship('Gift', secondary=gift_choice, lazy='subquery', backref=db.backref('users', lazy=True))


###CREATE TABLE gifts (
###gift_id integer PRIMARY KEY,
###gift_name varchar(250),
###price_range_id integer, //FK to price_ranges
###description varchar(250),
###purchase_link varchar(250)
###);
class Gift(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    gift_name = db.Column(db.String(250), unique=True)
    price_range_id = db.Column(db.Integer, db.ForeignKey('price.id'), nullable=False)
    description = db.Column(db.String(250))
    purchase_link = db.Column(db.String(250))

###CREATE TABLE games (
###game_id integer PRIMARY KEY,
###admin varchar,
###num_active_players integer,
###max_capacity integer,
###price_range integer, //FK to price_ranges
###has_started integer,
###);
class Game(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    admin = db.Column(db.String(250))
    num_active_players = db.Column(db.Integer)
    max_capacity = db.Column(db.Integer)
    price_range = db.Column(db.Integer, db.ForeignKey('price.id'), nullable=False)
    has_started = db.Column(db.Integer)
    players = db.relationship('User', secondary=players, lazy='subquery', backref=db.backref('games', lazy=True))

###CREATE TABLE price_ranges (
###price_range_id integer PRIMARY KEY,
###min integer,
###max integer
###);
class Pricerange(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    min = db.Column(db.Integer, nullable=False)
    max = db.Column(db.Integer, nullable=False)
    gifts = db.relationship('Gift', backref='price', lazy=True)
    games = db.relationship('Game', backref='price', lazy=True)