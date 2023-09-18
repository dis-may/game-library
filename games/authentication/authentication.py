# Authentication blueprint for the games web application.

from flask import Blueprint, request, render_template, url_for, session, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator

import games.adapters.repository as repo
import games.authentication.services as services
import games.utilities.utilities as utilities

<<<<<<< HEAD


=======
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator
from functools import wraps
>>>>>>> 1526125ceea3efb077d140e9f4fb2b390e46c57c

# set up the blueprint
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_error = None
    password_error = None

    if form.validate_on_submit():
        if services.get_user(form.user_name.data, repo.repo_instance):
            username_error = 'Sorry, this username is already taken. Please try again.'
        else:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            session.clear()
            session['username'] = form.user_name.data
            return redirect(url_for('home_bp.home'))
    return render_template(
        'register.html',
        form=form,
        username_error=username_error,
        password_error=password_error,
        handler_url=url_for('authentication_bp.register'),
        genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance),
        heading='Register'
    )


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
        'login.html',
        form=form,
        error=error,
        username=username,
        genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance),
        heading='Log in'
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