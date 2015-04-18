from app import db
from . import login_manager
from datetime import datetime
from flask import current_app, url_for
import random, string
import datetime
from sqlalchemy.exc import IntegrityError

from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Permission:
	FOLLOW =  0x01
	ADMINISTER = 0x80

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
	default = db.Column(db.Boolean, default = False, index = True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref = 'role', lazy = 'dynamic')

	@staticmethod
	def insert_roles():
		roles = {
			'User': (Permission.FOLLOW, True),
			'Administrator': (0xff, False)
		}

		for r in roles:
			role = Role.query.filter_by(name = r).first()
			if role is None:
				role = Role(name = r, permissions = roles[r][0],
					default = roles[r][1])
				db.session.add(role)
			db.session.commit()

	def __repr__(self):
		return "<Role %r>" % self.name


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), unique = True, index = True)
	username = db.Column(db.String(64), unique = True, index = True)
	_password_hash = db.Column(db.String(128))
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	reports = db.relationship('Report', backref = 'owner', lazy = 'dynamic')

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email in current_app.config['ADMINS']:
				self.role = Role.query.filter_by(permissions = 0xff).first()
			if self.role is None:
				self.role = Role.query.filter_by(default = True).first()

	@property
	def password(self):
	    raise AttributeError('password is not a reliable readable attribute.')

	@password.setter
	def password(self, password):
	    self._password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self._password_hash, password)

	def can(self, permissions):
		return self.role is not None and \
		(self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.ADMINISTER)

	def has_reports(self):
		return True if self.reports.count() > 0 else False

	def __repr__(self):
		return "<User %r>" % self.username

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser

class Report(db.Model):
	__tablename__ = 'report'
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(128))
	description = db.Column(db.Text)
	location = db.Column(db.String(128))
	created = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	reactors = db.relationship('Reactor', backref = 'report', lazy = 'dynamic')
	heatExchangers = db.relationship('HeatExchanger', backref = 'report', lazy = 'dynamic')
	dryers = db.relationship('Dryer', backref = 'report', lazy = 'dynamic')
	revenue = db.Column(db.Float)
	NAICS = db.Column(db.Integer)
	coal_frac = db.Column(db.Float)
	oil_frac = db.Column(db.Float)
	natgas_frac = db.Column(db.Float)
	
	def __init__(self, title = None, description = None, location = None, revenue= None):
		self.title = title
		self.description = description
		self.location = location
		self.revenue = revenue
		self.created = datetime.datetime.utcnow()

	def has_reactors(self):
		return True if self.reactors.count() > 0 else False
	
	def has_heatX(self):
		return True if self.heatExchangers.count() > 0 else False
	
	def has_dryer(self):
		return True if self.dryers.count() > 0 else False
	
	def has_oequip(self):
		return True if self.dryers.count() >0 else False
	
	def power(self, equip_type):
		totalkw=0.0
		for each in self.equip_type:
			totalkw += each.power()
		return totalkw	

	def ghg(self, equip_type):	#returns pounds of CO2 for each equipment type
		totalkw=self.power(equip_type)
		coal=coal_frac*totalkw*2.15 #each term in lb of CO2
		oil=oil_frac*totalkw*1.81
		gas=natgas_frac*totalkw*1.21
		return coal+oil+gas
		#the data came from USEIA updated March 2015
	def __repr__(self):
		return "Report: {0}".format(self.title)


