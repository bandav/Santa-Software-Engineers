from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from .models import User, Game
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from . import db
from werkzeug.security import generate_password_hash
import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.types import String

games = Blueprint('games', __name__)

@games.route('/show_create_game')
def show_create_game():
      return render_template('create_game.html')

@games.route('/create_game', methods=['POST'])
def create_game():
      return render_template('create_game.html')

@games.route('/game_created', methods=['POST'])
def game_creation_handler():
    if request.form.get('action') == "Game Created": 
        
        title = request.form.get('title')
        max_capacity = request.form.get('max_capacity')
        max_price = request.form.get('max_price')
        min_price = request.form.get('min_price')

        if not title or not max_capacity or not max_price or not min_price:
          flash('Fill out all the fields!')
          return redirect(url_for('games.show_create_game'))
            

        new_game = Game(title=title, admin=current_user.username, num_active_players=1, max_capacity=max_capacity, max_price=max_price, min_price=min_price)
        current_user.join(new_game)
        
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('main.profile'))

@games.route('/disp_created_games/<id>/<game_num>')
def disp_created_games(id, game_num):  
    game_list = get_created_games(id)
    if (len(game_list) == 0):
        return "You have no created games. Go back and create one!"
    game_num = int(game_num)
    list_len = len(game_list)
    while (game_num >= list_len):
        game_num-=1
    game_html = game_to_html(game_list[game_num])
    return render_template('created_games.html', id=id, game_num=game_num, game_html=game_html, list_len=list_len)

def get_created_games(id):
    print("hit!!")
    print("id is this: " + id)
    url = db.engine.url
    engine = create_engine(url)
    session = Session(bind=engine)
    session.connection(execution_options={"isolation_level": "READ UNCOMMITTED"})  
    user = User.query.filter_by(id=id).first()
    print("user" + user.username)     
    created_games = Game.query.filter_by(admin=user.username)
    print(created_games)
    result = []
    for game in created_games:
      result.append(game.id)
    session.commit()
    return result

@games.route('/disp_all_games/<game_num>')
def disp_all_games(game_num):  
    game_list = get_all_games()
    if (len(game_list) == 0):
        return "No games right now!"
    game_num = int(game_num)
    list_len = len(game_list)
    while (game_num >= list_len):
        game_num-=1
    game_html = game_to_html(game_list[game_num])
    return render_template('all_games.html', game_num=game_num, game_html=game_html, list_len=list_len)

def get_all_games():   
    all_games = Game.query.all()
    result = []
    for game in all_games:
      result.append(game.id)
    return result

@games.route('/disp_joined_games/<id>/<game_num>')
def disp_joined_games(id, game_num):
    game_list = get_joined_games(id)
    if (not game_list or len(game_list) == 0):
        return "You have no joined games. Go back to join one!"
    game_num = int(game_num)
    list_len = len(game_list)
    while (game_num >= list_len):
        game_num-=1
    game_html = game_to_html(game_list[game_num])
    return render_template('joined_games.html', id=id, game_num=game_num, game_html=game_html, list_len=list_len)

def get_joined_games(id):
    all_games = Game.query.all()
    result = []
    for game in all_games:
      if current_user.is_playing(game):
        result.append(game.id)
    return result

@games.route('/join_game/<id>')
def join_game(id):
  url = db.engine.url
  engine = create_engine(url)
  session = Session(bind=engine)
  session.connection(execution_options={"isolation_level": "READ UNCOMMITTED"})  
  game = Game.query.filter_by(id=id).first()
  if current_user.is_playing(game):
      flash("You're already playing this game!")
      return redirect(url_for('main.profile'))
  game.num_active_players += 1
  current_user.join(game)
  session.commit()
  db.session.commit()
  if 'url' in cur_session:
    return redirect(cur_session['url'])
  else:
    return redirect(url_for('main.profile'))

@games.route('/unjoin_game/<id>')
def unjoin_game(id):
  url = db.engine.url
  engine = create_engine(url)
  session = Session(bind=engine)
  session.connection(execution_options={"isolation_level": "READ UNCOMMITTED"})  
  game = Game.query.filter_by(id=id).first()
  if game is None:
      return redirect(url_for('index', id=id))
  game.num_active_players -= 1
  current_user.unjoin(game)
  session.commit()
  db.session.commit()
  if 'url' in cur_session:
    return redirect(cur_session['url'])
  else:
    return redirect(url_for('main.profile')) 

def game_to_html(game_id):
    cur_session['url'] = request.url
    url = db.engine.url
    engine = create_engine(url)

    obj = Game.query.filter_by(id=game_id).first()

    #prepared statement
    admin_sql = text("SELECT admin FROM game WHERE id = :id").bindparams(bindparam("id", String))
    results = engine.execute(admin_sql, id=game_id)
    admin = results.first()[0]

    print(admin)
    count = 0

    html_string_base = "<div class=\"box\"> \
        <article class=\"media\">\
          <div class=\"media-content\">\
            <div class=\"content\">\
              <p>\
                <strong>" + str(obj.title) + "</strong>\
                <br>" + "Created by: @" + str(admin) + "</p>\
                <br>" + "Capacity: " + str(obj.num_active_players) + "/" + str(obj.max_capacity) + "</p>\
                <br>" + "Gifts range from $" + str(obj.min_price) + " to $" + str(obj.max_price) + "</p>\
            </div>\
        </article>\
        </div>"

    html_string_unjoined = "<form action=\"/join_game/"+str(game_id)+"\">\
                  <button class=\"button is-block is-black is-medium is-fullwidth\" button style=\"margin:5px\">Join Game</button>\
                </form>"

    html_string_joined = " <form action=\"/unjoin_game/"+str(game_id)+"\">\
                <button class=\"button is-block is-black is-medium is-fullwidth\" button style=\"margin:5px\">Leave Game</button>\
              </form>"

    html_string_view = "<div class=\"level-right\">\
              <form action=\"/view_game/"+str(game_id)+"\">\
                <button class=\"button is-block is-black  is-medium is-fullwidth\">View Game</button>\
              </form>"

    html_string_base += html_string_view
    if current_user.is_playing(obj) and obj.admin != current_user.username:
      html_string_base += html_string_joined
    else:
      if (obj.num_active_players < obj.max_capacity) and obj.admin != current_user.username:
        html_string_base += html_string_unjoined 
  

    # Finish off whatever button state the post had
    html_string_base += "</nav>"

    # Finish off the whole html
    html_string_base += "</div>"

    return html_string_base

