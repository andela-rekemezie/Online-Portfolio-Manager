from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_pyfile('config.py')
db = SQLAlchemy(application)

application = Flask(__name__)
application.config.from_pyfile('config.py')
db = SQLAlchemy(application)
