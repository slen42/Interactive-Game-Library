from flask import Blueprint, render_template
from games.data_repository import data_repo
from games.services.authentication.login_required_function import login_required
from games.services.authentication.render_with_auth import render_template_with_auth

user_profile_page = Blueprint('user_profile_page', __name__)

@user_profile_page.route('/user_profile')
@login_required
def user_profile():
    return render_template_with_auth('/user_profile/user_profile.html',genres=data_repo.get_genres())