@games.route('/view_game/<game_num>')
def view_game(game_num): 
  url = db.engine.url
  engine = create_engine(url)
  session = Session(bind=engine)
  session.connection(execution_options={"isolation_level": "READ UNCOMMITTED"})  
  game_num = int(game_num)
  game_list = get_all_games()
  list_len = len(game_list)
  if (game_num > 0):
    game_num -= 1

  game = Game.query.filter_by(id=game_list[game_num]).first()

  is_admin = False
  if (game.admin == current_user.username):
    is_admin = True

  view_game_html = view_game_to_html(game_list[game_num])
  session.commit()
  return render_template('view_game.html', name=current_user.username, game_num=game_num, view_game_html=view_game_html, list_len=list_len, is_admin=is_admin)

def get_secret_santa(game_id):
  game = Game.query.filter_by(id=game_id).first()
  all_users = User.query.all()
  players = []
  index = 0
  curr_user_index = 0

  for user in all_users:
    if (User.is_playing(user, game)):
      players.append(user)
      if user.username == current_user.username:
        curr_user_index = index
    
    index += 1
  
  if curr_user_index >= len(players) - 1:
    secret_santa = players[0]
  else:
    secret_santa = players[curr_user_index + 1]

  return secret_santa

def view_game_to_html(game_id):   
    cur_session['url'] = request.url
    url = db.engine.url
    engine = create_engine(url)

    game = Game.query.filter_by(id=game_id).first()
    #admin = User.query.filter_by(username=game.admin).first()

    admin_sql = text("SELECT admin FROM game WHERE id = :id").bindparams(bindparam("id", String))
    results = engine.execute(admin_sql, id=game_id)
    admin = results.first()[0]

    all_users = User.query.all()
    players = []

    for user in all_users:
      if (User.is_playing(user, game)):
        players.append(user)

    capacity_str = ""
    if (User.is_playing(current_user, game)) and game.num_active_players == game.max_capacity:
      secret_santa = get_secret_santa(game_id)
      capacity_str = "<br>Game has started. You're the Secret Santa for <strong>" + secret_santa.username + "</strong>! <br> *Click the button below to view their wish list"
      #TODO FIX METHOD TO REDIRECT TO
      html_string_shuffle = "<form action=\"/disp_all_gifts/1\">\
            <button class=\"button is-block is-black is-medium is-fullwidth\" button style=\"margin:10px\">View " + secret_santa.username + "'s Gift List</button>\
          </form>"
    elif (User.is_playing(current_user, game)) and game.num_active_players < game.max_capacity:
      capacity_str = "<br> *Game will automatically start once capacity is met"
    elif (not User.is_playing(current_user, game)) and game.num_active_players == game.max_capacity:
      html_string_shuffle = "<br> Game is full"

    html_string_base = "<div class=\"box\"> \
        <article class=\"media\">\
          <div class=\"media-content\">\
            <div class=\"content\">\
              <p>\
                <strong>" + str(game.title) + "</strong>\
                <br>" + "Created by: @" + str(admin) + "<br>\
                <br> Capacity: " + str(game.num_active_players) + "/" + str(game.max_capacity) + capacity_str + "\
                <br><br> Gifts range from $" + str(game.min_price) + " to $" + str(game.max_price)
    
    html_string_end_base = "</p>\
      </div>\
        </article>\
        </div>\
          <div class=\"level-right\">"
    
    #adding player list
    count = 1
    html_string_base += "<br>\
      <br>"
    for player in players:
      html_string_base += "Player " + str(count) + ": " + player.username + "<br>"
      count += 1

    html_string_base += html_string_end_base

    html_string_unjoined = "\
      <form action=\"/join_game/"+str(game_id)+"\">\
                  <button class=\"button is-block is-black is-medium is-fullwidth\">Join Game</button>\
                </form>"

    html_string_joined = "\
       <form action=\"/unjoin_game/"+str(game_id)+"\">\
                <button class=\"button is-block is-black is-medium is-fullwidth\" button style=\"margin:5px\">Leave Game</button>\
              </form>"
  

    if current_user.is_playing(game) and game.admin != current_user.username:
      html_string_base += html_string_joined
    else:
      if (game.num_active_players < game.max_capacity) and game.admin != current_user.username:
        html_string_base += html_string_unjoined 
  
    if game.num_active_players == game.max_capacity:
      html_string_base += html_string_shuffle
    elif game.admin == current_user.username and game.num_active_players < game.max_capacity:
      html_string_base += "Not enough players to start game"
    
    # Finish off whatever button state the post had
    html_string_base += "</nav>"

    # Finish off the whole html
    html_string_base += "</div>"

    return html_string_base
