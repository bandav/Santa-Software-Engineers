from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

likes = Blueprint('likes', __name__)

@likes.route('/liked_gifts')
def liked_gifts():

    # likes_list = get_all_likes()
    testing = liked_gift.query.filter_by(liking_id=current_user.id).first()
    print(testing)

    print(current_user.username)
    print(current_user.id)
    return render_template('likes.html')

def get_all_likes():
    all_likes = liked_gift.query.filter_by(liking_id=current_user.id)
    curr_user = User.query.filter_by(username=current_user.username).first()
    result = []
    for liked_gift in all_likes:
      result.append(liked_gifts.liked_id)
    return result 


    