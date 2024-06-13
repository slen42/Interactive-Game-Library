from games.services.game_details.average_rating import calc_average_rating
from games.data_repository import data_repo
from games.domainmodel.model import User, Review


def test_average_rating():
    game = data_repo.get_games()[-1]

    assert calc_average_rating(game.game_id) == None
    assert len(
        [review for review in game.reviews if isinstance(review, Review)]) == 0

    user = User('sookaphatone', 'bruises101')
    data_repo.add_review(game.game_id, user.username, 'comment', 1)
    data_repo.add_review(game.game_id, user.username, 'comment', 2)
    data_repo.add_review(game.game_id, user.username, 'comment', 4)
    data_repo.add_review(game.game_id, user.username, 'comment', 5)

    assert calc_average_rating(game.game_id, True) == 3
    assert calc_average_rating(game.game_id, False) == 3.0
