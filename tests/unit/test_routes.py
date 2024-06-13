from games import create_app


def test_routes_exist():
    app = create_app()
    routes_exist_expected = [
        '/',

        # games
        '/browse',
        '/search/game=<game_name>/publisher=<publisher_name>/genres=<selected_genres>/<page_num>',
        '/genre',
        '/game',

        # auth routes
        '/register',
        '/login',
        '/logout',
    ]

    for route in routes_exist_expected:
        route_exists = False
        for rule in app.url_map.iter_rules():
            if route in str(rule):
                route_exists = True
                break

        if not route_exists:
            raise ValueError("missing the following route: " + route)
