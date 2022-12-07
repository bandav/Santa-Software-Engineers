from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from .models import User, Game, playing
from . import db
from werkzeug.security import generate_password_hash

edit = Blueprint('edit', __name__)

@edit.route('/edit_profile', methods=['POST'])
def edit_profile():
    return render_template('edit_profile.html', current_user = current_user.username)

@edit.route('/update_profile', methods=['POST'])
def update_profile():
  if request.form.get('action') == "Confirm 2":
    displayname = request.form.get('displayname')
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')

    print(displayname)
    print(oldpassword)
    print(newpassword)
    return "HOLA"





    