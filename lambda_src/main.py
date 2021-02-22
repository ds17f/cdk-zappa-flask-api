import json
from collections import namedtuple

Request = namedtuple('Request', ["method", "path"])


def parse_request(event):
    http_method = event.get("httpMethod")
    path = event.get("path")
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
        "/test": echo_response,
        "/hello": echo_response,
    },
    "POST": {
        "/": echo_response,
    },
}


def handler(event, context):
    # print(f"request: {json.dumps(event)}")
    # return make_plain_text_return(json.dumps(event))
    request = parse_request(event)
    method_paths = ROUTER.get(request.method)
    handler_fn = method_paths.get(request.path)

    return handler_fn(event, context)


if __name__ == "__main__":
    def make_event(http_method, path):
        return {
            "httpMethod": http_method,
            "path": path,
        }

    print(handler(make_event("GET", "/")), None)