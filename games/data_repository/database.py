from typing import List
from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from games.domainmodel.model import User, Game, Review, Genre, Publisher
from games.data_repository.abstract import AbstractDataRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlDatabaseRepository(AbstractDataRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # users

    def get_users(self) -> List[User]:
        users = self._session_cm.session.query(User).all()
        return users

    def get_user(self, username: str) -> User:
        users = self.get_users()
        user = [user for user in users if user.username == username]

        if len(user) > 0:
            print(user[0].favourite_games)
            return user[0]
        return None

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)

        if user and user.password == password:
            return True
        return False

    def add_user(self, username, password):
        users = self.get_users()
        if len([user for user in users if user.username == username]) > 0:
            return {'success': False, "message": "This username is already taken, so registration has failed."}

        try:
            user = User(username, password)
        except ValueError as error:
            error_message = error.args[0]
            return {'success': False, "message": error_message + " So registration has failed."}

        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

        return {'success': True, "message": "User successfully added!"}

    def update_user(self, user: User):
        self._session_cm.session.merge(user)
        self._session_cm.commit()

    # genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def get_genre(self, genre_name: str):
        genre = None
        try:
            genre = self._session_cm.session.query(Genre).filter(
                Genre._Genre__genre_name == genre_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return genre

    # games
    def get_games(self) -> List[Game]:
        games = self._session_cm.session.query(Game).all()
        return games

    def get_game(self, game_id: int):
        games = self.get_games()
        for game in games:
            if game.game_id == game_id:
                return game

        # game doesn't exist

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.add(game)
            scm.commit()

    def add_review(self, game_being_reviewed_id: int, username_of_reviewer: str, comment: str, rating: int, ) -> dict:
        try:
            user = self.get_user(username_of_reviewer)
            game = self.get_game(game_being_reviewed_id)

            review = Review(user, game, int(rating), comment)
            game.add_review(review)
            user.add_review(review)

            with self._session_cm as scm:
                scm.session.add(review)
                scm.session.merge(game)
                scm.session.merge(user)
                scm.commit()
            return {'success': True, 'message': f"Successfully added review for: {game.title}"}
        except Exception as e:
            return {'success': False, 'message': f"{e.args[0]}. So review could not be added."}

    # publisher
    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()
