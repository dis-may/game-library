from games.adapters.repository import AbstractRepository
from games.domainmodel.model import make_review, Game


class NonExistentGameException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_game(game_id: int, repo: AbstractRepository):
    return repo.get_game(game_id)


def is_valid_user(user_name: str, repo: AbstractRepository):
    if repo.get_user(user_name) is not None:
        return True
    return False


def add_review(game_id: int, username: str, rating: int, comment: str, repo: AbstractRepository):
    game = repo.get_game(game_id)
    if game is None:
        raise NonExistentGameException
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    review = make_review(user, game, rating, comment)
    # right now reviews are not stored in the memory repo in their own list
    # reviews are linked to the game and user object
    repo.add_review(review)


def get_reviews(game_id, repo: AbstractRepository):
    game = repo.get_game(game_id)
    return game.reviews


def has_posted(game_id: int, username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        return False
    for review in user.reviews:
        if review.game.game_id == game_id:
            return True
    return False


def get_average_rating(game_id: int, repo: AbstractRepository):
    game = repo.get_game(game_id)
    total = 0
    count = 0
    for review in game.reviews:
        total += review.rating
        count += 1
    if count == 0:
        return -1
    else:
        return total / count
