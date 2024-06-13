from flask import Blueprint
from games.services.authentication.render_with_auth import render_template_with_auth
from games.services.browse.paginating_games import get_ordered_games, calculate_num_pages, get_page_of_games
from games.data_repository import data_repo
from games.services.browse_genre import genre_name_filter


genre_page = Blueprint('genre_page', __name__)


@genre_page.route('/genre/<genre_name>/')
@genre_page.route('/genre/<genre_name>/<page_num>')
def genre(genre_name: str, page_num="1"):
    page_num = int(page_num)
    num_pages = calculate_num_pages(
        genre_name_filter(data_repo.get_games(), genre_name))
    return render_template_with_auth('browse_genre/browse_genre.html', genre=genre_name, genres=data_repo.get_genres(),
                                     current_page_num=page_num, num_pages=num_pages,
                                     games=get_page_of_games(page_num, genre_name_filter(get_ordered_games(data_repo), genre_name)))
