from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from .. import db
from ..models import User, Report, Reactor
#from ..decorators import admin_required, permission_required
import json
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc
from flask.ext.login import login_required, current_user
<<<<<<< Updated upstream

from .forms import ReactorForm, HeatXForm

=======
from .forms import PlantInfoForm
>>>>>>> Stashed changes

@main.route('/')
@main.route('/index')
def index():
	return render_template('main/home.html')

@main.route('/dashboard')
@login_required
def dashboard():
	return render_template('main/dashboard.html')

<<<<<<< Updated upstream
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
=======
@main.route('/input', methods = ['GET', 'POST'])
@main.route('/input/<int:id>', methods =['GET','POST'])
def input(id=None):
	plantinfoform=PlantInfoForm()
	if id is not None:
		if plantinfoform.revenue.data>0:
			newplantinfo=plantinfoform.revenue.data
			db.session.add(newplantinfo)
			db.session.commit()
	else:	
		if plantinfoform.validate_on_submit():
			plant=Report(title=plantinfoform.title.data, description=plantinfoform.description.data, location=plantinfoform.location.data, revenue=plantinfoform.revenue.data)
			plant.NAICS=plantinfoform.NAICS.data
			db.session.add(plant)
			db.session.commit()
				
			
	return render_template('main/input.html',
						plantinfoform=plantinfoform)


>>>>>>> Stashed changes
