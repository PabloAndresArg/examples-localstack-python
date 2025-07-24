
import boto3

def create_sqs_queue():
    # Crear el cliente SQS apuntando a LocalStack
    sqs = boto3.client('sqs',
        endpoint_url='http://localhost:4566',
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )

    queue_name = 'queue-for-example-lambda'
    try:
        response = sqs.create_queue(QueueName=queue_name)
        print(f"Cola SQS '{queue_name}' creada exitosamente!")
        print(f"URL de la cola: {response['QueueUrl']}")
    except Exception as e:
        print(f"Error al crear la cola: {str(e)}")

if __name__ == "__main__":
    create_sqs_queue()
