from games.data_repository.abstract import AbstractDataRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader as Reader
from typing import List
from games.domainmodel.model import Game, User, Review, Publisher


class MemoryRepository (AbstractDataRepository):
    def __init__(self):
        reader = Reader('games/adapters/data/games.csv')
        reader.read_csv_file()

        self._games: List[Game] = reader.dataset_of_games
        self._genres = sorted(reader.dataset_of_genres)
        self._users = []
        self._publishers = []

    # users

    def get_user(self, username: str) -> User:
        user = [user for user in self._users if user.username == username]

        if len(user) > 0:
            return user[0]
        return None

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)

        if user and user.password == password:
            return True
        return False

    def add_user(self, username, password):
        if len([user for user in self._users if user.username == username]) > 0:
            return {'success': False, "message": "This username is already taken, so registration has failed."}

        try:
            user = User(username, password)
        except ValueError as error:
            error_message = error.args[0]
            return {'success': False, "message": error_message + " So registration has failed."}

        self._users.append(user)
        return {'success': True, "message": "User successfully added!"}

    # genres
    def get_genres(self):
        return self._genres

    def get_genre(self, genre_name: str):
        genre = [genre for genre in self._genres if genre.genre_name == genre_name]
        return genre if len(genre) else None

    # games
    def get_games(self):
        return self._games

    def get_game(self, game_id: int):
        for game in self._games:
            if game.game_id == game_id:
                return game

        # game doesn't exist

    def add_game(self, game: Game):
        isinstance(game, Game) and self._games.append(game)

    def add_review(self, game_being_reviewed_id: int, username_of_reviewer: str, comment: str, rating: int, ) -> dict:
        try:
            user = self.get_user(username_of_reviewer)
            game = self.get_game(game_being_reviewed_id)

            review = Review(user, game, int(rating), comment)
            game.add_review(review)
            user.add_review(review)
            return {'success': True, 'message': f"Successfully added review for: {game.title}"}
        except Exception as e:
            return {'success': False, 'message': f"{e.args[0]}. So review could not be added."}

    # publisher

    def add_publisher(self, publisher: Publisher):
        isinstance(publisher, Publisher) and self._publishers.append(publisher)
