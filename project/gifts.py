from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .models import User, Gift
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
    return redirect(cur_session['url'])
  else:
    return redirect(url_for('main.profile', id=id))

@gifts.route('/unlike_gift/<id>')
def unlike_gift(id):
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

@gifts.route('/search_range', methods=['POST'])
def search_range():
  if request.form.get('action') == "Search":
    lower_range = request.form.get('lower_range')
    upper_range = request.form.get('upper_range')
    
  return "yay"



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