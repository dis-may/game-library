from flask import Blueprint
from flask import request, render_template, url_for

import games.genres.services as genre_services
import games.adapters.repository as repo

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/')
def home():
    genre_list = genre_services.get_list_of_genres(repo.repo_instance)
    # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    # return render_template('gameDescription.html', game=some_game)
    return render_template('layout.html', genre_list=genre_list)
