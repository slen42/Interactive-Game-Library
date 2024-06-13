from flask import Blueprint
from games.services.authentication.render_with_auth import render_template_with_auth
from games.services.browse.paginating_games import get_page_of_games, calculate_num_pages
from games.data_repository import data_repo


browse_page = Blueprint('browse_page', __name__)


@browse_page.route('/browse/')
@browse_page.route('/browse/<page_number>')
def browse(page_number="1"):
    page_number = int(page_number)

    return render_template_with_auth('browse/main.html', games=get_page_of_games(page_number), num_pages=calculate_num_pages(),
                                     current_page_num=page_number, genres=data_repo.get_genres())
