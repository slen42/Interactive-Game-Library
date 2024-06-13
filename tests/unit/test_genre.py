from typing import List
from games.services.browse_genre import genre_name_filter
from games.domainmodel.model import Game


def test_genre_browse(testing_data_repo):
    for genre in testing_data_repo.get_genres():
        filtered: List[Game] = genre_name_filter(
            testing_data_repo.get_games(), genre)
        for games in filtered:
            assert genre in games.genres
