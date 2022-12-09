from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from .models import Game, Gift
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from . import db
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.types import String

stats = Blueprint('stats', __name__)

@stats.route('/stats')
def show_stats():
    url = db.engine.url
    engine = create_engine(url)
    num_created = 0
    num_joined = 0

    all_games = Game.query.all()
    for game in all_games:
        if current_user.is_playing(game):
            num_joined += 1
        
        #prepared statement
        admin_sql = text("SELECT admin FROM game WHERE id = :id").bindparams(bindparam("id", String))
        results = engine.execute(admin_sql, id=game.id)
        admin = results.first()[0]

        if (admin == current_user.username):
            num_created += 1

    num_liked = 0
    max_liked_price = -1
    min_liked_price = 1238492291

    all_gifts = Gift.query.all()
    for gift in all_gifts:
        if current_user.is_liking(gift):
            num_liked += 1
            # price = gift.price

            #prepared statement
            price_sql = text("SELECT price FROM gift WHERE id = :id").bindparams(bindparam("id", String))
            results = engine.execute(price_sql, id=gift.id)
            price = results.first()[0]

            if (price > max_liked_price):
                max_liked_price = price
            if (price < min_liked_price):
                min_liked_price = price
    
    # no liked gifts
    if (max_liked_price == -1 and min_liked_price == 1238492291):
        max_liked_price = 0
        min_liked_price = 0

    stats_html = "<div class=\"box\"> \
        <article class=\"media\">\
          <div class=\"media-content\">\
            <div class=\"content\">\
              <p>\
                Number of games created: " + str(num_created) + "</p>\
                <br>" + "Number of games joined: " + str(num_joined) + "</p>\
                <br>" + "Number of gifts liked: " + str(num_liked) + "</p>\
                <br>" + "Maximum price of all gifts liked: " + str(max_liked_price) + "</p>\
                <br>" + "Minimum price of all gifts liked: " + str(min_liked_price) + "</p>\
            </div>\
        </article>\
        </div>"

    return render_template('stats.html', name=current_user.username, stats_html=stats_html)