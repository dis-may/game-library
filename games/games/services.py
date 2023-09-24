from games.adapters.repository import AbstractRepository
import games.utilities.utilities as utilities


def get_sorted_game_list(repo: AbstractRepository, sort='id', order='asc'):
    all_games = repo.get_all_games()
    all_games_sorted = utilities.sort_a_games_list(all_games, sort, order)
    return all_games_sorted


def get_user_wishlist(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    user_wishlist = user.favourite_games
    print("games/services", user_wishlist)
    return user_wishlist
