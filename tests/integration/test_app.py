import sys
import os
import pytest
import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_healthcheck(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'"status": "healthy"' in rv.data

def test_get_item_route(client, mocker):
    mocker.patch('app.table.get_item', return_value={'Item': {'id': 'test-id', 'name': 'test-name'}})
    rv = client.get('/picus/get/test-id')
    response_data = json.loads(rv.data)
    body = json.loads(response_data['body'])
    assert rv.status_code == 200
    assert body['id'] == 'test-id'
    assert body['name'] == 'test-name'

def test_list_items_route(client, mocker):
    mocker.patch('app.table.scan', return_value={'Items': [{'id': 'test-id'}]})
    rv = client.get('/picus/list')
    response_data = json.loads(rv.data)
    body = json.loads(response_data['body'])
    assert rv.status_code == 200
    assert body == [{"id": "test-id"}]

def test_put_item_route(client, mocker):
    mocker.patch('app.table.put_item', return_value=None)
    rv = client.post('/picus/put', json={'name': 'test-name'})
    response_data = json.loads(rv.data)
    body = json.loads(response_data['body'])
    assert rv.status_code == 200
    assert 'id' in body
