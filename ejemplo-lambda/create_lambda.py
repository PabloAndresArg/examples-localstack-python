

import boto3
import uuid

def lambda_handler(event, context):
    print("Event received:", event)
    # Configurar el cliente DynamoDB (LocalStack)
    try:
        dynamodb = boto3.resource('dynamodb',
            endpoint_url='http://localhost:4566',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
        table = dynamodb.Table('MensajesProcesados')
    except Exception as e:
        print(f"Error connecting to DynamoDB: {str(e)}")
        raise
    
    print("Connected to DynamoDB table:", table.name)
    
    for record in event.get('Records', []):
        print(record)
        body = record.get('body', '')
        mensaje_id = str(uuid.uuid4())
        print(f"Mensaje recibido de SQS: {body}")
        # Guardar en DynamoDB
        table.put_item(
            Item={
                'id': mensaje_id,
                'body': body
            }
        )

    return {
        'statusCode': 200,
        'body': 'Mensajes procesados y almacenados en DynamoDB'
    }
    
lambda_handler({'Records':[{ 'body': { 'msg': 'lambda' } }]}, None)  # Llamada de prueba para verificar el funcionamiento
