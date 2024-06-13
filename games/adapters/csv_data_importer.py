import csv
from pathlib import Path

from games.data_repository.abstract import AbstractDataRepository
from games.domainmodel.model import Game, Genre, User, Publisher, make_genre_association,  ModelException


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_games_and_genres(data_path: Path, data_repo: AbstractDataRepository, database_mode: bool):
    genres = set()

    games_filename = str(data_path / "games.csv")
    for data_row in read_csv_file(games_filename):
        game_key = int(data_row[0])
        # number_of_genres = len(data_row) - 6
        game_genres = data_row[18].split(",")

        game = Game(game_key, data_row[1])

        game.release_date = data_row[2]
        game.price = float(data_row[3])
        game.description = data_row[4]
        game.image_url = data_row[7]
        game.website_url = data_row[8]

        # add the publisher
        game_publisher = Publisher(data_row[16])
        data_repo.add_publisher(game_publisher)
        game.publisher = game_publisher

        # Add any new genres; associate the current game with genres.
        for genre_name in game_genres:
            genre = Genre(genre_name)
            if genre not in genres:
                # genres[genre] = list()
                genres.add(genre)
            # genres[genre].append(game_key)
            else:
                genre = data_repo.get_genre(genre.genre_name)

            game.add_genre(genre)

        data_repo.add_game(game)
