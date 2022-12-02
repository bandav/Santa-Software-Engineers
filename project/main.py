# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User, Game

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.displayname, id=current_user.id)

@main.route('/games')
@login_required
def games():
    # FIXME: Provide the correct parameters to the game
    return render_template('games.html', name=current_user.displayname)