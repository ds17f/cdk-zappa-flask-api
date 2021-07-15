import os
import json
from collections import namedtuple

from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/tablename')
def tablename():
    dynamo_table_name = os.environ.get("DYNAMO_TABLE_NAME")
    return dynamo_table_name
