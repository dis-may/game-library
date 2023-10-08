from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist

from sqlalchemy import (
    Table, MetaData, Column, Integer, Float, String, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=True),
    Column('game_price', Float, nullable=False),
    Column('release_date', String(50), nullable=True),
    Column('game_description', String(1024), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name'))
)

publishers_table = Table(
    'publishers', metadata,
    Column('name', String(255), primary_key=True)
)

genres_table = Table(
    'genres', metadata,
    Column('genre_name', String(255), primary_key=True, nullable=False)
)

users_table = Table(
    'users', metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('game_id', ForeignKey('games.game_id')),
    Column('comment', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

wishlists_table = Table(
    'wishlists', metadata,
    Column('wishlist_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('game_id', ForeignKey('games.game_id'))
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_name', ForeignKey('genres.genre_name'))
)


def map_model_to_tables():
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__publisher': relationship(Publisher),
        '_Game__reviews': relationship(Review, back_populates='_Review__game'),
        '_Game__genres': relationship(Genre, secondary=game_genres_table),
        '_Game__wishlists': relationship(Wishlist, back_populates='_Wishlist__game')
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
    })

    mapper(User, users_table, properties={
        # '_User__user_id': users_table.c.user_id,
        '_User__name': users_table.c.name,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(Review, back_populates='_Review__user'),
        '_User__favourite_games': relationship(Wishlist, back_populates='_Wishlist__user')
    })

    mapper(Review, reviews_table, properties={
        # '_Review__review_id': reviews_table.c.review_id,
        '_Review__comment': reviews_table.c.comment,
        '_Review__rating': reviews_table.c.rating,
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__game': relationship(Game, back_populates='_Game__reviews')
    })

    mapper(Wishlist, wishlists_table, properties={
        # '_Wishlist__wishlist_id': wishlists_table.c.wishlist_id,
        '_Wishlist__user': relationship(User, back_populates='_User__favourite_games'),
        '_Wishlist__game': relationship(Game, )  # back_populates='_Game__wishlists' THERE IS NO WISHLIST UNDER GAMES
    })
