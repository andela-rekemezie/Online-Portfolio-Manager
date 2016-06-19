from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from flask_login import LoginManager, login_user, current_user, session, redirect, login_required, logout_user
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired

application = Flask(__name__)
application.config.from_pyfile('config.py')
application.config['CSRF_ENABLED'] = True,
application.config['SECRET_KEY'] = 'THIS IS THE SECRET FOR THE GATEWAY'
db = SQLAlchemy(application)

# Three steps to use flask-login
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = '/signin'


# adding user loader decorator
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


# Model definition for the signup form
class SignupForm(Form):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    agree = BooleanField('Agree', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])


# Model definition for login form
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember', validators=[DataRequired()])


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
    portfolio = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=False)

    def __init__(self, password=None, username=None, firstname=None, lastname=None, email=None, tagline=None,
                 avatar=None, portfolio=None, active=None):
        self.username = username,
        self.firstname = firstname,
        self.lastname = lastname,
        self.email = email,
        self.portfolio = portfolio,
        self.password = password,
        self.avatar = avatar,
        self.tagline = tagline,
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
        return render_template("themes/water/index.html", signin_form=LoginForm(), page_title="Portfolio manager")
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
        return render_template('themes/water/portfolio.html', signin_form=LoginForm(),
                               page_title='This is the new guys in Town: ' + username, user=user)
    return render_template("themes/water/portfolio.html", signin_form=LoginForm(), page_title=username, user=user)


@application.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        username_exist = User.query.filter_by(username=form.username.data).first()
        email_exist = User.query.filter_by(email=form.email.data).first()
        if username_exist:
            form.username.errors.append('User already exists')
        if email_exist:
            form.email.errors.append('Email already exists')
        if username_exist or email_exist:
            return render_template('themes/water/signup.html', form=form, signinpage_form=LoginForm(),
                                   page_title='Sign up form')
        else:
            user.firstname = 'firstname',
            user.lastname = 'lastname',
            user.email = form.username.data,
            user.password = form.password.data,
            user.portfolio = 'This is a test portfolio',
            user.avatar = 'http://placehold.it/350/300',
            db.session.add(user)
            db.session.commit()
            return render_template('themes/water/signup-success.html', signinpage_form=LoginForm(), form=form,
                                   page_title='Success page on signup',
                                   user=user)
    else:
        return render_template('themes/water/signup.html', signinpage_form=LoginForm(), form=form,
                               page_title='This is the signup form')


@application.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            form.email.errors.append('User does not exist')
            return render_template(url_for('signin'), signinpage_form=form)
        if user.password != form.password.data:
            return render_template(url_for('signin'), signinpage_form=form)
        login_user(user, remember=form.remember_me.data)
        session['signed'] = True
        session['username'] = user.username
        if session.get('next'):
            next_page = session.get('next')
            session.pop('next')
            return redirect(next_page)
        else:
            return redirect(url_for('index'))
    else:
        session['next'] = request.args.get('next')
        return render_template('themes/water/signin.html', signinpage_form=LoginForm(),
                               page_title='this is Login route')


@application.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template(url_for('profile'), page_title="Customizable profile page")


@application.route('/signout')
def logout():
    session.pop('username')
    session.pop('signed')
    logout_user()
    return redirect(url_for('logout'))


if __name__ == '__main__':
    # init_db()
    application.run(debug=True, host='0.0.0.0', port=9000)
