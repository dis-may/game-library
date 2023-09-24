from flask import Blueprint, request, render_template, url_for, session, redirect

import games.gameDescription.services as services
import games.adapters.repository as repo
import games.utilities.utilities as utilities

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired

gameDescription_blueprint = Blueprint('gameDescription_bp', __name__)


@gameDescription_blueprint.route('/gameDescription', methods=['GET', 'POST'])
def game_desc_page():
    # make the review form
    add_review_clicked = True # since if it is True, it will be POST method and the GET block won't set it
    review_form = ReviewForm()
    if request.method == 'GET':
        # read the GET query parameters
        game_id = int(request.args.get('game_id'))
        # loading the hidden game_id field with the game_id
        review_form.game_id.data = game_id
        review_form_parameter = request.args.get('game_review_form', 'hide')
        add_review_clicked = True if review_form_parameter == 'show' else False
    else:
        game_id = int(review_form.game_id.data)
        # Get the game with the specified ID.
    game = services.get_game(game_id, repo.repo_instance)

    if request.method == "POST" and review_form.validate():
        # if review_form.validate_on_submit():
        rating = int(review_form.rating.data)
        comment = review_form.comment.data
        services.add_review(game_id, session['user_name'], rating, comment, repo.repo_instance)

        genre_url_dict = utilities.get_genre_url_dictionary(repo.repo_instance)
        # getting the reviews
        reviews = services.get_reviews(game_id, repo.repo_instance)
        submit_url = url_for('gameDescription_bp.game_desc_page', game_id=game_id)
        user_logged_in = services.is_valid_user(session['user_name'], repo.repo_instance)
        return redirect(url_for('gameDescription_bp.game_desc_page', game_id=game_id))

    genre_url_dict = utilities.get_genre_url_dictionary(repo.repo_instance)
    # getting the reviews
    reviews = services.get_reviews(game_id, repo.repo_instance)
    submit_url = url_for('gameDescription_bp.game_desc_page', game_id=game_id)
    try:
        has_posted = services.has_posted(game_id, session['user_name'], repo.repo_instance)
    except KeyError:
        has_posted = False
    return render_template('gameDescription.html',
                           game=game,
                           genre_url_dict=genre_url_dict,
                           form=review_form,
                           heading=game.title,
                           reviews=reversed(reviews),
                           submit_url=submit_url,
                           user_logged_in=utilities.is_valid_user(repo.repo_instance),
                           add_review_clicked=add_review_clicked,
                           has_posted=has_posted
                           )


class ReviewForm(FlaskForm):
    game_id = HiddenField("Game ID")
    rating = SelectField('Rating:    ', validators=[
        InputRequired(message='Please give a rating value')
    ],
                         choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]
                         )
    comment = TextAreaField('Comment: ', validators=[
        DataRequired(),
        Length(min=2, message='Your comment is too short')])

    submit = SubmitField('Submit')
