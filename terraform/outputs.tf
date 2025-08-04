
output "dynamodb_table_name" {
  value = aws_dynamodb_table.my_table.name
}

output "sqs_queue_url" {
  value = aws_sqs_queue.my_queue.url
}

output "lambda_function_name" {
  value = aws_lambda_function.my_lambda.function_name
}

output "s3_bucket_name" {
  value = aws_s3_bucket.my_bucket.bucket
}