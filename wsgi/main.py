from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, PasswordField, HiddenField, validators
from wtforms import TextAreaField, BooleanField
from wtforms.validators import Length, Email
from wtforms.validators import Optional, DataRequired, EqualTo

application = Flask(__name__)
application.config.from_pyfile('config.py')
application.config['CSRF_ENABLED'] = True,
application.config['SECRET_KEY'] = 'THIS IS THE SECRET FOR THE GATEWAY'
db = SQLAlchemy(application)


# Model definition of the form
class SignUpForm(Form):
    email = StringField('Email Address', validators=[
        DataRequired('Your email is required'),
        Length(min=5, message=u'Your email is too short'),
        Email(message='That\'s not a valid email address')
    ])
    password = PasswordField('Password', validators=[
        Length(min=8, message='Your password is too short'),
        DataRequired('Your password is required')
    ])
    agree = BooleanField('agree', validators=[
        DataRequired(u'You need to check the box to continue')
    ])

    username = StringField('choose your username', validators=[
        Length(min=6, message=u'Your username is too short'), DataRequired()])


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


@application.route('/signup', methods=['POST', 'GET'])
def signup():
    import pdb
    pdb.set_trace()
    if request.method == "POST":
        form = SignUpForm(request.form)
        if form.validate():
            user = User()
            form.populate_obj(user)
            username_exist = User.query.filter_by(username=form.username.data).first()
            email_exist = User.query.filter_by(email=form.email.data).first()
            print (username_exist, email_exist)
            if username_exist:
                form.username.errors.append('User already exists')
            if email_exist:
                form.email.errors.append('Email already exists')
            if username_exist or email_exist:
                return render_template('themes/water/signup.html', form=form, page_title='Sign up form')
            else:
                user.firstname = 'firstname',
                user.lastname = 'lastname',
                user.email = 'email',
                user.password = 'password',
                user.portfolio = 'This is a test portfolio',
                user.avatar = 'http://placehold.it/350/300',
                db.session.add(user)
                db.session.commit()
                return render_template('themes/water/signup-success.html', page_title='Success page on signup',
                                       user=user)
        else:
            return render_template('themes/water/signup.html', form=SignUpForm(), page_title='This is the signup form')
    return render_template('themes/water/signup.html', form=SignUpForm(), page_title='This is the signup form')


@application.route('/login')
def login():
    return render_template('themes/water/login.html', page_title='this is Login route')


if __name__ == '__main__':
    init_db()
    application.run(debug=True, host='0.0.0.0', port=9000)
