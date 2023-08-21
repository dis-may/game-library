from flask import Blueprint
from flask import request, render_template, url_for

import games.games.services as services
import games.adapters.repository as repo
import games.genres.services

games_blueprint = Blueprint(
    'games_bp', __name__)


@games_blueprint.route('/games', methods=['GET'])
def games_page():
    # Read query parameters.
    sort = request.args.get('sort')
    games_list = services.get_game_list(repo.repo_instance)[:21]  # shows first 20 games for testing
    return render_template('games.html', games_list=games_list, genre_list=games.genres.services.get_list_of_genres(repo.repo_instance))
