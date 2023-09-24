from flask import Blueprint
from flask import request, render_template, url_for, session

import games.genres.services as genre_services
import games.adapters.repository as repo
import games.utilities.utilities as utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/')
def home():
    genre_url_dict = utilities.get_genre_url_dictionary(repo.repo_instance)
    return render_template('home.html',
                           genre_url_dict=genre_url_dict,
                           heading="My Game Library",
                           user_logged_in=utilities.is_valid_user(repo.repo_instance)
                           )
