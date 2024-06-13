from flask import  session, render_template
from games.data_repository import data_repo

def render_template_with_auth(template_name_or_list,**context) -> str:
    return render_template(template_name_or_list, **context, user=data_repo.get_user(session.get('username')))