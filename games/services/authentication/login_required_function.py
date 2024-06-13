from functools import wraps
from flask import redirect, session
from games.data_repository import data_repo


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "username" not in session or not data_repo.get_user(session['username']):
            return redirect('/login')

        return view(**kwargs)

    return wrapped_view
