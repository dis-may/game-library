from flask import Blueprint
from flask import request, render_template, url_for

import games.genres.services as services
import games.adapters.repository as repo
import games.utilities.utilities as utilities
from math import ceil

genres_blueprint = Blueprint(
    'genres_bp', __name__)


# @genres_blueprint.route('/genre', methods=['GET'])
# def get_genre_list_by_genre():
#     # Read query parameters.
#     target_genre = request.args.get('genre')
#     games_list = services.get_games_by_genre(repo.repo_instance, target_genre)[:20]  # shows first 20 games for testing
#     return render_template('games.html',
#                            games_list=games_list, )


@genres_blueprint.route('/genres', methods=['GET'])
def get_game_list_by_genre():
    # Read query parameters.
    sort = request.args.get('sort')
    page = request.args.get('page', 1, type=int)
    target_genre = request.args.get('genre')

    # Calculate the range of games to display on the current page.
    start_index = (page - 1) * 21
    end_index = start_index + 21

    all_games = services.get_games_by_genre_name(repo.repo_instance, target_genre)
    # Get the list of games to display on the current page.
    games_list = all_games[start_index:end_index]

    # Total number of pages
    total_pages = ceil(len(all_games) / 21)
    print(total_pages)

    return render_template('games.html',
                           games_list=games_list,
                           genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance),
                           heading=target_genre,
                           page=page,
                           total_pages=total_pages,
                           int=int
                           )
