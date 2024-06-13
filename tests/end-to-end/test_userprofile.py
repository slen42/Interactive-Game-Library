from games.data_repository import data_repo
from flask import session


def hasErrorMessage(html_string):
    return 'class="error"' in str(html_string)

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

def review_check(string):
    if "<b>Game:</b>" in string and "<b>Rating:</b>" in string and "<b>Comment:</b>:" in string:
        return True
    return False

def logout(client):
    response = client.get("/logout")
    # session is still accessible
    assert session.get('username') == None

def test_non_user_access_profile(client): #non-user can not get to  user profile page
    with client:
        logout(client)
    
        response = client.get('/user_profile')
        assert response.status_code == 302
        assert response.headers['Location'] == '/login'
        
def user_access_profile_page_and_contents(client):#user can see user profile page and see the reviews and wishlist
    with client:
        user = login_with_random_account(client)
        
        response = client.get('/user_profile')
        assert response.status_code == 200
        
        assert review_check(str(response.data))
