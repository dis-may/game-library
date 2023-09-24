from flask import Blueprint, request, render_template, session, redirect, url_for
import games.utilities.utilities as utilities
import games.wishlist.services as services
from games.authentication.authentication import login_required
import games.adapters.repository as repo
from math import ceil

wishlist_blueprint = Blueprint('wishlist_bp', __name__)


@wishlist_blueprint.route('/add_to_wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    username = session['user_name']
    current_game_id = int(request.form['current_game'])
    services.add_to_wishlist(current_game_id, username, repo.repo_instance)
    return redirect(request.referrer)


@wishlist_blueprint.route('/remove_from_wishlist', methods=['POST'])
@login_required
def remove_from_wishlist():
    username = session['user_name']
    current_game_id = int(request.form['current_game'])
    services.remove_from_wishlist(current_game_id, username, repo.repo_instance)
    return redirect(request.referrer)


@wishlist_blueprint.route('/wishlist')
@login_required
def get_wishlist():
    wishlist = get_wishlist

    user_logged_in = utilities.is_valid_user(repo.repo_instance)
    print("user_logged_in",user_logged_in)
    if user_logged_in:
        favourite_games = utilities.get_user_wishlist(session['user_name'], repo.repo_instance)
    else:
        favourite_games = []

    # Read query parameters.
    sort = request.args.get('sort')
    page = request.args.get('page', 1, type=int)
    order = request.args.get('order')

    # Calculate the range of games to display on the current page
    start_index = (page - 1) * 21
    end_index = start_index + 21

    games_list = favourite_games[start_index:end_index]

    # Total number of pages
    total_pages = ceil(len(favourite_games) / 21)

    pagination_urls = [url_for('wishlist_bp.get_wishlist', page=i, order=order) for i in
                       range(1, total_pages + 1)]

    return render_template('wishlist.html', wishlist=wishlist, games_list=games_list,
                           genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance),
                           heading="Wishlist",
                           page=page,
                           total_pages=total_pages,
                           int=int,
                           pagination_urls=pagination_urls,
                           sort=sort,
                           order=order,
                           user_logged_in=user_logged_in,
                           user_favourite_games=favourite_games
                           )
