"""
Entrypoints for game related lambdas. Handles all incoming requests as well as the scheduled load job.
"""
# TODO: If this module grows too large, split out handlers into separate modules. If the dependancys differ enough, move to seporate folders leveraging a common layer.
# TODO: Enhance logging throughout. Extend logger to add trace ids for each request to simplify correlating logs that relate to the same request execution.

import games_service
from lambda_util import api_wrapper


@api_wrapper
def get_games_handler(event, context):
    name = None
    query_string_parameters = event.get("queryStringParameters", {})
    if query_string_parameters:
        name = query_string_parameters.get("name", None)

    return games_service.search_games(name=name)


@api_wrapper
def load_games_handler(event, context):
    games_service.load_games()

    return {
        "message": "done",
    }


@api_wrapper
def checkout_game_handler(event, context):
    game_hash = event['pathParameters']['game_hash']
    # TODO: Validate the actual body of the message
    games_service.checkout_game(game_hash)

    return {
        "message": "done"
    }
