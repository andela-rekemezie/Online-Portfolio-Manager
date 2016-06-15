import os

SQLALCHEMY_DATABASE_URI = os.environ['OPENSHIFT_POSTGRESQL_DB_URL'] if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL')\
    else 'postgresql://rowland@localhost:5432/portfolio'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'secret key'
DEBUG = True
