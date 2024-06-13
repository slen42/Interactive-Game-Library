from flask import Blueprint

search_page = Blueprint('search_page', __name__)


def game_name_filter(unfiltered_games, filter_text):
    return [game
            for game in unfiltered_games
            if filter_text.lower() in game.title.lower()]


def publisher_name_filter(unfiltered_games, filter_text):
    return [game
            for game in unfiltered_games
            if filter_text.lower() in game.publisher.publisher_name.lower()]


def genres_filter(unfiltered_games, selected_genres):
    filtered = []

    for game in unfiltered_games:
        for genre in selected_genres:
            if genre in [genre1.genre_name for genre1 in game.genres]:
                filtered.append(game)
                break

    return filtered


def search_filter(unfiltered_games, game_filter_text, publisher_filter_text, selected_genres=None):
    filtered = unfiltered_games

    if game_filter_text != "_" and game_filter_text:
        filtered = game_name_filter(filtered, game_filter_text)

    if publisher_filter_text != "_" and publisher_filter_text:
        filtered = publisher_name_filter(filtered, publisher_filter_text)

    if selected_genres:
        filtered = genres_filter(filtered, selected_genres)

    return filtered
