from games.services.browse.paginating_games import default_games_per_page, calculate_num_pages, get_page_of_games


def test_get_page(testing_data_repo):
    num_pages = calculate_num_pages(data_repo=testing_data_repo)
    for page_num in range(1, num_pages, 5):
        assert len(get_page_of_games(
            page_num, data_repo=testing_data_repo)) == default_games_per_page

    assert len(get_page_of_games(num_pages, data_repo=testing_data_repo)
               ) <= default_games_per_page


def test_num_pages(testing_data_repo):
    assert calculate_num_pages(data_repo=testing_data_repo) == (len(testing_data_repo.get_games()) //
                                                                default_games_per_page) + 1


def test_calculate_num_pages(testing_data_repo):
    def create_empty_array(size):
        return [None for _ in range(size)]

    assert calculate_num_pages(create_empty_array(
        50), 10, data_repo=testing_data_repo) == 5
    assert calculate_num_pages(create_empty_array(
        49), 10, data_repo=testing_data_repo) == 5
    assert calculate_num_pages(create_empty_array(
        51), 10, data_repo=testing_data_repo) == 6
