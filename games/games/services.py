from games.adapters.repository import AbstractRepository


def get_game_list(repo: AbstractRepository):
    return repo.get_games()
