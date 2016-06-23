from __init__ import db
from collections import OrderedDict


# Model definition for the User
class User(db.Model):
    """Remember always not to use commas in your model definitions"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    firstname = db.Column(db.String(56))
    lastname = db.Column(db.String(69))
    tagline = db.Column(db.String(60))
    password = db.Column(db.String)
    email = db.Column(db.String(255), unique=True)
    time_registered = db.Column(db.DateTime)
    avatar = db.Column(db.String(255))
    biography = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=False)
    portfolio = db.relationship('Portfolio')

    def __init__(self, password=None, username=None, firstname=None, lastname=None, email=None, tagline=None,
                 avatar=None, biography=None, active=None):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.biography = biography
        self.password = password
        self.avatar = avatar
        self.tagline = tagline
        self.active = active

    @staticmethod
    def is_anonymous():
        return False

    def is_active(self):
        return self.active

    @staticmethod
    def is_authenticated():
        return True

    def get_id(self):
        return self.id


class Portfolio(db.Model):
    # __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)
    tags = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title=None, description=None, tags=None):
        self.description = description
        self.tags = tags
        self.title = title

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper_.c.keys():
            result[key] = getattr(self, key)
        return result
