from flask import Blueprint, redirect
from games.services.authentication.render_with_auth import render_template_with_auth
from games.services.browse.paginating_games import get_ordered_games, get_page_of_games, calculate_num_pages
import json
from games.data_repository import data_repo
from games.services.search import search_filter

search_page = Blueprint('search_page', __name__)


@search_page.route('/search/game=<game_name>/publisher=<publisher_name>/genres=<selected_genres>/<page_num>')
def show_search_results(game_name="", publisher_name="", selected_genres="[]", page_num="1"):
    selected_genres = json.loads(selected_genres)
    results = search_filter(get_ordered_games(data_repo), game_name,
                            publisher_name, selected_genres)

    page_num = int(page_num)
    num_pages = calculate_num_pages(results)

    if num_pages == 0:
        return render_template_with_auth('search/no_search_results.html')

    if page_num > num_pages or page_num < 1:
        return redirect(f"./1", code=302)

    genre_strings = [genre.genre_name for genre in data_repo.get_genres()]

    return render_template_with_auth('search/results.html', results=get_page_of_games(page_num, results),

                                     # this stuff is to let the user know what the current state is
                                     # which page r they on?
                                     current_page_num=page_num,
                                     num_pages=num_pages,

                                     # what is the filter inputs
                                     game_search=game_name,
                                     publisher_search=publisher_name,
                                     selected_genres=selected_genres,
                                     all_genres=genre_strings
                                     )
