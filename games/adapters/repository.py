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
    def get_games_by_id(self) -> List[Game]:
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
    def get_number_of_games(self) -> int:
        """Returns the number of games in the repository"""
        raise NotImplementedError
