import json
import logging
from decimal import Decimal


class BadRequest(Exception):
    pass


class DecimalEncoder(json.JSONEncoder):
    """
    Simple class to allow processing of dictionaries containing decimals. Consider alternate json library.
    """

    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return json.JSONEncoder.default(self, o)


def api_wrapper(func):
    def wrapper(event, context):
        try:
            result = func(event, context)
            return {
                "statusCode": 200,
                "body": json.dumps(
                    result,
                    cls=DecimalEncoder
                ),
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "http://gravie-developer-test.s3-website-us-east-1.amazonaws.com",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT"
                },
            }
        except BadRequest as exc:
            logging.exception("Invalid Request")
            return {
                "statusCode": 400,
                "body": str(exc),  # TODO: don't return the direct exception. That's not secure.
            }
        except Exception as exc:
            logging.exception("failed to list games")
            return {
                "statusCode": 500,
                "body": str(exc),  # TODO: don't return the direct exception. That's not secure.
            }
    return wrapper
