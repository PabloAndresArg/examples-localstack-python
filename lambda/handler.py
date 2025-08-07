

import boto3
import uuid



def lambda_handler(event, context):
    print("Event received:", event)
    table = get_dynamodb_table()
    try:
        for record in event.get('Records', []):
            body = record.get('body', '')
            message_id = record.get('messageId', str(uuid.uuid4()))
            save_record_to_dynamodb(table, message_id, body)
    except Exception as e:
        print(f"Error processing records: {str(e)}") # not visible in localstack
        raise

    return {
        'statusCode': 200,
        'body': 'Records processed successfully'
    }


def save_record_to_dynamodb(table, message_id, body):
    """Save a single record to DynamoDB table"""
    try:
        table.put_item(Item={'id': message_id, 'body': body})
        print(f"Saved Record - Message ID: {message_id}, Body: {body}")
    except Exception as e:
        print(f"Error saving record {message_id}: {str(e)}")
        raise

def get_dynamodb_table():
    """Get DynamoDB table connection"""
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('MyTableDynamo')
        print("Connected to DynamoDB table:", table.name)
        return table
    except Exception as e:
        print(f"Error connecting to DynamoDB: {str(e)}")
        raise