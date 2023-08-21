from flask import Blueprint
from flask import request, render_template, url_for

import games.genres.services as services
import games.adapters.repository as repo

genres_blueprint = Blueprint(
    'genres_bp', __name__)


@genres_blueprint.route('/genre', methods=['GET'])
def get_genre_list_by_genre():
    # Read query parameters.
    target_genre = request.args.get('genre')
    games_list = services.get_games_by_genre(repo.repo_instance, target_genre)[:20] # shows first 20 games for testing
    return render_template('games.html', games_list=games_list)

