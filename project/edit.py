from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

edit = Blueprint('edit', __name__)

@edit.route('/edit_profile', methods=['POST'])
def edit_profile():
    return render_template('edit_profile.html', current_user = current_user.username)

@edit.route('/update_profile', methods=['POST'])
def update_profile():
  if request.form.get('action') == "Confirm":
    displayname = request.form.get('displayname')
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')

    #TODO: CHECK OLD PASSWORD

    if not check_password_hash(current_user.password, oldpassword): 
        # flash('Please check your login details and try again.')
        return "Wrong password entered. Try again" # if user doesn't exist or password is wrong, reload the page

    curr_user = User.query.filter_by(username=current_user.username).first()
    curr_user.displayname = displayname
    curr_user.password = generate_password_hash(newpassword, method='sha256')
    db.session.commit()
    
    return redirect(url_for('main.index'))





    