class Reactor(db.Model):
	__tablename__ = 'reactor'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(160))
	reactant1 = db.Column(db.String(128))
	reactant2 = db.Column(db.String(128))
	reactant3 = db.Column(db.String(128))
	product1 = db.Column(db.String(128))
	product2 = db.Column(db.String(128))
	product3 = db.Column(db.String(128))
	catalyst1 = db.Column(db.String(128))
	catalyst2 = db.Column(db.String(128))
	power = db.Column(db.Float)
	efficiency = db.Column(db.Float)
	loadingRate = db.Column(db.Float)
	nonToxicPollutants = db.Column(db.Float)
	toxicWater = db.Column(db.Float)
	toxicAir = db.Column(db.Float)
	releaseFraction = db.Column(db.Float)
	report_id = db.Column(db.Integer, db.ForeignKey('report.id'))

	def __init__(self, **kwargs):
		self.name 				= kwargs.get('name', None)
		self.reactant1 			= kwargs.get('reactant1', None)
		self.reactant2 			= kwargs.get('reactant2', None)
		self.reactant3 			= kwargs.get('reactant3', None)
		self.product1 			= kwargs.get('product1', None)
		self.product2 			= kwargs.get('product2', None)
		self.product3 			= kwargs.get('product3', None)
		self.catalyst1 			= kwargs.get('catalyst1', None)
		self.catalyst2 			= kwargs.get('catalyst2', None)
		self.power 				= kwargs.get('power', None)
		self.efficiency 		= kwargs.get('efficiency', None)
		self.loadingRate 		= kwargs.get('loadingRate', None)
		self.nonToxicPollutants = kwargs.get('nonToxicPollutants', None)
		self.toxicWater 		= kwargs.get('toxicWater', None)
		self.toxicAir 			= kwargs.get('toxicAir', None)
		self.releaseFraction	= kwargs.get('releaseFraction', None)
		self.report_id			= kwargs.get('report_id', None)

	def __repr__(self):
		return "Reactor: {0}".format(self.name)
	def power(self):
		return self.power/self.efficiency

class HeatExchanger(db.Model):
	__tablename__ = 'heatexchanger'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(160))
	flowRate = db.Column(db.Float)
	specificHeat = db.Column(db.Float)
	tempIn = db.Column(db.Float)
	tempOut = db.Column(db.Float)
	efficiency = db.Column(db.Float)
	report_id = db.Column(db.Integer, db.ForeignKey('report.id'))

	def __init__(self, **kwargs):
		self.name 			= kwargs.get('name', None)
		self.flowRate 		= kwargs.get('flowRate', None)
		self.specificHeat 	= kwargs.get('specificHeat', None)
		self.tempIn 		= kwargs.get('tempIn', None)
		self.tempOut 		= kwargs.get('tempOut', None)
		self.efficiency 	= kwargs.get('efficiency', None)



	def __repr__(self):
		return "Reactor: {0}".format(self.name)
	
	def power(self):
		return self.power/self.efficiency

class Dryer(db.Model):
	__tablename__ = 'dryer'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(160))
	flowRate = db.Column(db.Float)
	nonToxicAir = db.Column(db.Float)
	toxicAir = db.Column(db.Float)
	releaseFraction = db.Column(db.Float)
	specificHeat = db.Column(db.Float)
	tempIn = db.Column(db.Float)
	tempOut = db.Column(db.Float)
	latentHeat = db.Column(db.Float)
	efficiency = db.Column(db.Float)
	report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
	power = db.Column(db.Float)
	def __init__(self, **kwargs):
		self.name 				= kwargs.get('name', None)
		self.flowRate 			= kwargs.get('flowRate', None)
		self.nonToxicAir    	= kwargs.get('nonToxicAir', None)
		self.toxicAir 			= kwargs.get('toxicAir', None)
		self.releaseFraction 	= kwargs.get('releaseFraction', None)
		self.specificHeat 		= kwargs.get('specificHeat', None)
		self.tempIn 			= kwargs.get('tempIn', None)
		self.tempOut 			= kwargs.get('tempOut', None)
		self.latentHeat 		= kwargs.get('latentHeat', None)
		self.efficiency 		= kwargs.get('efficiency', None)

	def __repr__(self):
		return "Reactor: {0}".format(self.name)
	
	def power(self):
		if self.power> 0.0:
			return self.power/self.efficiency
		return self.flowrate*(self.tempIn-self.tempOut)*self.latentHeat/self.efficiency;
	
	
class OtherEquipment(db.Model):
	__tablename__ = 'otherequipment'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(160))
	flowRate = db.Column(db.Float)
	power = db.Column(db.Float)
	efficiency = db.Column(db.Float)
	report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
	
	def __init__(self, **kwargs):
		self.name 				= kwargs.get('name', None)
		self.flowRate 			= kwargs.get('flowRate', None)
		self.power   		 	= kwargs.get('power', None)
		self.efficiency 		= kwargs.get('efficiency', None)
		
	def power(self):
		return self.power/self.efficiency
