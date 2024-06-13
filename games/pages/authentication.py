from flask import Blueprint, redirect, request, session
from games.services.authentication.render_with_auth import render_template_with_auth
from games.data_repository import data_repo
from games.services.authentication.forms import RegisterForm, LoginForm

authentication_page = Blueprint('authentication_page', __name__)


@authentication_page.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    def render_register_template(error_message=None):
        return render_template_with_auth('authentication/register.html', form=form, error_message=error_message)

    if request.method == 'GET':
        return render_register_template()

    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if confirm_password != password:
        return render_register_template("Your password and confirm password are not the same, so registration has failed.")

    result = data_repo.add_user(username, password)
    if not result['success']:
        return render_register_template(result['message'])

    return redirect('/login')


@authentication_page.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    form = LoginForm()

    def render_login_template(error_message=None):
        return render_template_with_auth('authentication/login.html', form=form, error_message=error_message)

    if request.method == 'GET':
        return render_login_template()

    username = request.form.get('username')
    password = request.form.get('password')

    if not data_repo.authenticate_user(username, password):
        return render_login_template('Username & password did not match!')

    session['username'] = username
    return redirect('/')


@authentication_page.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
