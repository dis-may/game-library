from games.adapters.repository import AbstractRepository
import games.utilities.utilities as utilities


def get_games_by_title(repo: AbstractRepository, target_name: str, sort="id", order="asc"):
    games_list = repo.get_games_by_title_search(target_name)
    games_list_sorted = utilities.sort_a_games_list(games_list, sort, order)
    return games_list_sorted


def get_games_by_publisher(repo: AbstractRepository, target_name: str, sort="id", order="asc"):
    games_list = repo.get_games_by_publisher_search(target_name)
    games_list_sorted = utilities.sort_a_games_list(games_list, sort, order)
    return games_list_sorted


def get_games_by_description(repo: AbstractRepository, target_name: str, sort="id", order="asc"):
    games_list = repo.get_games_by_description_search(target_name)
    games_list_sorted = utilities.sort_a_games_list(games_list, sort, order)
    return games_list_sorted
