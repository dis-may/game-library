from flask import Blueprint, request, render_template, url_for

import games.gameDescription.services as services
import games.adapters.repository as repo
import games.utilities.utilities as utilities

gameDescription_blueprint = Blueprint('gameDescription_bp', __name__)


@gameDescription_blueprint.route('/gameDescription', methods=['GET'])
def game_desc_page():
    # Read query parameters.
    game_id = int(request.args.get('game_id'))

    # Get the game with the specified ID.
    game = services.get_game(game_id, repo.repo_instance)

    genre_url_dict = utilities.get_genre_url_dictionary(repo.repo_instance)

    return render_template('gameDescription.html', game=game, genre_url_dict=genre_url_dict)
