"""Initialize Flask app."""

from flask import Flask
import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate


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

        from .gameDescription import gameDescription
        app.register_blueprint(gameDescription.gameDescription_blueprint)

        from .searchBar import searchBar
        app.register_blueprint(searchBar.searchBar_blueprint)

        from .wishlist import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)

    # @app.route('/')
    # def home():
    #     some_game = create_some_game()
    #     # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    #     # return render_template('gameDescription.html', game=some_game)
    #     return render_template('layout.html', genre_list=get_list_of_genres(repo.repo_instance))

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
