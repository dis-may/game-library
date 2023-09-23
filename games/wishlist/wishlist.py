from flask import Blueprint, request, render_template, session
import games.adapters.repository as repo
import games.utilities.utilities as utilities
from games.authentication.authentication import login_required

wishlist_blueprint = Blueprint('wishlist_bp', __name__)

@wishlist_blueprint.route('/add_to_wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    current_game_id = request.form['current_game']




    genre_url_dict = utilities.get_genre_url_dictionary(repo.repo_instance)
    return render_template('home.html',
                           genre_url_dict=genre_url_dict,
                           heading="My Game Library")
