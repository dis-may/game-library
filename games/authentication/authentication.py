# Authentication blueprint for the games web application.

from flask import Blueprint, request, render_template, url_for, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator

import games.adapters.repository as repo
import games.authentication.services as services
import games.utilities.utilities as utilities


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps

# set up the blueprint
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None

    if form.validate_on_submit():
        try:
            services.add_user(form.name.data, form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('authentication_bp.register'))
        except services.NameNotUniqueException:
            user_name_not_unique = 'Your username is already taken - please supply another'

    return render_template(
        'register.html',
        form=form,
        heading='Register',
        user_name_error_message=user_name_not_unique,
        handler_url=url_for('authentication_bp.register'),
        genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance)
    )


# login and registration
@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    user_name = None

    # if the user is already logged in, redirect to home page
    if form.validate_on_submit():
        try:
            user_name = form.user_name.data
            services.authenticate_user(
                form.user_name.data, form.password.data, repo.repo_instance
            )
            session.clear()
            session['user_name'] = user_name
            return redirect(url_for('home_bp.home'))
        except services.AuthenticationException:
            error = 'Incorrect username or password.'
    return render_template(
        'login.html',
        heading='Log in',
        form=form,
        error=error,
        user_name=user_name,
        genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance)
    )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


class LoginForm(FlaskForm):
    user_name = StringField('Username', [DataRequired()])
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
    name = StringField('Name', [
        DataRequired(message='Your name is required'),
        Length(min=1, message='Your name is too short')])

    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])

    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])

    submit = SubmitField('Register')
