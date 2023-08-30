from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Genre
import games.utilities.utilities as utilities


def get_sorted_games_by_genre(repo: AbstractRepository, target_genre: str, sort='id', order='asc'):
    game_list = repo.get_games_by_genre(Genre(target_genre))
    game_list_sorted = utilities.sort_a_games_list(game_list, sort, order)
    return game_list_sorted
