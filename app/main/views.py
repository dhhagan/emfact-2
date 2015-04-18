from flask import render_template, session, redirect, url_for, flash, current_app
from . import main
from .. import db
from ..models import User, Report, Reactor
#from ..decorators import admin_required, permission_required
import json
from flask.ext.sqlalchemy import get_debug_queries
from sqlalchemy import desc
from flask.ext.login import login_required, current_user
from .forms import ReactorForm, HeatXForm, PlantInfoForm

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

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
	plantinfoform = PlantInfoForm()

	report = Report.query.filter_by(id = id).first()

	if report is not None:
		# pre-populate the fields in the plant info form only
		plantinfoform.revenue.data = report.revenue
		plantinfoform.title.data = report.title
		plantinfoform.description.data = report.description
		plantinfoform.NAICS.data = report.NAICS

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

		if plantinfoform.validate_on_submit():
			report.title = plantinfoform.title.data
			report.description = plantinfoform.description.data
			report.NAICS = plantinfoform.NAICS.data
			report.location = plantinfoform.location.data
			report.revenue = plantinfoform.revenue.data

			try:
				db.session.add(report)
				db.session.commit()
			except:
				flash("Could not Update report")

			return redirect(url_for('main.view_report', id = report.id))
		else:
			flash("Fail")

	else:
		report = Report()
		db.session.add(report)
		db.session.commit()

		report = Report.query.order_by(desc(Report.id)).first()

		if plantinfoform.validate_on_submit():
			report.title = plantinfoform.title.data
			report.description = plantinfoform.description.data
			report.location = plantinfoform.location.data
			report.revenue = plantinfoform.revenue.data
			report.NAICS = plantinfoform.NAICS.data

			try:
				db.session.add(report)
				db.session.commit()
			except:
				flash("Plant Info could not be created.")

			return redirect(url_for('main.view_report', id = report.id))

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
		plantinfoform = plantinfoform,
		report = report)