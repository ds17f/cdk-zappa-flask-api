import os
import json
from dataclasses import dataclass, asdict

from botocore.exceptions import ClientError
from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)

DYNAMO_TABLE_NAME = os.environ["DYNAMO_TABLE_NAME"]


@dataclass
class RetroVideoGame:
    id: int
    title: str
    system: str
    release_year: str
    rating: int


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/tablename')
def tablename():
    return DYNAMO_TABLE_NAME


def get_table():
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(DYNAMO_TABLE_NAME)


@app.route('/games', methods=["GET"])
def get_games():
    table = get_table()
    response = table.scan()
    return jsonify(response["Items"])


@app.route('/game/<id>', methods=["GET"])
def get_game(id=None):
    table = get_table()
    try:
        response = table.get_item(Key={'id': int(id)})
    except ClientError as e:
        print(e.response['Error']['Message'])
        return jsonify(e.response['Error']['Message'])
    else:
        return jsonify(response['Item'])


@app.route('/game', methods=["POST"])
def add_game():
    posted_json = request.get_json()
    print(posted_json)
    game = RetroVideoGame(**posted_json)
    table = get_table()
    response = table.put_item(
        Item=asdict(game)
    )
    return jsonify(response)



