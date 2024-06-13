from typing import List
from flask import Blueprint, session, redirect
from games.services.authentication.render_with_auth import render_template_with_auth
from games.services.authentication.login_required_function import login_required
from games.data_repository import data_repo
from games.services.browse.paginating_games import calculate_num_pages, get_page_of_games
from games.domainmodel.model import Game

wishlist_page = Blueprint('wishlist_page', __name__)


@wishlist_page.route('/wishlist/')
@wishlist_page.route('/wishlist/<page_num>')
@login_required
def wishlist(page_num: str = "1"):
    wishlist_games: List[Game] = data_repo.get_user(
        session.get('username')).favourite_games

    page_num = int(page_num)
    num_pages = calculate_num_pages(wishlist_games)

    # if page_num > num_pages or page_num < 1:
    # return redirect(f"./1", code=302)

    return render_template_with_auth('wishlist/main.html', wishlist_games=wishlist_games, genres=data_repo.get_genres(),
                                     # this stuff is to let the user know what the current state is
                                     # which page r they on?
                                     current_page_num=page_num, num_pages=num_pages,
                                     games=get_page_of_games(page_num, wishlist_games))


@wishlist_page.route('/wishlist/delete/<game_id>', methods=['POST'])
@login_required
def remove_button(game_id: str):
    game_id = int(game_id)
    game = data_repo.get_game(game_id)
    updated_user = data_repo.get_user(session.get('username'))
    updated_user.remove_favourite_game(game)
    data_repo.update_user(updated_user)

    return redirect('/wishlist/')
