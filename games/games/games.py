from flask import Blueprint
from flask import request, render_template, url_for

from math import ceil

import games.games.services as services
import games.adapters.repository as repo
import games.utilities.utilities as utilities

games_blueprint = Blueprint(
    'games_bp', __name__)


@games_blueprint.route('/games', methods=['GET'])
def games_page():
    # Read query parameters.
    sort = request.args.get('sort')
    page = request.args.get('page', 1, type=int)
    order = request.args.get('order')

    # Calculate the range of games to display on the current page
    start_index = (page - 1) * 21
    end_index = start_index + 21

    all_games = services.get_sorted_game_list(repo.repo_instance, sort, order)
    # Get the list of games to display on the current page.
    games_list = all_games[start_index:end_index]

    # Total number of pages
    total_pages = ceil(len(all_games) / 21)

    pagination_urls = [url_for('games_bp.games_page', page=i, sort=sort, order=order) for i in range(1, total_pages+1)]
    sort_url = url_for('games_bp.games_page')

    return render_template('games.html',
                           games_list=games_list,
                           genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance),
                           heading="All Games",
                           page=page,
                           total_pages=total_pages,
                           int=int,
                           pagination_urls=pagination_urls,
                           sort=sort,
                           order=order,
                           sort_url=sort_url
                           )