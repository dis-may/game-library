from flask import Blueprint
from flask import request, render_template, url_for
from games.adapters.repository import AbstractRepository

import games.utilities.services as services

utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genre_url_dictionary(repo: AbstractRepository):
    genre_list = services.get_genre_names(repo)
    genre_url_dict = {}
    for genre in genre_list:
        genre_url_dict[genre] = url_for('genres_bp.games_by_genre_page', genre=genre)

    return genre_url_dict
