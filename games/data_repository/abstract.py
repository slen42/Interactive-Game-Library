import abc
from typing import List
from games.domainmodel.model import User, Game, Genre


class AbstractDataRepository(abc.ABC):
    # users
    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def authenticate_user(self, username: str, password: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, username: str, password: str) -> dict:
        raise NotImplementedError

    # games
    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, game_id: int) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    # reviews
    @abc.abstractmethod
    def add_review(self, comment: str, rating: int) -> dict:
        raise NotImplementedError

    # genres
    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        return NotImplementedError
