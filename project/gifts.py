from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .models import User, Gift, Game
from . import db
from werkzeug.security import generate_password_hash

gifts = Blueprint('gifts', __name__)

@gifts.route('/disp_all_gifts/<gift_num>')
def disp_all_gifts(gift_num):  
    url = db.engine.url
    engine = create_engine(url)
    session = Session(bind=engine)
    session.connection(execution_options={"isolation_level": "READ UNCOMMITTED"})   
    gift_list = get_all_gifts()
    if (len(gift_list) == 0):
        return redirect(url_for('main.profile'))
    gift_num = int(gift_num)
    list_len = len(gift_list)
    while (gift_num >= list_len):
        gift_num-=1
    gift_html = gift_to_html(gift_list[gift_num])
    return render_template('explore_gifts.html', gift_num=gift_num, gift_html=gift_html, list_len=list_len, id = current_user.id)

def get_all_gifts(): 
    url = db.engine.url
    engine = create_engine(url)
    session = Session(bind=engine)
    session.connection(execution_options={"isolation_level": "READ UNCOMMITTED"})  
    all_gifts = Gift.query.all()
    result = []
    for gift in all_gifts:
      result.append(gift.id)
    session.commit()
    return result

@gifts.route('/like_gift/<id>')
def like_gift(id):
  print("liked en gifts.py")
  url = db.engine.url
  engine = create_engine(url)
  session = Session(bind=engine)
  session.connection(execution_options={"isolation_level": "READ UNCOMMITTED"})  
  gift = Gift.query.filter_by(id=id).first()
  if current_user.is_liking(gift):
      flash("You've already liked this gift!")
      return redirect(url_for('main.profile'))
  gift.likes += 1
  current_user.like(gift)
  session.commit()
  db.session.commit()
  if 'url' in cur_session:
    print("just liked, about to return")
    print(cur_session['url'])
    return redirect(cur_session['url'])
  else:
    return redirect(url_for('main.profile', id=id))

@gifts.route('/unlike_gift/<id>')
def unlike_gift(id):
  print("unliked en gifts.py")
  url = db.engine.url
  engine = create_engine(url)
  session = Session(bind=engine)
  session.connection(execution_options={"isolation_level": "READ UNCOMMITTED"})  
  gift = Gift.query.filter_by(id=id).first()
  if gift is None:
      return redirect(url_for('index', id=id))
  gift.likes -= 1
  current_user.unlike(gift)
  session.commit()
  db.session.commit()
  if 'url' in cur_session:
    return redirect(cur_session['url'])
  else:
    return redirect(url_for('main.profile', id=id))

@gifts.route('/range')
def range():
  return render_template('range.html')

@gifts.route('/search_range/<gift_num>', methods=['POST'])
def search_range(gift_num):
  if request.form.get('action') == "Search" or request.form.get('next') == "Next Gift" or request.form.get('prev') == "Previous Gift" or request.form.get('action') == "Dislike" or request.form.get('action') == "Like":
    lower_range = request.form.get('lower_range')
    upper_range = request.form.get('upper_range') 
    print(lower_range)
    print(upper_range)
    gift_list = get_range_gifts(lower_range, upper_range)

    if (not gift_list or len(gift_list) == 0):
      return "There are no gifts in this range"
    gift_num = int(gift_num)
    list_len = len(gift_list)

    print(gift_num)
    while (gift_num >= list_len):
      gift_num -= 1

    print(gift_num)
    gift_html = gift_to_html(gift_list[gift_num])
    return render_template('explore_range.html', id=id, gift_num = gift_num, gift_html = gift_html, list_len=list_len, lower_range=lower_range, upper_range=upper_range)

def get_range_gifts(lower_range, upper_range): 
    url = db.engine.url
    engine = create_engine(url)
    session = Session(bind=engine)
    session.connection(execution_options={"isolation_level": "READ UNCOMMITTED"})

    gifts_in_range = Gift.query.filter(Gift.price.between(lower_range, upper_range))
    result = []
    for gift in gifts_in_range:
      result.append(gift.id)
    session.commit()
    return result

