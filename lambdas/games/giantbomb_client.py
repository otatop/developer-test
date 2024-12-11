import requests

# TODO: Move to parameter store in AWS and encrypt
API_KEY = "d8fb97bdc1e0857eea97ff0b1401346fa9812fcf"
USER_AGENT_HEADERS = {'User-agent': 'keith-test-app'}


def get_games(offset):
    # TODO: that passing an API key on a url is not secure. Talk to vendor about switching that to a header.
    game_request = requests.get(f'https://www.giantbomb.com/api/games/?format=json&api_key={API_KEY}&offset={offset}',
                                headers=USER_AGENT_HEADERS)
    status_code = game_request.status_code
    if status_code == 200:
        return game_request.json()
    # TODO: expand to raise different exceptions for different status codes
    raise Exception(f"Failed to retrieve games list. status_code={status_code} response={game_request.text}")
