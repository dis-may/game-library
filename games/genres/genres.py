from flask import Blueprint
from flask import request, render_template, url_for

import games.genres.services as services
import games.adapters.repository as repo
import games.utilities.utilities as utilities
from math import ceil

genres_blueprint = Blueprint(
    'genres_bp', __name__)


@genres_blueprint.route('/genres', methods=['GET'])
def games_by_genre_page():
    # Read query parameters.
    sort = request.args.get('sort')
    page = request.args.get('page', 1, type=int)
    order = request.args.get('order')
    target_genre = request.args.get('genre')

    all_games = services.get_sorted_games_by_genre(repo.repo_instance, target_genre, sort, order)
    # Calculate the range of games to display on the current page.
    start_index = (page - 1) * 21
    end_index = start_index + 21

    # Get the list of games to display on the current page.
    games_list = all_games[start_index:end_index]

    # Total number of pages
    total_pages = ceil(len(all_games) / 21)
    print(total_pages)

    pagination_urls = [url_for('genres_bp.games_by_genre_page',
                               page=i,
                               genre=target_genre,
                               sort=sort,
                               order=order) for i in range(1, total_pages + 1)]

    sort_url = url_for('genres_bp.games_by_genre_page')

    return render_template('games.html',
                           games_list=games_list,
                           genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance),
                           heading=f"{target_genre} Games",
                           page=page,
                           total_pages=total_pages,
                           int=int,
                           pagination_urls=pagination_urls,
                           target_genre=target_genre,
                           sort_url=sort_url,
                           sort=sort,
                           order=order
                           )
