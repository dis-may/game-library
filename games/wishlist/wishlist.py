from flask import Blueprint, request, render_template, flash
import games.adapters.repository as repo
import games.utilities.utilities as utilities

wishlist_blueprint = Blueprint('wishlist_bp', __name__)

@wishlist_blueprint.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    if request.method == "POST":
        game_added = request.form["game"]

        flash(f'Added "{game_added}" to your wishlist', 'success')

    return render_template('wishlist.html',
                           genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance),
                           wishlist=wishlist
                           )
