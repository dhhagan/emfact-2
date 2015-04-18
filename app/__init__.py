from flask import Flask
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.markdown import Markdown
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	
	config[config_name].init_app(app)
	moment.init_app(app)
	pagedown.init_app(app)
	markdown = Markdown(app)
	db.init_app(app)
	login_manager.init_app(app)

	from .main import main as main_blueprint
	from .auth import auth as auth_blueprint

	app.register_blueprint(main_blueprint)
	app.register_blueprint(auth_blueprint, url_prefix = '/auth')

	return app

#app = create_app('production')