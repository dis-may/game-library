from games.adapters.repository import AbstractRepository
from games.domainmodel.model import make_review, Game


class NonExistentGameException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_game(game_id: int, repo: AbstractRepository):
    return repo.get_game(game_id)


def add_review(game_id: int, username: str, rating: int, comment: str, repo: AbstractRepository):
    game = repo.get_game(game_id)
    if game is None:
        raise NonExistentGameException
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    make_review(user, game, rating, comment)
    # right now reviews are not stored in the memory repo in their own list
    # reviews are linked to the game and user object


def get_reviews(game_id, repo: AbstractRepository):
    game = repo.get_game(game_id)
    return game.reviews
