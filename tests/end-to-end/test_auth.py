from flask import session
from games.data_repository import data_repo


def hasErrorMessage(htmlString):
    return 'class="error"' in str(htmlString)


def test_auth_valid(client):
    with client:
        # register
        response = client.post(
            "/register", data={"username": "sookaphatone1", "password": "bruises101", "confirm_password": "bruises101"})
        assert response.status_code == 302
        assert response.headers['Location'] == '/login'
        assert not hasErrorMessage(response.data)

        # login
        response = client.post(
            "/login", data={"username": "sookaphatone1", "password": "bruises101"})
        # session is still accessible
        assert session["username"] == 'sookaphatone1'
        assert response.status_code == 302
        assert response.headers['Location'] == '/'
        assert not hasErrorMessage(response.data)

        # logout
        response = client.get("/logout")
        # session is still accessible
        assert response.headers['Location'] == '/'
        assert session.get('username') == None

    # session is no longer accessible


def test_auth_invalid_lowercase_username(client):
    # register
    response = client.post(
        "/register", data={"username": "Sav", "password": "edgeworld101", "confirm_password": "Edgeworld101"})
    assert response.status_code == 200
    assert hasErrorMessage(response.data)


def test_auth_invalid(client):
    with client:
        # register
        response = client.post(
            "/register", data={"username": "sookaphatone2", "password": "bruises102", "confirm_password": "bruises101"})
        assert response.status_code == 200
        assert hasErrorMessage(response.data)

        response = client.post(
            "/register", data={"username": "sookaphatone2", "password": "bruise", "confirm_password": "bruise"})
        assert response.status_code == 200
        assert hasErrorMessage(response.data)

        response = client.post(
            "/register", data={"username": "", "password": "bruise101", "confirm_password": "bruise101"})
        assert response.status_code == 200
        assert hasErrorMessage(response.data)

        # login
        assert session.get("username") == None
        data_repo.add_user('testuser3', 'testpassword3')
        response = client.post(
            "/login", data={"username": "testuser3", "password": "testpassword2"})
        # session is still accessible
        assert session.get("username") == None
        assert response.status_code == 200
        assert hasErrorMessage(response.data)

    # session is no longer accessible
