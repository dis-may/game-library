from flask import Blueprint, request, render_template, url_for, redirect, flash
import games.adapters.repository as repo
import games.utilities.utilities as utilities

wishlist_blueprint = Blueprint('wishlist_bp', __name__)

wishlist = []
def list_append(game):
    global wishlist
    wishlist.append(game)
@wishlist_blueprint.route('/wishlist', methods=['GET', 'POST'])
def games_wishlist():
    if request.method == "POST":
        game_added = request.form["game"]
        list_append(game_added)

    return render_template('wishlist.html',
                           genre_url_dict=utilities.get_genre_url_dictionary(repo.repo_instance),
                           wishlist = wishlist
                           )




