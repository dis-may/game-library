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
    rally cars amidst photorealistic sceneries. Realistic weather effects, rolling hills, and animated scenery all add
     to game's visual perfection. Xpand Rally also features highly detailed models of modern rally cars and handling 
     physics developed with the help of rally sport professionals which further enhance the realism of driving experience. 
     Xpand Rally combines the best elements of Rally and Rally Cross racing in one unique gaming experience. The game offers 
     a career mode based on time trials during both individual races and World Championship Series which will satisfy 
     traditional Rally fans. The Rally Cross fans won't be disappointed either - they can challenge several opponents
      in head to head racing during competitions based on real and fictitious race events. Xpand Rally, as the only title
       on the market, brings the economy factor into a rally game. The player starts with a junk car and competes in 
       races to earn money and acquire upgrades, repair damage, tweak performance and pay the race entry fees. Along with 
       the tuning-up, the car's condition affects its handling. Due to accurate damage system, it is highly dependent on
        the player's driving skills. The physical handling model is also influenced by car parts configuration and 
        provides both authentic feel and joy of driving. The interactive race track surroundings with enhanced game 
        physics and the innovative approach to changing daytime and weather conditions, both influencing the car handling, 
        are other hallmarks of Xpand Rally that distinguish it from other racing games. For the first time among rally games 
        Xpand Rally includes a complete set of easy-to-use editing tools enabling to create new tracks, cars or even game mods."""
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


def test_saving_of_review(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session, ("Missy", "missy", "Password1234"))

    rows = empty_session.query(Game).all()
    game = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "missy").one()

    # Create a new Comment that is bidirectionally linked with the User and Game.
    comment_text = "I love this game so much!"
    review = make_review(user, game, 3, comment_text)

    # Note: if the bidirectional links between the new Comment and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, game_id, comment FROM reviews'))

    assert rows == [(user_key, game_key, comment_text)]


def test_saving_of_game(empty_session):
    game = make_game()
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, game_title, game_price FROM games'))
    assert rows == [(3010, "Xpand Rally", 4.99)]


def test_saving_genre_game(empty_session):
    game = make_game()
    genre = make_genre()

    # Establish the bidirectional relationship between the Article and the Tag.
    # make_genre_association(game, genre)
    game.add_genre(genre)

    # Persist the Article (and Tag).
    # Note: it doesn't matter whether we add the Tag or the Article. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(game)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_key = rows[0][0]

    # Check that the tags table has a new record.
    rows = list(empty_session.execute('SELECT genre_name FROM genres'))
    genre_key = rows[0][0]
    assert rows[0][0] == "Free to Play"

    # Check that the article_tags table has a new record.
    rows = list(empty_session.execute('SELECT game_id, genre_name from game_genres'))
    game_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]

    assert game_key == game_foreign_key
    assert genre_key == genre_foreign_key


def test_save_reviewed_game(empty_session):
    # Create Article User objects.
    game = make_game()
    user = make_user()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    comment_text = "this game is the best"
    review = make_review(user, game, 5, comment_text)

    # Save the new Article.
    empty_session.add(game)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT game_id FROM games'))
    article_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT user_id FROM users'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the articles and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, game_id, comment FROM reviews'))
    assert rows == [(user_key, article_key, comment_text)]

