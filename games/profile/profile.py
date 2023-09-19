from flask import Blueprint, request, render_template, url_for

import games.genres.services as genre_services
import games.adapters.repository as repo
import games.utilities.utilities as utilities

profile_blueprint = Blueprint('profile_bp', __name__)

@profile_blueprint.route('/profile', methods=['GET'])
def profile_page():
    genre_url_dict = utilities.get_genre_url_dictionary(repo.repo_instance)
    return render_template('profile.html',
                           genre_url_dict=genre_url_dict,
                           heading="My Game Library")
