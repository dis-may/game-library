from games.adapters.repository import AbstractRepository


def get_user_reviews(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    return user.reviews
