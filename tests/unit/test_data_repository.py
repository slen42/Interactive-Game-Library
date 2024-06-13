from games.data_repository import data_repo
from games.domainmodel.model import User

test_cases = [
    # format is username, password, valid or not
    # but lower cases can't have same username as higher cases
    ('', '', False),
    ('sookaphatone', 'password', True),
    ('username2', '', False),
    ('', 'password', False),
    ('1234567', 'hey', False),
    (None, 'hey', False),
    ('username3', None, False),
    ('username3', 12345678, False),
    ('username3', 'thereisapassword', True),
    ('username3', 'differentone', False),
]

# users


def add_users():
    for username, password, added in test_cases:
        try:
            data_repo.add_user(username, password)
            assert added == True
            assert User(username, password) in data_repo._users
        except Exception as e:
            assert added == False
            continue


def test_get_user():
    add_users()

    for username, password, added in test_cases:
        if added:
            assert data_repo.get_user(username) == User(username, password)
        else:
            assert data_repo.get_user(username) == None or data_repo.get_user(
                username).password != password


def test_authenticate_user():
    add_users()

    for username, password, added in test_cases:
        if added:
            assert data_repo.authenticate_user(username, password) == True
        else:
            assert data_repo.authenticate_user(username, password) == False


def test_get_game():
    games_list = data_repo.get_games()
    for index in [0, 10, -1] + list(range(1, len(games_list), 5)):
        assert data_repo.get_game(
            games_list[index].game_id) == games_list[index]


def test_num_games():
    num_tests_in_games_csv_file = 981
    assert len(data_repo.get_games()) == num_tests_in_games_csv_file
