# TODO: Consider moving supporting classes to a lambda layer and appropriately package if the code base grows

import hashlib
import boto3

from boto3.dynamodb.conditions import Attr

import giantbomb_client
from lambda_util import BadRequest

dynamodb = boto3.resource('dynamodb')
games_table = dynamodb.Table('games-table')


def search_games(name=None):
    # TODO: dynamo scans are slow. At a minumum set up a secondary index to do a query on the name, but ideally
    #  configure cloud search to injest from dynamo and have search pull directly from there

    scan_kwargs = {}
    if name:
        scan_kwargs['FilterExpression'] = Attr("lower_name").contains(name.lower())
    response = games_table.scan(**scan_kwargs)
    data = response['Items']

    # TODO: We really should support proper paging, not just load up the entire table in memory. This is a memory risk
    while 'LastEvaluatedKey' in response:
        response = games_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    # TODO: If there are no results, try doing a live load from the vendor based on the provided name.

    # TODO: Convert items into something more formal like a dataclass if we're doing serious work on them
    for item in data:
        item.pop('raw', None)

    # TODO: If items are empty, try a real time load from game bomb but search based on the input title. If we recieve a rate limit error, then just return empty.

    return data


def load_games():
    games_count = 0
    number_of_total_results = 1

    while games_count < number_of_total_results and games_count < 300:  # limit total games since this is a demo project
        games_response = giantbomb_client.get_games(games_count)
        number_of_total_results = games_response['number_of_total_results']
        games = games_response['results']
        games_count += len(games)

        for game in games:
            converted_game = convert_game(game)
            games_table.put_item(
                Item=converted_game
            )


def convert_game(game):
    lower_name = game["name"].lower()
    cleaned_name = lower_name.replace(" ", "")
    name_hash = hashlib.md5(cleaned_name.encode()).hexdigest()

    icon_url = game["image"]["icon_url"]

    # TODO: add more fields the users would care about
    converted_game = {
        "gameHash": name_hash,
        "name": game["name"],
        "lower_name": lower_name,
        "icon": icon_url,
        "raw": game
    }
    return converted_game


def checkout_game(game_hash):
    response = games_table.get_item(
        Key={
            'gameHash': game_hash,
        }
    )
    game_record = response['Item']
    checkout_count = game_record.get("checkoutCount", 0)
    if checkout_count > 0:
        raise BadRequest("The game has already been checked out")
    game_record["checkoutCount"] = checkout_count + 1
    games_table.put_item(
        Item=game_record
    )
