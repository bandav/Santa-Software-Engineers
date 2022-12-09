# models.py

from flask_login import UserMixin
from . import db

# Relations

###CREATE TABLE players (
###user_id integer, //FK to users
###game_id integer, //FK to games
###PRIMARY KEY (user_id, game_id)
###);
joined_game = db.Table('joined_game',
    db.Column('player_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
)

###CREATE TABLE gift_choice (
###gift_id integer, // FK to gifts
###user_id integer, //FK to users
###PRIMARY KEY (gift_id, user_id)
###);
# Likes in gifts, renamed relation so liked_gift for readability
liked_gift = db.Table('liked_gift',
    db.Column('liking_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('liked_id', db.Integer, db.ForeignKey('gift.id'))
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
    displayname = db.Column(db.String(250, index=True))

    liked = db.relationship('Gift', secondary=liked_gift,backref=db.backref('liked_gift', lazy='dynamic'), lazy='dynamic')
    
    def like(self, gift):
        if not self.is_liking(gift):
            self.liked.append(gift)

    def unlike(self, gift):
        if self.is_liking(gift):
            self.liked.remove(gift)

    def is_liking(self, gift):
        return self.liked.filter(
        liked_gift.c.liked_id == gift.id).count() > 0 

    joined = db.relationship('Game', secondary=joined_game,backref=db.backref('joined_game', lazy='dynamic'), lazy='dynamic')
    
    def join(self, game):
        if not self.is_playing(game):
            self.joined.append(game)

    def unjoin(self, game):
        if self.is_playing(game):
            self.joined.remove(game)

    def is_playing(self, game):
        return self.joined.filter(
        joined_game.c.game_id == game.id).count() > 0   

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
    price = db.Column(db.Integer, index=True)
    description = db.Column(db.String(250))
    purchase_link = db.Column(db.String(250))
    likes = db.Column(db.Integer)

###CREATE TABLE games (
###game_id integer PRIMARY KEY,
###admin varchar,
###num_active_players integer,
###max_capacity integer,
###max_price integer,
###min_price integer,
###);
class Game(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    title=db.Column(db.String(250))
    admin = db.Column(db.String(250))
    num_active_players = db.Column(db.Integer)
    max_capacity = db.Column(db.Integer)
    max_price = db.Column(db.Integer)
    min_price = db.Column(db.Integer)