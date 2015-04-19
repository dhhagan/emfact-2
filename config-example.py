import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'power-basic+'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	CSRF_ENABLED = True
	ADMINS = ['david@davidhhagan.com']
	DATA_POINTS_PER_PAGE = 100
	SQLALCHEMY_RECORD_QUERIES = True
	SLOW_DB_QUERY_TIME = 0.5

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'dev-emfact.db')

class TestingConfig(Config):
	TESTING = True
	WTF_CSRF_ENABLED = False
	PRESERVE_CONTEXT_ON_EXCEPTION = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')

class ProductionConfig(Config):
	DEBUG = False
	WTF_CSRF_ENABLED = True
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'emfact.db')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}