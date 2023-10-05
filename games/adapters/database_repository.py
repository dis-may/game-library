from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher, User, Review

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

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.add(game)
            scm.commit()

    def get_game(self, game_id: int) -> Game:
        games = None
        try:
            games = self._session_cm.session.query(Game).filter(Game._Game__id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return games

    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        if genre is None:
            games = self._session_cm.session.query(Game).all()
            return games
        else:
            # Return articles matching target_date; return an empty list if there are no matches.
            games = self._session_cm.session.query(Game).filter(Game._Game__Genre == genre).all()
            return games

    def get_games_by_title_search(self, query: str) -> List[Game]:
        games = self._session.query(Game).filter(Game.title.ilike(f'%{query}%')).all()
        return games

    def get_games_by_publisher_search(self, query: str) -> List[Game]:
        games = self._session.query(Game).filter(Game.publisher.publisher_name.ilike(f'%{query}%')).all()
        return games

    def get_games_by_description_search(self, query: str) -> List[Game]:
        games = self._session.query(Game).filter(Game.description.ilike(f'%{query}%')).all()
        return games

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()
    def get_publishers(self) -> List[Publisher]:
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers

    def get_genres(self):
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    # def get_reviews(game_id, repo: AbstractRepository):
    #     reviews = self._session_cm.query(...).all()
    #     return reviews
    #
    # def add_review(game_id: int, username: str, rating: int, comment: str, repo: AbstractRepository):
    #     super().add_review(comment)
    #     with self._session_cm as scm:
    #         scm.session.add(comment)
    #         scm.commit()

