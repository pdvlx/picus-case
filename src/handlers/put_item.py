import json
import uuid

def put_item(event, context, table):
    try:
        data = json.loads(event['body'])
        item_id = str(uuid.uuid4()) 
        data['id'] = item_id
        table.put_item(Item=data)
        return {
            "statusCode": 200,
            "body": json.dumps({'id': item_id})
        }
    except Exception as e:
        from app import app
        app.logger.error(f"Error putting item: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Could not save item"})
        }