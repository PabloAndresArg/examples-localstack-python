

import boto3
import uuid

def lambda_handler(event, context):
    print("Event received:", event)
    try:
        dynamodb = boto3.resource('dynamodb',
            region_name='us-east-1'
        )
        table = dynamodb.Table('MyTableDynamo')
    except Exception as e:
        print(f"Error connecting to DynamoDB: {str(e)}")
        raise

    print("Connected to DynamoDB table:", table.name)
    try:
      for record in event.get('Records', []):
        body = record.get('body', '')
        message_id = record.get('messageId', str(uuid.uuid4()))
        print(f"Message ID: {message_id}, Body: {body}")
        table.put_item(
            Item={
                'id': message_id,
                'body': body
            }
        )
        print(f"Saved Record: {message_id}")
    except Exception as e:
        print(f"Error in insert new record {str(e)}") # not visible in localstack
        raise

    return {
        'statusCode': 200,
        'body': 'Records processed successfully'
    }

