from games.adapters.repository import AbstractRepository

def get_sorted_game_list(repo: AbstractRepository, sort_by='id', order='asc'):
    if sort_by == 'title':
        if order == 'asc':
            return repo.get_games_by_title()
        elif order == 'desc':
            games = repo.get_games_by_title()
            games.reverse()
            return games
    elif sort_by == 'price':
        if order == 'asc':
            return repo.get_games_by_price()
        elif order == 'desc':
            games = repo.get_games_by_price()
            games.reverse()
            return games
    else:
        return repo.get_games_by_id()
