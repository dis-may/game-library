from flask import Blueprint, request, render_template, url_for

import games.searchBar.services as services
import games.adapters.repository as repo
import games.utilities.utilities as utilities
from math import ceil

searchBar_blueprint = Blueprint('search_bp', __name__)


@searchBar_blueprint.route('/search_games', methods=['GET'])
def games_search_page():
    # Read query parameters.
    sort = request.args.get('sort')
    order = request.args.get('order')
    query = request.args.get('query').lower()
    page = request.args.get('page', 1, type=int)
    search_type = request.args.get('search_type')

    # Calculate the range of games to display on the current page.
    items_per_page = 21
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    # Get the list of games that match the search query.
    if search_type == 'title':
        search_results = services.get_games_by_title(repo.repo_instance, query, sort, order)
    elif search_type == 'publisher':
        search_results = services.get_games_by_publisher(repo.repo_instance, query, sort, order)
    elif search_type == 'description':
        search_results = services.get_games_by_description(repo.repo_instance, query, sort, order)
    else:
        search_results = []


    # Get the list of games to display on the current page.
    games_list = search_results[start_index:end_index]
    total_pages = ceil(len(search_results) / items_per_page)

    pagination_urls = [
        url_for('search_bp.games_search_page',
                page=i,
                query=query,
                search_type=search_type
                ) for i in range(1, total_pages + 1)
    ]

    sort_url = url_for('search_bp.games_search_page')

    return render_template('games.html',
                           games_list=games_list,
                           genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance),
                           query=query,
                           page=page,
                           total_pages=total_pages,
                           int=int,
                           pagination_urls=pagination_urls,
                           heading=f"'{query}'",
                           sort_url=sort_url,
                           search_type=search_type,
                           sort=sort,
                           order=order,
                           )
