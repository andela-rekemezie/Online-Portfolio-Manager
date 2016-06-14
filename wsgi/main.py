from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_pyfile('config.py')
db = SQLAlchemy(application)


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
    db.create_all()
    db.session.add(User(username='ekowibowo', firstname='Eko',
                        lastname='Suprapto Wibowo', password='rahasia',
                        email='swdev.bali@gmail.com',
                        tagline='A cool coder and an even cooler Capoeirista',
                        portfolio='I love Python very much!',
                        avatar='http://placekitten.com/200/300'))
    db.session.commit()


@application.route('/')
@application.route('/<username>')
def index(username=None):
    if username is None:
        return render_template("themes/water/index.html", page_title="Portfolio manager")
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User()
        user.username = username
        user.firstname = 'Tony'
        user.lastname = 'Adamma'
        user.portfolio = 'Pleased and Awesome is the day I was born and I have got every \
        reason to be happy for the Lord of Host has made me glad at all times'
        user.avatar = 'http://placekitten.com/350/300'
        db.session.add(user)
        db.session.commit()
        return render_template('themes/water/portfolio.html',
                               page_title='This is the new guys in Town: ' + username, user=user)
    return render_template("themes/water/portfolio.html", page_title=username, user=user)


if __name__ == '__main__':
    init_db()
    application.run(debug=True, host='0.0.0.0', port=9000)
