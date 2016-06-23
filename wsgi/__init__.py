from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_pyfile('config.py')
application.config['CSRF_ENABLED'] = True,
application.config['SECRET_KEY'] = 'THIS IS THE SECRET FOR THE GATEWAY'
db = SQLAlchemy(application)
