from . import db


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
    portfolio = db.Column(db.String(255))

    def __init__(self, password=None, username=None, firstname=None, lastname=None, email=None, tagline=None,
                 avatar=None, portfolio=None):
        self.username = username,
        self.firstname = firstname,
        self.lastname = lastname,
        self.email = email,
        self.portfolio = portfolio,
        self.password = password,
        self.avatar = avatar,
        self.tagline = tagline


def init_db():
    db.drop_all()
    db.create__all()
    db.session.add(User(username='ekowibowo', firstname='Eko',
                         lastname='Suprapto Wibowo', password='rahasia',
                         email='swdev.bali@gmail.com',
                         tagline='A cool coder and an even cooler Capoeirista',
                         bio='I love Python very much!',
                         avatar='/static/avatar.png'))
