from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from .models import User, Game
from . import db
from werkzeug.security import generate_password_hash

games = Blueprint('posts', __name__)

@games.route('/create_game', methods=['POST'])
@login_required
def create_game():
    if request.form.get('action') == "Create Post":
      return render_template('create_post.html')

@games.route('/disp_created_games')
def disp_created_games(id, game_num, type):
    game_list = get_created_games(id)
    if (not game_list or len(game_list) == 0):
        flash("You haven't created any games!")
        return redirect(url_for('main.profile'))
    game_num = int(game_num)
    list_len = len(game_list)
    while (game_num >= list_len):
        game_num-=1
    game_html = game_to_html(game_list[game_num])
    # FIXME: below html was officially userline
    return render_template('created_games.html', id=id, game_num=game_num, game_html=game_html, list_len=list_len)

def get_created_games(user_id):
    created_games = Game.query.filter_by(admin=user_id)
    result = []
    for game in created_games:
      result.append(game.id)
    return result

def game_to_html(game_id):
 
    cur_session['url'] = request.url
    obj = Game.query.filter_by(id=game_id).first()
    admin = User.query.filter_by(username=obj.admin).first()
    count = 0

    html_string_base = "<div class=\"box\"> \
        <article class=\"media\">\
          <div class=\"media-content\">\
            <div class=\"content\">\
              <p>\
                <strong>" + str(obj.title) + "</strong>\
                <br>" + "Created by: @" + str(admin.username) +  + "</p>\
                <br>" + str(obj.num_active_players) + "/" + str(obj.max_capacity) + "</p>\
                <br>" + "Price Range: " + str(obj.price_range) + "</p>\
            </div>\
        </article>\
        </div>"

    html_string_unjoined = "<div class=\"level-right\">\
                <form action=\"/join_game/"+str(game_id)+"\">\
                  <button>Join Game</button>\
                </form>"

    html_string_joined = "<div class=\"level-right\">\
              <form action=\"/view_game/"+str(game_id)+"\">\
                <button>Dislike</button>\
              </form>"

    if obj.has_started:
      if obj.is_playing(current_user):
        html_string_base += html_string_joined
      else:
        if (obj.num_active_players > obj.max_capacity) and (obj.has_started == 1):
          html_string_base += html_string_unjoined    

    # Finish off whatever button state the post had
    html_string_base += "</nav>"

    # Finish off the whole html
    html_string_base += "</div>"

    return html_string_base