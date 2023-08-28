import abc
from typing import List  # check if this is needed

from games.domainmodel.model import Game, Genre, Publisher

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f"RepositoryException {message}")


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_game(self, game: Game):
        """Adds a game to the repository list of games"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        """Returns a list of Game objects"""
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_games_by_release_date(self) -> List[Game]:
    #     """Returns a list of Game objects ordered by release date"""
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def get_games_by_title(self) -> List[Game]:
    #     """Returns a list of Game objects ordered by title in alphabetical order"""
    #     raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        """Returns a list of Game objects with the specified Genre"""
        raise NotImplementedError
    @abc.abstractmethod
    def get_number_of_games(self) -> int:
        """Returns the number of games in the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher):
        """Adds a publisher to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self) -> List[Publisher]:
        """Returns a list of Publisher objects"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre):
        """Adds a genre to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self):
        """Returns a list of Genre objects"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, game_id: int) -> Game:
        """Returns a game with the specified id"""
        raise NotImplementedError
