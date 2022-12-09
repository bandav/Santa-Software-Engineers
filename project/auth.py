# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from sqlalchemy import create_engine
from . import db
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.types import String

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    url = db.engine.url
    engine = create_engine(url)

    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False


    user = User.query.filter_by(username=username).first()
   
    #prepared statement - for password
    sql = text("SELECT password FROM User WHERE username = :uname").bindparams(bindparam("uname", String))
    results = engine.execute(sql, uname=username)
    actual_password = results.first()[0]
   
    # check if user actually exists
    if not user: #or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
    
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not check_password_hash(actual_password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page
 
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    url = db.engine.url
    engine = create_engine(url)

    username = request.form.get('username')
    displayname = request.form.get('displayname')
    password = request.form.get('password')

    #prepared statement
    sql = text("SELECT username FROM User WHERE username = :uname").bindparams(bindparam("uname", String))
    results = engine.execute(sql, uname=username)
    usernames = results.first()

    # for u in usernames:
    #     print(u)
    #     print(username)
    if (len(usernames) > 0):
        # print(u)
        flash('Sorry, that username already exists!')
        return redirect(url_for('auth.signup'))
    # user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    # if user: # if a user is found, we want to redirect back to signup page so user can try again  
    #     flash('Sorry, that username already exists!')
    #     return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(username=username, displayname=displayname, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))