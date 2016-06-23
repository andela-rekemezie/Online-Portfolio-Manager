from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import Email, DataRequired


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


# Model definition for portoform
class PortoForm(Form):
    portfolio_id = HiddenField()
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
