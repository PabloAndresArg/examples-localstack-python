# Desplegar y conectar Lambda con SQS en LocalStack

## 1. Empaquetar la función Lambda

```bash
zip lambda_function.zip create_lambda.py
```

## 2. Crear la función Lambda en LocalStack

```bash
awslocal lambda create-function \
  --function-name my-lambda \
  --runtime python3.11 \
  --handler create_lambda.lambda_handler \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --zip-file fileb://lambda_function.zip
```

## 3. Crear la tabla donde almacenaremos los mensajes

```bash
awslocal dynamodb create-table \
    --table-name MensajesProcesados \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```


## 4. crear una cola enviar y escuchar mensajes

````bash
awslocal sqs create-queue --queue-name queue-for-example-lambda
awslocal sqs list-queues

````


## 5. Dar permiso a SQS para invocar la Lambda

```bash
awslocal lambda add-permission \
  --function-name my-lambda \
  --statement-id sqs-invoke \
  --action lambda:InvokeFunction \
  --principal sqs.amazonaws.com \
  --source-arn arn:aws:sqs:us-east-1:000000000000:queue-for-example-lambda
```

## 6. Conectar la SQS con la Lambda

```bash
awslocal lambda create-event-source-mapping \
  --function-name my-lambda \
  --event-source-arn arn:aws:sqs:us-east-1:000000000000:queue-for-example-lambda
```

## 7. enviar un mensaje de prueba a la SQS
```bash
awslocal sqs send-message \
  --queue-url http://localhost:4566/000000000000/queue-for-example-lambda \
  --message-body "{'Records':[{ 'body': { 'msg': 'lambda' } }]}"
```


