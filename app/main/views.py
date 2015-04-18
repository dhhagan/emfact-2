from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from .. import db
from ..models import User, Report, Reactor
#from ..decorators import admin_required, permission_required
import json
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc
from flask.ext.login import login_required, current_user

from .forms import ReactorForm, HeatXForm


@main.route('/')
@main.route('/index')
def index():
	return render_template('main/home.html')

@main.route('/dashboard')
@login_required
def dashboard():
	return render_template('main/dashboard.html')

@main.route('/view-report', methods = ['GET', 'POST'])
@main.route('/view-report/<int:id>', methods = ['GET', 'POST'])
def view_report(id = None):
	reactorForm = ReactorForm()
	heatXForm = HeatXForm()

	report = Report.query.filter_by(id = id).first()
	if report is not None:
		# pre-populate the fields in the plant info form only
		if reactorForm.validate_on_submit():
			new_reactor = Reactor(
				name = reactorForm.name.data,
				power = reactorForm.power.data,
				efficiency = reactorForm.efficiency.data,
				report_id = report.id)

			try:
				db.session.add(new_reactor)
				db.session.commit()
			except:
				flash("Could not create new reactor")

			return redirect(url_for('main.view_report', id = report.id))
	else:
		report = Report()
		db.session.add(report)
		db.session.commit()

		report = Report.query.order_by(desc(Report.id)).first()

		if reactorForm.validate_on_submit():
			new_reactor = Reactor(
				name = reactorForm.name.data,
				power = reactorForm.power.data,
				efficiency = reactorForm.efficiency.data,
				report_id = report.id)

			try:
				db.session.add(new_reactor)
				db.session.commit()
			except:
				flash("Could not create new reactor")

			return redirect(url_for('main.view_report', id = report.id))

	return render_template('main/report.html',
		reactorForm = reactorForm,
		heatXForm = heatXForm,
		report = report)