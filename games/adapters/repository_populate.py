import os
from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader


def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    games = reader.dataset_of_games

    for game in games:
        repo.add_game(game)

    genres = reader.dataset_of_genres

    for genre in genres:
        repo.add_genre(genre)

    publishers = reader.dataset_of_publishers

    for pub in publishers:
        repo.add_publisher(pub)
