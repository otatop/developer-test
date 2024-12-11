import responses
from lambdas.games import giantbomb_client


# TODO: Add unit tests for other modules
from lambdas.games.giantbomb_client import API_KEY, USER_AGENT_HEADERS


@responses.activate
def test_get_games():
    responses.add(responses.GET,
                  f'https://www.giantbomb.com/api/games/?format=json&api_key={API_KEY}&offset=0',
                  headers=USER_AGENT_HEADERS,
                  json={'fluffy': 'cat'},
                  status=200)
    result = giantbomb_client.get_games(0)
    print(result)
    assert result["fluffy"] == "cat"
