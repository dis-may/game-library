from flask import Blueprint
from flask import request, render_template, url_for

import games.genres.services as genre_services
import games.adapters.repository as repo
import games.utilities.utilities as utilities

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/')
def home():
    genre_url_dict = utilities.get_genre_url_dictionary(repo.repo_instance)
    # genre_list = genre_services.get_list_of_genres(repo.repo_instance)
    # Use Jinja to customize a predefined html page rendering the layout
    # for showing a single game.
    # return render_template('gameDescription.html', game=some_game)
    return render_template('home.html', genre_url_dict=genre_url_dict)
