from typing import List
from games.services.search import search_filter
from games.services.browse.paginating_games import get_ordered_games
from games.domainmodel.model import Game
from random import randint
import copy


def test_no_filter_is_all_games(testing_data_repo):
    ordered_games_list = get_ordered_games(testing_data_repo)
    assert len(search_filter(ordered_games_list, '_', '_')
               ) == len(ordered_games_list)
    assert search_filter(ordered_games_list, '_', '_') == ordered_games_list


def test_game_filter_reduces_num_results(testing_data_repo):
    """as the game filter text gets longer, 
    the filtered results decreases (or stays same)"""

    ordered_games_list = get_ordered_games(testing_data_repo)

    game_search_text = 'call'
    publisher_search_text = '_'
    prev_len = len(ordered_games_list)

    for up_to_digit in range(len(game_search_text)):
        filtered = search_filter(
            ordered_games_list, game_search_text[:up_to_digit], publisher_search_text)

        assert len(filtered) <= prev_len
        assert type(filtered) is list
        prev_len = len(filtered)


def test_publisher_filter_reduces_num_results(testing_data_repo):
    """as the publisher filter text gets longer, 
    the filtered results decreases (or stays same)"""

    ordered_games_list = get_ordered_games(testing_data_repo)

    game_search_text = '_'
    publisher_search_text = 'bad'
    prev_len = len(ordered_games_list)

    for up_to_digit in range(len(publisher_search_text)):
        filtered = search_filter(
            ordered_games_list, game_search_text, publisher_search_text[:up_to_digit])

        assert len(filtered) <= prev_len
        assert type(filtered) is list
        prev_len = len(filtered)


def test_genres_filter(testing_data_repo):
    ordered_games_list = get_ordered_games(testing_data_repo)

    for genre in ['Action', 'Adventure', 'Indie']:
        filtered: List[Game] = search_filter(
            ordered_games_list, '_', '_', [genre])

        for game in filtered:
            assert genre in [
                game_genre.genre_name for game_genre in game.genres]


def test_whole_search(testing_data_repo):
    ordered_games_list = get_ordered_games(testing_data_repo)

    def test_searching_for_specific_games():
        test_searches = [
            # game search, publisher search, trying to find game with this id
            ('cal', 'act', None, 7940),
            ('cal', 'act', ['Action'], 7940),
            ('10 Se', '_', None, 435790),
            ('_', 'Curve Games', None, 435790),
            ('_', 'Curve ', None, 435790),
            ('_', 'Phoenixx Inc.', ['Casual'], 1466930)
            # add more here...
        ]

        for game_text, pub_text, genres, id in test_searches:
            found = False
            for game in search_filter(ordered_games_list, game_text, pub_text, genres):
                assert type(game) == Game

                if game.game_id == id:
                    found = True
                    break

            assert found

    def test_searching_random_substring():
        def random_substring(string):
            start_index = randint(0, len(string)-1)
            substring_len = randint(0, len(string)-start_index-1)
            return string[start_index:start_index+substring_len]

        def random_sublist(full_list):
            sublist_len = randint(0, len(full_list)-1)

            full_list = copy.deepcopy(full_list)
            sublist = []
            for _ in range(sublist_len):
                index_of_el = randint(0, len(full_list)-1)
                sublist.append(full_list[index_of_el])
                full_list.pop(index_of_el)

            return sublist

        for game in ordered_games_list:
            # all random search parameters
            title_substring = random_substring(game.title)
            publisher_substring = random_substring(
                game.publisher.publisher_name)
            genres = [
                genre.genre_name for genre in random_sublist(game.genres)]
            assert game in search_filter(ordered_games_list,
                                         title_substring, publisher_substring, genres)

    test_searching_for_specific_games()
    test_searching_random_substring()
