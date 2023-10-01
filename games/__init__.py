"""Initialize Flask app."""
from pathlib import Path

from flask import Flask
import games.adapters.repository as repo
from games.adapters.repository_populate import populate
from games.adapters.memory_repository import MemoryRepository


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    # data_path = Path('games') / 'adapters' / 'data'

    # if app.config['TESTING'] == 'True':
    #     # Load test configuration, and override any configuration settings.
    #     app.config.from_mapping(test_config)
    #     data_path = app.config['TEST_DATA_PATH']

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

        from .gameDescription import gameDescription
        app.register_blueprint(gameDescription.gameDescription_blueprint)

        from .searchBar import searchBar
        app.register_blueprint(searchBar.searchBar_blueprint)

        from .wishlist import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)

    return app
