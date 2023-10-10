import abc
from typing import List  # check if this is needed

from games.domainmodel.model import Game, Genre, Publisher, User, Review

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
    def get_all_games(self) -> List[Game]:
        """Returns a list of Game objects"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        """Returns a list of Game objects with the specified Genre"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_title_search(self, query: str) -> List[Game]:
        """Returns a list of Game objects with the specified Genre"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_publisher_search(self, query: str) -> List[Game]:
        """Returns a list of Game objects with the specified Genre"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_description_search(self, query: str) -> List[Game]:
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

    @abc.abstractmethod
    def add_user(self, user):
        """Adds a user to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """Returns a user with the specified user name"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_users(self):
        """Returns all users registered in the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review):
        """Adds a review to the repository"""
        if review.user is None or review not in Review.user.reviews:
            raise RepositoryException("Review not correctly attached to a User")
        if review.game is None or review not in Review.game.reviews:
            raise RepositoryException("Review not correctly attached to a Game")

    @abc.abstractmethod
    def get_reviews(self) -> List[Review]:
        """Returns all reviews for a game"""
        raise NotImplementedError

    @abc.abstractmethod
    def update_user(self, user: User):
        raise NotImplementedError
