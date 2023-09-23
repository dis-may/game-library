from flask import Blueprint, request, render_template, session, redirect
import games.utilities.utilities as utilities
import games.wishlist.services as services
from games.authentication.authentication import login_required
import games.adapters.repository as repo


wishlist_blueprint = Blueprint('wishlist_bp', __name__)

@wishlist_blueprint.route('/add_to_wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    username = session['user_name']
    current_game_id = int(request.form['current_game'])
    services.add_to_wishlist(current_game_id, username, repo.repo_instance)
    return redirect(request.referrer)

def remove_from_wishlist():
    username = session['user_name']
    current_game_id = int(request.form['current_game'])
    services.remove_from_wishlist(current_game_id, username, repo.repo_instance)
    return redirect(request.referrer)

@wishlist_blueprint.route('/wishlist')
@login_required
def get_wishlist():
    wishlist = get_wishlist
    return render_template('wishlist.html', wishlist = wishlist)

