from games.data_repository import data_repo
import math


# alphabetically ordered

default_games_per_page = 15


def get_ordered_games(data_repo):
    games_list = data_repo.get_games()
    return sorted(games_list, key=lambda game: game.title)


def calculate_num_pages(games=None, max_games_per_page=default_games_per_page, data_repo=data_repo):
    games = games or get_ordered_games(data_repo)

    return math.ceil(len(games)/max_games_per_page)


def get_page_of_games(page_num: int, games=None, max_games_per_page=default_games_per_page, data_repo=data_repo):
    games = games or get_ordered_games(data_repo)

    first_game_index = max_games_per_page*(page_num-1)
    last_game_index = max_games_per_page*page_num

    return games[first_game_index:last_game_index]
