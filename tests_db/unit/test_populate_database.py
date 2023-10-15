from sqlalchemy import select, inspect

from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    # Get information about tables
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'games', 'genres', 'publishers', 'reviews', 'users',
                                           'wishlists']


def test_database_populate_select_all_games(database_engine):
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['game_id'], row['game_title']))

        num_games = len(all_games)
        assert num_games == 877

        assert all_games[0] == (3010, 'Xpand Rally')


def test_database_populate_select_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        correct_genre_names = ['Action', 'Adventure', 'Casual', 'Indie',
                               'Early Access', 'Massively Multiplayer', 'RPG',
                               'Simulation', 'Racing', 'Sports', 'Strategy',
                               'Free to Play', 'Education', 'Animation & Modeling',
                               'Audio Production', 'Utilities', 'Video Production',
                               'Design & Illustration', 'Game Development', 'Software Training',
                               'Photo Editing', 'Web Publishing', 'Violent', 'Gore']

        assert all_genre_names == correct_genre_names


def test_database_populate_select_all_publishers(database_engine):
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publisher_names = []
        for row in result:
            all_publisher_names.append(row['name'])

        assert len(all_publisher_names) == 798

        assert all_publisher_names[0] == 'Activision'
        assert all_publisher_names[-1] == 'Pixel Wonder'


def test_database_populate_select_all_reviews(database_engine):
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append(row['review_id'])

        assert all_reviews == [] # since the database does not come prepopulated with reviews


def test_database_populate_select_all_users(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == []  # no users are prepopulated in the database!

