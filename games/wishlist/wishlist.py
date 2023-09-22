from flask import Blueprint, request, render_template, url_for

import games.adapters.repository as repo
import games.utilities.utilities as utilities

from games.authentication.authentication import login_required

wishlist_blueprint = Blueprint('wishlist_bp', __name__)


@wishlist_blueprint.route('/wishlist', methods=['GET'])
@login_required
def games_wishlist():
    return render_template('wishlist.html',
                           genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance)
                           )

