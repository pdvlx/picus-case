import json
import boto3
import os
import logging
from botocore.exceptions import ClientError

REGION = os.getenv('AWS_REGION', 'eu-central-1')
TABLE_NAME = os.getenv('DYNAMODB_TABLE', 'PicusTable')
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)


logging.basicConfig(level=logging.INFO)

def delete_item(event, context):
    key = event['pathParameters'].get('key')
    
    if not key:
        logging.warning("Bad Request: Missing 'key' parameter")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Bad Request: Missing 'key' parameter"})
        }

    try:
        logging.info(f"Attempting to delete item with key: {key}")
       
        response = table.delete_item(
            Key={
                'id': key
            },
            ConditionExpression="attribute_exists(id)" 
        )
        
        logging.info(f"Item with key {key} deleted successfully.")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Item with key {key} deleted successfully."})
        }

    except ClientError as e:

        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            logging.warning(f"Item with key {key} does not exist.")
            return {
                "statusCode": 404,
                "body": json.dumps({"message": f"Item with key {key} does not exist."})
            }
        else:
            logging.error(f"Internal Server Error: {e.response['Error']['Message']}")
            return {
                "statusCode": 500,
                "body": json.dumps({"message": f"Internal Server Error: {e.response['Error']['Message']}"})
            }
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Internal Server Error: {str(e)}"})
        }