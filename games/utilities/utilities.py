from flask import Blueprint
from flask import url_for, session
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


def sort_a_games_list(games_list, sort: str, order: str):
    if sort == 'title':
        if order == 'asc':
            sorted_list = sorted(games_list, key=lambda game: game.title)
            return sorted_list
        elif order == 'desc':
            sorted_list = sorted(games_list, key=lambda game: game.title, reverse=True)
            return sorted_list
    elif sort == 'price':
        if order == 'asc':
            sorted_list = sorted(games_list, key=lambda game: game.price)
            return sorted_list
        elif order == 'desc':
            sorted_list = sorted(games_list, key=lambda game: game.price, reverse=True)
            return sorted_list
    else:
        return games_list  # will sort by id as default


def is_valid_user(repo: AbstractRepository):
    try:
        username = session['user_name']
        return services.is_valid_user(username, repo)
    except KeyError: # i.e. the session hasn't been created yet
        return False
