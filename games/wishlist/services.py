from games.adapters.repository import AbstractRepository
import games.utilities.utilities as utilities

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

def get_sorted_game_list(repo: AbstractRepository, sort='id', order='asc'):
    all_games = repo.get_all_games()
    all_games_sorted = utilities.sort_a_games_list(all_games, sort, order)
    return all_games_sorted



