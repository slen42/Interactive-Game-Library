def genre_name_filter(unfiltered_games, genre_name):
    return [game
            for game in unfiltered_games
            if genre_name in [str(genre1.genre_name) for genre1 in game.genres]]
