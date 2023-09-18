# Authentication blueprint for the games web application.

from flask import Blueprint, request, render_template, url_for, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator

import games.adapters.repository as repo
import games.authentication.services as services
import games.utilities.utilities as utilities




# set up the blueprint
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


# login and registration
@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    username = None

    # if the user is already logged in, redirect to home page
    if form.validate_on_submit():
        try:
            username = form.username.data
            services.authenticate_user(
                form.username.data, form.password.data, repo.repo_instance
            )
            session.clear()
            session['username'] = username
            return redirect(url_for('home_bp.home'))
        except services.AuthenticationException:
            error = 'Incorrect username or password.'
    return render_template(
        'authentication/login.html',
        title='Log in',
        form=form,
        error=error,
        username=username
    )


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    submit = SubmitField('Log In')


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = 'Your password must be at least 8 characters, and contain an upper case letter,\
             a lower case letter and a digit'
        self.message = message

    # check if the password is valid
    def __call__(self, form, field):
        schema = PasswordValidator()

        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()

        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')