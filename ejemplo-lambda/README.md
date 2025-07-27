# Desplegar y conectar Lambda con SQS en LocalStack

## 0. activar el ambiente virtual porque usaremos awslocal

```bash
source /Users/pargueta/Desktop/PRUEBAS/.venv/bin/activate
```

## 1. Empaquetar la función Lambda

```bash
zip lambda_function.zip handler.py
```

## 2. Crear la función Lambda en LocalStack

```bash
awslocal lambda create-function \
  --function-name my-lambda \
  --runtime python3.11 \
  --handler handler.lambda_handler \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --zip-file fileb://lambda_function.zip

awslocal lambda list-functions
```

## 3. Crear la tabla donde almacenaremos los mensajes

```bash
awslocal dynamodb create-table \
    --table-name MyTableDynamo \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

## 4. crear una cola enviar y escuchar mensajes

```bash
awslocal sqs create-queue --queue-name queue-for-example-lambda
awslocal sqs list-queues

```

## 5. Dar permiso a SQS para invocar la Lambda

```bash

awslocal lambda add-permission \
  --function-name my-lambda  \
  --statement-id sqs-access \
  --action "lambda:*" \
  --principal "*" \
  --source-arn arn:aws:sqs:us-east-1:000000000000:queue-for-example-lambda


awslocal lambda add-permission \
  --function-name my-lambda \
  --statement-id dynamodb-access \
  --action "dynamodb:*" \
  --principal "*" \
  --source-arn arn:aws:dynamodb:us-east-1:000000000000:table/MyTableDynamo
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
  --message-body "{ 'msg': 'lambda .... '}"
```


## 8. crear el S3 de reporte

```bash
awslocal s3 mb s3://my-bucket
```
