"""Initialize Flask app."""

from flask import Flask


from games.data_repository.setup_database import setup_database

import games.data_repository as repo

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')

    setup_database(app)

    with app.app_context():
        from games.pages.home import home_page
        from games.pages.browse import browse_page
        from games.pages.search import search_page
        from games.pages.game_details import game_details_page
        from games.pages.browse_genre import genre_page
        from games.pages.user_profile import user_profile_page

        from games.pages.authentication import authentication_page
        from games.pages.wishlist import wishlist_page

        app.register_blueprint(home_page)
        app.register_blueprint(browse_page)
        app.register_blueprint(search_page)
        app.register_blueprint(game_details_page)
        app.register_blueprint(genre_page)

        app.secret_key = '03<&wL4ko7b,'
        app.register_blueprint(authentication_page)

        # pages that require authentication 👇
        app.register_blueprint(wishlist_page)
        app.register_blueprint(user_profile_page)

    return app
