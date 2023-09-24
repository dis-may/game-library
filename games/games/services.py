from games.adapters.repository import AbstractRepository
import games.utilities.utilities as utilities


def get_sorted_game_list(repo: AbstractRepository, sort='id', order='asc'):
    all_games = repo.get_all_games()
    all_games_sorted = utilities.sort_a_games_list(all_games, sort, order)
    return all_games_sorted



