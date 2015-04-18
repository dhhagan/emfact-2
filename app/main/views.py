from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from .. import db
from ..models import User, Report
#from ..decorators import admin_required, permission_required
import json
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.login import login_required, current_user


@main.route('/')
@main.route('/index')
def index():
	return render_template('main/home.html')

@main.route('/dashboard')
@login_required
def dashboard():
	return render_template('main/dashboard.html')