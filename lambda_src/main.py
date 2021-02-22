import json
from collections import namedtuple

Request = namedtuple('Request', ["method", "path"])


def parse_request(context):
    request_context = context.get("requestContext")
    http_method = request_context.get("httpMethod")
    path = request_context.get("path")
    return Request(http_method, path)


def make_plain_text_return(body: str):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain"
        },
        "body": body,
    }


def echo_response(event, context):
    return make_plain_text_return(json.dumps(event))


ROUTER = {
    "GET": {
        "/": echo_response,
    },
    "POST": {
        "/": echo_response,
    },
}


def handler(event, context):
    # print(f"request: {json.dumps(event)}")
    # return make_plain_text_return(json.dumps(event))
    request = parse_request(context)
    method_paths = ROUTER.get(request.method)
    handler_fn = method_paths.get(request.path)

    return handler_fn(event, context)
