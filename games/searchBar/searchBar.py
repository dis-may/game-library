from flask import Blueprint, request, render_template, url_for

import games.searchBar.services as services
import games.adapters.repository as repo
from math import ceil

searchBar_blueprint = Blueprint('search_bp', __name__)


@searchBar_blueprint.route('/search_games', methods=['GET'])
def games_search_page():
    # Read query parameters.
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    # target_search = request.args.get('name')

    # Calculate the range of games to display on the current page.
    items_per_page = 21
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Get the list of games that match the search query.
    search_results = services.search_games(repo.repo_instance, query)

    # Get the list of games to display on the current page.
    games_list = search_results[start_index:end_index]

    total_pages = ceil(len(games_list) / 21)
    print(total_pages)

    pagination_urls = [url_for('searchBar_bp.games_search_page',
                               page=i,
                               query=query,
                               genre=target_search) for i in range(1, total_pages+1)]

    return render_template('games.html',
                           games_list=games_list,
                           query=query,
                           page=page,
                           total_pages=total_pages,
                           int=int,
                           pagination_urls=pagination_urls
                           )
