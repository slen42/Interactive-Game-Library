from flask import session
from typing import List
from games.domainmodel.model import Game
from games.data_repository import data_repo


def hasErrorMessage(htmlString):
    return 'class="error"' in str(htmlString)


def logout(client):
    response = client.get("/logout")
    # session is still accessible
    assert session.get('username') == None


# returns the user that is logged in
def login_with_random_account(client):
    logout(client)

    # log in
    random_username = 'username00'
    user = data_repo.get_user(random_username)
    if not user:
        data_repo.add_user(random_username, 'randompassword')
        user = data_repo.get_user(random_username)

    response = client.post(
        "/login", data={"username": user.username, "password": user.password})

    # session is still accessible
    assert session["username"] == user.username
    assert response.status_code == 302
    assert not hasErrorMessage(response.data)

    return user


def inWishlist(game_id: str):
    game_id = int(game_id)
    game = data_repo.get_game(game_id)
    wishlist_games: List[Game] = data_repo.get_user(session.get('username')).favourite_games
    if game not in wishlist_games:
        return False
    return True


def test_description_wishlist_button(client):
    with client:
        logout(client)

        # trying to add game to wishlist in game description without login
        response = client.post(f'/game/{data_repo.get_games()[0].game_id}/update-wishlist/')
        assert response.headers['Location'] == '/login'
        assert response.status_code == 302

        login_with_random_account(client)

        # trying to add game to wishlist in game description with login
        response = client.post(f'/game/{data_repo.get_games()[0].game_id}/update-wishlist/')
        assert inWishlist(data_repo.get_games()[0].game_id)
        assert response.status_code == 200

        # trying to remove game from wishlist at game description with login
        response = client.post(f'/game/{data_repo.get_games()[0].game_id}/update-wishlist/')
        assert not inWishlist(data_repo.get_games()[0].game_id)
        assert response.status_code == 200


def test_remove_button(client):
    with client:
        logout(client)

        # trying to enter wishlist without login
        response = client.get(f'/wishlist/')
        assert response.headers['Location'] == '/login'
        assert response.status_code == 302

        login_with_random_account(client)

        # trying to enter wishlist with login
        response = client.get(f'/wishlist/')
        assert response.status_code == 200

        # trying to add game to wishlist with login
        response = client.post(f'/game/{data_repo.get_games()[0].game_id}/update-wishlist/')
        assert inWishlist(data_repo.get_games()[0].game_id)
        assert response.status_code == 200

        # trying to remove game from wishlist in wishlist page with login
        response = client.post(f'/wishlist/delete/{data_repo.get_games()[0].game_id}')
        assert not inWishlist(data_repo.get_games()[0].game_id)
        assert response.headers['Location'] == '/wishlist/'
        assert response.status_code == 302
