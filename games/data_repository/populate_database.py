from pathlib import Path

from games.data_repository.abstract import AbstractDataRepository
from games.adapters.csv_data_importer import load_games_and_genres


def populate(data_path: Path, repo: AbstractDataRepository, database_mode: bool):
    # Load articles and tags into the repository.
    print('running populate')
    load_games_and_genres(data_path, repo, database_mode)

    # Load users into the repository.
    # users = load_users(data_path, repo)

    # Load comments into the repository.
    # load_comments(data_path, repo, users)
