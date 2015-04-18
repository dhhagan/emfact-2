from app import db
from . import login_manager
from datetime import datetime
from flask import current_app, url_for
import random, string
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

	def __repr__(self):
		return "<User %r>" % self.username

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser