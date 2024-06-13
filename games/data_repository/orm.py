from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Float, ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from games.domainmodel import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('username', String(255), primary_key=True,
           unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255))
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user', ForeignKey('users.username')),
    Column('game', ForeignKey('games.game_id')),
    Column('comment', String(1024), nullable=False),
    Column('rating', Integer, nullable=False)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('price', Float, nullable=False),
    Column('publisher_name', ForeignKey('publishers.id'), nullable=False),
    Column('release_date', String(255), nullable=False),
    Column('description', String(1024)),
    Column('image_url', String(255), nullable=False),
    Column('website_url', String(255))
)

genres_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(64), unique=True, nullable=False)
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_id', ForeignKey('genres.id'))
)

user_favourite_games_table = Table(
    'user_favourite_games', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('favourite_game_id', ForeignKey('games.game_id')),
    Column('username', ForeignKey('users.username'))
)


def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__favourite_games': relationship(model.Game, secondary=user_favourite_games_table),
        '_User__reviews': relationship(model.Review, back_populates='_Review__user')
    })

    mapper(model.Review, reviews_table, properties={
        '_Review__comment': reviews_table.c.comment,
        '_Review__rating': reviews_table.c.rating,
        '_Review__user': relationship(model.User, back_populates='_User__reviews'),
        '_Review__game': relationship(model.Game, back_populates='_Game__reviews'),
        'game': reviews_table.c.game,
        'user': reviews_table.c.user,
    })

    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(model.Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__price': games_table.c.price,
        '_Game__game_title': games_table.c.title,
        '_Game__publisher': relationship(model.Publisher),
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.description,
        '_Game__image_url': games_table.c.image_url,
        '_Game__website_url': games_table.c.website_url,
        '_Game__reviews': relationship(model.Review, back_populates='_Review__game'),
        '_Game__genres': relationship(model.Genre, secondary=game_genres_table,
                                      back_populates='_Genre__games_with_genre')
    })
    mapper(model.Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
        '_Genre__games_with_genre': relationship(
            model.Game,
            secondary=game_genres_table,
            back_populates="_Game__genres"
        )
    })
