import json

def list_items(event, context, table):
    try:
        response = table.scan()
        items = response.get('Items', [])
        return {
            "statusCode": 200,
            "body": json.dumps(items)
        }
    except Exception as e:
        from app import app
        app.logger.error(f"Error listing items: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Could not retrieve items"})
        }