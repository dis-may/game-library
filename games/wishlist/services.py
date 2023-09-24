from games.adapters.repository import AbstractRepository

class NonExistentGameException(Exception):
    pass

class UnknownUserException(Exception):
    pass

def add_to_wishlist(game_id: int, username: str, repo: AbstractRepository):
    current_game = repo.get_game(game_id)
    if current_game is None:
        raise NonExistentGameException
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    user.add_favourite_game(current_game)


def remove_from_wishlist(game_id: int, username: str, repo: AbstractRepository):
    current_game = repo.get_game(game_id)
    if current_game is None:
        raise NonExistentGameException
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    user.remove_favourite_game(current_game)

def get_wishlist(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is not None:
        return user.wishlist
    return None



