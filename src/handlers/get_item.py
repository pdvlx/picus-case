import json

def get_item(event, context, table):
    try:
        key = event['pathParameters']['key']
        response = table.get_item(Key={'id': key})
        item = response.get('Item', None)
        if item is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Item not found"})
            }
        return {
            "statusCode": 200,
            "body": json.dumps(item)
        }
    except Exception as e:
        from app import app
        app.logger.error(f"Error retrieving item: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Could not retrieve item"})
        }