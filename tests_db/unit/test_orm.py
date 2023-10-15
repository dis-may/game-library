import pytest

import datetime

from games.domainmodel.model import Publisher, Genre, Game, User, make_review
from sqlalchemy.exc import IntegrityError


def insert_user(empty_session, values=None):
    new_name = "Rose"
    new_username = 'rose123'
    new_password = "Password123"

    if values is not None:
        new_name = values[0]
        new_username = values[1]
        new_password = values[2]

    empty_session.execute('INSERT INTO users (name, user_name, password) VALUES (:name, :user_name, :password)',
                          {'name': new_name, 'user_name': new_username, 'password': new_password})
    row = empty_session.execute('SELECT user_id from users where user_name = :user_name',
                                {'user_name': new_username}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (name, user_name, password) VALUES (:name, :user_name, :password)',
                              {'name': value[0], 'user_name': value[1], 'password': value[2]})
    rows = list(empty_session.execute('SELECT user_id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_game(empty_session):
    game_desc = """Xpand Rally is a breathtaking game that gives you the true to life experience of driving powerful 
    rally cars amidst photorealistic sceneries. """
    empty_session.execute(
        'INSERT INTO games (game_id, game_title, game_price, release_date, game_description, game_image_url, publisher_name) VALUES '
        '(:game_id, "Xpand Rally", :game_price, "Aug 24, 2006", '
        ':game_description, '
        '"https://cdn.akamai.steamstatic.com/steam/apps/3010/header.jpg?t=1639506578", '
        '"Techland")',
        {'game_id': 3010, 'game_price': 4.99, 'game_description': game_desc}
    )
    row = empty_session.execute('SELECT game_id from games').fetchone()
    return row[0]


def insert_games(empty_session):
    # inserts two games instead of just one
    empty_session.execute(
        'INSERT INTO games (game_id, game_title, game_price, release_date, game_description, game_image_url, publisher_name) '
        'VALUES '
        '(3010, "Xpand Rally", 4.99, "Aug 24, 2006", '
        '"placeholder game description for game 1", '
        '"https://cdn.akamai.steamstatic.com/steam/apps/3010/header.jpg?t=1639506578", '
        '"Techland"), '
        '(7940, "Call of Duty", 9.99, "Nov 12, 2007", '
        '"placeholder game description for game 2", '
        '"https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118", '
        '"Activision") '
    )
    rows = list(empty_session.execute('SELECT game_id from games'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_publisher(empty_session):
    empty_session.execute(
        'INSERT INTO publishers (name) VALUES ("Concerned Ape")'
    )
    row = empty_session.execute('SELECT name from publishers').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES ("Action"), ("Adventure")'
    )
    rows = list(empty_session.execute('SELECT genre_name from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_game_genre_associations(empty_session, game_key, genre_keys):
    stmt = 'INSERT INTO game_genres (game_id, genre_name) VALUES (:game_id, :genre_name)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'game_id': game_key, 'genre_name': genre_key})


def insert_wishlist_entry(empty_session, user_key, game_key):
    statement = 'INSERT INTO wishlists (user_id, game_id) VALUES (:user_id, :game_id)'
    empty_session.execute(statement, {'user_id': user_key, 'game_id': game_key})


def insert_reviewed_game(empty_session):
    game_key = insert_game(empty_session)  # this inserts Xpand Rally game defined above
    user_key = insert_user(empty_session)  # also using above function with user called Rose

    timestamp_1 = datetime.datetime.now()
    timestamp_2 = datetime.datetime.now()

    empty_session.execute(
        'INSERT INTO reviews (user_id, game_id, comment, rating, timestamp) VALUES '
        '(:user_id, :article_id, "Comment 1", :rating, :timestamp_1),'
        '(:user_id, :article_id, "Comment 2", :rating, :timestamp_2)',
        {'user_id': user_key, 'article_id': game_key, 'rating': 5, 'timestamp_1': timestamp_1,
         'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT game_id from games').fetchone()
    return row[0]


def make_game():
    game = Game(3010, 'Xpand Rally')
    game.price = 4.99
    return game


def make_user():
    user = User("Martha", 'marthajones', "Password123")
    return user

def make_publisher():
    publisher = Publisher("Concerned Ape")
    return publisher


def make_genre():
    genre = Genre("Free to Play")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Donna", "donnanoble", "Password1234"))
    users.append(("Clara", 'clara', "Password123"))
    insert_users(empty_session, users)

    expected = [
        User("Donna", "donnanoble", "Password1234"),
        User("Clara", 'clara', "Password123"),
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("marthajones", "Password123")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("Andrew", 'andrew', "Password123"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "andrew", "Password111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_game(empty_session):
    game_key = insert_game(empty_session)
    expected_game = make_game()
    fetched_game = empty_session.query(Game).one()

    assert expected_game == fetched_game
    assert game_key == fetched_game.game_id


def test_loading_of_genre_game(empty_session):
    game_key = insert_game(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_game_genre_associations(empty_session, game_key, genre_keys)

    game = empty_session.query(Game).get(game_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert genre in game.genres


def test_loading_of_reviewed_game(empty_session):
    insert_reviewed_game(empty_session)

    rows = empty_session.query(Game).all()
    game = rows[0]

    for comment in game.reviews:
        assert comment.game_id == game.game_id


def test_loading_of_publisher(empty_session):
    publisher_key = insert_publisher(empty_session)
    expected_publisher = make_publisher()
    fetched_publisher = empty_session.query(Publisher).one()
    assert expected_publisher == fetched_publisher
    assert publisher_key == fetched_publisher.publisher_name


def test_loading_of_wishlist(empty_session):
    # the wishlist table here is basically a user games association table
    game_keys = insert_games(empty_session)
    user_key = insert_user(empty_session)
    for game_key in game_keys:
        insert_wishlist_entry(empty_session, user_key, game_key)

    user = empty_session.query(User).get(user_key)
    games = [empty_session.query(Game).get(key) for key in game_keys]

    for game in games:
        assert game in user.favourite_games # this is where the wishlist is stored in the domain model


def test_saving_of_review(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session, ("Missy", "missy", "Password1234"))

    rows = empty_session.query(Game).all()
    game = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "missy").one()

    # Create a new Review that is bidirectionally linked with the User and Game.
    comment_text = "I love this game so much!"
    review = make_review(user, game, 3, comment_text)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, game_id, comment FROM reviews'))

    assert rows == [(user_key, game_key, comment_text)]


def test_saving_of_game(empty_session):
    game = make_game()
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, game_title, game_price FROM games'))
    # check that the Game object can be saved correctly in the games table
    assert rows == [(3010, "Xpand Rally", 4.99)]


def test_saving_of_publisher(empty_session):
    publisher = make_publisher()
    empty_session.add(publisher)
    empty_session.commit()
    rows = list(empty_session.execute('SELECT name FROM publishers'))
    # test that the Publisher object can be saved correctly in the publishers table
    assert rows[0] == (publisher.publisher_name,)


def test_saving_genre_game(empty_session):
    game = make_game()
    genre = make_genre()

    # game knows about genres, but genres does not know about games
    # hence only need to add genre to the game
    game.add_genre(genre)
    empty_session.add(game)
    empty_session.commit()

    # checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_key = rows[0][0]

    # Check that the genres table has a new record.
    rows = list(empty_session.execute('SELECT genre_name FROM genres'))
    genre_key = rows[0][0]
    assert rows[0][0] == "Free to Play"

    # Check that the game_genres table has a new record.
    rows = list(empty_session.execute('SELECT game_id, genre_name from game_genres'))
    game_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]

    assert game_key == game_foreign_key
    assert genre_key == genre_foreign_key


def test_saving_game_publisher(empty_session):
    game = make_game()
    publisher = make_publisher()
    game.publisher = publisher
    empty_session.add(game)
    empty_session.commit()
    game_rows = list(empty_session.execute('SELECT game_id, publisher_name FROM games'))
    publisher_rows = list(empty_session.execute('SELECT name FROM publishers'))
    assert game.game_id == game_rows[0][0]
    assert publisher.publisher_name == publisher_rows[0][0] # testing that it is saved
    # test that by adding a game, the publisher table is also populated with the correct value
    assert game_rows[0][1] == publisher_rows[0][0]


def test_save_reviewed_game(empty_session):
    game = make_game()
    user = make_user()

    # Create a new review that is bidirectionally linked with the User and Game
    comment_text = "this game is the best"
    review = make_review(user, game, 5, comment_text)

    # Save the new game only to the session
    empty_session.add(game)
    empty_session.commit()

    # get the game key by reading from the table, which should have inserted correctly
    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_key = rows[0][0]

    # get the user key by reading from the user table, which should have also inserted correctly
    rows = list(empty_session.execute('SELECT user_id FROM users'))
    user_key = rows[0][0]

    # Check that the reviews table has also had a new entry added
    rows = list(empty_session.execute('SELECT user_id, game_id, comment FROM reviews'))
    assert rows == [(user_key, game_key, comment_text)]


def test_save_wishlist(empty_session):
    game = make_game()
    user = make_user()
    user.add_favourite_game(game)
    empty_session.add(user)
    empty_session.commit()

    # get the game key from the game table, which should have inserted correctly
    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_key = rows[0][0]

    # get the user key from the table, which should have inserted correctly
    rows = list(empty_session.execute('SELECT user_id FROM users'))
    user_key = rows[0][0]

    # Check that the wishlist table has a new record that links the user and game tables
    rows = list(empty_session.execute('SELECT user_id, game_id FROM wishlists'))
    assert rows == [(user_key, game_key)]
