from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from .models import User, Gift
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

likes = Blueprint('likes', __name__)

@likes.route('/disp_liked_gifts/<id>/<gift_num>')
def disp_liked_gifts(id, gift_num):
    gift_list = get_liked_gifts(id)
    if (not gift_list or len(gift_list) == 0):
        return "You have no liked gifts. Go back and like one!"
    gift_num = int(gift_num)
    list_len = len(gift_list)
    while (gift_num >= list_len):
        gift_num -= 1
    gift_html = gift_to_html(gift_list[gift_num])

    return render_template('likes.html', id=id, gift_num = gift_num, gift_html = gift_html, list_len=list_len)

def get_liked_gifts(id):
    all_gifts = Gift.query.all()
    result = []
    for gift in all_gifts:
      if current_user.is_liking(gift):
        result.append(gift.id)
    return result

def gift_to_html(gift_id):
    cur_session['url'] = request.url
    obj = Gift.query.filter_by(id=gift_id).first()

    html_string_base = "<div class=\"box\"> \
        <article class=\"media\">\
          <div class=\"media-content\">\
            <div class=\"content\">\
              <p>\
                <strong>" + str(obj.gift_name) + "</strong>\
                <br>" + "Price: " + str(obj.price) + "</p>\
                <br>" + "Description: " + str(obj.description) + "</p>\
            </div>\
        </article>\
        </div>"

    

    html_string_liked = " <div class=\"level-right\">  <form action=\"/unjoin_game/"+str(gift_id)+"\">\
                <button class=\"button is-block is-black is-medium is-fullwidth\" button style=\"margin:5px\">Unlike Gift</button>\
              </form>"

    if current_user.is_liking(obj):
      html_string_base += html_string_liked
    # else:
    #   if (obj.num_active_players < obj.max_capacity):
    #     html_string_base += html_string_unjoined 
  

    # Finish off whatever button state the post had
    html_string_base += "</nav>"

    # Finish off the whole html
    html_string_base += "</div>"

    return html_string_base