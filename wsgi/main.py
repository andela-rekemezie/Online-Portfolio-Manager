import hashlib
import json
from flask import render_template, url_for, request
from flask_login import LoginManager, login_user, current_user, session, redirect, login_required, logout_user
from __init__ import db, application
from models import User, Portfolio
from form import LoginForm, SignupForm, PortoForm

# Three steps to use flask-login
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = '/signin'


# adding user loader decorator
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


def hash_password(string):
    hash_salt = string + application.config['SECRET_KEY']
    return hashlib.sha224(hash_salt).hexdigest()


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
        user.biography = 'Pleased and Awesome is the day I was born and I have got every \
        reason to be happy for the Lord of Host has made me glad at all times'
        user.avatar = 'http://placekitten.com/350/300'
        db.session.add(user)
        db.session.commit()
        return render_template('themes/water/portfolio.html', signin_form=LoginForm(), portoform=PortoForm(),
                               page_title='This is the new guys in Town: ' + username, user=user)
    return render_template("themes/water/portfolio.html", signin_form=LoginForm(), portoform=PortoForm(),
                           page_title=username, user=user)


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
            user.email = form.email.data,
            user.password = hash_password(form.password.data),
            user.biography = 'This is a test portfolio',
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
            return render_template('themes/water/signin.html', signinpage_form=form)
        if user.password != hash_password(form.password.data):
            return render_template('themes/water/signin.html', signinpage_form=form)
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
@login_required
def profile():
    return render_template('themes/water/profile.html', page_title="Customizable profile page")


@application.route('/signout')
def signout():
    session.pop('username')
    session.pop('signed')
    logout_user()
    return redirect(url_for('index'))


@application.route('/get_portfolio/<id>')
@login_required
def get_portfolio(id):
    portfolio = Portfolio.query.get(id)
    return json.dumps(portfolio._asdict())


@application.route('/portfolio_add_update', methods=['GET', 'POST'])
# @login_required
def portfolio_add_update():
    form = PortoForm(request.form)
    if form.validate_on_submit():
        result = {'iserror': False}
        if not form.portfolio_id.data:
            user = User.query.filter_by(username=session['username']).first()
            if user is not None:
                user.portfolio.append(
                    Portfolio(title=form.title.data, description=form.description.data, tags=form.tags.data))
                db.session.commit()
                result['savedsuccess'] = True
            else:
                result['savedsuccess'] = False
                portfolio = Portfolio.query.get(get_portfolio(form.portfolio_id.data))
                form.populate_obj(portfolio)
                result['savedsuccess'] = True
            return json.dumps(result)

    form.errors['iserror'] = True
    return json.dumps(form.errors)


@application.route('/delete_portfolio/<id>', methods=['DELETE'])
@login_required
def delete_portfolio(id):
    portfolio = Portfolio.query.get(id)
    db.session.delete(portfolio)
    db.session.commit()
    result = {'result': 'success'}
    return json.dumps(result)


def init_db():
    db.drop_all()
    db.create_all()
    user = User(username='"Xampper', firstname='Prusilla',
                lastname='Anonymous', password=hash_password('maska'),
                email='swdev.bali@gmail.com',
                tagline='Incredibly fast programmer',
                biography='I love Python very much!',
                avatar='http://placekitten.com/500/300')
    user.portfolio.append(Portfolio(title='awesome', description='Great description', tags='python,django'))
    user.portfolio.append(Portfolio(title='awesome123', description='Great description123', tags='java,javascript'))
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    init_db()
    application.run(debug=True, host='0.0.0.0', port=9000)
