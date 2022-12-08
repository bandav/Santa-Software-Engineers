from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

likes = Blueprint('likes', __name__)

@likes.route('/liked_gifts')
def liked_gifts():
    print(current_user.username)
    return render_template('likes.html')



    