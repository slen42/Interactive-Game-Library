from games.data_repository import data_repo
from games.domainmodel.model import Review


def calc_average_rating(game_id: int, round=False) -> float:
    game = data_repo.get_game(game_id)

    if not game:
        return

    total = 0
    reviews_counted = 0
    for review in game.reviews:
        if isinstance(review, Review):
            total += review.rating
            reviews_counted += 1

    if not reviews_counted:
        return

    return total/reviews_counted if round else total//reviews_counted
