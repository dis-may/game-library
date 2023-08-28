from games.adapters.repository import AbstractRepository


def get_game(game_id: int, repo: AbstractRepository):
    return repo.get_game(game_id)
