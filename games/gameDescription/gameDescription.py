from flask import Blueprint, request, render_template, url_for, session

import games.gameDescription.services as services
import games.adapters.repository as repo
import games.utilities.utilities as utilities

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

gameDescription_blueprint = Blueprint('gameDescription_bp', __name__)


@gameDescription_blueprint.route('/gameDescription', methods=['GET', 'POST'])
def game_desc_page():
    # make the review form
    review_form = ReviewForm()
    if request.method == 'GET':
        # read the GET query parameters
        game_id = int(request.args.get('game_id'))
        # loading the hidden game_id field with the game_id
        review_form.game_id.data = game_id
    else:
        game_id = int(review_form.game_id.data)
        # Get the game with the specified ID.
    game = services.get_game(game_id, repo.repo_instance)

    if review_form.validate_on_submit():
        rating = int(review_form.rating.data)
        comment = review_form.comment.data
        services.add_review(game_id, session['user_name'], rating, comment, repo.repo_instance)

    genre_url_dict = utilities.get_genre_url_dictionary(repo.repo_instance)

    # getting the reviews
    reviews = services.get_reviews(game_id, repo.repo_instance)
    submit_url = url_for('gameDescription_bp.game_desc_page', game_id=game_id)
    return render_template('gameDescription.html',
                           game=game,
                           genre_url_dict=genre_url_dict,
                           form=review_form,
                           heading=game.title,
                           reviews=reviews,
                           submit_url=submit_url
                           )


class ReviewForm(FlaskForm):
    game_id = HiddenField("Game ID")
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    comment = TextAreaField('Review', [
        DataRequired(),
        Length(min=3, message='Your comment is too short')])

    submit = SubmitField('Submit')
