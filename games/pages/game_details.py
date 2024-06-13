from flask import Blueprint, request, session
from games.services.authentication.render_with_auth import render_template_with_auth
from games.services.authentication.login_required_function import login_required
from games.data_repository import data_repo
from games.services.game_details.add_review_form import AddReviewForm
from games.services.game_details.average_rating import calc_average_rating

game_details_page = Blueprint(
    'game_details_page', __name__)


def render_game_details(game_id: str, feedback: str = None, success=False):
    game_id = int(game_id)
    game = data_repo.get_game(game_id)
    add_review_form = AddReviewForm()
    logged_in_user = session.get('username')

    if game:
        return render_template_with_auth('game_details/main.html',
                                         game=game, genres=data_repo.get_genres(),
                                         favourites=data_repo.get_user(
                                             logged_in_user).favourite_games if logged_in_user else [],
                                         average_rating=calc_average_rating(
                                             game_id, True),

                                         add_review_form=add_review_form,
                                         add_review_form_feedback=feedback,
                                         add_review_success=success)

    return render_template_with_auth('game_details/no_game_found.html')


@game_details_page.route('/game/<game_id>')
def game_details(game_id: str):
    return render_game_details(game_id)


@game_details_page.route('/game/<game_id>/add-review/', methods=['POST'])
@login_required
def add_review(game_id: str):
    try:
        result = data_repo.add_review(int(game_id), session['username'], request.form.get(
            'comment'), request.form.get('rating'))
        return render_game_details(game_id, result['message'], result['success'])
    except Exception as e:
        return render_game_details(game_id, e.args[0], False)


@game_details_page.route('/game/<game_id>/update-wishlist/', methods=['POST'])
@login_required
def wish_button(game_id: str):
    game_id = int(game_id)
    game = data_repo.get_game(game_id)
    favourites = data_repo.get_user(session.get('username')).favourite_games

    if game in data_repo.get_games():
        updatedUser = data_repo.get_user(session.get('username'))

        if game in favourites:
            updatedUser.remove_favourite_game(game)
        else:
            updatedUser.add_favourite_game(game)

        data_repo.update_user(updatedUser)
        favourites = updatedUser.favourite_games

        return render_game_details(game_id)

    return render_template_with_auth('game_details/no_game_found.html')
