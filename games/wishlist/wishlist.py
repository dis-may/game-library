from flask import Blueprint, request, render_template, url_for, redirect, flash
import games.adapters.repository as repo
import games.utilities.utilities as utilities

wishlist_blueprint = Blueprint('wishlist_bp', __name__)


@wishlist_blueprint.route('/wishlist', methods=['GET'])
def games_wishlist():
    return render_template('wishlist.html',
                           genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance)
                           )