@gifts.route('/secret_wishlist/<game_id>/<secret_santa>/<gift_num>')
def secret_wishlist(secret_santa, game_id, gift_num):
  person_to_gift = User.query.filter_by(id=secret_santa).first()
  game_id = int(game_id)
  game_playing = Game.query.filter_by(id=game_id).first()
  game_lower_bound = game_playing.min_price
  game_upper_bound = game_playing.max_price
  # print(game_lower_bound)
  # print(game_upper_bound)
  print("your person to gift is " + person_to_gift.username)
  gift_list = get_secret_gifts(person_to_gift, game_lower_bound, game_upper_bound)
  print(gift_list)
  if (not gift_list or len(gift_list) == 0):
    return (person_to_gift.username + " has not liked any gifts, tell them to like some!")
  gift_num = int(gift_num)
  list_len = len(gift_list)
  while (gift_num >= list_len):
    gift_num -= 1
  gift_html = gift_to_html(gift_list[gift_num])

  return render_template('explore_wishlist.html',id=person_to_gift.id, game_id=game_id, person_to_gift=person_to_gift.username, gift_num = gift_num, gift_html = gift_html, list_len=list_len)

def get_secret_gifts(person_to_gift, lower_range, upper_range):
    print("lower is below:")
    print(lower_range)
    print("upper is below:")
    print(upper_range)
    all_gifts = Gift.query.filter(Gift.price.between(upper_range, lower_range))
    # print(all_gifts[0].gift_name)
    # print(all_gifts)
    result = []
    for gift in all_gifts:
      if person_to_gift.is_liking(gift):
        result.append(gift.id)
    return result

def gift_to_html(gift_id):
 
    cur_session['url'] = request.url
    obj = Gift.query.filter_by(id=gift_id).first()

    likes = obj.likes

    html_string_base = "<div class=\"box\"> \
        <article class=\"media\">\
          <div class=\"media-content\">\
            <div class=\"content\">\
              <p>\
                <strong>" + str(obj.gift_name) + "</strong>\
                <br>" + "Costs $" + str(obj.price) + "</p>\
                <br>" + str(obj.description) + "</p>\
                <button class=\"button is-block is-link is-normal\" button style=\"margin:5px\"><a href=" + str(obj.purchase_link) + ">Link to Gift</a></button><div class=\"field is-grouped\" style=\"padding-top: 10px;\">"
    html_string_base += "</article>\
        </div>"
    
    html_string_liked = "<div class=\"level-right\">\
              <form action=\"/unlike_gift/"+str(gift_id)+"\">\
                <button class=\"button is-block is-black is-normal\" button style=\"margin:5px\">Dislike</button>\
              </form>"

    html_string_unliked = "<div class=\"level-right\">\
                <form action=\"/like_gift/"+str(gift_id)+"\">\
                  <button class=\"button is-block is-black is-normal\" button style=\"margin:5px\">Like</button>\
                </form>" 

    if current_user.is_liking(obj):
        html_string_base += html_string_liked
    else:
        html_string_base += html_string_unliked 

    # Finish off whatever button state the post had
    html_string_base += "<div class=\"level-left\">\
              <p>\
                Likes: " + str(likes) + "</p>\
              </div>\
            </nav>"

    # Finish off the whole html
    html_string_base += "</div>"

    return html_string_base
    cur_session['url'] = request.url
    obj = Gift.query.filter_by(id=gift_id).first()

    likes = obj.likes

    html_string_base = "<div class=\"box\"> \
        <article class=\"media\">\
          <div class=\"media-content\">\
            <div class=\"content\">\
              <p>\
                <strong>" + str(obj.gift_name) + "</strong>\
                <br>" + "Costs $" + str(obj.price) + "</p>\
                <br>" + str(obj.description) + "</p>\
                <button class=\"button is-block is-link is-normal\" button style=\"margin:5px\"><a href=" + str(obj.purchase_link) + ">Link to Gift</a></button><div class=\"field is-grouped\" style=\"padding-top: 10px;\">"
    html_string_base += "</article>\
        </div>"
    
    html_string_liked = "<div class=\"level-right\">\
              <form action=\"/unlike_gift_POST/"+str(gift_id)+" method=\"POST\"\">\
                <button class=\"button is-block is-black is-normal\" value=\"Dislike\" name=\"action\" button style=\"margin:5px\">Dislike</button>\
              </form>"

    html_string_unliked = "<div class=\"level-right\">\
                <form action=\"/like_gift_POST/"+str(gift_id)+" method=\"POST\"\">\
                  <button class=\"button is-block is-black is-normal\" value=\"Like\" name=\"action\" button style=\"margin:5px\">Like</button>\
                </form>" 

    if current_user.is_liking(obj):
        html_string_base += html_string_liked
    else:
        html_string_base += html_string_unliked 

    # Finish off whatever button state the post had
    html_string_base += "<div class=\"level-left\">\
              <p>\
                Likes: " + str(likes) + "</p>\
              </div>\
            </nav>"

    # Finish off the whole html
    html_string_base += "</div>"

    return html_string_base

