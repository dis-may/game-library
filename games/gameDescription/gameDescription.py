from flask import Blueprint, request, render_template, url_for

import games.games.services as services
import games.adapters.repository as repo


gameDescription_blueprint = Blueprint('gameDescription_bp', __name__)


@gameDescription_blueprint.route('/gameDescription', methods=['GET'])
def game_desc_page():
    # Read query parameters.
    game_id = request.args.get('id')

    # Get the game with the specified ID.
    game = services.get_game(game_id, repo.repo_instance)

    return render_template('gameDescription.html', game=game)
