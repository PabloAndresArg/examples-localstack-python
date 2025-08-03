"""Main application module.

This module initializes and configures the FastAPI application.
"""
from fastapi import FastAPI
from app.config.aws_config import AWSConfig
from app.services.s3_service import S3Service
from app.services.dynamo_service import DynamoService
from app.routes import s3_routes

# Initialize FastAPI application
app = FastAPI(title="S3 Export API", description="API for exporting DynamoDB records to S3")

# Configure AWS services
aws_config = AWSConfig()
dynamodb = aws_config.get_dynamodb_resource()
s3_client = aws_config.get_s3_client()

# Initialize services
table_dynamo = dynamodb.Table(aws_config.table_name)
dynamo_service = DynamoService(table_dynamo)
s3_service = S3Service(s3_client, aws_config.bucket_name)

# Include routes
app.include_router(s3_routes.initialize_router(s3_service, dynamo_service))

# Run the application if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    # Start the server with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Listen on all available network interfaces