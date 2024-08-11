from flask import Flask, Response, request
from handlers import get_item, list_items, put_item
from middleware.error_handler import handle_errors
import boto3
import os
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

REGION = os.getenv('AWS_REGION', 'eu-central-1')
TABLE_NAME = os.getenv('DYNAMODB_TABLE', 'PicusTable')
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

handle_errors(app)

@app.route('/', methods=['GET'])
def healthcheck():
    response_data = {"status": "healthy"}
    response_json = json.dumps(response_data)
    return Response(response=response_json, status=200, mimetype='application/json')

@app.route('/picus/get/<string:key>', methods=['GET'])
def get_item_route(key):
    event = {'pathParameters': {'key': key}}
    return get_item.get_item(event, None, table)

@app.route('/picus/list', methods=['GET'])
def list_items_route():
    return list_items.list_items({}, None, table)

@app.route('/picus/put', methods=['POST'])
def put_item_route():
    event = {'body': request.data.decode('utf-8')}
    return put_item.put_item(event, None, table)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)