from flask import Blueprint, request, render_template, url_for, session

import games.genres.services as genre_services
import games.adapters.repository as repo
import games.utilities.utilities as utilities
import games.profile.services as services
from games.authentication.authentication import login_required

profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile', methods=['GET'])
@login_required
def profile_page():
    genre_url_dict = utilities.get_genre_url_dictionary(repo.repo_instance)
    recently_added_games = utilities.get_user_wishlist(session['user_name'], repo.repo_instance)[-3:]
    recently_added_games.reverse()
    reviews = services.get_user_reviews(session['user_name'], repo.repo_instance)
    return render_template('profile.html',
                           genre_url_dict=genre_url_dict,
                           heading="My Game Library",
                           user_logged_in=utilities.is_valid_user(repo.repo_instance),
                           reviews=reviews,
                           recently_added_games=recently_added_games
                           )
