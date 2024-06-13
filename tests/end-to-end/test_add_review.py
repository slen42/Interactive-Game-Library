from games.data_repository import data_repo
from flask import session


def hasErrorMessage(html_string):
    return 'class="error"' in str(html_string)


def hasReviewForm(html_string, game_id):
    def stripWhitespace(string: str):
        return string.replace(" ", "").replace("\n", "")

    html_string = str(html_string)

    review_form = f'''<form action="/game/{game_id}/add-review/" method="post">
        <input id="csrf_token" name="csrf_token" type="hidden"
     <label for="comment">Comment</label> <input id="comment" name="comment" required size="20" type="text" value="">
     <label for="rating">Rating</label> <input id="rating" name="rating" required size="20" type="number" value="">'''

    for line in review_form.split('\n'):
        if line not in html_string:
            return False
    return True


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


def test_add_review_valid(client):
    with client:
        logout(client)

        # trying to post review without login
        response = client.get(f'/game/{data_repo.get_games()[0].game_id}')
        assert not hasReviewForm(
            response.data, data_repo.get_games()[0].game_id)
        assert response.status_code == 200

        login_with_random_account(client)

        # check review page again
        response = client.get(f'/game/{data_repo.get_games()[0].game_id}')
        assert '<form' in str(response.data)
        assert response.status_code == 200

        # post review again
        response = client.post(
            f'/game/{data_repo.get_games()[0].game_id}/add-review/', data={'comment': 'sdkj', 'rating': 5})
        assert response.status_code == 200
        assert '<p class="success">' in str(response.data)


def test_add_review_invalid(client):
    with client:
        login_with_random_account(client)

        # check review page again
        response = client.get(f'/game/{data_repo.get_games()[0].game_id}')
        assert hasReviewForm(response.data, data_repo.get_games()[0].game_id)
        assert response.status_code == 200

        # post review again
        response = client.post(
            f'/game/{data_repo.get_games()[0].game_id}/add-review/', data={'comment': 'sdkj', 'rating': 6})
        assert response.status_code == 200
        assert hasErrorMessage(response.data)

        response = client.post(
            f'/game/{data_repo.get_games()[0].game_id}/add-review/', data={'comment': 'sdkj', 'rating': -1})
        assert response.status_code == 200
        assert hasErrorMessage(response.data)

        response = client.post(
            f'/game/{data_repo.get_games()[0].game_id}/add-review/', data={'comment': '', 'rating': 4})
        assert response.status_code == 200
        assert hasErrorMessage(response.data)
