"""Initialize Flask app."""

from flask import Flask, render_template
import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate

# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from games.domainmodel.model import Game

# delete the import statement below it is just for testing!
from games.genres.services import get_list_of_genres


# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
def create_some_game():
    some_game = Game(1, "Call of Duty® 4: Modern Warfare®")
    some_game.release_date = "Nov 12, 2007"
    some_game.price = 9.99
    some_game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of " \
                            "the Call of Duty® series, delivers the most intense and cinematic action experience ever. "
    some_game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    return some_game


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    repo.repo_instance = MemoryRepository()  # repo_instance is a global variable in repository.py
    populate(repo.repo_instance)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .genres import genres
        app.register_blueprint(genres.genres_blueprint)

        from .games import games
        app.register_blueprint(games.games_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

    # @app.route('/')
    # def home():
    #     some_game = create_some_game()
    #     # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    #     # return render_template('gameDescription.html', game=some_game)
    #     return render_template('layout.html', genre_list=get_list_of_genres(repo.repo_instance))

    return app
