from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask import session as cur_session
from flask_login import login_required, current_user
from .models import User, Game
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from . import db
from werkzeug.security import generate_password_hash

stats = Blueprint('stats', __name__)

@stats.route('/stats')
def show_stats():
    return "Your statistics"