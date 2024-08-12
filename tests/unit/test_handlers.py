import pytest
from unittest.mock import MagicMock
from src.handlers import get_item, list_items, put_item

@pytest.fixture
def mock_table():
    return MagicMock()

def test_get_item(mock_table):
    mock_table.get_item.return_value = {'Item': {'id': 'test-id', 'name': 'test-name'}}
    event = {'pathParameters': {'key': 'test-id'}}
    result = get_item.get_item(event, None, mock_table)
    assert result['statusCode'] == 200
    assert result['body'] == '{"id": "test-id", "name": "test-name"}'

def test_get_item_not_found(mock_table):
    mock_table.get_item.return_value = {}
    event = {'pathParameters': {'key': 'non-existent-id'}}
    result = get_item.get_item(event, None, mock_table)
    assert result['statusCode'] == 404
    assert result['body'] == '{"error": "Item not found"}'

def test_list_items(mock_table):
    mock_table.scan.return_value = {'Items': [{'id': 'test-id'}]}
    result = list_items.list_items({}, None, mock_table)
    assert result['statusCode'] == 200
    assert result['body'] == '[{"id": "test-id"}]'

def test_put_item(mock_table):
    event = {'body': '{"name": "test-name"}'}
    result = put_item.put_item(event, None, mock_table)
    assert result['statusCode'] == 200
    assert 'id' in result['body']
