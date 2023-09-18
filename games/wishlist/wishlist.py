from flask import Blueprint, request, render_template, url_for

wishlist_blueprint = Blueprint('wishlist_bp', __name__)


@wishlist_blueprint.route('/wishlist', methods=['GET'])
def games_wishlist():
    return render_template('wishlist.html')
