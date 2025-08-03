terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configuración del provider AWS para LocalStack
provider "aws" {
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    lambda   = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
    sqs      = "http://localhost:4566"
    s3       = "http://localhost:4566"
    iam      = "http://localhost:4566"
  }
}

# DynamoDB Table
resource "aws_dynamodb_table" "my_table" {
  name           = "MyTableDynamo"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }
}

# SQS Queue
resource "aws_sqs_queue" "my_queue" {
  name = "queue-for-example-lambda"
}


# IAM Role para Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Política para permitir acceso a SQS y DynamoDB
resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "sqs:*",
          "dynamodb:*"
        ]
        Resource = [
          aws_sqs_queue.my_queue.arn,
          aws_dynamodb_table.my_table.arn
        ]
      }
    ]
  })
}

# Lambda Function
resource "aws_lambda_function" "my_lambda" {
  filename      = "../lambda/lambda_function.zip"
  function_name = "my-lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "handler.lambda_handler"
  runtime       = "python3.10"

  depends_on = [aws_iam_role_policy.lambda_policy]
}

# Event Source Mapping entre SQS y Lambda
resource "aws_lambda_event_source_mapping" "sqs_lambda" {
  event_source_arn = aws_sqs_queue.my_queue.arn
  function_name    = aws_lambda_function.my_lambda.function_name
  enabled          = true
}
