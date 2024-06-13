from flask import Blueprint
from games.services.authentication.render_with_auth import render_template_with_auth
from games.data_repository import data_repo

home_page = Blueprint('home_page', __name__)


@home_page.route('/')
def home():
    genre_strings = [genre.genre_name for genre in data_repo.get_genres()]
    return render_template_with_auth('/home/home.html',
                                     genres=data_repo.get_genres(),
                                     all_genres=genre_strings,
                                     selected_genres=genre_strings)
