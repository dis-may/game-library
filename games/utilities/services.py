from games.adapters.repository import AbstractRepository


def get_genre_names(repo: AbstractRepository):
    genre_list = repo.get_genres()
    return [genre.genre_name for genre in genre_list]


def is_valid_user(user_name: str, repo: AbstractRepository):
    if repo.get_user(user_name) is not None:
        return True
    return False
